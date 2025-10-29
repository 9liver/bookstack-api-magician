# Schnellstart-Anleitung

## Installation

```bash
# Klone das Repository
git clone <repository-url>
cd bookstack-api-magician

# Installiere Dependencies
pip install -r requirements.txt

# Optional: Installiere das Paket
pip install -e .
```

## Konfiguration

1. Erstelle eine `.env` Datei:
```bash
cp .env.example .env
```

2. Trage deine BookStack-Zugangsdaten ein:
```env
BOOKSTACK_URL=https://deine-bookstack-instanz.de
BOOKSTACK_TOKEN_ID=dein_token_id
BOOKSTACK_TOKEN_SECRET=dein_token_secret
```

### BookStack API-Token erstellen

1. Melde dich bei deiner BookStack-Instanz an
2. Gehe zu **Einstellungen** → **API-Tokens**
3. Klicke auf **Token erstellen**
4. Kopiere Token-ID und Secret in die `.env` Datei

## Erste Schritte

### 1. Verbindung testen

```bash
python cli.py test
```

### 2. Inhalte auflisten

```bash
# Shelves auflisten
python cli.py shelves list

# Books auflisten
python cli.py books list

# Benutzer auflisten
python cli.py users list
```

### 3. Neues Shelf erstellen

```bash
python cli.py shelves create --name "Mein Regal" --description "Beschreibung"
```

### 4. Neues Book erstellen

```bash
python cli.py books create --name "Mein Buch" --description "Ein tolles Buch"
```

### 5. Neue Page erstellen

```bash
python cli.py pages create --book-id 1 --name "Startseite" --markdown "# Willkommen"
```

## Als Python-Modul verwenden

```python
from bookstack_api import BookStackClient

# Client initialisieren
client = BookStackClient()

# Verbindung testen
if client.test_connection():
    print("Verbunden!")

# Shelves auflisten
shelves = client.shelves.list()
for shelf in shelves:
    print(f"Shelf: {shelf['name']}")

# Neues Book erstellen
book = client.books.create(
    name="Mein API-Buch",
    description="Erstellt via API"
)
print(f"Book erstellt: {book['id']}")

# Page mit Markdown erstellen
page = client.pages.create(
    book_id=book['id'],
    name="Erste Seite",
    markdown="# Hallo Welt\n\nDies ist meine erste Seite!"
)
print(f"Page erstellt: {page['id']}")
```

## Beispielskripte

Im `examples/` Verzeichnis findest du weitere Beispiele:

- `basic_usage.py` - Grundlegende Operationen
- `bulk_operations.py` - Batch-Operationen
- `user_management.py` - Benutzerverwaltung
- `export_content.py` - Inhalte exportieren

```bash
# Beispiel ausführen
python examples/basic_usage.py
```

## CLI-Hilfe

```bash
# Allgemeine Hilfe
python cli.py --help

# Hilfe für spezifische Befehle
python cli.py shelves --help
python cli.py books --help
python cli.py users --help
```

## Häufige Anwendungsfälle

### Komplette Dokumentationsstruktur erstellen

```python
from bookstack_api import BookStackClient

client = BookStackClient()

# Shelf erstellen
shelf = client.shelves.create(name="Dokumentation")

# Book erstellen
book = client.books.create(name="Handbuch")

# Chapter erstellen
chapter = client.chapters.create(
    book_id=book['id'],
    name="Kapitel 1"
)

# Pages erstellen
for i in range(1, 4):
    client.pages.create(
        book_id=book['id'],
        chapter_id=chapter['id'],
        name=f"Seite {i}",
        markdown=f"# Seite {i}\n\nInhalt..."
    )

# Book zum Shelf hinzufügen
client.shelves.update(shelf['id'], books=[book['id']])
```

### Benutzer in großen Mengen erstellen

```python
users_data = [
    {"name": "Max Mustermann", "email": "max@example.com"},
    {"name": "Anna Schmidt", "email": "anna@example.com"},
]

for user_info in users_data:
    client.users.create(
        name=user_info['name'],
        email=user_info['email'],
        send_invite=True
    )
```

## Fehlerbehebung

### Verbindungsfehler

```bash
# Überprüfe URL und Credentials in .env
cat .env

# Teste Verbindung
python cli.py test
```

### API-Fehler

Die meisten API-Fehler werden mit hilfreichen Meldungen angezeigt:

- **401 Unauthorized**: Überprüfe Token-ID und Secret
- **403 Forbidden**: Keine Berechtigung für diese Aktion
- **404 Not Found**: Ressource existiert nicht
- **422 Validation Error**: Ungültige Eingabedaten

## Weitere Informationen

Siehe [README.md](README.md) für vollständige API-Dokumentation.
