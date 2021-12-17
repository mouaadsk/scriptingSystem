import os
from webdav3.client import Client
import datetime
from modules.enum import LogMessageType



"""
Class used to handle all the webdav Operations (Connecting , uploading the files and removing all old files)


Parameters : 
config : dictionary (holds all the webDavHandler configurations such as cridentials, tgz information and availabilty of files)

Variables : 
logger : LogHandler (coantines the LogHandler object used in the whole program)
tgzName : text (The name of the TGZ file to upload)
tgzPath : text (the path were the tgzFile exists , usually is the tmp folder)
serverLink : text (The link used to build connection with webdav server)
serverUsername and serverPassword: text (username to connect with the webDav server)
client : WebdavClient (Object to handle the webDav connection and file upload)
availabilityDuration : int (number of days which file need to exceed to be deleted )  


Methodes : 
uploadTGZ : return None (uploading the tgz file to the webDav server)
checkIfUploaded : return bool (checking if the tgz  fiel named tgzName exists or not in the webdav server)
removeOldFiles : returns None (removing all files which have creation time older with availabilityduration days )

"""

class WebDavHandler :
    def __init__(self, config):
        #initializing all local configurations variables from the config file
            self.logger = config["logger"]
            self.tgzName = config["tgzName"]
            self.tgzPath = config["tgzPath"]
            self.serverLink = config["cridentials"]["serverLink"]
            self.serverUsername = config["cridentials"]["serverLsername"]
            self.serverPassword = config["cridentials"]["serverPassword"]
            self.client = None
            self.availabilityDuration = config["availabilityDuration"]
            self.logger.addLogLine(LogMessageType.Info,"WebDavHandler Creation", "WebDav Handler created succefully")
    def UploadTGZ(self):
        try : 
            # Creating the server configutation
            options = {
                        'webdav_hostname': self.serverLink,
                        'webdav_login':    self.serverUsername,
                        'webdav_password': self.serverPassword
                    }
            # initializing the client with the configuration
            self.client = Client(options)
            #Not checking the ssl certificate
            self.client.verify = False 
            # uplaoding the tgz file which is in the the tgzPath 
            self.client.upload_sync(remote_path=self.tgzName,local_path=self.tgzPath+"/"+self.tgzName)
            self.logger.addLogLine(LogMessageType.Info, "Uplaoding the TGZ File ", "The File : " + self.tgzName + "is uploaded succefully" )
        except Exception as e :
            # Addign errors to the log file
            self.logger.addLogLine(LogMessageType.Error,"WebDav TGZ Upload ",
            " Please check your webdav configuration : link ,username or password is incorrect")
    def checkIfUploaded(self):
        if self.client is not None:
            #checking if the tgzFile exists in the webDav server
            isUploaded = self.client.check(self.tgzName)
            self.logger.addLogLine(LogMessageType.Info , "TGZ File WebDav", "Checking if the tgz file is uploaded " + str(isUploaded))
            return isUploaded
        return False
    #detecting the old file and removing them
    def removeOldFiles(self):
        try:
            if self.client is not None:
                    # getting the files of the webDav server
                    files = self.client.list(".")
                    dead_line = (datetime.datetime.today()- datetime.timedelta(days=self.availabilityDuration)).date()
                    for file in files:
                        try:
                            date = datetime.datetime.strptime(
                                file.replace(".tgz", ""), "%Y%d%m"
                            ).date()
                            #testing the date of the file if it is valid or not
                            if date < dead_line:
                                self.client.clean(file)
                                self.logger.addLogLine.info(LogMessageType.Info,"WebDav Server Cleaning : ",file+" is removed in the server")
                        except ValueError:
                            self.logger.addLogLine(LogMessageType.Error, "Webdav Server Cleaning", "Couldn't remove the " + file + " File ")
                            pass
                    self.logger.addLogLine(LogMessageType.INFO,"WebDav removing old files", "All Old Files are removed from the server")                                    
            else :
                self.logger.addLogLine(LogMessageType.Critical,"WebDav removing old files", "WebDav Client is not initialized : Please check you cridentials in config (link, username and password)")                
        except (IOError, OSError) as err:
            if err is OSError:
                path = "Local"
            else:
                path = "Remote"
            self.logger.addLogLine(LogMessageType.error,"WebDav Connect", path + " path does not exists.")