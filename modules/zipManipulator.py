import requests
import zipfile
import os
import datetime
import tarfile
import enum


class LogMessageType(enum.Enum):
    Debug = 1
    Info = 2
    Critical = 3
    Warning = 4
    Error = 5
    Exception = 6


class ZipClass:
    """
    This class is used to manipulate and download the zip file from the link passed 
    by the config paramter
    
    Paramaters : 
    config : dictionary containing all necessary fields to 

    Variables :
    zipFileName : text (the name of zip file to be downlaoded)
    savingPath : text (the temporary directory which used to process the files)
    zipUrl : text (link to get th zipFile)
    fileInfos : ZipInfo (all zip file infos)
    fileName : text (the name of the dumpfile contained in the zipFile)
    tgzName : text (used to save the file name of the TGZ file created)
    logger : LogHandler object

    Methodes :
    downloadZip : returns None (used to download the zipFile)
    extractContent : returns None (extracts the files contained in the zip file downaded into the savingPath)
    clean : return None (remove the ZipFile, extracted files and the tgz File)
    checkIfContainsTheFileAndGetInfos : returns None (checks if the downloaded zipfile contains the FileName-DumpFile- and filling the zipInfos variable) 
    checkTheCorrectDay : return None (checking if the day of creation of DumpFile contained in the zipFile is correct)
    compressIntoTGZ : Adding the dumpFile into a .tgz File and save it in the savingPath directory
    """
    def __init__(self, config):
        print("ZipClass is initialized")
        self.zipFileName = config["zipFileName"]
        self.savingPath = config["savingPath"]
        self.zipUrl = config["zipUrl"]
        self.fileInfos = None
        self.fileName = config["fileName"]
        self.tgzName = None
        self.logger = config["logger"]


    """Downloading the zip file and saving it in the savingPath"""
    def downloadZip(self):
        try:
            # Data retrieving from the url given
            r = requests.get(self.zipUrl)
            with open(self.savingPath+"/"+self.zipFileName, "wb") as f:
                f.write(r.content)
        except requests.exceptions.ConnectionError:
            self.logger.addLogLine(LogMessageType.Critical,
                                   "Zip Downloading ", "counld't connect to the server, please check zipLink and the server if it is still running")
        except requests.exceptions.HTTPError as err:
            self.logger.addLogLine(LogMessageType.Critical,
                                   "Zip Downloading", "Zip File is not downloadd: " + err.args[0])
        except requests.exceptions.Timeout:
            self.logger.addLogLine(LogMessageType.Critical,
                                   "Zip Downloading ", " Timout connecting to the web server ")
        except requests.exceptions.RequestException:
            self.logger.addLogLine(
                LogMessageType.Critical, "Zip Downloading ", "Unknown error.")

    def extractContent(self):
        try:
            zipRef = zipfile.ZipFile(self.savingPath+"/"+self.zipFileName, 'r')
            zipRef.extractall(self.savingPath)
            zipRef.close()
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Critical,"Extracting the zip File", "Error in extracting the file : "+str(e))
    def clean(self):
        try:
            os.remove(self.savingPath + "/" + self.zipFileName)
            os.remove(self.savingPath + "/" + self.fileName)
            os.remove(self.savingPath + "/" + self.tgzName)
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Error,"Cleaning the zip files", "Error occured while removing the zipClass junk : "+str(e))

    def checkIfContainsTheFileAndGetInfos(self):
        try:
            zipRef = zipfile.ZipFile(self.savingPath+"/"+self.zipFileName, 'r')
            for zipInfo in zipRef.filelist:
                if(zipInfo.filename == self.fileName):
                    self.fileInfos = zipInfo
                    zipRef.close()
                    return True
            zipRef.close()
            return False
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Critical,"Zip File Checking", "Error occured whicle checking zip file content "+str(e))

    def checkCorrectDay(self):
        try:
            fileDate = datetime.date(*(self.fileInfos).date_time[0:3])
            # getting the today's date
            todayDate = datetime.date.today()
            #comparing if the the day of the file is correct
            return datetime.date.today() == fileDate
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Error,"Zip Correct day checking ", "Error occured whicle checking zip file day "+str(e))

    def compressIntoTGZ(self):
        try:
            today = datetime.date.today()
            self.tgzName = ("%d%d%d" %
                            (today.year, today.month, today.day))+".tgz"
            tar = tarfile.open("%s/%s" %
                               (self.savingPath, self.tgzName), "w:gz")
            tar.add(("%s/%s" % (self.savingPath, self.fileName)),
                    arcname=self.fileName)
            tar.close()
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Critical,"TGZ compressing", "Could't compress the file : please make sure you installed all dependencies "+str(e))
