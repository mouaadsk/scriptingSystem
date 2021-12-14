import os
from modules.zipManipulator import ZipClass
from webServer.webserver import MyServer



def main():
    myServer = None
    zipManipulator = None
    try : 
        myServer = MyServer(7123)
        myServer.runServer()
        print(os.getcwd())
        # zipManipulator = ZipClass(os.getcwd()+"/tmp","http://localhost:4444/webServer/my_zip.zip")
        # zipManipulator.downloadZip()
        print("Server is run")
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()