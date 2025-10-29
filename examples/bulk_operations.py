#!/usr/bin/env python3
"""Bulk operations example for BookStack API."""

from bookstack_api import BookStackClient

client = BookStackClient()

def create_documentation_structure():
    """Create a complete documentation structure."""

    print("Creating documentation structure...")

    # Create main shelf
    shelf = client.shelves.create(
        name="Technical Documentation",
        description="Complete technical documentation"
    )
    print(f"Created shelf: {shelf['name']}")

    # Create multiple books
    books = []
    book_names = [
        "Installation Guide",
        "User Manual",
        "API Reference",
        "FAQ"
    ]

    for book_name in book_names:
        book = client.books.create(
            name=book_name,
            description=f"Complete {book_name.lower()}"
        )
        books.append(book)
        print(f"Created book: {book['name']}")

    # Add all books to shelf
    book_ids = [book['id'] for book in books]
    client.shelves.update(shelf['id'], books=book_ids)
    print(f"Added {len(books)} books to shelf")

    # Create chapters and pages for first book
    installation_book = books[0]

    chapters_data = [
        {
            "name": "Prerequisites",
            "pages": [
                "System Requirements",
                "Software Dependencies",
                "Hardware Requirements"
            ]
        },
        {
            "name": "Installation Steps",
            "pages": [
                "Download",
                "Configuration",
                "First Run"
            ]
        },
        {
            "name": "Troubleshooting",
            "pages": [
                "Common Issues",
                "Error Messages",
                "Getting Help"
            ]
        }
    ]

    for chapter_data in chapters_data:
        chapter = client.chapters.create(
            book_id=installation_book['id'],
            name=chapter_data['name']
        )
        print(f"Created chapter: {chapter['name']}")

        for page_name in chapter_data['pages']:
            page = client.pages.create(
                book_id=installation_book['id'],
                chapter_id=chapter['id'],
                name=page_name,
                markdown=f"# {page_name}\n\nContent goes here..."
            )
            print(f"  Created page: {page['name']}")

    print("\nStructure created successfully!")
    print(f"- 1 Shelf: {shelf['name']}")
    print(f"- {len(books)} Books")
    print(f"- {len(chapters_data)} Chapters")
    print(f"- {sum(len(c['pages']) for c in chapters_data)} Pages")

    return shelf, books


def list_all_content():
    """List all content in the BookStack instance."""

    print("\n=== Content Summary ===\n")

    # List shelves
    shelves = client.shelves.list()
    print(f"Shelves: {len(shelves)}")
    for shelf in shelves:
        print(f"  - {shelf['name']} (ID: {shelf['id']})")

    # List books
    books = client.books.list()
    print(f"\nBooks: {len(books)}")
    for book in books:
        print(f"  - {book['name']} (ID: {book['id']})")

    # List chapters
    chapters = client.chapters.list()
    print(f"\nChapters: {len(chapters)}")
    for chapter in chapters[:10]:  # Limit to first 10
        print(f"  - {chapter['name']} (ID: {chapter['id']})")

    # List pages
    pages = client.pages.list(count=20)
    print(f"\nPages: {len(pages)}")
    for page in pages[:10]:  # Limit to first 10
        print(f"  - {page['name']} (ID: {page['id']})")


if __name__ == "__main__":
    # Create structure
    create_documentation_structure()

    # List all content
    list_all_content()
