import time
import os
import logging
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Словарь сообщений для разных языков
MESSAGES = {
    "en": {
        "new": "[NEW] File created: {}",
        "updated": "[UPDATED] File modified: {}",
        "deleted": "[DELETED] File deleted: {}",
        "monitoring": "Monitoring folder: {}",
        "error": "Error: {} is not a valid directory",
        "start": "=== Monitoring started at {} ===\nFolder: {}"
    },
    "ru": {
        "new": "[НОВЫЙ] Файл создан: {}",
        "updated": "[ИЗМЕНЁН] Файл изменён: {}",
        "deleted": "[УДАЛЁН] Файл удалён: {}",
        "monitoring": "Мониторинг папки: {}",
        "error": "Ошибка: {} не является папкой",
        "start": "=== Мониторинг запущен в {} ===\nПапка: {}"
    },
    "de": {
        "new": "[NEU] Datei erstellt: {}",
        "updated": "[AKTUALISIERT] Datei geändert: {}",
        "deleted": "[GELÖSCHT] Datei gelöscht: {}",
        "monitoring": "Überwachung des Ordners: {}",
        "error": "Fehler: {} ist kein gültiges Verzeichnis",
        "start": "=== Überwachung gestartet am {} ===\nOrdner: {}"
    }
}


class IFCFileHandler(FileSystemEventHandler):
    """Handler for monitoring IFC file system events.

    Tracks creation, modification, and deletion of .ifc files with debounce mechanism
    to prevent duplicate notifications from rapid successive events.
    """

    def __init__(self, lang="en", base_folder=""):
        """Initialize IFC file handler.

        Args:
            lang (str): Language for messages ('en', 'ru', 'de'). Defaults to 'en'.
            base_folder (str): Base folder for relative path calculation. Defaults to ''.
        """
        self.lang = lang if lang in MESSAGES else "en"
        self.file_records = {}  # словарь: путь -> mtime
        self.last_update_time = {}  # словарь: путь -> время последнего логирования
        self.debounce_delay = 1.0  # задержка в секундах
        self.base_folder = os.path.abspath(base_folder)

    def relative_path(self, full_path):
        """Convert absolute path to relative path from base folder.

        Args:
            full_path (str): Absolute file path.

        Returns:
            str: Relative path with backslash separators, or original path on error.
        """
        try:
            rel = os.path.relpath(full_path, self.base_folder)
            return "\\" + rel.replace("/", "\\")
        except Exception:
            return full_path

    def log_message(self, key, path):
        """Log and print a message with timestamp.

        Args:
            key (str): Message key from MESSAGES dictionary ('new', 'updated', 'deleted').
            path (str): File path to include in message.
        """
        rel_path = self.relative_path(path)
        msg = MESSAGES[self.lang][key].format(rel_path)
        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}")
        logging.info(msg)

    def get_file_mtime(self, path):
        """Get file modification time.

        Args:
            path (str): File path.

        Returns:
            float: Modification time as Unix timestamp, or None if file not accessible.
        """
        try:
            return os.path.getmtime(path)
        except Exception:
            return None

    def should_log_update(self, path):
        """Check if enough time has passed to log another update for this file (debounce).

        Args:
            path (str): File path.

        Returns:
            bool: True if update should be logged, False if within debounce window.
        """
        current_time = time.time()
        last_time = self.last_update_time.get(path, 0)
        if current_time - last_time >= self.debounce_delay:
            self.last_update_time[path] = current_time
            return True
        return False

    def on_created(self, event):
        """Handle file creation event.

        Args:
            event: FileSystemEvent object from watchdog.
        """
        if not event.is_directory and event.src_path.lower().endswith(".ifc"):
            file_mtime = self.get_file_mtime(event.src_path)
            self.file_records[event.src_path] = file_mtime
            self.log_message("new", event.src_path)

    def on_modified(self, event):
        """Handle file modification event.

        Checks if modification time has changed and logs update if debounce condition is met.

        Args:
            event: FileSystemEvent object from watchdog.
        """
        if not event.is_directory and event.src_path.lower().endswith(".ifc"):
            new_mtime = self.get_file_mtime(event.src_path)
            old_mtime = self.file_records.get(event.src_path)

            if new_mtime and new_mtime != old_mtime:
                self.file_records[event.src_path] = new_mtime
                if self.should_log_update(event.src_path):
                    self.log_message("updated", event.src_path)

    def on_deleted(self, event):
        """Handle file deletion event.

        Args:
            event: FileSystemEvent object from watchdog.
        """
        if not event.is_directory and event.src_path.lower().endswith(".ifc"):
            if event.src_path in self.file_records:
                del self.file_records[event.src_path]
            if event.src_path in self.last_update_time:
                del self.last_update_time[event.src_path]
            self.log_message("deleted", event.src_path)


def monitor_folder(path_to_watch, lang="en"):
    """Start monitoring a folder for IFC file changes.

    Runs indefinitely until interrupted (Ctrl+C).

    Args:
        path_to_watch (str): Path to folder to monitor.
        lang (str): Language for messages ('en', 'ru', 'de'). Defaults to 'en'.
    """
    event_handler = IFCFileHandler(lang, path_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()
    print(MESSAGES[lang]["monitoring"].format(path_to_watch))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IFC files monitoring tool")
    parser.add_argument("folder", help="Path to the folder to monitor")
    parser.add_argument("--lang", choices=["en", "ru", "de"], default="en",
                        help="Language for messages (default: en)")
    parser.add_argument("--log", default="ifc_monitor.log",
                        help="Log file name (default: ifc_monitor.log)")
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(MESSAGES[args.lang]["error"].format(args.folder))
    else:
        # Заголовок в лог-файле
        with open(args.log, "a", encoding="utf-8") as f:
            f.write("\n")
            f.write(MESSAGES[args.lang]["start"].format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                os.path.abspath(args.folder)
            ) + "\n")

        # Настройка логирования
        logging.basicConfig(
            filename=args.log,
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        monitor_folder(args.folder, args.lang)
