"""Bulk operations module for importing structures from JSON."""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class BulkImporter:
    """Handle bulk import operations from JSON files."""

    def __init__(self, client):
        """Initialize with BookStack client."""
        self.client = client
        self.created_items = {
            "shelves": [],
            "books": [],
            "chapters": [],
            "pages": [],
            "users": []
        }

    def import_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Import structures from JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            Dictionary with created items
        """
        console.print(f"[cyan]Loading JSON from: {file_path}[/cyan]")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Determine import type and delegate
        if "users" in data:
            self._import_users(data["users"])

        if "structures" in data:
            self._import_structures(data["structures"])

        if "shelves" in data:
            # Direct shelf import (legacy)
            for shelf_data in data["shelves"]:
                self._create_shelf_with_books(shelf_data)

        if "books" in data:
            # Direct book import
            for book_data in data["books"]:
                self._create_book_with_contents(book_data)

        return self.created_items

    def _import_users(self, users_data: List[Dict[str, Any]]):
        """Import multiple users."""
        console.print(f"\n[yellow]Creating {len(users_data)} users...[/yellow]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Creating users...", total=len(users_data))

            for user_data in users_data:
                try:
                    # Extract user parameters
                    name = user_data.get("name")
                    email = user_data.get("email")

                    if not name or not email:
                        console.print(f"[red]Skipping user: missing name or email[/red]")
                        continue

                    # Check if LDAP user
                    external_auth_id = user_data.get("external_auth_id") or user_data.get("ldap_id")

                    user_params = {
                        "name": name,
                        "email": email,
                        "language": user_data.get("language", "en"),
                    }

                    # Add LDAP/external auth
                    if external_auth_id:
                        user_params["external_auth_id"] = external_auth_id
                        console.print(f"[cyan]Creating LDAP user: {name}[/cyan]")
                    else:
                        # Regular user with password or invitation
                        if user_data.get("password"):
                            user_params["password"] = user_data["password"]
                        else:
                            user_params["send_invite"] = user_data.get("send_invite", True)

                    # Add roles if specified
                    if user_data.get("roles"):
                        user_params["roles"] = user_data["roles"]

                    user = self.client.users.create(**user_params)
                    self.created_items["users"].append(user)

                    console.print(f"[green]✓[/green] Created user: {user['name']} (ID: {user['id']})")

                except Exception as e:
                    console.print(f"[red]✗ Error creating user {name}: {e}[/red]")

                progress.update(task, advance=1)

    def _import_structures(self, structures: List[Dict[str, Any]]):
        """Import complete nested structures."""
        console.print(f"\n[yellow]Creating {len(structures)} structures...[/yellow]")

        for structure in structures:
            struct_type = structure.get("type")

            if struct_type == "shelf":
                self._create_shelf_structure(structure)
            elif struct_type == "book":
                self._create_book_with_contents(structure)
            else:
                console.print(f"[red]Unknown structure type: {struct_type}[/red]")

    def _create_shelf_structure(self, shelf_data: Dict[str, Any]):
        """Create a shelf with all nested books, chapters, and pages."""
        console.print(f"\n[cyan]Creating shelf: {shelf_data.get('name')}[/cyan]")

        # Create shelf
        shelf = self.client.shelves.create(
            name=shelf_data["name"],
            description=shelf_data.get("description"),
            tags=shelf_data.get("tags")
        )
        self.created_items["shelves"].append(shelf)
        console.print(f"[green]✓[/green] Shelf created (ID: {shelf['id']})")

        book_ids = []

        # Create books in this shelf
        for book_data in shelf_data.get("books", []):
            book = self._create_book_with_contents(book_data)
            if book:
                book_ids.append(book['id'])

        # Update shelf with books
        if book_ids:
            self.client.shelves.update(shelf['id'], books=book_ids)
            console.print(f"[green]✓[/green] Added {len(book_ids)} books to shelf")

        return shelf

    def _create_shelf_with_books(self, shelf_data: Dict[str, Any]):
        """Legacy: Create shelf with books."""
        return self._create_shelf_structure(shelf_data)

    def _create_book_with_contents(self, book_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a book with all chapters and pages."""
        console.print(f"\n[cyan]Creating book: {book_data.get('name')}[/cyan]")

        try:
            # Create book
            book = self.client.books.create(
                name=book_data["name"],
                description=book_data.get("description"),
                tags=book_data.get("tags")
            )
            self.created_items["books"].append(book)
            console.print(f"[green]✓[/green] Book created (ID: {book['id']})")

            # Create chapters
            for chapter_data in book_data.get("chapters", []):
                self._create_chapter_with_pages(book['id'], chapter_data)

            # Create standalone pages (not in chapters)
            for page_data in book_data.get("pages", []):
                self._create_page(book['id'], None, page_data)

            return book

        except Exception as e:
            console.print(f"[red]✗ Error creating book: {e}[/red]")
            return None

    def _create_chapter_with_pages(self, book_id: int, chapter_data: Dict[str, Any]):
        """Create a chapter with all its pages."""
        console.print(f"  [cyan]Creating chapter: {chapter_data.get('name')}[/cyan]")

        try:
            chapter = self.client.chapters.create(
                book_id=book_id,
                name=chapter_data["name"],
                description=chapter_data.get("description"),
                priority=chapter_data.get("priority"),
                tags=chapter_data.get("tags")
            )
            self.created_items["chapters"].append(chapter)
            console.print(f"  [green]✓[/green] Chapter created (ID: {chapter['id']})")

            # Create pages in this chapter
            for page_data in chapter_data.get("pages", []):
                self._create_page(book_id, chapter['id'], page_data)

            return chapter

        except Exception as e:
            console.print(f"  [red]✗ Error creating chapter: {e}[/red]")
            return None

    def _create_page(self, book_id: int, chapter_id: Optional[int], page_data: Dict[str, Any]):
        """Create a single page."""
        page_name = page_data.get("name", "Untitled")
        console.print(f"    [cyan]Creating page: {page_name}[/cyan]")

        try:
            page = self.client.pages.create(
                book_id=book_id,
                chapter_id=chapter_id,
                name=page_name,
                html=page_data.get("html"),
                markdown=page_data.get("markdown"),
                priority=page_data.get("priority"),
                tags=page_data.get("tags")
            )
            self.created_items["pages"].append(page)
            console.print(f"    [green]✓[/green] Page created (ID: {page['id']})")

            return page

        except Exception as e:
            console.print(f"    [red]✗ Error creating page: {e}[/red]")
            return None

    def print_summary(self):
        """Print summary of created items."""
        console.print("\n[bold green]Import Summary:[/bold green]")
        console.print(f"  Shelves:  {len(self.created_items['shelves'])}")
        console.print(f"  Books:    {len(self.created_items['books'])}")
        console.print(f"  Chapters: {len(self.created_items['chapters'])}")
        console.print(f"  Pages:    {len(self.created_items['pages'])}")
        console.print(f"  Users:    {len(self.created_items['users'])}")
