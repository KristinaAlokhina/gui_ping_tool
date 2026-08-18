# Grafisches Ping-Werkzeug (Advanced GUI Ping Tool)

<p align="center">
  <a href="#-deutsch">Deutsch</a> • 
  <a href="#-english">English</a>
</p>

---

## 🇩🇪 Deutsch

### 🚀 Funktionen
* **Asynchroner Ping-Test**: Nahtlose Ausführung von Netzwerkanfragen im Hintergrund (Threading verhindert das Einfrieren der GUI bei der Host-Überprüfung).
* **🔄 Endlos-Ping (Loop Mode)**: Kontinuierliche Überwachung eines Hosts im Sekundentakt für Echtzeit-Diagnosen.
* **🔊 Audio-Benachrichtigung**: Automatisches akustisches Signal (System-Bell) bei Statusänderungen des Netzwerks (z. B. wenn ein Host offline geht).
* **⚡ Schnellauswahl-Presets**: Integrierte Tasten für den Schnellzugriff auf `Localhost (127.0.0.1)`, `Router (GW)` und `Google DNS (8.8.8.8)`.
* **Intelligente Latenz-Analyse**: Automatische Filterung der Konsolenausgabe über Regex zur exakten Extraktion der Paketlaufzeit in Millisekunden (ms) – kompatibel mit deutschen und englischen Betriebssystemen.
* **Dynamische UI-Steuerung**: Der Prüf-Button passt sich autonom an (Start/Stopp-Logik), während das Eingabefeld im Loop-Modus gesperrt wird, um Fehlkonfigurationen zu vermeiden.
* **Erweiterte Verlaufslogik**: Automatische Aufteilung der validierten Abfragen (unterstützt Hostnamen, IPv4 und IPv6) in Echtzeit auf zwei dedizierte Tabs ("Zuletzt verwendet" und "Häufig genutzt").
* **Interaktive Listen**: Ein Doppelklick auf historische Einträge fügt die Adresse sofort in das Hauptfeld ein und wechselt den Tab.
* **Persistente Speicherung**: Alle Abfragen bleiben durch die lokale Dateianbindung (`ping_history.txt`) auch nach Schließen der App vollständig erhalten.

### 🛠️ Technologien
* Python 3.10+
* GUI-Framework: **Tkinter** mit modernem `ttk`-Layout ('clam' Theme)
* Systemnahe Module: `subprocess` (mit unterdrücktem Konsolen-Flackern auf Windows via `STARTUPINFO`) und `platform`
* Datenverarbeitung: Reguläre Ausdrücke (`re`) und asynchrone Threads (`threading`)
* Datenspeicher: Lokale Dateiverbindung für transaktionssicheres Logging mit integrierter Bereinigungsfunktion

### 📂 Struktur der Benutzeroberfläche
Das Anwendungsfenster verwendet ein Tab-basiertes Layout:
* **Ping-Test**: Ein zentraler Eingabebereich mit Fokus-Steuerung, Schnellauswahl-Leiste, Checkboxen für Loop/Sound und einem Status-Indikator, der über dynamische Farbcodierung (Grün/Rot) die Erreichbarkeit signalisiert.
* **Zuletzt verwendet**: Eine historische Auflistung der letzten 10 kontaktierten Hosts in umgekehrter chronologischer Reihenfolge.
* **Häufig genutzt**: Eine analytische Rangliste der am häufigsten abgefragten Netzwerkgeräte zur schnellen Diagnose.

### 📦 Installation & Ausführung

#### Option 1: Start über CLI (Entwicklungsmodus)
1. Repository klonen:
   ```bash
   git clone https://github.com/KristinaAlokhina
   ```
2. In den Projektordner wechseln:
   ```bash
   cd gui_ping_tool
   ```
3. Anwendung ausführen:
   ```bash
   python gui_ping_tool.py
   ```

#### Option 2: Eigenständige EXE-Datei erstellen (Windows)
Falls Sie das Tool als portable Anwendung ohne Python-Installation nutzen möchten:
1. `pyinstaller` installieren:
   ```bash
   pip install pyinstaller
   ```
2. Die ausführbare Datei generieren:
   ```bash
   python -m PyInstaller --noconsole --onefile gui_ping_tool.py
   ```
3. Die fertige App im neu erstellten Ordner `dist/` abholen.

---

## 🇺🇸 English

### 🚀 Features
* **Asynchronous Ping Engine**: Seamless execution of network requests in the background (Threading prevents GUI freezing during host checks).
* **🔄 Continuous Ping (Loop Mode)**: Monitor network hosts dynamically with 1-second update intervals for live diagnosis.
* **🔊 Audio Notifications**: Automatic system bell alert on host status changes (e.g., when a monitored host drops offline).
* **⚡ Quick-Select Presets**: Dedicated single-click buttons for immediate access to `Localhost (127.0.0.1)`, `Router (GW)`, and `Google DNS (8.8.8.8)`.
* **Smart Latency Parsing**: Automatic console output filtering via Regex to accurately extract packet round-trip times in milliseconds (ms) – compatible with English and German OS locales.
* **Dynamic UI Control**: The action button adapts itself autonomously (Start/Stop logic) while locking the input field during loops to block duplicate overlapping requests.
* **Advanced History Logic**: Real-time distribution of validated inputs (supporting hostnames, IPv4, and IPv6) into two dedicated tabs ("Recent" and "Frequent").
* **Interactive List Boxes**: Double-clicking on historical entries immediately loads the address into the input field and switches tabs.
* **Persistent Storage**: All diagnostic logs are securely stored locally and remain fully intact inside `ping_history.txt` after closing the application.

### 🛠️ Technologies
* Python 3.10+
* GUI Framework: **Tkinter** utilizing modern `ttk` layouts ('clam' theme)
* Core System Modules: `subprocess` (with suppressed console flickering on Windows via `STARTUPINFO`) and `platform`
* Processing Power: Regular Expressions (`re`) and asynchronous multi-threading (`threading`)
* Data Management: Plain-text local database integration with built-in clean-up functionality

### 📂 User Interface Structure
The interface window is divided into a versatile tabbed panel:
* **Ping Test**: The main diagnostic hub featuring an auto-focused entry field, quick-preset bar, loop/sound checkboxes, and a status label with responsive color-coding (Green/Red).
* **Recent**: A chronological feed tracking the last 10 tested hosts in reverse order for immediate lookup.
* **Frequent**: An analytical leaderboard sorting the most heavily targeted network hosts for priority testing.

### 📦 Installation & Setup

#### Option 1: Build from Source (CLI Mode)
1. Clone the repository:
   ```bash
   git clone https://github.com/KristinaAlokhina
   ```
2. Navigate to the project directory:
   ```bash
   cd gui_ping_tool
   ```
3. Run the application:
   ```bash
   python gui_ping_tool.py
   ```

#### Option 2: Build a Standalone Executable (Windows)
To run the utility as an independent portable `.exe` file without a Python environment:
1. Install `pyinstaller`:
   ```bash
   pip install pyinstaller
   ```
2. Generate the binary file:
   ```bash
   python -m PyInstaller --noconsole --onefile gui_ping_tool.py
   ```
3. Retrieve your executable from the newly created `dist/` directory.
