import requests
import enum 

class LogMessageType(enum.Enum):
    Debug = 1
    Info = 2
    Critical = 3
    Warning = 4
    Error = 5
    Exception = 6


class MattermostHandler:
    def __init__(self, config):
        self.hookLink = config["hookLink"]
        self.mattermostMessages = ["| Progress               | Message                 | Action Status      |","|:------------------------|:-----------------------:|:-------------------"]
        self.configurations = {"progressColumnLength" : 25,"messageColumnLength" : 25, "statusColumnLength" : 20}
        self.errorCounts = {"crtitical" : 0,"warning" : 0,"debug" : 0, "error" : 0}
        self.logger = config["logger"]
    def addLine(self,logMessageType ,logAction , messageText):
        message = " %s"%logAction
        for i in range(self.configurations["progressColumnLength"]-len(logAction)):
            message+=" "
        message+=("| %s"%(messageText))
        for i in range(self.configurations["messageColumnLength"]-len(messageText)):
            message+=" "
        if logMessageType is LogMessageType.Info:
            message += "| :white_check_mark: "
        elif logMessageType is LogMessageType.Warning:
            message += "| :warning:          "
            self.errorCounts["warning"]+=1
        elif logMessageType is LogMessageType.Error:
            message += "| :no_entry:         "
            self.errorCounts["error"]+=1
        elif logMessageType is LogMessageType.Critical:
            message += "| :octagonal_sign:   "
            self.errorCounts["critical"]+=1
        elif logMessageType is LogMessageType.Debug:
            message += "| :construction:     "
            self.errorCounts["debug"]+=1
        self.mattermosMessages.append(message)
    def getFormattedMessage(self):
        formattedMessage = ""
        for i in range(len(self.mattermostMessages)):
            formattedMessage+=self.mattermostMessges[i]
        return formattedMessage
    def sendNotification(self):
        payload = {
            "icon_url": "https://www.mattermost.org/wp-content/uploads/2016/04/icon.png",
            "text": self.getFormattedMessage(),
        }
        try:
            # Post request on Mattermost TSE server
            req = requests.post(self.hooks, json=payload)
            # Raise error if request was not accepted.
            req.raise_for_status()

        except requests.exceptions.ConnectionError:
            self.logger.addLogLine(LogMessageType.error,
                "Mattermost notification"," Notification not sent. Connection error, please check your mattermost hook is still runinng.")
        except requests.exceptions.HTTPError as err:
            self.logger.addLogLine(LogMessageType.error,"Mattermost notification "," Notification not sent. HTTP error code: " + err.args[0])
        except requests.exceptions.Timeout:
            self.logger.addLogLine(LogMessageType.error,"Mattermost notification "," Notification not sent. Timeout, please retry and check the mattermost link.")
        except requests.exceptions.RequestException:
            self.logger.addLogLine(LogMessageType.error,"Mattermost notification "," Could't send the mattermost post request.")