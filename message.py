import json


def create_message(data):
    if type(data) is dict:
        isJson = True
        data = json.dumps(data).encode()
    elif type(data) is bytes:
        isJson = False
    else:
        raise Exception("create_message must recieve dictionary or bytes object")
    isJsonInStr = 1 if isJson else 0
    return f"{len(data):<10}".encode()+f"{isJsonInStr}".encode()+data
