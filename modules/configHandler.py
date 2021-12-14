import json
from os.path import exists
import os

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
    "sendEmail": true,
    "logFileName": "log.log",
    "attachLog": true
}"""


class ConfigHandler:
    def __init__(self, configPath, configFileName):
        self.config = None
        self.configPath = configPath
        self.configFileName = configFileName
        self.loadConfig()

    def loadConfig(self):
        try:
            jsonFile = open("%s/%s" % (self.configPath, self.configFileName))
            self.config = json.load(jsonFile)
        except Exception as e:
            print(e)

    def generateConfig(self):
        try:
            if(self.checkConfigFileExists()):
                os.remove(self.configFileName)
            with open("config.json", "w") as configFile:
                json.dump(defaultConfig, configFile, indent="\t")
                print("Configuration file regenerated successfully.")
        except Exception as e:
            print(e)

    def checkIfConfigFileExists(self):
        return exists(self.configFileName)

    def getConfig(self):
        return self.config

    def getSMTPConfig(self):
        smtpConfig = self.config["smtpConfig"]
        smtpConfig["attachLog"] = self.config["attachLog"]
        smtpConfig["logFileName"] = self.config["logFileName"]
        return smtpConfig
