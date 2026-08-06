import os
import platform
import subprocess
import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Datei für den Verlauf
HISTORY_FILE = "ping_history.txt"

def ping_host(host):
    """Führt einen Ping-Befehl aus und gibt (Erfolg, Details/Zeit) zurück."""
    is_windows = platform.system().lower() == 'windows'
    param = '-n' if is_windows else '-c'
    command = ['ping', param, '1', host]
    
    try:
        # Verwende startupinfo unter Windows, um das Aufblinken der Konsole zu verhindern
        startupinfo = None
        if is_windows:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
        output = subprocess.run(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            timeout=3, 
            text=True,
            startupinfo=startupinfo
        )
        
        if output.returncode == 0:
            # Versuche die Zeit (ms) aus der Ausgabe zu extrahieren
            match = re.search(r'(?:time|Zeit)[<=](\d+(?:\.\d+)?) ?ms', output.stdout, re.IGNORECASE)
            time_str = f" ({match.group(1)} ms)" if match else ""
            return True, f"ONLINE{time_str}"
        else:
            return False, "OFFLINE: Keine Antwort"
    except subprocess.TimeoutExpired:
        return False, "OFFLINE: Zeitüberschreitung"
    except Exception as e:
        return False, f"Fehler: {str(e)}"

def save_to_history(host):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp},{host}\n")

def clear_history_file():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

def load_history_stats():
    if not os.path.exists(HISTORY_FILE):
        return [], []
    
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return [], []
    
    recent_hosts = []
    host_counts = {}
    
    for line in reversed(lines):
        line = line.strip()
        if not line or "," not in line:
            continue
        try:
            _, host = line.split(",", 1)
        except ValueError:
            continue
        
        if host not in recent_hosts:
            recent_hosts.append(host)
        
        host_counts[host] = host_counts.get(host, 0) + 1
            
    frequent_hosts = [h for h, c in sorted(host_counts.items(), key=lambda item: item[1], reverse=True)]
    
    return recent_hosts[:10], frequent_hosts[:10]

class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Network Ping Tool")
        self.root.geometry("520x500")
        self.root.minsize(450, 400)
        
        # Style konfigurieren
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Tabs erstellen
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_main = ttk.Frame(self.notebook)
        self.tab_recent = ttk.Frame(self.notebook)
        self.tab_freq = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_main, text="Ping-Test")
        self.notebook.add(self.tab_recent, text="Zuletzt verwendet")
        self.notebook.add(self.tab_freq, text="Häufig genutzt")
        
        self.setup_main_tab()
        self.setup_lists_tabs()
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def setup_main_tab(self):
        lbl = ttk.Label(self.tab_main, text="IP-Adresse oder Domain eingeben:", font=("Arial", 11))
        lbl.pack(pady=(20, 5))
        
        self.entry_host = ttk.Entry(self.tab_main, font=("Arial", 12), width=35)
        self.entry_host.pack(pady=5)
        self.entry_host.focus()
        self.entry_host.bind("<Return>", lambda event: self.start_ping())
        
        self.btn_ping = ttk.Button(self.tab_main, text="Verbindung prüfen", command=self.start_ping)
        self.btn_ping.pack(pady=15)
        
        self.lbl_result = tk.Label(
            self.tab_main, 
            text="Status: Warte auf Eingabe...", 
            font=("Arial", 11, "bold"), 
            bg="#f0f0f0", 
            fg="grey",
            wraplength=400
        )
        self.lbl_result.pack(fill='both', expand=True, padx=20, pady=20)

    def setup_lists_tabs(self):
        # Tab "Zuletzt verwendet"
        ttk.Label(self.tab_recent, text="Verlauf (Doppelklick zum Auswählen):", font=("Arial", 10)).pack(pady=(10, 5))
        self.list_recent = tk.Listbox(self.tab_recent, font=("Arial", 11), height=12)
        self.list_recent.pack(fill='both', expand=True, padx=10, pady=5)
        self.list_recent.bind("<Double-Button-1>", lambda e: self.select_from_list(self.list_recent))
        
        # Tab "Häufig genutzt"
        ttk.Label(self.tab_freq, text="Häufig kontaktierte Hosts (Doppelklick zum Auswählen):", font=("Arial", 10)).pack(pady=(10, 5))
        self.list_freq = tk.Listbox(self.tab_freq, font=("Arial", 11), height=12)
        self.list_freq.pack(fill='both', expand=True, padx=10, pady=5)
        self.list_freq.bind("<Double-Button-1>", lambda e: self.select_from_list(self.list_freq))
        
        # Verlauf löschen Button (unten platziert)
        self.btn_clear = ttk.Button(self.root, text="Verlauf löschen", command=self.clear_history)
        self.btn_clear.pack(pady=(0, 10))

    def start_ping(self):
        host = self.entry_host.get().strip()
        if not host:
            messagebox.showwarning("Hinweis", "Das Eingabefeld darf nicht leer sein!")
            return
            
        # Einfache Validierung gegen ungültige Zeichen
        if not re.match(r"^[a-zA-Z0-9.-]+$", host):
            messagebox.showerror("Fehler", "Ungültiges Format für Hostname oder IP!")
            return
        
        self.btn_ping.config(state="disabled")
        self.lbl_result.config(text=f"Prüfung für {host} läuft...", fg="black", bg="#ffe0b2")
        
        # Ping in separatem Thread ausführen, um GUI-Einfrieren zu verhindern
        thread = threading.Thread(target=self._async_ping, args=(host,), daemon=True)
        thread.start()

    def _async_ping(self, host):
        is_alive, msg = ping_host(host)
        save_to_history(host)
        
        # GUI im Hauptthread aktualisieren
        self.root.after(0, lambda: self._update_ui_result(host, is_alive, msg))

    def _update_ui_result(self, host, is_alive, msg):
        self.btn_ping.config(state="normal")
        if is_alive:
            self.lbl_result.config(text=f"{host} -> {msg}", fg="white", bg="#2e7d32")
        else:
            self.lbl_result.config(text=f"{host} -> {msg}", fg="white", bg="#c62828")

    def select_from_list(self, listbox):
        selection = listbox.curselection()
        if selection:
            host = listbox.get(selection)
            self.entry_host.delete(0, tk.END)
            self.entry_host.insert(0, host)
            self.notebook.select(self.tab_main)

    def clear_history(self):
        if messagebox.askyesno("Löschen", "Möchten Sie den gesamten Verlauf wirklich löschen?"):
            clear_history_file()
            self.refresh_lists()

    def refresh_lists(self):
        recent, freq = load_history_stats()
        
        self.list_recent.delete(0, tk.END)
        for host in recent:
            self.list_recent.insert(tk.END, host)
            
        self.list_freq.delete(0, tk.END)
        for host in freq:
            self.list_freq.insert(tk.END, host)

    def on_tab_change(self, event):
        self.refresh_lists()

if __name__ == "__main__":
    window = tk.Tk()
    app = PingApp(window)
    window.mainloop()
