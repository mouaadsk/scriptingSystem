import smtplib
import ssl
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email_validator import validate_email
import enum
import os
class LogMessageType(enum.Enum):
    Debug = 1
    Info = 2
    Critical = 3
    Warning = 4
    Error = 5
    Exception = 6


class EmailHandler :
    def __init__(self, config):
        try :
            self.authentication = config["authentication"]
            self.serverIp = config["serverIp"]
            self.serverPort = config["serverPort"]
            self.destinations = config["destinations"]
            self.emailTitle = config["emailTitle"]
            self.attachLog = config["attachLog"]
            self.logFileName = config["logFileName"]
            self.emailHandler = None
            self.localServer = None
            self.logger = config["logger"]
            self.initializeService()
        except Exception as e:
            self.logger.addLine(LogMessageType.Error, "Configuration", "Please chack that you added all the needed configurations in the config file")
    def initializeService(self):
        try:
            context = ssl.create_default_context()
            # Open secure connection with SMTP server to send e-mails
            self.emailHandler = smtplib.SMTP_SSL(
                self.serverIp, port=self.serverPort
            )

        except TimeoutError:
            self.logger.addLogLine(
                LogMessageType.Error,
                "SMTP Connection",
                "Timeout error, please check you email server state (maybe it is down)",
            )

        except smtplib.SMTPServerDisconnected as e:
            self.logger.addLogLine(
                LogMessageType.Error,
                "SMTP Connection",
                "Server disconnected us , please reconfigue it to accept the connection ",
            )
    def sendFromLocal(self, linesList):
    #TODO : here we create an internal smtp server : Need to change this in here
        try:
            message = MIMEMultipart()
            message.set_unixfrom('author')
            message['To'] = email.utils.formataddr(('Recipient', self.destinations[0]))
            message['From'] = email.utils.formataddr(('Author', self.authentication["email"]))
            message["Subject"] = self.emailTitle
            message.attach(MIMEText(self.formatEmailContent(linesList)))
            if(self.attachLog):
                message = self.attachLogToMessage(message)
            localServer = smtplib.SMTP('localhost')
            localServer.set_debuglevel(1)
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Error,"Email Creation","An Error occured during creation of the email ")
        finally:
            localServer.send_message(message)
            self.logger.addLogLine(LogMessageType.INFO,"Sending the email","Daily report email is sent succefully")
    def sendEmails(self):
        try:
            if(len(self.destinations)==0):
                self.logger.addLogLine(LogMessageType.Warning, "Sending Email Block", "Please add some destination in the config file")
            self.emailHandler.login(self.authentication["email"],self.authentication["password"])
            self.logger.addLogLine(LogMessageType.Error, "SMTP Login", "Successful Login")
            message = MIMEMultipart()
            message["Subject"] = self.emailTitle
            message["To"] = self.destinations[0]
            message["From"] = self.authentication["email"]
            message.attach(MIMEText(self.formatEmailContent(self.logger.getLogLines())))
            if(self.attachLog):
                message = self.attachLogToMessage(message)
            for email in self.destinations:
                if(validate_email(email)):
                    message["To"] = email
                    self.emailHandler.send_message(message)
                else :
                    self.logger.addLogLine(LogMessageType.Warning, "Senfing Email Block ", email + " is an Invalid Email")
        except smtplib.SMTPAuthenticationError:
            self.logger.addLogLine(LogMessageType.Error,"SMTP Login "," The cridentials aren't correct : please check username and password in the config file (email is not sent)") 
        except smtplib.SMTPNotSupportedError:
            self.logger(LogMessageType.Error,"SMTP Login"," Couldn't connect : the auth command isn't accepted by the server (email is not sent)")
        # Another error
        except smtplib.SMTPException:
            self.logger(LogMessageType.Error,"SMTP Login"," Unknown error occured while SMTP Logging (email is not sent).")
        finally :
            if(self.emailHandler!=None):
                self.emailHandler.quit()
    def formatEmailContent(self, linesList):
        formattedContent = ""
        for line in linesList:
            formattedContent += line + "\n"
        return formattedContent
    def attachLogToMessage(self, message):
        try:
            fileInstance = MIMEBase("application", "octet-stream")
            logFile = open(os.getcwd()+"/"+self.logFileName, "rb")
            fileInstance.set_payload(logFile.read())
            encoders.encode_base64(fileInstance)
            fileInstance.add_header("Content-Disposition", "attachment; filename= " + self.logFileName)
            message.attach(fileInstance)
            return message
        except EnvironmentError:
            self.logger(LogMessageType.Warning,"Attaching log to email "," Unknown error occured during attaching the log to the email. No attachment is sent with email.")
            
