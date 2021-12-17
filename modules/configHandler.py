import json
from os.path import exists
import os
import datetime
from modules.enum import LogMessageType

#Default configuration to be dumped into the config file
defaultConfig = """{
    "fileName": "dimpfile.sql",
    "zipUrl": "http://localhost:7123/webServer/my_zip.zip",
    "loaclServerConfig": {
        "port": 9999
    },
    "zipFileName": "my_zip.zip",
    "smtpConfig": {
        "authentication": {
            "email": "noreply@ariba.ma",
            "password": "Agadir414$"
        },
        "serverIp": "mail.ariba.ma",
        "serverPort": 465,
        "emailTitle": "Daily Report",
        "destinations": [
            "mouaadsk@protonmail.com"
        ]
    },
    "webDavConfig" : {
        "cridentials" : {
            "serverLink" : "http://webdav.local/svn",
            "serverLsername" : "admin",
            "serverPassword" : "admin"    
        }
    },
    "nfsConfig" : {
        "mountPath" : "nfs_mount_directory",
        "rootPassword" : "",
        "host" : "nfs link here"

    },
    "mattermostConfig" : {
        "hookLink" : "https://chat.telecomste.fr/hooks/13ta3nw3e787tnxxqkyxfh5xnr"
    },
    "sendEmail" : "always",
    "logFileName": "log.log",
    "attachLog": true
}"""




"""
Config loading and extracting handler


Parameters : 
configPath : text (The path where the config file exists)
configFileName : text 
logger : text (The log handler)

Methodes : 
loadConfig : return None (parsing the configutaitons from the config json file)
generateConfig : return None (dumping the configuration into the config.json file)
checkIfConfigFileExists : return bool (chekcs if the config file exists in the path)
getTGZName : return text (Generates the tgzFileName from today's date)
getSMTPConfig : return dictionay (gets the emailHandler config needed)
getWebDavConfig : return dictionay (gets the webDabHandler config needed)
getNfsConfig : return dictionay (gets the NFSHandler config needed)
getMattermostConfig : return dictionay (gets the MattermostHandler config needed)
getZipManipulatorConfig : return dictionay (gets the ZipManipulator config needed)
getLocalServerConfig  : return dictionay (gets the WebServer config needed)



"""



class ConfigHandler:
    def __init__(self, configPath, configFileName, logger=None):
        self.configPath = configPath
        self.configFileName = configFileName
        self.logger = logger
        #Loading the configurations from the config file
        self.loadConfig()
        self.logger.addLogLine(LogMessageType.Info, "Creating Config Object" , "ConfigHandler object is created succefully")

    def loadConfig(self):
        try:
            jsonFile = open("%s/%s" % (self.configPath, self.configFileName))
            self.config = json.load(jsonFile)
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Error, "Opening the config file",
                                   "Error while opening the log file : " + str(e))

    def generateConfig(self):
        try:
            if(self.checkConfigFileExists()):
                os.remove(self.configFileName)
            with open("config.json", "w") as configFile:
                json.dump(defaultConfig, configFile, indent="\t")
                self.logger.addLogLine(LogMessageType.Info,"Generating the config file ","Configuration file regenerated successfully.")
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Error, "Generating the config",
                                   "Error while opening the log file : please check that config.json exists in the directory")

    def checkIfConfigFileExists(self):
        return exists(self.configFileName)

    def getTGZName(self):
        today = datetime.date.today()
        return ("%d%d%d" %
                (today.year, today.month, today.day))+".tgz"

    def getConfig(self):
        return self.config

    def getSMTPConfig(self):
        smtpConfig = self.config["smtpConfig"]
        smtpConfig["attachLog"] = self.config["attachLog"]
        smtpConfig["logFileName"] = self.config["logFileName"]
        smtpConfig["logger"] = self.logger
        smtpConfig["sendEmail"] = self.config["sendEmail"]
        return smtpConfig

    def getWebDavConfig(self):
        webDavConfig = self.config["webDavConfig"]
        webDavConfig["tgzName"] = self.getTGZName()
        webDavConfig["tgzPath"] = os.getcwd()+"/tmp"
        webDavConfig["logger"] = self.logger
        webDavConfig["availabilityDuration"] = self.config["availabilityDuration"]
        return webDavConfig

    def getNfsConfig(self):
        nfsConfig = self.config["nfsConfig"]
        nfsConfig["logger"] = self.logger
        nfsConfig["availabilityDuration"] = nfsConfig["availabilityDuration"]
        return nfsConfig

    def getMattermostConfig(self):
        mattermostConfig = self.config["mattermostConfig"]
        mattermostConfig["logger"] = self.logger
        return mattermostConfig
    def getZipManipulatorConfig(self):
        zipConfig = {"zipUrl" : self.config["zipUrl"], "fileName" : self.config["fileName"],"zipFileName" : self.config["zipFileName"]}
        zipConfig["logger"] = self.logger
        zipConfig["savingPath"] = os.getcwd()+"/tmp"
        return zipConfig
    def getLocalServerConfig(self):
        return self.config["localServerConfig"]

def generateConfig():
    tempConfigFile = ConfigHandler(os.getcwd()+"/../","config.json")
    tempConfigFile.generateConfig()



if __name__ == "__main__":
    generateConfig()