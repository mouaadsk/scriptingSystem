import enum 
import logging
from imp import reload

class LogMessageType(enum.Enum):
    Debug = 1
    Info = 2
    Critical = 3
    Warning = 4
    Error = 5
    Exception = 6
    
class LogHandler:
    def __init__(self):
        self.lines = []
        try:
            #clearing the logFile content
            open("log.log", "w").close()
            self.errorCounts = {"crtitical" : 0,"warning" : 0,"debug" : 0, "error" : 0}
            reload(logging)
            logging.basicConfig(filename="log.log",format="%(asctime)s - %(levelname)s - %(message)s",filemode='a',level=logging.NOTSET)
            self.logger = logging.getLogger("script_logger")
        except Exception as e:
            print(e)
    def addLogLine(self, logMessageType ,logAction , messageText):
        try :
            msg = "%s : %s" %(logAction ,messageText)
            self.lines.append(msg)
            if logMessageType is LogMessageType.Info:
                self.logger.info(msg)
            elif logMessageType is LogMessageType.Warning:
                self.logger.warning(msg)
                self.errorCounts["warning"]+=1
            elif logMessageType is LogMessageType.Error:
                self.logger.error(msg)
                self.errorCounts["error"]+=1
            elif logMessageType is LogMessageType.Critical:
                self.logger.critical(msg)
                self.errorCounts["critical"]+=1
            elif logMessageType is LogMessageType.Debug:
                self.logger.debug(msg)
                self.errorCounts["debug"]+=1
        except Exception as e:
            print(e)
    def close(self):
        self.logger.close()
    def getLogLines(self):
        return self.lines;