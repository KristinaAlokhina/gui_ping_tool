<p align="center">
  <ins><b><kbd>&nbsp;DESKTOP APPLICATION&nbsp;</kbd></b></ins>
</p>

<h1 align="center" style="font-size: 2.5rem; font-weight: 900; color: #1a1a1a; margin-top: 10px; margin-bottom: 10px; border-bottom: none;">
  ⚡ ADVANCED NETWORK PING TOOL (v2.0)
</h1>

<p align="center">
  <strong>Ein modernes, threadsicheres ICMP-Diagnosewerkzeug mit grafischer Benutzeroberfläche und intelligenter Verlaufshistorie.</strong>
  <br />
  <i>Entwickelt mit Python, Tkinter und Multithreading für verzögerungsfreie Echtzeit-Netzwerkanalysen.</i>
</p>

<p align="center">
  <a href="#-deutsch">🇩🇪 Deutsch</a> • 
  <a href="#-english">🇺🇸 English</a> • 
  <a href="#-русский">🇷🇺 Русский</a> • 
  <a href="#-українська">🇺🇦 Українська</a>
</p>

---

## 🇩🇪 Deutsch

Die Anwendung bietet Netzwerkadministratoren und Entwicklern eine performante Oberfläche zur Echtzeit-Überwachung von Servern, Routern und Webseiten, ohne die UI während der Ping-Intervalle zu blockieren.

### 🚀 Funktionen
* **Asynchrones Multithreading 🧵**: Der Ping-Prozess läuft isoliert in einem Hintergrund-Thread (`threading.Thread`). Die grafische Oberfläche bleibt auch bei Verbindungsabbrüchen oder langen Timeouts zu 100% flüssig und bedienbar.
* **Endlos-Schleife & Status-Tracker 🔄**: Option für kontinuierliche Netzwerk-Scans (Loop). Das Tool überwacht den Host ununterbrochen und bietet eine zuschaltbare Audio-Benachrichtigung bei Statusänderungen (Online ⇄ Offline).
* **Intelligentes Verlaufs-Caching 📊**: Speichert alle Abfragen persistent in `ping_history.txt`. Über ein tabbasiertes Notebook-Layout werden automatisch die Top 10 der zuletzt verwendeten sowie der am häufigsten kontaktierten Hosts ermittelt.
* **Cross-Plattform Parser 🌍**: Erkennt das zugrundeliegende Betriebssystem (Windows / Unix-Derivate) und passt die Ping-Parameter automatisch an. Reguläre Ausdrücke (RegEx) parsen die Latenzzeiten plattformübergreifend auf deutschen und englischen Systemen.
* **Presets & Quick-Select ⚡**: Integrierte Schnellauswahl-Tasten für typische Diagnose-Ziele (`Localhost`, `Standard-Gateway`, `Google Public DNS`).

### 🛠️ Technologien
* **GUI-Framework**: Python Tkinter (modernisiert via `ttk`-Theming & Notebook-Komponenten)
* **Prozess-Steuerung**: `subprocess` mit unterdrückten OS-Konsolenfenstern (`STARTF_USESHOWWINDOW`) unter Windows.
* **RegEx-Engine**: `re` zur Filterung nativer Latenz-Strings (`ms`).

### 📦 Installation & Ausführung

#### Ausführung aus dem Quellcode
Es wird eine Standard-Installation von Python 3.x benötigt. Das Tool nutzt ausschließlich native Bibliotheken – es sind **keine** `pip install`-Abhängigkeiten erforderlich.

1. Repository klonen:
   ```bash
   git clone https://github.com
   ```
2. In den Projektordner wechseln:
   ```bash
   cd network-ping-tool
   ```
3. Die Anwendung starten:
   ```bash
   python ping_tool.py
   ```

---

## 🇺🇸 English

A high-performance asynchronous ICMP diagnostic utility tailored for monitoring host availability, tracking latency fluctuations, and logging long-term network states.

### 🚀 Features
* **Non-Blocking Multithreading 🧵**: Decouples subprocess network streams into dedicated worker threads, ensuring the UI Tkinter canvas never locks or freezes during transmission delays.
* **Continuous Loop & Audio Alerts 🔄**: Supports automated endless ping executions alongside intelligent state tracking that triggers notification chimes when network states change.
* **Advanced History Notebook 📊**: Tracks historical connection nodes inside `ping_history.txt`, dynamically populating dedicated UI list views for the "Top 10 Recent" and "Most Frequent" targets.
* **Universal OS Regex Pipeline 🌍**: Fluidly maps parameters between Windows and Unix standards while regex definitions extract ping return latencies (`ms`) across varying system locales.
* **Instant Target Presets ⚡**: Flash-binds frequent system endpoints (`Localhost`, `Router Gateway`, `Google DNS`) for accelerated interface dispatching.

### 🛠️ Technologies
* **Framework**: Python Tkinter (stylized with structural flat `ttk` parameters)
* **Execution Core**: Native `subprocess` engine utilizing isolated `STARTUPINFO` pipes to hide system prompt screens.
* **Data Logging**: Local UTF-8 flat-file log buffers mapping standard `datetime` stamps.

### 📦 Installation & Setup

#### Running from Source
Requires a standard Python 3.x environment. Built purely on standard library modules with zero third-party packages required.

1. Clone the repository:
   ```bash
   git clone https://github.com
   ```
2. Navigate to project root:
   ```bash
   cd network-ping-tool
   ```
3. Initialize the tool:
   ```bash
   python ping_tool.py
   ```

---

## 🇷🇺 Русский

Продвинутая графическая утилита для диагностики сетевых соединений. Позволяет пинговать хосты в реальном времени, вести учет стабильности подключения и анализировать историю запросов.

### 🚀 Возможности
* **Асинхронный многопоточный движок 🧵**: Все сетевые запросы выполняются в фоновом режиме через `threading`. Графический интерфейс никогда не зависает и не блокируется, даже при потере пакетов или долгих таймаутах.
* **Бесконечный цикл и звуковые алерты 🔄**: Режим непрерывного мониторинга (Endlos-Ping) со встроенным трекером изменений. Приложение может подавать звуковой сигнал при переходе хоста из Онлайн в Оффлайн и наоборот.
* **Умные вкладки истории и статистики 📊**: Все запросы логируются в файл `ping_history.txt`. Программа автоматически вычисляет топ-10 последних и топ-10 самых часто используемых адресов, позволяя выбрать их двойным кликом.
* **Кроссплатформенный парсинг (RegEx) 🌍**: Автоматически определяет тип ОС (Windows/Linux) и подбирает нужные флаги. Регулярные выражения адаптированы для парсинга времени отклика (`ms`) на русских, английских и немецких версиях систем.
* **Панель быстрых пресетов ⚡**: Кнопки моментального выбора для базовых сетевых узлов (`Localhost`, `Роутер/Шлюз`, `Google DNS`).

### 🛠️ Технологии
* **Графика**: Python Tkinter (с использованием контейнеров `ttk.Notebook` и тем `clam`)
* **Сетевой слой**: Модуль `subprocess` со скрытием системных окон консоли (`STARTF_USESHOWWINDOW`).
* **Аналитика**: Библиотека `datetime` для фиксации точного времени проверок.

### 📦 Установка и запуск

#### Запуск из исходного кода
Требуется только предустановленный пакет Python 3.x. Программа написана без использования сторонних зависимостей, устанавливать модули через `pip` не нужно.

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com
   ```
2. Перейдите в папку проекта:
   ```bash
   cd network-ping-tool
   ```
3. Запустите сетевой монитор:
   ```bash
   python ping_tool.py
   ```

---

## 🇺🇦 Українська

Просунута графічна утиліта для діагностики мережевих з'єднань. Дозволяє пінгувати хости в реальному часі, вести облік стабільності підключення та аналізувати історію запитів.

### 🚀 Можливості
* **Асинхронний багатопотоковий движок 🧵**: Усі мережеві запити виконуються у фоновому режимі через `threading`. Графічний інтерфейс ніколи не зависає і не блокується, навіть при втраті пакетів або довгих таймаутах.
* **Нескінченний цикл та звукові сповіщення 🔄**: Режим безперервного моніторингу (Endlos-Ping) із вбудованим трекером змін. Програма може подавати звуковий сигнал при переході хоста з Онлайн в Офлайн і навпаки.
* **Розумні вкладки історії та статистики 📊**: Усі запити логуються у файл `ping_history.txt`. Програма автоматично обчислює топ-10 останніх та топ-10 найчастіше використовуваних адрес, дозволяючи вибрати їх подвійним кліком.
* **Кросплатформений парсинг (RegEx) 🌍**: Автоматично визначає тип ОС (Windows/Linux) та підбирає потрібні прапори. Регулярні вирази адаптовані для парсингу часу відгуку (`ms`) на українських, англійських та німецьких версіях систем.
* **Панель швидких пресетів ⚡**: Кнопки моментального вибору для базових мережевих вузлів (`Localhost`, `Роутер/Шлюз`, `Google DNS`).

### 🛠️ Технології
* **Графіка**: Python Tkinter (з використанням контейнерів `ttk.Notebook` та тем `clam`)
* **Мережевий шар**: Модуль `subprocess` із приховуванням системних вікон консолі (`STARTF_USESHOWWINDOW`).
* **Аналітика**: Бібліотека `datetime` для фіксації точного часу перевірок.

### 📦 Встановлення та запуск

#### Запуск із вихідного коду
Вам знадобиться лише встановлений інтерпретатор Python 3.x. Програма написана без використання сторонніх залежностей, встановлювати модулі через `pip` не потрібно.

1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com
   ```
2. Перейдіть до папки проєкту:
   ```bash
   cd network-ping-tool
   ```
3. Запустіть мережевий монітор:
   ```bash
   python ping_tool.py
   ```
