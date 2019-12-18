import json

#the create_message fucntion recieves a dictionary or bytes stream,
#then create a bytes stream consisting of:
#  1. the size of the input (the size takes 10 bytes).
#  2. a single byte to indicate if the message is json or not.
#  3. the message itself(encoded if was json)

#input itself
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
