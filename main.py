import email
import os
from typing import final
from modules.configHandler import ConfigHandler
from modules.emailHandler import EmailHandler
from modules.logHandler import LogHandler
from modules.mattermostHandler import MattermostHandler
from modules.webDavHndler import WebDavHandler
from modules.zipManipulator import ZipClass
from webServer.webserver import MyServer
from modules.enum import LogMessageType


def main():
    ## Initializing all needed Handlers
    logger = LogHandler()
    configHandler = ConfigHandler(os.getcwd(),"config.json",logger)
    zipManipulator = ZipClass(configHandler.getZipManipulatorConfig())
    emailHandler = EmailHandler(configHandler.getSMTPConfig())
    matterMostHandler = MattermostHandler(configHandler.getMattermostConfig())
    webDavHandler = WebDavHandler(configHandler.getWebDavConfig())
    try:
        #The process to upload, chekc and remove the old files 
        zipManipulator.downloadZip()
        if(zipManipulator.checkIfContainsTheFileAndGetInfos()):
            if(zipManipulator.checkCorrectDay()):
                if(webDavHandler.checkIfUploaded() == False):
                    zipManipulator.extractContent()
                    zipManipulator.compressIntoTGZ()
                    webDavHandler.removeOldFiles()
                    webDavHandler.UploadTGZ()
                    if(webDavHandler.checkIfUploaded() == True):
                        logger.addLogLine(LogMessageType.Info,"TGZ Upload Status" , "TGZ File is uploaded succefully into the server")
                    else:
                        logger.addLogLine(LogMessageType.Critical,"Checking file in the server" , "Couldn't upload the TGZ file into the webdav server, please check the sebDavConfirutation int config file")
                    zipManipulator.clean()
                else:
                    logger.addLogLine(LogMessageType.Info,"Checking file in the server" , "The TGZ file already exists in the server")
            else:
                logger.addLogLine(LogMessageType.Error, "Zip Checking : " , "The current date of the file is not Today")

            
        else:
            logger.addLogLine(LogMessageType.Critical, "Zip Checking : " , "Zip File doesn't contain the wanted file.")
    except Exception as e:
        print(e)
        LogHandler.addLogLine(LogMessageType.Critical, "Starting The Programm","Could't start the Automated system")
    finally:
        emailHandler.sendEmails()
        matterMostHandler.sendNotification()

if __name__ == "__main__":
    main()