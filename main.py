import server
import callbacks

#init server with ip, port, and a root directory.
s = server.server('localhost', 50000, 'files')

#add commands to the server commands
s.actions['dirlist'] = callbacks.dirlist_callback
s.actions['cd'] = callbacks.cd_callback
s.actions["download"] = callbacks.download_callback

s.listen()
