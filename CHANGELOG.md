# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [1.0.0] - 2025-10-29

### Hinzugefügt

- Vollständiger BookStack API Client
- Verwaltung von Shelves (Regale)
  - Erstellen, Lesen, Aktualisieren, Löschen
  - Export als HTML, Markdown, Plain Text
- Verwaltung von Books (Bücher)
  - Erstellen, Lesen, Aktualisieren, Löschen
  - Export-Funktionen
- Verwaltung von Chapters (Kapitel)
  - Erstellen, Lesen, Aktualisieren, Löschen
  - Zuordnung zu Books
- Verwaltung von Pages (Seiten)
  - Erstellen, Lesen, Aktualisieren, Löschen
  - Unterstützung für HTML und Markdown
  - Zuordnung zu Books und Chapters
- Benutzerverwaltung
  - Erstellen, Lesen, Aktualisieren, Löschen
  - Einladungen versenden
  - Mehrsprachige Unterstützung
- CLI-Interface mit Rich-Formatierung
  - Farbige Tabellenausgabe
  - JSON-Export-Option
  - Interaktive Bestätigungen
- Umfassende Fehlerbehandlung
  - Spezifische Exceptions für verschiedene Fehlertypen
  - Hilfreiche Fehlermeldungen
- Konfiguration über .env Datei
- Beispielskripte
  - Grundlegende Verwendung
  - Batch-Operationen
  - Benutzerverwaltung
  - Content-Export
- Vollständige Dokumentation
  - README mit API-Referenz
  - Schnellstart-Anleitung
  - Lizenz (MIT)

### Features

- Automatische Paginierung
- Sortier- und Filterfunktionen
- Tag-Unterstützung
- Export-Funktionen
- Batch-Operationen
- Type Hints für bessere IDE-Unterstützung
- Pydantic-Modelle für Datenvalidierung

### Technische Details

- Python 3.8+ Unterstützung
- Verwendet `requests` für HTTP-Anfragen
- `click` für CLI
- `rich` für formatierte Ausgabe
- `pydantic` für Datenmodelle
- `python-dotenv` für Konfiguration
