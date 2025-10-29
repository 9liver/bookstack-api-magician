#!/usr/bin/env python3
"""Command-line interface for BookStack API Magician."""

import click
import json
import os
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from bookstack_api import BookStackClient
from bookstack_api.exceptions import BookStackAPIError

console = Console()


def get_client():
    """Get BookStack client instance."""
    try:
        return BookStackClient()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Make sure to configure .env file with your credentials[/yellow]")
        raise click.Abort()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """BookStack API Magician - Manage your BookStack instance via CLI."""
    pass


# ==========================
# Shelves Commands
# ==========================

@cli.group()
def shelves():
    """Manage shelves."""
    pass


@shelves.command("list")
@click.option("--count", type=int, help="Number of items to return")
@click.option("--offset", type=int, help="Offset for pagination")
@click.option("--sort", help="Sort field (e.g., 'name', '-created_at')")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def shelves_list(count, offset, sort, output_json):
    """List all shelves."""
    client = get_client()
    try:
        shelves_data = client.shelves.list(count=count, offset=offset, sort=sort)

        if output_json:
            click.echo(json.dumps(shelves_data, indent=2))
        else:
            table = Table(title="Shelves")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Slug", style="yellow")
            table.add_column("Books", style="magenta")

            for shelf in shelves_data:
                books_count = len(shelf.get("books", []))
                table.add_row(
                    str(shelf.get("id")),
                    shelf.get("name"),
                    shelf.get("slug"),
                    str(books_count),
                )

            console.print(table)
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@shelves.command("get")
@click.argument("shelf_id", type=int)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def shelves_get(shelf_id, output_json):
    """Get a specific shelf by ID."""
    client = get_client()
    try:
        shelf = client.shelves.get(shelf_id)

        if output_json:
            click.echo(json.dumps(shelf, indent=2))
        else:
            console.print(f"[cyan]ID:[/cyan] {shelf.get('id')}")
            console.print(f"[cyan]Name:[/cyan] {shelf.get('name')}")
            console.print(f"[cyan]Slug:[/cyan] {shelf.get('slug')}")
            console.print(f"[cyan]Description:[/cyan] {shelf.get('description', 'N/A')}")
            console.print(f"[cyan]Books:[/cyan] {len(shelf.get('books', []))}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@shelves.command("create")
@click.option("--name", required=True, help="Shelf name")
@click.option("--description", help="Shelf description")
@click.option("--books", help="Comma-separated list of book IDs")
def shelves_create(name, description, books):
    """Create a new shelf."""
    client = get_client()
    try:
        book_ids = [int(b) for b in books.split(",")] if books else None
        shelf = client.shelves.create(name=name, description=description, books=book_ids)
        console.print(f"[green]Shelf created successfully![/green]")
        console.print(f"ID: {shelf.get('id')}, Name: {shelf.get('name')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@shelves.command("update")
@click.argument("shelf_id", type=int)
@click.option("--name", help="New shelf name")
@click.option("--description", help="New shelf description")
@click.option("--books", help="Comma-separated list of book IDs")
def shelves_update(shelf_id, name, description, books):
    """Update an existing shelf."""
    client = get_client()
    try:
        book_ids = [int(b) for b in books.split(",")] if books else None
        shelf = client.shelves.update(shelf_id, name=name, description=description, books=book_ids)
        console.print(f"[green]Shelf updated successfully![/green]")
        console.print(f"ID: {shelf.get('id')}, Name: {shelf.get('name')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@shelves.command("delete")
@click.argument("shelf_id", type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this shelf?")
def shelves_delete(shelf_id):
    """Delete a shelf."""
    client = get_client()
    try:
        client.shelves.delete(shelf_id)
        console.print(f"[green]Shelf {shelf_id} deleted successfully![/green]")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


# ==========================
# Books Commands
# ==========================

@cli.group()
def books():
    """Manage books."""
    pass


@books.command("list")
@click.option("--count", type=int, help="Number of items to return")
@click.option("--offset", type=int, help="Offset for pagination")
@click.option("--sort", help="Sort field")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def books_list(count, offset, sort, output_json):
    """List all books."""
    client = get_client()
    try:
        books_data = client.books.list(count=count, offset=offset, sort=sort)

        if output_json:
            click.echo(json.dumps(books_data, indent=2))
        else:
            table = Table(title="Books")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Slug", style="yellow")

            for book in books_data:
                table.add_row(
                    str(book.get("id")),
                    book.get("name"),
                    book.get("slug"),
                )

            console.print(table)
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@books.command("get")
@click.argument("book_id", type=int)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def books_get(book_id, output_json):
    """Get a specific book by ID."""
    client = get_client()
    try:
        book = client.books.get(book_id)

        if output_json:
            click.echo(json.dumps(book, indent=2))
        else:
            console.print(f"[cyan]ID:[/cyan] {book.get('id')}")
            console.print(f"[cyan]Name:[/cyan] {book.get('name')}")
            console.print(f"[cyan]Slug:[/cyan] {book.get('slug')}")
            console.print(f"[cyan]Description:[/cyan] {book.get('description', 'N/A')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@books.command("create")
@click.option("--name", required=True, help="Book name")
@click.option("--description", help="Book description")
def books_create(name, description):
    """Create a new book."""
    client = get_client()
    try:
        book = client.books.create(name=name, description=description)
        console.print(f"[green]Book created successfully![/green]")
        console.print(f"ID: {book.get('id')}, Name: {book.get('name')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@books.command("update")
@click.argument("book_id", type=int)
@click.option("--name", help="New book name")
@click.option("--description", help="New book description")
def books_update(book_id, name, description):
    """Update an existing book."""
    client = get_client()
    try:
        book = client.books.update(book_id, name=name, description=description)
        console.print(f"[green]Book updated successfully![/green]")
        console.print(f"ID: {book.get('id')}, Name: {book.get('name')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@books.command("delete")
@click.argument("book_id", type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this book?")
def books_delete(book_id):
    """Delete a book."""
    client = get_client()
    try:
        client.books.delete(book_id)
        console.print(f"[green]Book {book_id} deleted successfully![/green]")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


# ==========================
# Chapters Commands
# ==========================

@cli.group()
def chapters():
    """Manage chapters."""
    pass


@chapters.command("list")
@click.option("--count", type=int, help="Number of items to return")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def chapters_list(count, output_json):
    """List all chapters."""
    client = get_client()
    try:
        chapters_data = client.chapters.list(count=count)

        if output_json:
            click.echo(json.dumps(chapters_data, indent=2))
        else:
            table = Table(title="Chapters")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Book ID", style="yellow")

            for chapter in chapters_data:
                table.add_row(
                    str(chapter.get("id")),
                    chapter.get("name"),
                    str(chapter.get("book_id")),
                )

            console.print(table)
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@chapters.command("create")
@click.option("--book-id", required=True, type=int, help="Book ID")
@click.option("--name", required=True, help="Chapter name")
@click.option("--description", help="Chapter description")
def chapters_create(book_id, name, description):
    """Create a new chapter."""
    client = get_client()
    try:
        chapter = client.chapters.create(book_id=book_id, name=name, description=description)
        console.print(f"[green]Chapter created successfully![/green]")
        console.print(f"ID: {chapter.get('id')}, Name: {chapter.get('name')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@chapters.command("delete")
@click.argument("chapter_id", type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this chapter?")
def chapters_delete(chapter_id):
    """Delete a chapter."""
    client = get_client()
    try:
        client.chapters.delete(chapter_id)
        console.print(f"[green]Chapter {chapter_id} deleted successfully![/green]")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


# ==========================
# Pages Commands
# ==========================

@cli.group()
def pages():
    """Manage pages."""
    pass


@pages.command("list")
@click.option("--count", type=int, help="Number of items to return")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def pages_list(count, output_json):
    """List all pages."""
    client = get_client()
    try:
        pages_data = client.pages.list(count=count)

        if output_json:
            click.echo(json.dumps(pages_data, indent=2))
        else:
            table = Table(title="Pages")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Book ID", style="yellow")

            for page in pages_data:
                table.add_row(
                    str(page.get("id")),
                    page.get("name"),
                    str(page.get("book_id")),
                )

            console.print(table)
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@pages.command("get")
@click.argument("page_id", type=int)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def pages_get(page_id, output_json):
    """Get a specific page by ID."""
    client = get_client()
    try:
        page = client.pages.get(page_id)

        if output_json:
            click.echo(json.dumps(page, indent=2))
        else:
            console.print(f"[cyan]ID:[/cyan] {page.get('id')}")
            console.print(f"[cyan]Name:[/cyan] {page.get('name')}")
            console.print(f"[cyan]Book ID:[/cyan] {page.get('book_id')}")
            console.print(f"[cyan]Chapter ID:[/cyan] {page.get('chapter_id', 'N/A')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@pages.command("create")
@click.option("--book-id", required=True, type=int, help="Book ID")
@click.option("--name", required=True, help="Page name")
@click.option("--html", help="Page content as HTML")
@click.option("--markdown", help="Page content as Markdown")
@click.option("--chapter-id", type=int, help="Chapter ID (optional)")
def pages_create(book_id, name, html, markdown, chapter_id):
    """Create a new page."""
    client = get_client()
    try:
        page = client.pages.create(
            book_id=book_id,
            name=name,
            html=html,
            markdown=markdown,
            chapter_id=chapter_id,
        )
        console.print(f"[green]Page created successfully![/green]")
        console.print(f"ID: {page.get('id')}, Name: {page.get('name')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@pages.command("update")
@click.argument("page_id", type=int)
@click.option("--name", help="New page name")
@click.option("--html", help="New HTML content")
@click.option("--markdown", help="New Markdown content")
def pages_update(page_id, name, html, markdown):
    """Update an existing page."""
    client = get_client()
    try:
        page = client.pages.update(page_id, name=name, html=html, markdown=markdown)
        console.print(f"[green]Page updated successfully![/green]")
        console.print(f"ID: {page.get('id')}, Name: {page.get('name')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@pages.command("delete")
@click.argument("page_id", type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this page?")
def pages_delete(page_id):
    """Delete a page."""
    client = get_client()
    try:
        client.pages.delete(page_id)
        console.print(f"[green]Page {page_id} deleted successfully![/green]")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


# ==========================
# Users Commands
# ==========================

@cli.group()
def users():
    """Manage users."""
    pass


@users.command("list")
@click.option("--count", type=int, help="Number of items to return")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def users_list(count, output_json):
    """List all users."""
    client = get_client()
    try:
        users_data = client.users.list(count=count)

        if output_json:
            click.echo(json.dumps(users_data, indent=2))
        else:
            table = Table(title="Users")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Email", style="yellow")

            for user in users_data:
                table.add_row(
                    str(user.get("id")),
                    user.get("name"),
                    user.get("email"),
                )

            console.print(table)
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@users.command("get")
@click.argument("user_id", type=int)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def users_get(user_id, output_json):
    """Get a specific user by ID."""
    client = get_client()
    try:
        user = client.users.get(user_id)

        if output_json:
            click.echo(json.dumps(user, indent=2))
        else:
            console.print(f"[cyan]ID:[/cyan] {user.get('id')}")
            console.print(f"[cyan]Name:[/cyan] {user.get('name')}")
            console.print(f"[cyan]Email:[/cyan] {user.get('email')}")
            console.print(f"[cyan]Language:[/cyan] {user.get('language', 'N/A')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@users.command("create")
@click.option("--name", required=True, help="User's full name")
@click.option("--email", required=True, help="User's email address")
@click.option("--password", help="User's password")
@click.option("--send-invite", is_flag=True, help="Send invitation email")
@click.option("--language", help="User's language (e.g., de, en)")
def users_create(name, email, password, send_invite, language):
    """Create a new user."""
    client = get_client()
    try:
        user = client.users.create(
            name=name,
            email=email,
            password=password,
            send_invite=send_invite,
            language=language,
        )
        console.print(f"[green]User created successfully![/green]")
        console.print(f"ID: {user.get('id')}, Name: {user.get('name')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@users.command("update")
@click.argument("user_id", type=int)
@click.option("--name", help="New user name")
@click.option("--email", help="New email address")
@click.option("--password", help="New password")
@click.option("--language", help="New language preference")
def users_update(user_id, name, email, password, language):
    """Update an existing user."""
    client = get_client()
    try:
        user = client.users.update(
            user_id,
            name=name,
            email=email,
            password=password,
            language=language,
        )
        console.print(f"[green]User updated successfully![/green]")
        console.print(f"ID: {user.get('id')}, Name: {user.get('name')}")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@users.command("delete")
@click.argument("user_id", type=int)
@click.option("--migrate-to", type=int, help="User ID to migrate content ownership to")
@click.confirmation_option(prompt="Are you sure you want to delete this user?")
def users_delete(user_id, migrate_to):
    """Delete a user."""
    client = get_client()
    try:
        client.users.delete(user_id, migrate_ownership_id=migrate_to)
        console.print(f"[green]User {user_id} deleted successfully![/green]")
    except BookStackAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


# ==========================
# Utility Commands
# ==========================

@cli.command()
def test():
    """Test API connection."""
    try:
        client = get_client()
        if client.test_connection():
            console.print("[green]Connection successful![/green]")
            console.print(f"Connected to: {client.base_url}")
        else:
            console.print("[red]Connection failed![/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


if __name__ == "__main__":
    cli()
