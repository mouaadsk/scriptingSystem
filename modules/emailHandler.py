import smtplib
import ssl
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email_validator import validate_email
from modules.enum import LogMessageType
import os


class EmailHandler:
    """
    This Class is used to handle all email (SMPT) operations 
    
    paramaters : 
    config : dictionary (contains all configuration needed to send an email)

    variables : 
    authentication : dictionary (holds the athentication crifentials of the smtp server to be used)
    serverIp : text (smtp server ip address)
    serverPort : int (the port used to connect to the SMTP server)
    destinations : list (emails list of the destination to send email to)
    emailTitle : text (the subject of the email)
    attachLog : bool (attaching the log file with the email or not)
    logger : LogHandler (log controlling object)
    sendEmail : text (when should we send the email {"critical", "always", "never})
    logFileName : text (the Lof file name)

    Methodes :
    InitializeService : returns None (Creating an SMTP_SSL object to build communication with the smtp server)
    sendEmailFromLocal : return None (used to send email from the local server to the destinations)
    sendEmails : returns None (Sending email to the destinations specified in the config file and passed by config to the object)
    formatEmailContent : return text (used to formatt the log content into lines to be sent in the email)
    attachLogMessages : return MIMEMultipart (adding and attaching the log content file to the email message)

    """
    def __init__(self, config):
        try:
            self.authentication = config["authentication"]
            self.serverIp = config["serverIp"]
            self.serverPort = config["serverPort"]
            self.destinations = config["destinations"]
            self.emailTitle = config["emailTitle"]
            self.attachLog = config["attachLog"]
            self.logFileName = config["logFileName"]
            self.sendEmail = config["sendEmail"]
            self.logger = config["logger"]
            self.connected = False
            self.initializeService()
        except Exception as e:
            self.logger.addLine(LogMessageType.Error, "Configuration",
                                "Please chack that you added all the needed configurations in the config file")
    # Trying to create a connection with the SMTP Server 
    def initializeService(self):
        try:
            # Creating an SMTP_SLL object to connect and send emails
            self.emailHandler = smtplib.SMTP_SSL(
                self.serverIp, port=self.serverPort
            )
            self.connected = True
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
    # method of sending te emails from the local server 
    def sendFromLocal(self, linesList):
        try:
            # Sending the email when the emailSend not set to never (only two other cases are possible "critical" and "always")
            if(self.sendEmail == "always" or (self.semdEmail == "critical" and self.logger.errorCounts["crtitical"] >= 0)):
                # Creating the object of the Email and filling its fields
                message = MIMEMultipart()
                message.set_unixfrom('author')
                message['To'] = email.utils.formataddr(
                    ('Recipient', self.destinations[0]))
                message['From'] = email.utils.formataddr(
                    ('Author', self.authentication["email"]))
                message["Subject"] = self.emailTitle
                message.attach(MIMEText(self.formatEmailContent(linesList)))
                # Attaching the log file with the email
                if(self.attachLog):
                    message = self.attachLogToMessage(message)
                localServer = smtplib.SMTP('localhost')
                localServer.set_debuglevel(1)
        except Exception as e:
            self.logger.addLogLine(LogMessageType.Error, "Email Creation",
                                   "An Error occured during creation of the email ")
        finally:
            #Sending the email to the destingation
            localServer.send_message(message)
            self.logger.addLogLine(
                LogMessageType.INFO, "Sending the email", "Daily report email is sent succefully")
    # the method to send emails using the smtp server 
    def sendEmails(self):
        try:
            # only sending email when we have always and critical in the configuration
            if(self.sendEmail == "always" or (self.semdEmail == "critical" and self.logger.errorCounts["crtitical"] >= 0)):
                #Checking if the destinations list is not empty and adding the error to the log
                if(len(self.destinations) == 0):
                    self.logger.addLogLine(
                        LogMessageType.Error, "Sending Email Block", "Please add some destination in the config file")
                    return
                # Trying to loging to the SMTP Server 
                self.emailHandler.login(
                    self.authentication["email"], self.authentication["password"])
                self.logger.addLogLine(
                    LogMessageType.Error, "SMTP Login", "Successful Login")
                message = MIMEMultipart()
                message["Subject"] = self.emailTitle
                if(self.logger.errorCounts["crtitical"]):
                    message["Subject"]+= " : Unsuccefull Execution"
                else:
                    message["Subject"]+= " : Successful Execution (TGZ Upload)"
                message["From"] = self.authentication["email"]
                message.attach(
                    MIMEText(self.formatEmailContent(self.logger.getLogLines())))
                if(self.attachLog):
                    message = self.attachLogToMessage(message)
                #Checking if the email added in destinations is a valid email address before sending it
                for email in self.destinations:
                    if(validate_email(email)):
                        message["To"] = email
                        self.emailHandler.send_message(message)
                    else:
                        self.logger.addLogLine(
                            LogMessageType.Warning, "Senfing Email Block ", email + " is an Invalid Email")
    # Catching all exceptions and adding them to the log file 
        except smtplib.SMTPAuthenticationError:
            self.logger.addLogLine(LogMessageType.Error, "SMTP Login ",
                                   " The cridentials aren't correct : please check username and password in the config file (email is not sent)")
        except smtplib.SMTPNotSupportedError:
            self.logger(LogMessageType.Error, "SMTP Login",
                        " Couldn't connect : the auth command isn't accepted by the server (email is not sent)")
        # Another error
        except smtplib.SMTPException:
            self.logger(LogMessageType.Error, "SMTP Login",
                        " Unknown error occured while SMTP Logging (email is not sent).")
        finally:
            if(self.emailHandler != None):
                self.emailHandler.quit()
    # Formatting the email content of the log to be sent with email
    def formatEmailContent(self, linesList):
        formattedContent = ""
        for line in linesList:
            formattedContent += line + "\n"
        return formattedContent
    # Attaching the log file to the email object
    def attachLogToMessage(self, message):
        try:
            # Creating a fileInstance and attaching it to the message as a payload
            fileInstance = MIMEBase("application", "octet-stream")
            logFile = open(os.getcwd()+"/"+self.logFileName, "rb")
            fileInstance.set_payload(logFile.read())
            encoders.encode_base64(fileInstance)
            #naming the attached file with the log name
            fileInstance.add_header(
                "Content-Disposition", "attachment; filename= " + self.logFileName)
            message.attach(fileInstance)
            return message
        except EnvironmentError:
            self.logger(LogMessageType.Warning, "Attaching log to email ",
                        " Unknown error occured during attaching the log to the email. No attachment is sent with email.")
