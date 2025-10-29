# BookStack API Magician

Ein umfassendes Python-Tool zur Verwaltung von BookStack über die API.

## Features

- 📚 **Ordnerstruktur-Verwaltung**
  - Shelves (Regale) erstellen, aktualisieren, löschen
  - Books (Bücher) verwalten
  - Chapters (Kapitel) organisieren
  - Pages (Seiten) bearbeiten

- 👥 **Benutzerverwaltung**
  - Benutzer erstellen und verwalten
  - Rollen und Berechtigungen zuweisen
  - Batch-Operationen

- 🔧 **CLI-Interface**
  - Einfache Kommandozeilen-Befehle
  - Interaktiver Modus
  - Batch-Operationen via JSON

## Installation

```bash
pip install -r requirements.txt
```

## Konfiguration

1. Kopiere `.env.example` zu `.env`:
```bash
cp .env.example .env
```

2. Trage deine BookStack-Credentials ein:
```
BOOKSTACK_URL=https://dein-bookstack.example.com
BOOKSTACK_TOKEN_ID=dein_token_id
BOOKSTACK_TOKEN_SECRET=dein_token_secret
```

## Verwendung

### Als Python-Modul

```python
from bookstack_api import BookStackClient

# Client initialisieren
client = BookStackClient(
    base_url="https://dein-bookstack.example.com",
    token_id="dein_token_id",
    token_secret="dein_token_secret"
)

# Shelves verwalten
shelves = client.shelves.list()
shelf = client.shelves.create(name="Mein Regal", description="Beschreibung")

# Books verwalten
books = client.books.list()
book = client.books.create(name="Mein Buch", description="Beschreibung")

# Benutzer verwalten
users = client.users.list()
user = client.users.create(
    name="Max Mustermann",
    email="max@example.com"
)
```

### CLI-Tool

```bash
# Shelves auflisten
python cli.py shelves list

# Shelf erstellen
python cli.py shelves create --name "Mein Regal" --description "Beschreibung"

# Book erstellen
python cli.py books create --name "Mein Buch"

# Benutzer auflisten
python cli.py users list

# Benutzer erstellen
python cli.py users create --name "Max Mustermann" --email "max@example.com"

# Komplette Struktur exportieren
python cli.py export --output structure.json

# Struktur importieren
python cli.py import --input structure.json
```

## API-Dokumentation

### Shelves (Regale)

- `shelves.list()` - Alle Shelves auflisten
- `shelves.get(id)` - Shelf nach ID abrufen
- `shelves.create(name, description, books)` - Neues Shelf erstellen
- `shelves.update(id, **kwargs)` - Shelf aktualisieren
- `shelves.delete(id)` - Shelf löschen

### Books (Bücher)

- `books.list()` - Alle Books auflisten
- `books.get(id)` - Book nach ID abrufen
- `books.create(name, description)` - Neues Book erstellen
- `books.update(id, **kwargs)` - Book aktualisieren
- `books.delete(id)` - Book löschen

### Chapters (Kapitel)

- `chapters.list()` - Alle Chapters auflisten
- `chapters.get(id)` - Chapter nach ID abrufen
- `chapters.create(book_id, name, description)` - Neues Chapter erstellen
- `chapters.update(id, **kwargs)` - Chapter aktualisieren
- `chapters.delete(id)` - Chapter löschen

### Pages (Seiten)

- `pages.list()` - Alle Pages auflisten
- `pages.get(id)` - Page nach ID abrufen
- `pages.create(book_id, name, html, markdown)` - Neue Page erstellen
- `pages.update(id, **kwargs)` - Page aktualisieren
- `pages.delete(id)` - Page löschen

### Users (Benutzer)

- `users.list()` - Alle Benutzer auflisten
- `users.get(id)` - Benutzer nach ID abrufen
- `users.create(name, email, **kwargs)` - Neuen Benutzer erstellen
- `users.update(id, **kwargs)` - Benutzer aktualisieren
- `users.delete(id)` - Benutzer löschen

## Beispiele

Siehe `examples/` Verzeichnis für vollständige Beispielskripte.

## Lizenz

MIT License
