import datetime
import os
import subprocess
import enum 

class LogMessageType(enum.Enum):
    Debug = 1
    Info = 2
    Critical = 3
    Warning = 4
    Error = 5
    Exception = 6

class NFSHandler:
    def __init__(self, config):
        self.config =config
        self.logger = config["logger"]
    def mountLocally(self):
        try:
            mountCommand = 'echo %s|sudo -S mount -t nfs "%s" "%s"'%(self.config["rootPassword"],self.config["host"], self.config["mountPath"])
            sp = subprocess.Popen(mountCommand,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            rc=sp.wait()
            out,err=sp.communicate()
            if(err):
                self.logger.addLogLine(LogMessageType.Critical, "NFS Mount", "Please check that you gave permission to the script, and all conifurations are correct (mountLink, mountDirectory, etc)")
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Critica, "NFS Mount", "Error while mounting the NFS Server"+str(e))
    def unmount(self):
        try:
            sp = subprocess.Popen("echo %s|sudo -S umount %s"%(self.config["rootPassword"],self.config["mountPath"]),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            rc=sp.wait()
            out,err=sp.communicate()
            if(err):
                self.logger.addLogLine(LogMessageType.Critical, "NFS Unmount", "Please check that you gave permission to the script, and all conifurations are correct (mountLink, mountDirectory, etc)")
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Critica, "NFS Unmount", "Error while unmounting the NFS Server"+str(e))
    def uploadTGZ(self):
        try:
            self.mountLocally()
            sp = subprocess.Popen('echo %s|sudo -S cp "%s/%s" "%s"'%(self.config["rootPassword"],self.config["tgzPath"],self.config["tgzFileName"],self.config["mountPath"]),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            rc=sp.wait()
            out,err=sp.communicate()
            if(err):
                self.logger.addLogLine(LogMessageType.Critical, "NFS Upload TGZ", "Please check that you gave permission to the script, and all conifurations are correct (mountLink, mountDirectory, etc)")
            self.unmount()
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Critica, "NFS Upload TGZ", "Error while uploading the TGZ File Server"+str(e))
    def checkIfFileAlreadyExists(self):
        self.mountLocally()
        fileExists = os.path.exists('"%s/%s"'%(self.config["mountPath"],self.config["tgzFileName"]))
        self.unmount()
        return fileExists