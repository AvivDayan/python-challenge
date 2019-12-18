import server
import callbacks

s = server.server('localhost', 50000, 'files')
s.actions['dirlist'] = callbacks.dirlist_callback
s.actions['cd'] = callbacks.cd_callback
s.actions["download"] = callbacks.download_callback

s.listen()
