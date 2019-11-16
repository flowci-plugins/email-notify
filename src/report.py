import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from util import getVar, fetchCredential

SmtpAddr = getVar('FLOWCI_EMAIL_SMTP')
IsSSL = getVar('FLOWCI_EMAIL_SSL')
FromAddr = getVar('FLOWCI_EMAIL_FROM')
ToAddr = getVar('FLOWCI_EMAIL_TO')
Credential = getVar('FLOWCI_EMAIL_CREDENTIAL', required=False)

def createServer():
    if IsSSL in ['true', 'yes']:
        return smtplib.SMTP_SSL(SmtpAddr, 465)
        
    return smtplib.SMTP(SmtpAddr)

def createHtml():
    msg = MIMEText('hello, send by Python...', 'html', 'utf-8')
    msg['From'] = FromAddr
    msg['To'] = ToAddr
    msg['Subject'] = Header('flow.ci report', 'utf-8').encode()

def fetchFlowUsers():
    global ToAddr
    # TODO: fetch flow userlist from api
    pass

def fetchCredentail():
    pass

def send():
    server = createServer()

    if ToAddr == 'FLOW_USERS':
        fetchFlowUsers()

    if Credential != None:
        c = fetchCredentail()
        server.login(c['pair']['username'], c['pair']['password'])

    msg = createHtml()
    server.sendmail(from_addr=FromAddr, to_addrs=ToAddr.split(','), msg=msg.as_string())
    server.quit()

send()
