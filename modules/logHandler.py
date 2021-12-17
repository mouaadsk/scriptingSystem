import logging
from imp import reload
from modules.enum import LogMessageType

"""
Class used to add lines into the log file

Variables :
logger : Logger (controls the logging file )

Methodes :
addLogLine : return None (formates and adds the logs into the log file as a line )
close : return None (closed the logger controler)
getLogLines : returns list (return the logs lines existed in the log file)

"""
    
class LogHandler:
    def __init__(self):
        self.lines = []
        try:
            #clearing the logFile content
            open("log.log", "w").close()
            # initializing the number of critical, errors and warning found while running the program
            self.errorCounts = {"crtitical" : 0,"warning" : 0,"debug" : 0, "error" : 0}
            # reloading the logger and initializing it
            reload(logging)
            logging.basicConfig(filename="log.log",format="%(asctime)s - %(levelname)s - %(message)s",filemode='a',level=logging.NOTSET)
            self.logger = logging.getLogger("script_logger")
            self.addLogLine(LogMessageType.Info, "Initilializing the logger objdect", "The logger object is initialized")
        except Exception as e:
            print(e)
    def addLogLine(self, logMessageType ,logAction , messageText):
        try :
            #formatting the log message to be added in the log file
            msg = "%s : %s" %(logAction ,messageText)
            self.lines.append(msg)
            # incrementing the number of states found while executing the script 
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