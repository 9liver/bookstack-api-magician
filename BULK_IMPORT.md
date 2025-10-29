# Bulk-Import Guide

Dieser Guide zeigt, wie du große Mengen an Daten und Strukturen mit JSON-Dateien in BookStack importieren kannst.

## Übersicht

Der Bulk-Import ermöglicht:
- ✅ Mehrere Benutzer gleichzeitig anlegen (LDAP & regulär)
- ✅ Komplette verschachtelte Strukturen erstellen (Shelf → Books → Chapters → Pages)
- ✅ Alle Ebenen in einem Schritt
- ✅ Validierung vor dem Import
- ✅ Dry-Run zum Testen

## Schnellstart

### 1. Beispiel-Datei generieren

```bash
# Vollständiges Beispiel mit allen Features
python cli.py bulk example my_structure.json --type full

# Nur Benutzer
python cli.py bulk example users.json --type users

# Nur Struktur
python cli.py bulk example structure.json --type structure

# Einfaches Beispiel
python cli.py bulk example simple.json --type simple
```

### 2. JSON-Datei bearbeiten

Passe die generierte JSON-Datei an deine Bedürfnisse an.

### 3. Validieren

```bash
python cli.py bulk validate my_structure.json
```

### 4. Dry-Run durchführen

```bash
python cli.py bulk import my_structure.json --dry-run
```

### 5. Import durchführen

```bash
python cli.py bulk import my_structure.json
```

## Use-Cases

### Use-Case 1: LDAP-Benutzer importieren

**Datei: `users_ldap.json`**

```json
{
  "users": [
    {
      "name": "Max Mustermann",
      "email": "max.mustermann@firma.de",
      "external_auth_id": "max.mustermann",
      "language": "de",
      "roles": [2]
    },
    {
      "name": "Anna Schmidt",
      "email": "anna.schmidt@firma.de",
      "external_auth_id": "anna.schmidt",
      "language": "de",
      "roles": [3]
    }
  ]
}
```

**Import:**
```bash
python cli.py bulk import users_ldap.json
```

**Wichtig für LDAP:**
- `external_auth_id` muss mit LDAP-Benutzername übereinstimmen
- Kein Passwort erforderlich
- LDAP muss in BookStack konfiguriert sein

### Use-Case 2: Komplette Dokumentationsstruktur erstellen

**Datei: `documentation.json`**

```json
{
  "structures": [
    {
      "type": "shelf",
      "name": "Projekt Alpha Dokumentation",
      "description": "Vollständige Projekt-Dokumentation",
      "books": [
        {
          "name": "Installations-Anleitung",
          "description": "Schritt-für-Schritt Installation",
          "chapters": [
            {
              "name": "Voraussetzungen",
              "description": "Was benötigt wird",
              "pages": [
                {
                  "name": "System-Anforderungen",
                  "markdown": "# System-Anforderungen\n\n- CPU: 2+ Kerne\n- RAM: 4GB"
                },
                {
                  "name": "Software-Abhängigkeiten",
                  "markdown": "# Software\n\n- PHP 8.1+\n- MySQL 5.7+"
                }
              ]
            },
            {
              "name": "Installation",
              "pages": [
                {
                  "name": "Schritt 1: Download",
                  "markdown": "# Download\n\n1. Gehe zu...\n2. Lade herunter..."
                },
                {
                  "name": "Schritt 2: Konfiguration",
                  "markdown": "# Konfiguration\n\n..."
                }
              ]
            }
          ],
          "pages": [
            {
              "name": "Schnellstart",
              "markdown": "# Schnellstart\n\nIn 5 Minuten loslegen!"
            }
          ]
        },
        {
          "name": "Benutzerhandbuch",
          "chapters": [
            {
              "name": "Erste Schritte",
              "pages": [
                {
                  "name": "Login",
                  "markdown": "# Anmeldung\n\nSo meldest du dich an..."
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Import:**
```bash
python cli.py bulk import documentation.json
```

**Ergebnis:**
- 1 Shelf erstellt
- 2 Books erstellt und dem Shelf zugeordnet
- Alle Chapters erstellt
- Alle Pages erstellt und zugeordnet

### Use-Case 3: Team-Onboarding

Erstelle Benutzer und Dokumentation in einem Schritt:

```json
{
  "users": [
    {
      "name": "Neuer Mitarbeiter 1",
      "email": "mitarbeiter1@firma.de",
      "external_auth_id": "mitarbeiter1",
      "language": "de",
      "roles": [2]
    },
    {
      "name": "Neuer Mitarbeiter 2",
      "email": "mitarbeiter2@firma.de",
      "external_auth_id": "mitarbeiter2",
      "language": "de",
      "roles": [2]
    }
  ],
  "structures": [
    {
      "type": "shelf",
      "name": "Onboarding",
      "books": [
        {
          "name": "Willkommen im Team",
          "pages": [
            {
              "name": "Erste Schritte",
              "markdown": "# Willkommen!\n\nHier findest du alle wichtigen Infos..."
            }
          ]
        }
      ]
    }
  ]
}
```

## JSON-Schema-Referenz

### Benutzer-Objekt

```json
{
  "name": "Name (erforderlich)",
  "email": "email@example.com (erforderlich)",
  "external_auth_id": "ldap_username (optional, für LDAP)",
  "password": "Passwort (optional, wenn kein LDAP)",
  "send_invite": true,
  "language": "de|en|...",
  "roles": [2, 3]
}
```

### Struktur-Objekt

```json
{
  "type": "shelf",
  "name": "Name (erforderlich)",
  "description": "Beschreibung (optional)",
  "tags": [
    {"name": "key", "value": "value"}
  ],
  "books": [...]
}
```

### Book-Objekt

```json
{
  "name": "Name (erforderlich)",
  "description": "Beschreibung (optional)",
  "tags": [...],
  "chapters": [...],
  "pages": [...]
}
```

### Chapter-Objekt

```json
{
  "name": "Name (erforderlich)",
  "description": "Beschreibung (optional)",
  "priority": 1,
  "tags": [...],
  "pages": [...]
}
```

### Page-Objekt

```json
{
  "name": "Name (erforderlich)",
  "markdown": "# Markdown-Inhalt",
  "html": "<h1>HTML-Inhalt</h1>",
  "priority": 1,
  "tags": [...]
}
```

**Hinweis:** Verwende entweder `markdown` oder `html`, nicht beides.

## Rollen-IDs

Standard-Rollen in BookStack:
- `1` = Guest (Gast)
- `2` = Viewer (Betrachter)
- `3` = Editor (Bearbeiter)
- `4` = Admin (Administrator)

**Tipp:** Überprüfe die Rollen-IDs in deiner BookStack-Instanz, da sie abweichen können.

## Tipps & Best Practices

### 1. Immer validieren

```bash
python cli.py bulk validate my_import.json
```

### 2. Dry-Run durchführen

```bash
python cli.py bulk import my_import.json --dry-run
```

### 3. Kleine Batches zuerst

Teste mit kleinen Dateien, bevor du große Importe durchführst.

### 4. Backups erstellen

Erstelle ein Backup deiner BookStack-Instanz vor großen Importen.

### 5. LDAP testen

Teste LDAP-Benutzer einzeln, bevor du viele importierst:

```json
{
  "users": [
    {
      "name": "Test User",
      "email": "test@firma.de",
      "external_auth_id": "test.user",
      "language": "de",
      "roles": [2]
    }
  ]
}
```

## Fehlerbehandlung

### Fehler: "Missing name or email"

**Problem:** Pflichtfelder fehlen

**Lösung:**
```bash
python cli.py bulk validate my_import.json
```

### Fehler: "Validation error"

**Problem:** Ungültige Daten (z.B. falsche Rollen-ID)

**Lösung:**
- Überprüfe Rollen-IDs
- Validiere JSON-Syntax
- Prüfe erforderliche Felder

### LDAP-Benutzer kann sich nicht anmelden

**Problem:** LDAP nicht konfiguriert oder falscher `external_auth_id`

**Lösung:**
1. Überprüfe LDAP-Konfiguration in BookStack
2. Teste LDAP-Verbindung
3. Stelle sicher, dass `external_auth_id` exakt dem LDAP-Username entspricht

## Fortgeschrittene Beispiele

### Mehrere Shelves mit vielen Books

```json
{
  "structures": [
    {
      "type": "shelf",
      "name": "Entwickler-Dokumentation",
      "books": [...]
    },
    {
      "type": "shelf",
      "name": "Benutzer-Dokumentation",
      "books": [...]
    },
    {
      "type": "shelf",
      "name": "Admin-Dokumentation",
      "books": [...]
    }
  ]
}
```

### Tags verwenden

```json
{
  "structures": [
    {
      "type": "shelf",
      "name": "Dokumentation",
      "tags": [
        {"name": "category", "value": "documentation"},
        {"name": "version", "value": "2.0"},
        {"name": "status", "value": "published"}
      ],
      "books": [...]
    }
  ]
}
```

## Programmatische Verwendung

Du kannst den BulkImporter auch direkt in Python verwenden:

```python
from bookstack_api import BookStackClient
from bookstack_api.bulk_import import BulkImporter

client = BookStackClient()
importer = BulkImporter(client)

# Import von Datei
result = importer.import_from_file("my_structure.json")

# Zusammenfassung anzeigen
importer.print_summary()

# Zugriff auf erstellte Items
shelves = importer.created_items["shelves"]
books = importer.created_items["books"]
users = importer.created_items["users"]
```

## Weitere Ressourcen

- Siehe `templates/` Verzeichnis für mehr Beispiele
- Siehe `examples/bulk_import_example.py` für Python-Code
- [BookStack API Dokumentation](https://demo.bookstackapp.com/api/docs)
