# Python 3 server example
from http.server import SimpleHTTPRequestHandler
import socketserver 

"""
Class to create a local webServer to download the zip file 
to test the webdav and NFS upload

Parameters : 
serverPort : server used to launch the server


variables :
serverPort : int 
fileDownloadServer : TCPServer (the server used to give the files to the user when they try to dowload the file)


Methodes : 
runServer : returns None (used to run the local server and launch in the serverPort)

"""



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

# function to run the server continuously
def runServer(localServerConfig):
    try : 
        myServer = MyServer(localServerConfig["port"])
        myServer.runServer()
        print("Server is run")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    runServer({"port" : 7123})