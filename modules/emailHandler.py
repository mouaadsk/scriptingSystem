import re
import json
import smtplib
import ssl
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email_validator import validate_email
import smtpd
import asyncore
import os
import threading

class EmlServer(smtpd.SMTPServer):
    no = 0
    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to:', rcpttos)
        print('Message length:', len(data))
        return



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
            self.initializeService()
        except Exception as e:
            print(e)
    def initializeService(self):
        try:
            context = ssl.create_default_context()
            # Open secure connection with SMTP server to send e-mails
            self.emailHandler = smtplib.SMTP_SSL(
                self.serverIp, port=self.serverPort
            )

        except TimeoutError:
            self.log_email_matt.warning(
                "E-mail server connection",
                "Timeout error, check e-mail server is down. E-mails not sent.",
            )

        except smtplib.SMTPServerDisconnected as e:
            print(e)
    def sendFromLocal(self, linesList):
    #TODO : here we create an internal smtp server : Need to change this in here
        try:
            message = MIMEMultipart()
            message.set_unixfrom('author')
            msg['To'] = email.utils.formataddr(('Recipient', self.destinations[0]))
            msg['From'] = email.utils.formataddr(('Author', self.authentication["email"]))
            message["Subject"] = self.emailTitle
            message.attach(MIMEText(self.formatEmailContent(linesList)))
            if(self.attachLog):
                message = self.attachLogToMessage(message)
            localServer = smtplib.SMTP('localhost')
            localServer.set_debuglevel(1)
            localServer.send_message(message)
        except Exception as e:
            print(e)
    
    def sendEmail(self, linesList):
        try:
            self.emailHandler.login(self.authentication["email"],self.authentication["password"])
            message = MIMEMultipart()
            message["Subject"] = self.emailTitle
            message["To"] = self.destinations[0]
            print(message["To"])
            message["From"] = self.authentication["email"]
            message.attach(MIMEText(self.formatEmailContent(linesList)))
            if(self.attachLog):
                message = self.attachLogToMessage(message)
            response = self.emailHandler.send_message(message)
        except smtplib.SMTPAuthenticationError:
            print("Logging-in email server , The server did not accept the username/password combination. E-mails not sent.") 
        except smtplib.SMTPNotSupportedError:
            print("Logging-in email server , The AUTH command is not supported by the server. E-mails not sent.")
        # Another error
        except smtplib.SMTPException:
            print("Logging-in email server, Unknown error occured while logging-in to your mail account. E-mail(s)not sent.")
        except Exception as e:
            print(e)
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
            print("Attachment, Unknown error occured during mail attachment loading. No attachment sent with e-mails.")
            
