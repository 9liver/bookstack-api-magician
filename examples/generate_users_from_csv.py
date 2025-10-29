#!/usr/bin/env python3
"""Generate user import JSON from CSV file."""

import csv
import json
import sys

def generate_users_from_csv(csv_file, output_file="users_import.json"):
    """
    Generate user import JSON from CSV file.

    CSV Format:
    name,email,ldap_username,language,role

    Example:
    Max Mustermann,max@firma.de,max.mustermann,de,2
    Anna Schmidt,anna@firma.de,anna.schmidt,de,3
    """
    users = []

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                user = {
                    "name": row['name'],
                    "email": row['email'],
                    "language": row.get('language', 'de')
                }

                # Add LDAP if present
                if row.get('ldap_username'):
                    user["external_auth_id"] = row['ldap_username']

                # Add role if present
                if row.get('role'):
                    user["roles"] = [int(row['role'])]

                # Add password if present (for non-LDAP users)
                if row.get('password') and not row.get('ldap_username'):
                    user["password"] = row['password']
                elif not row.get('ldap_username'):
                    # Send invite if no LDAP and no password
                    user["send_invite"] = True

                users.append(user)

        # Create JSON structure
        data = {"users": users}

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ Generated {len(users)} users")
        print(f"✓ Output file: {output_file}")
        print(f"\nNext steps:")
        print(f"  1. Validate: python cli.py bulk validate {output_file}")
        print(f"  2. Dry-run:  python cli.py bulk import {output_file} --dry-run")
        print(f"  3. Import:   python cli.py bulk import {output_file}")

    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing required column: {e}")
        print("Required columns: name, email")
        sys.exit(1)


def generate_users_from_list(names_emails, output_file="users_import.json", language="de", role=2):
    """
    Generate user import JSON from list of (name, email, ldap_username) tuples.

    Example:
    users_list = [
        ("Max Mustermann", "max@firma.de", "max.mustermann"),
        ("Anna Schmidt", "anna@firma.de", "anna.schmidt"),
    ]
    """
    users = []

    for item in names_emails:
        if len(item) == 2:
            name, email = item
            ldap = None
        elif len(item) == 3:
            name, email, ldap = item
        else:
            print(f"Warning: Skipping invalid item: {item}")
            continue

        user = {
            "name": name,
            "email": email,
            "language": language,
            "roles": [role]
        }

        if ldap:
            user["external_auth_id"] = ldap
        else:
            user["send_invite"] = True

        users.append(user)

    data = {"users": users}

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Generated {len(users)} users in {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generate_users_from_csv.py users.csv [output.json]")
        print("\nOr use programmatically:")
        print("  from generate_users_from_csv import generate_users_from_list")
        print()
        print("Example: Generate from list")

        # Example usage
        users_list = [
            ("Developer 1", "dev1@firma.de", "dev1"),
            ("Developer 2", "dev2@firma.de", "dev2"),
            ("Developer 3", "dev3@firma.de", "dev3"),
            ("Manager", "manager@firma.de", "manager"),
            ("Viewer", "viewer@firma.de", "viewer"),
        ]

        generate_users_from_list(users_list, "example_users.json", language="de", role=2)
        sys.exit(0)

    csv_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "users_import.json"

    generate_users_from_csv(csv_file, output_file)
