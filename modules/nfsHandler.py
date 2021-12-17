import datetime
import os
import subprocess
from modules.enum import LogMessageType


"""
NFS Connection hadnler : used to mount the NFS Server locally and copying file into it 


Methodes : 
unmout : return None (unmounting the mounted nfs server in the local storage)
mountLocally : return None (mounting the nfs server in the local)
uploadTGZ : return None (copying the tgzFile int o the mounted NFS Server)
checkIfFileAkreadyExists : return bool (Chekcing if the files exists in the nfs Server)



"""

class NFSHandler:
    def __init__(self, config):
        self.config =config
        self.logger = config["logger"]
    def mountLocally(self):
        try:
            #Creatin the command to mount the nfs server into the local
            mountCommand = 'echo %s|sudo -S mount -t nfs "%s" "%s"'%(self.config["rootPassword"],self.config["host"], self.config["mountPath"])
            #Executing the created command
            sp = subprocess.Popen(mountCommand,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            rc=sp.wait()
            out,err=sp.communicate()
            if(err):
                #Adding the errors in the log
                self.logger.addLogLine(LogMessageType.Critical, "NFS Mount", "Please check that you gave permission to the script, and all conifurations are correct (mountLink, mountDirectory, etc)")
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Critica, "NFS Mount", "Error while mounting the NFS Server"+str(e))
    def unmount(self):
        try:
            #Creating the command to unmount the NFS Server
            sp = subprocess.Popen("echo %s|sudo -S umount %s"%(self.config["rootPassword"],self.config["mountPath"]),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            rc=sp.wait()
            out,err=sp.communicate()
            if(err):
                self.logger.addLogLine(LogMessageType.Critical, "NFS Unmount", "Please check that you gave permission to the script, and all conifurations are correct (mountLink, mountDirectory, etc)")
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Critica, "NFS Unmount", "Error while unmounting the NFS Server"+str(e))
    def uploadTGZ(self):
        try:
            #Mounting the server locally then copying the tgzFile into it 
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
        #Mounting the nfs server locally then checking if it countins the tgzFile already
        self.mountLocally()
        fileExists = os.path.exists('"%s/%s"'%(self.config["mountPath"],self.config["tgzFileName"]))
        self.unmount()
        return fileExists