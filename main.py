import os
from modules.configHandler import ConfigHandler
from modules.emailHandler import EmailHandler
from modules.logHandler import LogHandler
from modules.mattermostHandler import MattermostHandler
from modules.webDavHndler import WebDavHandler
from modules.zipManipulator import ZipClass
from webServer.webserver import MyServer



def main():
    myServer = None
    logger = LogHandler()
    configHandler = ConfigHandler(os.getcwd(),"config.json",logger)
    zipManipulator = ZipClass(configHandler.getZipManipulatorConfig())
    emailHandler = EmailHandler(configHandler.getSMTPConfig())
    matterMostHandler = MattermostHandler(configHandler.getMattermostConfig())
    webDavHandler = WebDavHandler(configHandler.getWebDavConfig())
    localServerConfig = configHandler.getLocalServerConfig()
    runServer(localServerConfig)
    zipManipulator.downloadZip()
    zipManipulator.checkIfContainsTheFileAndGetInfos()
def runServer(localServerConfig):
    try : 
        myServer = MyServer(localServerConfig["port"])
        myServer.runServer()
        print("Server is run")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()