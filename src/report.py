import smtplib
import sys
import os
from jinja2 import Template, Environment, FileSystemLoader
from flowci import client
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

SmtpConfig = client.GetVar('FLOWCI_SMTP_CONFIG')
FromAddr = client.GetVar('FLOWCI_EMAIL_FROM')
ToAddr = client.GetVar('FLOWCI_EMAIL_TO')


API = client.Client()
Config = API.getConfig(SmtpConfig)

if Config == None:
    sys.exit('Cannot get smtp config')

if Config['category'] != 'SMTP':
    sys.exit('Invalid SMTP config')

SmtpSecure = Config['smtp']['secure'] # NONE, SSL, TLS
SmtpAddr = Config['smtp']['server']
SmtpPort = Config['smtp']['port']
SmtpUser = Config['smtp']['auth']['username']
SmtpPw = Config['smtp']['auth']['password']

print(Config)

def createServer():
    if SmtpSecure in ['ssl', 'SSL']:
        return smtplib.SMTP_SSL(SmtpAddr, SmtpPort)
        
    return smtplib.SMTP(SmtpAddr, SmtpPort)


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def createHtml():
    currentDir = os.path.dirname(os.path.abspath(__file__))

    loader = FileSystemLoader(currentDir)
    env = Environment(loader=loader)
    tm = env.get_template('template.html')

    job = client.GetCurrentJob()
    html = tm.render(job=job)
    print(html)

    msg = MIMEText(html, 'html', 'utf-8')
    msg['From'] = _format_addr('flow.ci <%s>' % FromAddr)
    msg['To'] = ToAddr

    subject = "flow.ci report"
    msg['Subject'] = Header(subject, 'utf-8').encode()
    return msg

def send():
    global ToAddr
    try:
        server = createServer()
        server.set_debuglevel(1)

        api = client.Client()

        if ToAddr == 'FLOW_USERS':
            users = api.listFlowUsers()
            emails = ''
            for user in users:
                emails += user['email'] + ","
            ToAddr = emails

        if SmtpUser != None:
            server.login(SmtpUser, SmtpPw)

        msg = createHtml()
        server.sendmail(from_addr=FromAddr, to_addrs=ToAddr.split(','), msg=msg.as_string())
        server.quit()
        print('[INFO] email been sent')
    except smtplib.SMTPException as e:
        print('[ERROR] on send email %s' % e)

send()
