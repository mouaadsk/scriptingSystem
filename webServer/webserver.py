# Python 3 server example
from http.server import SimpleHTTPRequestHandler
import socketserver 

class MyServer():
    def __init__(self, serverPort=5555):
        self.serverPort = serverPort
        self.fileDownloadServer = socketserver.TCPServer(("", self.serverPort), SimpleHTTPRequestHandler) 
    def runServer(self):
        try:
            print("The file server in the port %d" % self.serverPort)
            self.fileDownloadServer.serve_forever()
            # stoping the server when typing ctrl+c in the terminal 
        except KeyboardInterrupt:
            # self.fileDownloadServer.server_close()
            pass


