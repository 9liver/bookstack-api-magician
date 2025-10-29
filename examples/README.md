# Beispielskripte

Dieses Verzeichnis enthält Beispielskripte zur Verwendung des BookStack API Magician.

## Voraussetzungen

Stelle sicher, dass du die `.env` Datei im Hauptverzeichnis konfiguriert hast:

```bash
cd ..
cp .env.example .env
# Bearbeite .env und trage deine Credentials ein
```

## Verfügbare Beispiele

### 1. basic_usage.py

Grundlegende Verwendung aller Hauptfunktionen:
- Shelves erstellen und verwalten
- Books erstellen und verwalten
- Chapters erstellen
- Pages mit Markdown und HTML erstellen

```bash
python basic_usage.py
```

### 2. bulk_operations.py

Batch-Operationen für größere Strukturen:
- Erstellen kompletter Dokumentationsstrukturen
- Mehrere Books, Chapters und Pages auf einmal
- Übersicht aller Inhalte

```bash
python bulk_operations.py
```

### 3. user_management.py

Benutzerverwaltung:
- Benutzer auflisten
- Mehrere Benutzer erstellen
- Benutzerinformationen aktualisieren
- Benutzer suchen

```bash
python user_management.py
```

### 4. export_content.py

Export-Funktionen:
- Book-Struktur als JSON exportieren
- Shelf-Struktur exportieren
- Alle Benutzer exportieren

```bash
python export_content.py
```

## Anpassung

Alle Beispielskripte können als Vorlage für eigene Anwendungsfälle verwendet werden. Kopiere einfach das relevante Skript und passe es an deine Bedürfnisse an.

## Weitere Informationen

Siehe die [Hauptdokumentation](../README.md) und [Schnellstart-Anleitung](../QUICKSTART.md).
