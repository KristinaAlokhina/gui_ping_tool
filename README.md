# Grafisches Ping-Werkzeug (Advanced GUI Ping Tool)

<p align="center">
  <a href="#-deutsch">Deutsch</a> • 
  <a href="#-english">English</a>
</p>

---

## 🇩🇪 Deutsch

### 🚀 Funktionen
* **Asynchroner Ping-Test**: Nahtlose Ausführung von Netzwerkanfragen im Hintergrund (Threading verhindert das Einfrieren der GUI bei der Host-Überprüfung).
* **Intelligente Latenz-Analyse**: Automatische Filterung der Konsolenausgabe über Regex zur exakten Extraktion der Paketlaufzeit in Millisekunden (ms).
* **Dynamische UI-Steuerung**: Der Prüf-Button deaktiviert sich während der Laufzeit autonom, um parallele Fehlanfragen zu blockieren.
* **Erweiterte Verlaufslogik**: Automatische Aufteilung der Abfragen in Echtzeit auf zwei dedizierte Tabs ("Zuletzt verwendet" und "Häufig genutzt").
* **Interaktive Listen**: Ein Doppelklick auf historische Einträge fügt die Adresse sofort in das Hauptfeld ein und wechselt den Tab.
* **Persistente Speicherung**: Alle Abfragen bleiben durch die lokale Dateianbindung (`ping_history.txt`) auch nach Schließen der App vollständig erhalten.

### 🛠️ Technologien
* Python 3.10+
* GUI-Framework: **Tkinter** mit modernem `ttk`-Layout
* Systemnahe Module: `subprocess` (mit unterdrücktem Konsolen-Flackern auf Windows via `STARTUPINFO`) und `platform`
* Datenverarbeitung: Регулярные выражения (`re`) und asynchrone Threads (`threading`)
* Datenspeicher: Lokale Dateiverbindung für transaktionssicheres Logging mit Bereinigungsfunktion

### 📂 Struktur der Benutzeroberfläche
Das Anwendungsfenster verwendet ein Tab-basiertes Layout:
* **Ping-Test**: Ein zentraler Eingabebereich mit Fokus-Steuerung, einem Status-Indikator, der über dynamische Farbcodierung (Grün/Rot) die Erreichbarkeit signalisiert.
* **Zuletzt verwendet**: Eine historische Auflistung der letzten 10 kontaktierten Hosts in umgekehrter chronologischer Reihenfolge.
* **Häufig genutzt**: Eine analytische Rangliste der am häufigsten abgefragten Netzwerkgeräte zur schnellen Diagnose.

### 📦 Installation & Ausführung

#### Option 1: Start über CLI (Entwicklungsmodus)
1. Repository klonen:
   ```bash
   git clone https://[github.com](https://github.com/KristinaAlokhina)
   ```
2. In den Projektordner wechseln:
   ```bash
   cd gui_ping_tool
   ```
3. Anwendung ausführen:
   ```bash
   python gui_ping_tool.py
   ```

---

## 🇺🇸 English

### 🚀 Features
* **Asynchronous Ping Engine**: Seamless execution of network requests in the background (Threading prevents GUI freezing during host checks).
* **Smart Latency Parsing**: Automatic console output filtering via Regex to accurately extract packet round-trip times in milliseconds (ms).
* **Dynamic UI Control**: The test button deactivates itself autonomously during runtime to block overlapping duplicate requests.
* **Advanced History Logic**: Real-time distribution of logged queries into two dedicated tabs ("Recent" and "Frequent").
* **Interactive List Boxes**: Double-clicking on historical entries immediately loads the address into the input field and switches tabs.
* **Persistent Storage**: All diagnostic logs are securely stored locally and remain fully intact inside `ping_history.txt` after closing the application.

### 🛠️ Technologies
* Python 3.10+
* GUI Framework: **Tkinter** utilizing modern `ttk` layouts
* Core System Modules: `subprocess` (with suppressed console flickering on Windows via `STARTUPINFO`) and `platform`
* Processing Power: Regular Expressions (`re`) and asynchronous multi-threading (`threading`)
* Data Management: Plain-text local database integration with built-in clean-up functionality

### 📂 User Interface Structure
The interface window is divided into a versatile tabbed panel:
* **Ping Test**: The main diagnostic hub featuring an auto-focused entry field, action buttons, and a status label with responsive color-coding (Green/Red).
* **Recent**: A chronological feed tracking the last 10 tested hosts in reverse order for immediate lookup.
* **Frequent**: An analytical leaderboard sorting the most heavily targeted network hosts for priority testing.

### 📦 Installation & Setup

#### Option 1: Build from Source (CLI Mode)
1. Clone the repository:
   ```bash
   git clone https://[github.com](https://github.com/KristinaAlokhina)
   ```
2. Navigate to the project directory:
   ```bash
   cd gui_ping_tool
   ```
3. Run the application:
   ```bash
   python gui_ping_tool.py
   ```
