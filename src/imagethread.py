from threading import Thread, Lock
from queue import Queue
import requests


class ImageTask:
    
    def __init__(self, url: str, callback):
        self.__l = Lock()
        self.__aborted = False
        self.url = url
        self.__callback = callback
    
    def finish(self, data: bytes | None):
        with self.__l:
            if not self.__aborted:
                self.__callback(data, self)
    
    def aborted(self) -> bool:
        with self.__l:
            return self.__aborted
    
    def abort(self):
        with self.__l:
            self.__aborted = True


class ImageThread(Thread):
    
    def __init__(self):
        super().__init__(daemon=True)
        self.tasks: Queue[ImageTask] = Queue(0)
        
    def run(self) -> None:
        while True:
            t = self.tasks.get()
            if not t.aborted():
                data = None
                try:
                    data = requests.get(t.url).content
                except requests.exceptions.RequestException:
                    pass
                t.finish(data)


image_thread = ImageThread()
image_thread.start()
