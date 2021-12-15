import os
from webdav3.client import Client
import datetime
import enum

class LogMessageType(enum.Enum):
    Debug = 1
    Info = 2
    Critical = 3
    Warning = 4
    Error = 5
    Exception = 6

class WebDavHandler :
    def __init__(self, config):
            self.logger = config["logger"]
            self.tgzName = config["tgzName"]
            self.tgzPath = config["tgzPath"]
            self.server_link = config["cridentials"]["serverLink"]
            self.server_username = config["cridentials"]["serverLsername"]
            self.server_password = config["cridentials"]["serverPassword"]
            self.client = None
            self.logger.addLogLine(LogMessageType.Info,"WebDavHandler Creation", "WebDav Handler created succefully")
    def UploadTGZ(self):
        try : 
            options = {
                        'webdav_hostname': self.server_link,
                        'webdav_login':    self.server_username,
                        'webdav_password': self.server_password
                    }
            self.client = Client(options)
            #Not checking the ssl certificate
            self.client.verify = False 
            self.client.upload_sync(remote_path=self.tgz_name,local_path=self.tgz_path+"/"+self.tgz_name)
        except Exception as e :
            self.logger.addLogLine(LogMessageType.Error,"WebDav TGZ Upload ",
            " Please check your webdav configuration : link ,username or password is incorrect")
    def checkIfUploaded(self):
        if self.client is not None:
            isUploaded = self.client.check(self.tgz_name)
            self.logger.addLogLine(LogMessageType.Info , "TGZ File WebDav", "Checking if the tgz file is uploaded " + str(isUploaded))
            return isUploaded
        return False
    #detecting the old file and removing them
    def removeOldFiles(self):
        try:
            if self.client is not None:
                    # Current directory.
                    files = self.client.list(".")
                    dead_line = (
                    datetime.datetime.today()
                    - datetime.timedelta(days=self.time_to_save)
                    ).date()

                    for file in files:
                        try:
                            date = datetime.datetime.strptime(
                                file.replace(".tgz", ""), "%Y%d%m"
                            ).date()
                            if date < dead_line:
                                self.client.clean(file)
                                self.log_email_matt.info("WebDav archival : "+file+"is removed")
                        except ValueError:
                            pass
            else :
                self.logger.addLogLine(LogMessageType.Critical,"WebDav remocing old files", "WebDav Client is not initialized : Please check you cridentials in config (link, username and [assword])")                
        except (IOError, OSError) as err:
            if err is OSError:
                path = "Local"
            else:
                path = "Remote"
            self.logger.addLogLine(LogMessageType.error,"WebDav Connect", path + " path does not exists.")