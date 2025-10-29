#!/usr/bin/env python3
"""Example of using the bulk import functionality programmatically."""

from bookstack_api import BookStackClient
from bookstack_api.bulk_import import BulkImporter

# Initialize client
client = BookStackClient()

# Create importer
importer = BulkImporter(client)

# Example 1: Import from file
print("=== Example 1: Import from JSON file ===")
result = importer.import_from_file("templates/simple_book.json")
importer.print_summary()

# Example 2: Programmatic bulk creation
print("\n=== Example 2: Programmatic Bulk Creation ===")

# Create a complete documentation structure programmatically
structure_data = {
    "structures": [
        {
            "type": "shelf",
            "name": "Python API Examples",
            "description": "Examples created via Python API",
            "books": [
                {
                    "name": "Getting Started with BookStack",
                    "description": "A beginner's guide",
                    "chapters": [
                        {
                            "name": "Introduction",
                            "description": "Getting to know BookStack",
                            "pages": [
                                {
                                    "name": "What is BookStack?",
                                    "markdown": """# What is BookStack?

BookStack is a simple, self-hosted platform for organizing and storing information.

## Key Features

- Easy to use
- Self-hosted
- Open source
- Great for documentation
"""
                                },
                                {
                                    "name": "Why Use BookStack?",
                                    "markdown": """# Why Use BookStack?

BookStack provides a clean, intuitive interface for creating and managing documentation.

## Benefits

1. Simple organization
2. Rich text editing
3. Search functionality
4. User permissions
"""
                                }
                            ]
                        },
                        {
                            "name": "First Steps",
                            "description": "Your first tasks in BookStack",
                            "pages": [
                                {
                                    "name": "Creating Your First Book",
                                    "markdown": """# Creating Your First Book

Follow these steps to create your first book:

1. Click on "New Book"
2. Enter a name
3. Add a description
4. Click "Save"
"""
                                },
                                {
                                    "name": "Adding Pages",
                                    "markdown": """# Adding Pages

Pages are where you write your content.

## How to Add a Page

1. Open a book
2. Click "New Page"
3. Write your content
4. Save the page
"""
                                }
                            ]
                        }
                    ],
                    "pages": [
                        {
                            "name": "Quick Reference",
                            "markdown": """# Quick Reference

## Common Actions

- Create Book: Click "New Book"
- Create Page: Click "New Page"
- Search: Use the search bar
- Settings: Click your avatar

## Keyboard Shortcuts

- `Ctrl+S`: Save
- `Ctrl+K`: Search
- `Ctrl+Enter`: Preview
"""
                        }
                    ]
                }
            ]
        }
    ]
}

# Save to temp file and import
import json
import tempfile

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(structure_data, f, indent=2)
    temp_file = f.name

print(f"Created temporary file: {temp_file}")

# Import the structure
new_importer = BulkImporter(client)
result = new_importer.import_from_file(temp_file)
new_importer.print_summary()

# Clean up
import os
os.unlink(temp_file)

print("\n=== Example 3: Creating Multiple Users ===")

users_data = {
    "users": [
        {
            "name": "Documentation Admin",
            "email": "doc-admin@example.com",
            "external_auth_id": "doc.admin",
            "language": "en",
            "roles": [4]  # Admin role
        },
        {
            "name": "Content Editor",
            "email": "editor@example.com",
            "external_auth_id": "editor",
            "language": "en",
            "roles": [3]  # Editor role
        },
        {
            "name": "Documentation Viewer",
            "email": "viewer@example.com",
            "external_auth_id": "viewer",
            "language": "en",
            "roles": [2]  # Viewer role
        }
    ]
}

# Save and import users
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(users_data, f, indent=2)
    temp_file = f.name

user_importer = BulkImporter(client)
result = user_importer.import_from_file(temp_file)
user_importer.print_summary()

# Clean up
os.unlink(temp_file)

print("\n=== All Examples Completed ===")
