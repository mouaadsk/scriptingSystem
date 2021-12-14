import requests
import zipfile
import os
import datetime
import tarfile


class ZipClass :
    def __init__(self, savingPath, zipUrl, fileName):
        print("ZipClass is initialized")
        self.zipFileName = "my_zip.zip"
        self.savingPath = savingPath
        self.zipUrl = zipUrl
        self.fileInfos = None
        self.fileName = fileName
        self.tgzName = None
    """Downloading the zip file and saving it in the savingPath"""
    def downloadZip(self):
        try : 
            #Data retrieving from the url given
            r = requests.get(self.zipUrl)
            with open(self.savingPath+"/"+self.zipFileName, "wb") as f:
                f.write(r.content)
        except Exception as e:
            print(e)
    
    def extractContent(self):
        try:
            zipRef = zipfile.ZipFile(self.savingPath+"/"+self.zipFileName, 'r')
            zipRef.extractall(self.savingPath)
            zipRef.close()
        except Exception as e:
            print(e)
    def clean(self):
        try : 
            os.remove(self.savingPath + "/" + self.zipFileName)
            os.remove(self.savingPath + "/" + self.fileName)
            #os.remove(self.savingPath + "/" + self.tgzName)
        except Exception as e:
            print(e)
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
            print(e)
    def checkCorrectDay(self):
        try:
            fileDate = datetime.date(*(self.fileInfos).date_time[0:3])
            todayDate = datetime.date.today()
            return datetime.date.today() == fileDate
        except Exception as e:
            print(e)
    def compressIntoTGZ(self):
        try:
            today = datetime.date.today()
            self.tgzName = ("%d%d%d"%(today.year, today.month, today.day))+".tgz"
            tar = tarfile.open("%s/%s"%(self.savingPath,self.tgzName), "w:gz")
            tar.add(("%s/%s"%(self.savingPath, self.fileName)), arcname=self.fileName)
            tar.close()
        except Exception as e:
            print(e)