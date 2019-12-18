from pathlib import Path


class SocketData:
    def __init__(self):
        self.path = ""
        self.inBuffer = b''
        self.outBuffer = b''
        self.inSize = 0
        self.request_body = {}
        self.isJson = True

    def set_path(self, dir):
        self.path = Path(dir)
