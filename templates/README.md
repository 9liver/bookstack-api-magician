# JSON Templates

Dieses Verzeichnis enthält Beispiel-JSON-Dateien für Bulk-Import-Operationen.

## Verfügbare Templates

### 1. users_ldap.json

Erstellt LDAP-Benutzer mit external_auth_id:

```json
{
  "users": [
    {
      "name": "Max Mustermann",
      "email": "max.mustermann@example.com",
      "external_auth_id": "max.mustermann",
      "language": "de",
      "roles": [2]
    }
  ]
}
```

**Verwendung:**
```bash
python cli.py bulk import templates/users_ldap.json
```

### 2. users_regular.json

Erstellt reguläre Benutzer mit Passwort oder Einladung:

```json
{
  "users": [
    {
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "password": "SecurePassword123!",
      "language": "en",
      "send_invite": false
    }
  ]
}
```

### 3. complete_structure.json

Erstellt eine komplette verschachtelte Struktur mit:
- Shelf (Regal)
- Mehrere Books (Bücher)
- Chapters (Kapitel) in den Books
- Pages (Seiten) in den Chapters
- Tags und Metadaten

**Verwendung:**
```bash
python cli.py bulk import templates/complete_structure.json
```

### 4. simple_book.json

Erstellt ein einfaches Book mit Pages:

```json
{
  "books": [
    {
      "name": "Simple Documentation",
      "pages": [
        {
          "name": "Introduction",
          "markdown": "# Introduction\n\nWelcome!"
        }
      ]
    }
  ]
}
```

### 5. project_documentation.json

Erstellt eine vollständige Projektdokumentation mit mehreren Books und verschachtelten Chapters.

## JSON-Struktur

### Vollständiges Beispiel mit allen Optionen

```json
{
  "users": [
    {
      "name": "Benutzername (erforderlich)",
      "email": "email@example.com (erforderlich)",
      "external_auth_id": "ldap_username (optional, für LDAP)",
      "password": "Passwort (optional, wenn kein LDAP)",
      "send_invite": true,
      "language": "de",
      "roles": [2, 3]
    }
  ],
  "structures": [
    {
      "type": "shelf",
      "name": "Shelf Name (erforderlich)",
      "description": "Beschreibung (optional)",
      "tags": [
        {"name": "tag_name", "value": "tag_value"}
      ],
      "books": [
        {
          "name": "Book Name (erforderlich)",
          "description": "Beschreibung (optional)",
          "tags": [
            {"name": "tag_name", "value": "tag_value"}
          ],
          "chapters": [
            {
              "name": "Chapter Name (erforderlich)",
              "description": "Beschreibung (optional)",
              "priority": 1,
              "pages": [
                {
                  "name": "Page Name (erforderlich)",
                  "markdown": "# Markdown Content",
                  "html": "<h1>HTML Content</h1>",
                  "priority": 1,
                  "tags": [
                    {"name": "tag_name", "value": "tag_value"}
                  ]
                }
              ]
            }
          ],
          "pages": [
            {
              "name": "Standalone Page",
              "markdown": "# Content"
            }
          ]
        }
      ]
    }
  ]
}
```

## Hinweise

### LDAP-Benutzer

Für LDAP-Benutzer:
- Verwende `external_auth_id` statt `password`
- Der `external_auth_id` muss mit dem LDAP-Benutzernamen übereinstimmen
- Kein `send_invite` erforderlich

### Rollen

Standard-Rollen in BookStack:
- `1` = Guest
- `2` = Viewer
- `3` = Editor
- `4` = Admin

Passe die Rollen-IDs an deine BookStack-Instanz an.

### Content-Formate

Pages können entweder `markdown` oder `html` verwenden:
- `"markdown"`: Verwendet Markdown-Syntax
- `"html"`: Verwendet HTML-Markup

### Tags

Tags sind optional und folgen diesem Format:
```json
"tags": [
  {"name": "category", "value": "documentation"},
  {"name": "version", "value": "1.0"}
]
```

## Befehle

### Validieren vor dem Import

```bash
# JSON-Syntax prüfen
python cli.py bulk validate templates/users_ldap.json

# Dry-Run durchführen
python cli.py bulk import templates/complete_structure.json --dry-run
```

### Import durchführen

```bash
# Benutzer importieren
python cli.py bulk import templates/users_ldap.json

# Struktur importieren
python cli.py bulk import templates/complete_structure.json
```

### Beispiel-Datei generieren

```bash
# Vollständiges Beispiel
python cli.py bulk example my_import.json --type full

# Nur Benutzer
python cli.py bulk example users.json --type users

# Nur Struktur
python cli.py bulk example structure.json --type structure

# Einfaches Beispiel
python cli.py bulk example simple.json --type simple
```

## Eigene Templates erstellen

1. Kopiere ein passendes Template
2. Passe die Werte an deine Bedürfnisse an
3. Validiere die JSON-Datei
4. Führe einen Dry-Run durch
5. Importiere die Daten

## Troubleshooting

### Fehler: "Missing name or email"

Stelle sicher, dass jeder Benutzer `name` und `email` hat.

### Fehler: "Validation error"

- Prüfe die JSON-Syntax mit `bulk validate`
- Stelle sicher, dass alle erforderlichen Felder vorhanden sind
- Überprüfe die Rollen-IDs

### LDAP-Authentifizierung funktioniert nicht

- Stelle sicher, dass LDAP in BookStack konfiguriert ist
- Der `external_auth_id` muss exakt mit dem LDAP-Benutzernamen übereinstimmen
- Keine Leerzeichen oder Sonderzeichen im `external_auth_id`
