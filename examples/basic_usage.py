#!/usr/bin/env python3
"""Basic usage examples for BookStack API Magician."""

from bookstack_api import BookStackClient

# Initialize client
# Credentials will be loaded from .env file
client = BookStackClient()

# Test connection
if client.test_connection():
    print("Connected to BookStack!")
else:
    print("Connection failed!")
    exit(1)

# ==================
# Shelves Examples
# ==================

print("\n=== Shelves ===")

# List all shelves
shelves = client.shelves.list()
print(f"Total shelves: {len(shelves)}")

# Create a new shelf
new_shelf = client.shelves.create(
    name="API Documentation",
    description="Documentation created via API"
)
print(f"Created shelf: {new_shelf['name']} (ID: {new_shelf['id']})")

# ==================
# Books Examples
# ==================

print("\n=== Books ===")

# List all books
books = client.books.list()
print(f"Total books: {len(books)}")

# Create a new book
new_book = client.books.create(
    name="Getting Started Guide",
    description="A comprehensive guide for beginners"
)
print(f"Created book: {new_book['name']} (ID: {new_book['id']})")

# Add book to shelf
client.shelves.update(
    new_shelf['id'],
    books=[new_book['id']]
)
print(f"Added book to shelf")

# ==================
# Pages Examples
# ==================

print("\n=== Pages ===")

# Create a page with Markdown
new_page = client.pages.create(
    book_id=new_book['id'],
    name="Introduction",
    markdown="# Welcome\n\nThis is a page created via API!"
)
print(f"Created page: {new_page['name']} (ID: {new_page['id']})")

# Create a page with HTML
html_page = client.pages.create(
    book_id=new_book['id'],
    name="Advanced Topics",
    html="<h1>Advanced Topics</h1><p>This page uses HTML.</p>"
)
print(f"Created HTML page: {html_page['name']} (ID: {html_page['id']})")

# ==================
# Chapters Examples
# ==================

print("\n=== Chapters ===")

# Create a chapter
new_chapter = client.chapters.create(
    book_id=new_book['id'],
    name="Chapter 1: Basics",
    description="Introduction to the basics"
)
print(f"Created chapter: {new_chapter['name']} (ID: {new_chapter['id']})")

# Create a page within the chapter
chapter_page = client.pages.create(
    book_id=new_book['id'],
    chapter_id=new_chapter['id'],
    name="Basic Concepts",
    markdown="## Key Concepts\n\n- Concept 1\n- Concept 2\n- Concept 3"
)
print(f"Created page in chapter: {chapter_page['name']}")

# ==================
# Users Examples
# ==================

print("\n=== Users ===")

# List all users
users = client.users.list()
print(f"Total users: {len(users)}")

# Create a new user (uncomment to use)
# new_user = client.users.create(
#     name="John Doe",
#     email="john.doe@example.com",
#     password="SecurePassword123!",
#     language="en"
# )
# print(f"Created user: {new_user['name']} (ID: {new_user['id']})")

print("\n=== Done! ===")
print(f"Created: 1 shelf, 1 book, 1 chapter, 3 pages")
