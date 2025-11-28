# IFC Checker — Мониторинг IFC-файлов

Программа `IFC_checker.py` предназначена для автоматического мониторинга изменений в IFC-файлах в указанной папке. Поддерживает как консольный режим, так и графический интерфейс (`IFC_checker_GUI.py`).

---

## 📦 Основные возможности

- 🔍 Мониторинг создания, изменения и удаления `.ifc` файлов
- 📁 Рекурсивный обход всех подпапок
- 🧠 Фильтрация изменений по содержимому: логируются только реальные изменения версии (по хэшу)
- 🌐 Поддержка трёх языков сообщений: английский (`en`), русский (`ru`), немецкий (`de`)
- 📄 Ведение логов с возможностью указания имени лог-файла
- 🖥️ Графический интерфейс с выбором папки, языка и отображением событий

---

## ⚙️ Аргументы командной строки

```bash
python IFC_checker.py <путь_к_папке> [--lang <язык>] [--log <имя_лога>]
```

|Аргумент|Описание|Значение по умолчанию|
|---|---|---|
|folder|Путь к директории мониторинга| | 
|--lang|Выбор языка сообщений: en/ru/de (опционально)|en| 
|--log|Имя лог-файла для записи сообщений (опционально)|ifc_monitor.log| 

---

## 🧠 Логика фильтрации изменений
- При создании или изменении .ifc файла программа вычисляет его хэш (MD5)
- Если хэш отличается от предыдущего — считается, что файл обновлён
- Это позволяет игнорировать незначительные изменения (например, изменение метаданных или времени)

---

## 🖥️ Графический интерфейс (IFC_checker_GUI.py)
- Выбор папки мониторинга через диалог
- Выбор языка сообщений
- Кнопки:
- Start monitoring — запуск мониторинга
- Stop monitoring — остановка процесса
- Отображение событий в окне GUI
- Все сообщения также записываются в лог-файл

---

## 📂 Пример логов
```bash
=== Monitoring started at 2025-11-28 10:15:00 ===
Folder: C:\Users\Mikhail\Documents\IFC_Files

2025-11-28 10:20:05 [UPDATED] File modified: \Subfolder_1\some_file.ifc
2025-11-28 10:22:10 [DELETED] File deleted: \Subfolder_2\old_model.ifc
```
---

## ✅ Требования
- Python 3.7+
- Установленные модули:
- watchdog
- tkinter (входит в стандартную библиотеку)
- hashlib, argparse, logging

---

## 📌 Назначение
Программа предназначена для архитекторов, инженеров и BIM-координаторов, которым важно отслеживать изменения в IFC-моделях в рамках проектной работы или контроля версий. Подходит для использования в локальной сети, на рабочих станциях и в проектных группах.

----

# IFC Checker — IFC File Monitoring

The `IFC_checker.py` program is designed for automatic monitoring of changes in IFC files within a specified folder. It supports both command-line mode and a graphical interface (`IFC_checker_GUI.py`).

---

## 📦 Key Features

- 🔍 Monitors creation, modification, and deletion of `.ifc` files
- 📁 Recursively scans all subfolders
- 🧠 Filters changes by content: logs only real version updates (based on file hash)
- 🌐 Supports three message languages: English (`en`), Russian (`ru`), German (`de`)
- 📄 Logging with customizable log file name
- 🖥️ Graphical interface with folder selection, language choice, and live event display

---

## ⚙️ Command-Line Arguments

```bash
python IFC_checker.py <folder_path> [--lang <language>] [--log <log_filename>]
```

|Argument|Description|Default value|
|---|---|---| 
|folder|Path to the folder to monitor| | 
|--lang|Message language: en, ru, de (optional)|en| 
|--log|Log file name for recording events (optional)|ifc_monitor.log|

---

## 🧠 Change Filtering Logic
- When an .ifc file is created or modified, the program calculates its hash (MD5)
- If the hash differs from the previous version, the file is considered updated
- This avoids logging trivial changes (e.g., metadata or timestamp updates)

---

## 🖥️ Graphical Interface (IFC_checker_GUI.py)
- Folder selection via dialog
- Language selection dropdown
- Buttons:
- Start monitoring — launches monitoring
- Stop monitoring — terminates the process
- Event messages displayed in the GUI window
- All messages are also written to the log file

---

## 📂 Example Log Output
```bash
=== Monitoring started at 2025-11-28 10:15:00 ===
Folder: C:\Users\Mikhail\Documents\IFC_Files

2025-11-28 10:20:05 [UPDATED] File modified: \Subfolder_1\some_file.ifc
2025-11-28 10:22:10 [DELETED] File deleted: \Subfolder_2\old_model.ifc
```

---

## ✅ Requirements
- Python 3.7+
- Required modules:
- watchdog
- tkinter (included in standard library)
- hashlib, argparse, logging

---

## 📌 Purpose
This program is intended for architects, engineers, and BIM coordinators who need to track changes in IFC models as part of project workflows or version control. Suitable for use in local networks, workstations, and collaborative environments.
