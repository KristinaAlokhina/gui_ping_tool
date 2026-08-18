import os
import platform
import subprocess
import re
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Datei für den Verlauf
HISTORY_FILE = "ping_history.txt"

def ping_host(host):
    """Führt einen Ping-Befehl aus und gibt (Erfolg, Details/Zeit) zurück."""
    is_windows = platform.system().lower() == 'windows'
    param = '-n' if is_windows else '-c'
    # Timeout auf 1000ms erhöht für bessere Stabilität bei schlechter Verbindung
    command = ['ping', param, '1', '-w' if is_windows else '-W', '1000', host]
    
    try:
        startupinfo = None
        if is_windows:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
        output = subprocess.run(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            timeout=2, 
            text=True,
            startupinfo=startupinfo
        )
        
        if output.returncode == 0:
            # Findet die Antwortzeit in ms (funktioniert auf dt. und engl. Betriebssystemen)
            match = re.search(r'(?:time|zeit)[<=](\d+(?:\.\d+)?) ?ms', output.stdout, re.IGNORECASE)
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
        self.root.title("Advanced Network Ping Tool v2.0")
        self.root.geometry("550x580")
        self.root.minsize(500, 500)
        
        # Steuerungsvariablen für die Endlosschleife
        self.is_looping = False
        self.ping_thread = None
        self.last_state = None  # Verfolgt Statusänderungen für den Sound
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
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
        # Schnellauswahl-Tasten für Netzwerk-Ziele
        preset_frame = ttk.LabelFrame(self.tab_main, text=" Schnellauswahl ")
        preset_frame.pack(fill='x', padx=15, pady=10)
        
        ttk.Button(preset_frame, text="Localhost", command=lambda: self.set_host("127.0.0.1")).pack(side='left', padx=5, pady=5, expand=True)
        ttk.Button(preset_frame, text="Router (GW)", command=lambda: self.set_host("192.168.1.1")).pack(side='left', padx=5, pady=5, expand=True)
        ttk.Button(preset_frame, text="Google DNS", command=lambda: self.set_host("8.8.8.8")).pack(side='left', padx=5, pady=5, expand=True)

        lbl = ttk.Label(self.tab_main, text="IP-Adresse oder Domain eingeben:", font=("Arial", 10, "bold"))
        lbl.pack(pady=(10, 5))
        
        self.entry_host = ttk.Entry(self.tab_main, font=("Arial", 12), width=35)
        self.entry_host.pack(pady=5)
        self.entry_host.focus()
        self.entry_host.bind("<Return>", lambda event: self.toggle_ping())
        
        # Optionen (Checkboxen)
        opt_frame = ttk.Frame(self.tab_main)
        opt_frame.pack(pady=5)
        
        self.var_loop = tk.BooleanVar(value=False)
        self.cb_loop = ttk.Checkbutton(opt_frame, text="Endlos-Ping (Loop)", variable=self.var_loop, command=self.on_loop_toggle)
        self.cb_loop.pack(side='left', padx=10)
        
        self.var_sound = tk.BooleanVar(value=False)
        self.cb_sound = ttk.Checkbutton(opt_frame, text="Sound bei Statusänderung", variable=self.var_sound)
        self.cb_sound.pack(side='left', padx=10)
        
        # Start / Stopp Taste
        self.btn_ping = ttk.Button(self.tab_main, text="Verbindung prüfen", command=self.toggle_ping)
        self.btn_ping.pack(pady=10)
        
        # Status-Anzeigefenster
        self.lbl_result = tk.Label(
            self.tab_main, 
            text="Status: Warte auf Eingabe...", 
            font=("Arial", 12, "bold"), 
            bg="#f5f5f5", 
            fg="#757575",
            wraplength=420,
            relief="groove",
            bd=2
        )
        self.lbl_result.pack(fill='both', expand=True, padx=15, pady=15)

    def setup_lists_tabs(self):
        # Tab "Zuletzt verwendet"
        ttk.Label(self.tab_recent, text="Verlauf (Doppelklick zum Auswählen):", font=("Arial", 10)).pack(pady=(10, 5))
        self.list_recent = tk.Listbox(self.tab_recent, font=("Arial", 11), height=12, selectbackground="#a6c8ff")
        self.list_recent.pack(fill='both', expand=True, padx=10, pady=5)
        self.list_recent.bind("<Double-Button-1>", lambda e: self.select_from_list(self.list_recent))
        
        # Tab "Häufig genutzt"
        ttk.Label(self.tab_freq, text="Häufig kontaktierte Hosts (Doppelklick zum Auswählen):", font=("Arial", 10)).pack(pady=(10, 5))
        self.list_freq = tk.Listbox(self.tab_freq, font=("Arial", 11), height=12, selectbackground="#a6c8ff")
        self.list_freq.pack(fill='both', expand=True, padx=10, pady=5)
        self.list_freq.bind("<Double-Button-1>", lambda e: self.select_from_list(self.list_freq))
        
        self.btn_clear = ttk.Button(self.root, text="Verlauf löschen", command=self.clear_history)
        self.btn_clear.pack(pady=(0, 10))

    def set_host(self, host_ip):
        self.entry_host.config(state="normal")
        self.entry_host.delete(0, tk.END)
        self.entry_host.insert(0, host_ip)

    def on_loop_toggle(self):
        """Stoppt die Schleife, falls die Option während des Laufs deaktiviert wird."""
        if not self.var_loop.get() and self.is_looping:
            self.is_looping = False

    def toggle_ping(self):
        """Schaltet den Ping-Prozess ein oder aus (Start/Stopp-Logik)."""
        if self.is_looping:
            self.is_looping = False
            return
            
        host = self.entry_host.get().strip()
        if not host:
            messagebox.showwarning("Hinweis", "Das Eingabefeld darf nicht leer sein!")
            return
            
        # Validierung unterstützt jetzt auch IPv6-Zeichen und Doppelpunkte
        if not re.match(r"^[a-zA-Z0-9.:-]+$", host):
            messagebox.showerror("Fehler", "Ungültiges Format für Hostname oder IP!")
            return
        
        save_to_history(host)
        self.last_state = None
        
        if self.var_loop.get():
            self.is_looping = True
            self.btn_ping.config(text="Stoppen")
            self.entry_host.config(state="disabled")
            self.ping_thread = threading.Thread(target=self._loop_ping_worker, args=(host,), daemon=True)
            self.ping_thread.start()
        else:
            self.btn_ping.config(state="disabled")
            self.lbl_result.config(text=f"Prüfung für {host} läuft...", fg="black", bg="#ffe0b2")
            threading.Thread(target=self._single_ping_worker, args=(host,), daemon=True).start()

    def _single_ping_worker(self, host):
        is_alive, msg = ping_host(host)
        self.root.after(0, lambda: self._update_ui_result(host, is_alive, msg, reset_btn=True))

    def _loop_ping_worker(self, host):
        while self.is_looping:
            is_alive, msg = ping_host(host)
            
            # Tonsignal bei Statusänderung (Online -> Offline oder umgekehrt)
            if self.var_sound.get() and self.last_state is not None and self.last_state != is_alive:
                self.root.bell() # Standard-Systemton abspielen
                
            self.last_state = is_alive
            
            # Benutzeroberfläche asynchron aktualisieren
            self.root.after(0, lambda h=host, ia=is_alive, m=msg: self._update_ui_result(h, ia, m, reset_btn=False))
            time.sleep(1) # 1 Sekunde Pause zwischen den Pings
            
        # Nach Verlassen der Schleife das UI zurücksetzen
        self.root.after(0, self._reset_ui_after_loop)

    def _update_ui_result(self, host, is_alive, msg, reset_btn=False):
        timestamp = datetime.now().strftime("%H:%M:%S")
        display_text = f"[{timestamp}] {host}\n➔ {msg}"
        
        if is_alive:
                    self.lbl_result.config(text=display_text, fg="white", bg="#2e7d32") # Dunkelgrün
        else:
            self.lbl_result.config(text=display_text, fg="white", bg="#c62828") # Dunkelrot
            
        if reset_btn:
            self.btn_ping.config(state="normal")

    def _reset_ui_after_loop(self):
        self.btn_ping.config(text="Verbindung prüfen", state="normal")
        self.entry_host.config(state="normal")

    def select_from_list(self, listbox):
        selection = listbox.curselection()
        if selection:
            host = listbox.get(selection)
            self.set_host(host)
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
