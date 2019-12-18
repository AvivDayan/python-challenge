
import select
import socket
import socketData
import json
import message
from pathlib import PurePath
HEADER_SIZE = 10
CHUNK = 1024


class server:
    def __init__(self, ip, port, filesDir):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setblocking(0)
        self.server_socket.bind((ip, port))
        self.actions = {}
        self.filesDir = filesDir

    def listen(self):
        self.server_socket.listen(5)
        inputs = [self.server_socket]
        outputs = []
        sockets = {}

        while True:
            readable, writable, exceptional = select.select(
                inputs, outputs, inputs)
            for s in readable:
                if s is self.server_socket:
                    newSocket = s.accept()[0]
                    newSocket.setblocking(0)
                    inputs.append(newSocket)
                    sockets[newSocket] = socketData.SocketData()
                    sockets[newSocket].set_path(self.filesDir)
                    greeting = {
                        "message": "Welcome to the server",
                        "path": str(PurePath(sockets[newSocket].path))
                    }
                    sockets[newSocket].outBuffer = message.create_message(
                        greeting)
                    outputs.append(newSocket)
                else:
                    try:
                        data = s.recv(CHUNK)
                    except:
                        data=b''
                    if data:
                        if sockets[s].inSize == 0:
                            sockets[s].inSize = int(data[:HEADER_SIZE].decode())
                            sockets[s].isJson=True if int(data[HEADER_SIZE:HEADER_SIZE+1].decode()) else False
                            data = data[HEADER_SIZE+1:]
                        sockets[s].inBuffer += data
                        sockets[s].inSize -= len(data)
                        if sockets[s].inSize == 0:
                            self.create_out_buffer(sockets[s])
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        del sockets[s]

            for s in writable:
                nextPiece = sockets[s].outBuffer[:CHUNK]
                sockets[s].outBuffer = sockets[s].outBuffer[CHUNK:]
                try:
                    s.send(nextPiece)
                except:
                    outputs.remove(s)
                    continue
                if not sockets[s].outBuffer:
                    outputs.remove(s)

            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del sockets[s]

    def create_out_buffer(self, socket):
        if socket.isJson:
            socket.inBuffer.decode()
            socket.request_body = json.loads(socket.inBuffer)
            command = socket.request_body["command"]
            response= self.actions[command](socket) if command in self.actions else {
                'error': "no such command"}
            socket.inBuffer = b''
            socket.outBuffer = message.create_message(response)
