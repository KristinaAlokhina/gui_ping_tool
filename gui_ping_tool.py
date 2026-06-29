import os
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Datei für den Verlauf
HISTORY_FILE = "ping_history.txt"

def ping_host(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    try:
        output = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3)
        return output.returncode == 0
    except Exception:
        return False

def save_to_history(host):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp},{host}\n")

def load_history_stats():
    if not os.path.exists(HISTORY_FILE):
        return [], []
    
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    recent_hosts = []
    host_counts = {}
    
    for line in reversed(lines):
        line = line.strip()
        if not line or "," not in line:
            continue
        _, host = line.split(",", 1)
        
        if host not in recent_hosts:
            recent_hosts.append(host)
        
        host_counts[host] = host_counts.get(host, 0) + 1
            
    frequent_hosts = [h for h, c in sorted(host_counts.items(), key=lambda item: item[1], reverse=True)]
    
    return recent_hosts[:10], frequent_hosts[:10]

class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Network Ping Tool")
        self.root.geometry("500x450")
        
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
        # Eingabefeld
        lbl = ttk.Label(self.tab_main, text="IP-Adresse oder Domain eingeben:", font=("Arial", 11))
        lbl.pack(pady=15)
        
        self.entry_host = ttk.Entry(self.tab_main, font=("Arial", 12), width=35)
        self.entry_host.pack(pady=5)
        self.entry_host.focus()
        
        # Start-Button
        self.btn_ping = ttk.Button(self.tab_main, text="Verbindung prüfen", command=self.start_ping)
        self.btn_ping.pack(pady=15)
        
        # Status-Anzeige
        self.lbl_result = tk.Label(self.tab_main, text="Status: Warte auf Eingabe...", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="grey")
        self.lbl_result.pack(fill='x', padx=20, pady=20, ipady=15)

    def setup_lists_tabs(self):
        # Tab "Zuletzt verwendet"
        ttk.Label(self.tab_recent, text="Verlauf der letzten Abfragen (Doppelklick zum Auswählen):", font=("Arial", 10)).pack(pady=10)
        self.list_recent = tk.Listbox(self.tab_recent, font=("Arial", 11), height=15)
        self.list_recent.pack(fill='both', expand=True, padx=10, pady=10)
        self.list_recent.bind("<Double-Button-1>", lambda e: self.select_from_list(self.list_recent))
        
        # Tab "Häufig genutzt"
        ttk.Label(self.tab_freq, text="Die am häufigsten kontaktierten Hosts (Doppelklick zum Auswählen):", font=("Arial", 10)).pack(pady=10)
        self.list_freq = tk.Listbox(self.tab_freq, font=("Arial", 11), height=15)
        self.list_freq.pack(fill='both', expand=True, padx=10, pady=10)
        self.list_freq.bind("<Double-Button-1>", lambda e: self.select_from_list(self.list_freq))

    def start_ping(self):
        host = self.entry_host.get().strip()
        if not host:
            messagebox.showwarning("Hinweis", "Das Eingabefeld darf nicht leer sein!")
            return
        
        self.lbl_result.config(text="Prüfung läuft...", fg="orange", bg="#f0f0f0")
        self.root.update()
        
        is_alive = ping_host(host)
        save_to_history(host)
        
        if is_alive:
            self.lbl_result.config(text=f"ONLINE: {host} ist erreichbar", fg="white", bg="green")
        else:
            self.lbl_result.config(text=f"OFFLINE: {host} antwortet nicht", fg="white", bg="red")

    def select_from_list(self, listbox):
        selection = listbox.curselection()
        if selection:
            host = listbox.get(selection)
            self.entry_host.delete(0, tk.END)
            self.entry_host.insert(0, host)
            self.notebook.select(self.tab_main)

    def on_tab_change(self, event):
        recent, freq = load_history_stats()
        
        self.list_recent.delete(0, tk.END)
        for host in recent:
            self.list_recent.insert(tk.END, host)
            
        self.list_freq.delete(0, tk.END)
        for host in freq:
            self.list_freq.insert(tk.END, host)

if __name__ == "__main__":
    window = tk.Tk()
    app = PingApp(window)
    window.mainloop()
