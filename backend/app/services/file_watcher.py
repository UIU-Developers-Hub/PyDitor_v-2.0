#backend\app\services\file_watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.services.websocket_manager import websocket_manager
import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.loop = asyncio.get_event_loop()

    def on_modified(self, event):
        if event.is_directory:
            return
        
        relative_path = Path(event.src_path).relative_to(self.workspace_path)
        self.loop.create_task(self._notify_clients(str(relative_path), "modified"))

    def on_created(self, event):
        if event.is_directory:
            return
            
        relative_path = Path(event.src_path).relative_to(self.workspace_path)
        self.loop.create_task(self._notify_clients(str(relative_path), "created"))

    def on_deleted(self, event):
        if event.is_directory:
            return
            
        relative_path = Path(event.src_path).relative_to(self.workspace_path)
        self.loop.create_task(self._notify_clients(str(relative_path), "deleted"))

    async def _notify_clients(self, file_path: str, event_type: str):
        await websocket_manager.broadcast({
            "type": "file_change",
            "data": {
                "path": file_path,
                "event": event_type
            }
        })

class FileWatcher:
    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.observer = Observer()
        self.handler = FileChangeHandler(workspace_path)

    def start(self):
        self.observer.schedule(self.handler, str(self.workspace_path), recursive=True)
        self.observer.start()
        logger.info(f"Started file watcher for {self.workspace_path}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        logger.info("Stopped file watcher")
        