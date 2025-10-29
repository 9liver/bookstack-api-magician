#!/usr/bin/env python3
"""Export content examples for BookStack API."""

import json
from bookstack_api import BookStackClient

client = BookStackClient()


def export_book_structure(book_id: int, output_file: str = "book_structure.json"):
    """Export complete book structure to JSON."""
    print(f"Exporting book {book_id}...")

    # Get book details
    book = client.books.get(book_id)

    structure = {
        "book": {
            "id": book['id'],
            "name": book['name'],
            "description": book.get('description'),
            "slug": book.get('slug'),
        },
        "contents": []
    }

    # Get all pages in the book
    all_pages = client.pages.list(filter={'book_id': str(book_id)})

    # Get all chapters in the book
    all_chapters = client.chapters.list(filter={'book_id': str(book_id)})

    # Add chapters with their pages
    for chapter in all_chapters:
        chapter_data = {
            "type": "chapter",
            "id": chapter['id'],
            "name": chapter['name'],
            "description": chapter.get('description'),
            "pages": []
        }

        # Find pages in this chapter
        chapter_pages = [p for p in all_pages if p.get('chapter_id') == chapter['id']]
        for page in chapter_pages:
            page_detail = client.pages.get(page['id'])
            chapter_data['pages'].append({
                "id": page['id'],
                "name": page['name'],
                "markdown": page_detail.get('markdown', ''),
                "html": page_detail.get('html', '')
            })

        structure['contents'].append(chapter_data)

    # Add standalone pages (not in chapters)
    standalone_pages = [p for p in all_pages if p.get('chapter_id') is None or p.get('chapter_id') == 0]
    for page in standalone_pages:
        page_detail = client.pages.get(page['id'])
        structure['contents'].append({
            "type": "page",
            "id": page['id'],
            "name": page['name'],
            "markdown": page_detail.get('markdown', ''),
            "html": page_detail.get('html', '')
        })

    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

    print(f"Exported to {output_file}")
    print(f"- {len(all_chapters)} chapters")
    print(f"- {len(all_pages)} pages")


def export_shelf_structure(shelf_id: int, output_file: str = "shelf_structure.json"):
    """Export complete shelf structure to JSON."""
    print(f"Exporting shelf {shelf_id}...")

    # Get shelf details
    shelf = client.shelves.get(shelf_id)

    structure = {
        "shelf": {
            "id": shelf['id'],
            "name": shelf['name'],
            "description": shelf.get('description'),
            "slug": shelf.get('slug'),
        },
        "books": []
    }

    # Get all books in shelf
    for book_ref in shelf.get('books', []):
        book = client.books.get(book_ref['id'])
        book_data = {
            "id": book['id'],
            "name": book['name'],
            "description": book.get('description'),
            "slug": book.get('slug'),
        }
        structure['books'].append(book_data)

    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

    print(f"Exported to {output_file}")
    print(f"- {len(structure['books'])} books")


def export_all_users(output_file: str = "users.json"):
    """Export all users to JSON."""
    print("Exporting all users...")

    users = client.users.list()

    users_data = []
    for user in users:
        user_detail = client.users.get(user['id'])
        users_data.append({
            "id": user_detail['id'],
            "name": user_detail['name'],
            "email": user_detail['email'],
            "language": user_detail.get('language'),
            "created_at": user_detail.get('created_at'),
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(users_data)} users to {output_file}")


if __name__ == "__main__":
    # Example: Export first book
    books = client.books.list()
    if books:
        export_book_structure(books[0]['id'])

    # Example: Export first shelf
    shelves = client.shelves.list()
    if shelves:
        export_shelf_structure(shelves[0]['id'])

    # Example: Export all users
    export_all_users()
