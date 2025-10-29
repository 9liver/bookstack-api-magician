#!/usr/bin/env python3
"""User management examples for BookStack API."""

from bookstack_api import BookStackClient

client = BookStackClient()

def list_users():
    """List all users."""
    print("=== All Users ===\n")

    users = client.users.list()

    for user in users:
        print(f"ID: {user['id']}")
        print(f"Name: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Language: {user.get('language', 'N/A')}")
        print(f"Created: {user.get('created_at', 'N/A')}")
        print("-" * 40)


def create_bulk_users():
    """Create multiple users at once."""
    print("=== Creating Users ===\n")

    users_data = [
        {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "language": "en"
        },
        {
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "language": "en"
        },
        {
            "name": "Carol Williams",
            "email": "carol@example.com",
            "language": "de"
        }
    ]

    created_users = []

    for user_data in users_data:
        try:
            user = client.users.create(
                name=user_data['name'],
                email=user_data['email'],
                send_invite=True,  # Send invitation email
                language=user_data['language']
            )
            created_users.append(user)
            print(f"Created: {user['name']} ({user['email']})")
        except Exception as e:
            print(f"Error creating {user_data['name']}: {e}")

    print(f"\nTotal created: {len(created_users)} users")
    return created_users


def update_user_info(user_id: int):
    """Update user information."""
    print(f"=== Updating User {user_id} ===\n")

    try:
        # Get current user info
        user = client.users.get(user_id)
        print(f"Current name: {user['name']}")
        print(f"Current email: {user['email']}")

        # Update user
        updated_user = client.users.update(
            user_id,
            name=user['name'] + " (Updated)",
            language="de"
        )

        print(f"\nUpdated name: {updated_user['name']}")
        print(f"Updated language: {updated_user.get('language', 'N/A')}")

    except Exception as e:
        print(f"Error: {e}")


def search_users_by_email(email_pattern: str):
    """Search users by email pattern."""
    print(f"=== Searching Users (email contains '{email_pattern}') ===\n")

    all_users = client.users.list()
    matching_users = [
        user for user in all_users
        if email_pattern.lower() in user['email'].lower()
    ]

    print(f"Found {len(matching_users)} matching users:")
    for user in matching_users:
        print(f"  - {user['name']} ({user['email']})")


if __name__ == "__main__":
    # List all users
    list_users()

    # Create users (uncomment to use)
    # create_bulk_users()

    # Search users
    search_users_by_email("example.com")

    # Update user (uncomment and provide valid user ID)
    # update_user_info(1)
