import sys
import time
from render import run
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class EventHandler(FileSystemEventHandler):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.runs = 0
        self.callback = callback

    def on_any_event(self, event):
        print('\rRunning...', end='')
        self.callback()
        self.runs += 1
        print(f'\rRunning ({self.runs})', end='')
        time.sleep(0.5)
        return super().on_any_event(event)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else r'.\\source\\'
    observer = Observer()
    event_handler = EventHandler(run)
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()