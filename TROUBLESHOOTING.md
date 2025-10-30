# Troubleshooting Guide

Dieser Guide hilft dir, Verbindungsprobleme mit der BookStack API zu lösen.

## Schnelltest

```bash
# Einfacher Test
python cli.py test

# Detaillierter Test mit Diagnoseinformationen
python cli.py test --detailed

# Mit Debug-Ausgabe
python cli.py test --debug
```

## Häufige Probleme und Lösungen

### Problem 1: "Connection failed" / "Cannot connect to BookStack"

**Symptom:**
```
✗ Connection failed!
Error: Cannot connect to BookStack
```

**Mögliche Ursachen und Lösungen:**

#### 1.1 URL ist falsch

**Prüfen:**
```bash
cat .env | grep BOOKSTACK_URL
```

**Häufige Fehler:**
- ❌ `BOOKSTACK_URL=bookstack.firma.de` (fehlt `https://`)
- ❌ `BOOKSTACK_URL=https://bookstack.firma.de/` (trailing slash)
- ✅ `BOOKSTACK_URL=https://bookstack.firma.de`

**Lösung:**
```bash
# In .env Datei korrigieren
BOOKSTACK_URL=https://bookstack.firma.de
```

#### 1.2 BookStack läuft nicht

**Prüfen:**
```bash
# Teste manuell im Browser oder mit curl
curl https://bookstack.firma.de

# Oder
ping bookstack.firma.de
```

**Lösung:**
- Stelle sicher, dass BookStack läuft
- Überprüfe den Server-Status

#### 1.3 Firewall blockiert Zugriff

**Symptom:**
```
Connection error: Cannot reach https://bookstack.firma.de
Please check:
  1. URL is correct
  2. BookStack is running and accessible
  3. Network/firewall allows connection
```

**Lösung:**
- Prüfe Firewall-Regeln
- Teste von anderem Netzwerk
- Kontaktiere IT-Admin

### Problem 2: SSL Certificate Verification Failed

**Symptom:**
```
✗ Connection failed!
Error: SSL certificate verification failed
Type: ssl_error
```

**Ursache:**
Deine BookStack-Instanz verwendet ein selbst-signiertes SSL-Zertifikat.

**Lösung 1: SSL-Verifizierung deaktivieren (für Entwicklung)**

In `.env` Datei:
```bash
BOOKSTACK_VERIFY_SSL=false
```

**Lösung 2: Zertifikat zum System hinzufügen**

Linux:
```bash
sudo cp your-cert.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

**Lösung 3: Programmatisch deaktivieren**

```python
from bookstack_api import BookStackClient

client = BookStackClient(verify_ssl=False)
```

### Problem 3: Authentication Failed / 401 Unauthorized

**Symptom:**
```
✗ Connection failed!
Error: Authentication failed
Type: auth_error
```

**Ursache:**
Token-ID oder Token-Secret sind falsch.

**Lösung:**

#### 3.1 Überprüfe Credentials

```bash
cat .env
```

Stelle sicher:
```bash
BOOKSTACK_URL=https://bookstack.firma.de
BOOKSTACK_TOKEN_ID=dein_token_id
BOOKSTACK_TOKEN_SECRET=dein_token_secret
```

#### 3.2 Erstelle neuen API-Token

1. Melde dich bei BookStack an
2. Gehe zu: **Einstellungen** → **API-Tokens**
3. Klicke auf **Token erstellen**
4. Kopiere **Token-ID** und **Secret**
5. Trage sie in `.env` ein

#### 3.3 Überprüfe Token-Berechtigungen

- Token muss aktiv sein
- Token braucht entsprechende Berechtigungen
- Benutzer braucht Admin-Rechte (für manche Operationen)

### Problem 4: Request Timeout

**Symptom:**
```
✗ Connection failed!
Error: Connection timeout
Type: timeout
```

**Ursache:**
BookStack antwortet zu langsam oder ist nicht erreichbar.

**Lösung 1: Timeout erhöhen**

```python
from bookstack_api import BookStackClient

client = BookStackClient(timeout=60)  # 60 Sekunden
```

**Lösung 2: Server-Performance prüfen**
- Überprüfe BookStack-Server-Load
- Prüfe Datenbank-Performance
- Kontaktiere Server-Admin

### Problem 5: Missing Credentials

**Symptom:**
```
Error: Missing credentials. Provide base_url, token_id, and token_secret
```

**Ursache:**
`.env` Datei fehlt oder ist nicht korrekt.

**Lösung:**

1. Erstelle `.env` Datei:
```bash
cp .env.example .env
```

2. Fülle Credentials aus:
```bash
nano .env  # oder dein Editor
```

3. Stelle sicher, dass Datei im richtigen Verzeichnis ist:
```bash
ls -la .env
```

### Problem 6: "Check your base_url"

**Symptom:**
```
Connection error. Check your base_url.
```

**Debug-Schritte:**

1. **Teste mit detailliertem Output:**
```bash
python cli.py test --detailed
```

2. **Aktiviere Debug-Modus:**
```bash
python cli.py test --debug
```

3. **Überprüfe URL-Format:**
```bash
# Falsch:
BOOKSTACK_URL=bookstack.firma.de          # Fehlt Protokoll
BOOKSTACK_URL=http://bookstack.firma.de/  # Trailing slash
BOOKSTACK_URL=https://bookstack.firma.de/api  # Zu spezifisch

# Richtig:
BOOKSTACK_URL=https://bookstack.firma.de
```

4. **Teste manuell:**
```bash
curl https://bookstack.firma.de/api/books \
  -H "Authorization: Token YOUR_TOKEN_ID:YOUR_TOKEN_SECRET"
```

## Debug-Modus nutzen

### In CLI

```bash
# Debug-Modus aktivieren
python cli.py test --debug

# Oder in .env
DEBUG=true
python cli.py test
```

### In Python

```python
from bookstack_api import BookStackClient

client = BookStackClient(debug=True)
```

**Ausgabe:**
```
[DEBUG] GET https://bookstack.firma.de/api/books
[DEBUG] Params: None
```

## Erweiterte Diagnose

### Test-Script erstellen

Erstelle `test_connection.py`:

```python
#!/usr/bin/env python3
from bookstack_api import BookStackClient

# Teste Connection mit detailliertem Output
client = BookStackClient(debug=True)

print("Testing connection...")
result = client.test_connection_detailed()

print("\n=== Detailed Result ===")
print(f"Success: {result['success']}")
print(f"Base URL: {result['base_url']}")
print(f"Endpoint: {result['endpoint']}")
print(f"SSL Verify: {result['ssl_verify']}")

if not result['success']:
    print(f"\nError: {result['error']}")
    print(f"Type: {result['error_type']}")

    if result.get('error_details'):
        print(f"\nDetails: {result['error_details']}")

    if result['suggestions']:
        print("\nSuggestions:")
        for s in result['suggestions']:
            print(f"  - {s}")
```

```bash
python test_connection.py
```

### Netzwerk-Diagnose

```bash
# Teste DNS-Auflösung
nslookup bookstack.firma.de

# Teste Erreichbarkeit
ping bookstack.firma.de

# Teste Port
telnet bookstack.firma.de 443

# Teste HTTP(S)
curl -v https://bookstack.firma.de
```

## Konfigurationsbeispiele

### Lokale Entwicklung (HTTP, keine SSL)

```bash
BOOKSTACK_URL=http://localhost:8080
BOOKSTACK_TOKEN_ID=your_token
BOOKSTACK_TOKEN_SECRET=your_secret
BOOKSTACK_VERIFY_SSL=false
```

### Produktion mit SSL

```bash
BOOKSTACK_URL=https://bookstack.firma.de
BOOKSTACK_TOKEN_ID=your_token
BOOKSTACK_TOKEN_SECRET=your_secret
BOOKSTACK_VERIFY_SSL=true
```

### Selbst-signiertes Zertifikat

```bash
BOOKSTACK_URL=https://bookstack-internal.local
BOOKSTACK_TOKEN_ID=your_token
BOOKSTACK_TOKEN_SECRET=your_secret
BOOKSTACK_VERIFY_SSL=false
```

## Checkliste

Wenn nichts funktioniert, gehe diese Checkliste durch:

- [ ] `.env` Datei existiert im Projektverzeichnis
- [ ] `BOOKSTACK_URL` ist korrekt (mit `https://`, ohne trailing slash)
- [ ] `BOOKSTACK_TOKEN_ID` ist korrekt
- [ ] `BOOKSTACK_TOKEN_SECRET` ist korrekt
- [ ] BookStack ist erreichbar (teste im Browser)
- [ ] API-Token ist aktiv in BookStack
- [ ] Firewall erlaubt Verbindung
- [ ] SSL-Zertifikat ist gültig (oder `BOOKSTACK_VERIFY_SSL=false`)
- [ ] Python-Dependencies sind installiert (`pip install -r requirements.txt`)
- [ ] Keine Tippfehler in `.env` (Leerzeichen, Anführungszeichen, etc.)

## Hilfe bekommen

Wenn du immer noch Probleme hast:

1. **Führe aus:**
```bash
python cli.py test --detailed --debug
```

2. **Sammle Informationen:**
- BookStack Version
- Python Version (`python --version`)
- Betriebssystem
- Fehlermeldung (vollständig)

3. **Erstelle ein Issue:**
GitHub: https://github.com/yourusername/bookstack-api-magician/issues

4. **Logs prüfen:**
- BookStack Server-Logs
- Apache/Nginx Logs
- Python Traceback

## Siehe auch

- [README.md](README.md) - Hauptdokumentation
- [QUICKSTART.md](QUICKSTART.md) - Schnellstart-Guide
- [BookStack API Docs](https://demo.bookstackapp.com/api/docs) - Offizielle API-Dokumentation
