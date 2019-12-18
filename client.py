import socket
import json
import message
from prettytable import PrettyTable


def read_message(s):
    msgLenInBinary = s.recv(10)
    isJson = int(s.recv(1).decode())
    msgLen = int(msgLenInBinary.decode())
    data = b''
    while msgLen > 0:
        temp = s.recv(1024)
        data += temp
        msgLen -= len(temp)

    return json.loads(data.decode()) if isJson else data


def create_request(inputStr):
    splittedStr = inputStr.split(' ')

    return {
        "command": splittedStr[0],
        "arg": splittedStr[1] if len(splittedStr) > 1 else ""
    }


def print_table(list):
    if len(list) == 0:
        return
    headers = list[0].keys()
    t = PrettyTable(headers)
    for dic in list:
        t.add_row(dic.values())
    print(t)
    return


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50000))
greeting = read_message(s)
path = greeting["path"]
print(greeting["message"])
while True:
    inputStr = input(path+">")
    if inputStr == "exit":
        break
    request = create_request(inputStr)
    s.send(message.create_message(request))
    response = read_message(s)
    if type(response) is dict and "error" in response:
        print(response["error"])
        continue

    command = request["command"]
    if command == 'cd':
        path = response['path']
    elif command == 'dirlist':
        print("Path: "+path)
        print("Files:")
        print_table(response['files'])
    elif command == "download":
        f = open(request["arg"], "wb")
        f.write(response)
        print("file successfully downloaded")
        f.close()

s.close()
