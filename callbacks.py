from pathlib import Path, PurePath
import datetime
import os
downloads = {}


def download_callback(socketData):
    response = {}
    request = socketData.request_body
    filename = request["arg"]
    filePath = socketData.path/filename
    if filePath.exists() and not filePath.is_dir():
        response = filePath.read_bytes()
        fullPath = str(PurePath(filePath))
        downloads[fullPath] = downloads[fullPath] + 1 if fullPath in downloads else 1
    else:
        response["error"] = "the file doesnt exists or is a directory"
    return response


def cd_callback(socketData):
    response = {}
    arg = socketData.request_body["arg"]
    if arg == "..":
        if socketData.path.samefile(Path("files")):
            response["error"] = "already in root folder"
        else:
            socketData.path = socketData.path.parent
    else:
        path = socketData.path/arg
        if path.is_dir() and not path.samefile(socketData.path):
            socketData.path = path
        else:
            response["error"] = "no such directory"
    response['path'] = str(PurePath(socketData.path))
    return response


def dirlist_callback(socketData):
    files = os.listdir(socketData.path)
    response = {
        "files": create_files_data(socketData.path, files),
        "path": str(PurePath(socketData.path))
    }
    return response


def create_files_data(path, files):
    filesData = []
    for file in files:
        fileData = {}
        filePath = path/file
        fileData["name"] = filePath.name.split('.')[0]
        fileData["ext"] = ' - ' if filePath.is_dir() else filePath.suffix[1:]
        fileData["isDir"] = 'dir' if filePath.is_dir() else 'file'
        fileData["size"] = filePath.stat().st_size
        fileData["createTime"] = datetime.datetime.fromtimestamp(
            filePath.stat().st_ctime).strftime("%m/%d/%Y, %H:%M:%S")
        fullPath = str(PurePath(filePath))
        fileData["downloads"] = downloads[fullPath] if fullPath in downloads else 0
        filesData.append(fileData)
    return filesData
