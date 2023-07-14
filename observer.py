import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import clear

class FileChangeHandler(FileSystemEventHandler):
    clear.clear()
    def on_modified(self, event):
        with open('chat_logs.txt', 'r') as f:
            lines = f.readlines()
            print(lines[-1])  # Imprimir el último mensaje
            with open('realtime_logs.txt', 'a') as f2:
                f2.write(lines[-1])  # Escribir el último mensaje en otro archivo

if __name__ == "__main__":
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='chat_logs.txt', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
