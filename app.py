import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading


class RecursiveDirectoryHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        if os.path.isdir(path):
            return os.path.join(path, "index.html")
        else:
            return path


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, server):
        self.server = server

    def on_any_event(self, event):
        if event.is_directory:
            return
        self.server.restart()


class AutoRestartHTTPServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.observer = Observer()
        self.observer.schedule(FileChangeHandler(self), ".", recursive=True)
        self.observer.start()

    def restart(self):
        print("Restarting server...")
        self.observer.stop()
        self.server_close()
        self.observer.join()
        start_server()


def start_server():
    server_address = ("", 8000)
    httpd = AutoRestartHTTPServer(server_address, RecursiveDirectoryHandler)
    print("Server running on port 8000")
    httpd.serve_forever()


def run():
    start_server()


if __name__ == "__main__":
    run()
