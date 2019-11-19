import smtplib
import sys
import os
from jinja2 import Template, Environment, FileSystemLoader
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from util import Job, getVar, fetchCredential

SmtpAddr = getVar('FLOWCI_EMAIL_SMTP')
IsSSL = getVar('FLOWCI_EMAIL_SSL')
FromAddr = getVar('FLOWCI_EMAIL_FROM')
ToAddr = getVar('FLOWCI_EMAIL_TO')
Credential = getVar('FLOWCI_EMAIL_CREDENTIAL', required=False)

def createServer():
    if IsSSL in ['true', 'yes']:
        return smtplib.SMTP_SSL(SmtpAddr, 465)
        
    return smtplib.SMTP(SmtpAddr)


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def buildTemplateData():
    job = Job()

    return {
        'name': job.flowName,
        'number': job.number,
        'status': job.status,
        'startAt': job.startAt,
        'finishAt': job.finishAt,
        'duration': job.duration,
        'trigger': job.trigger,
        'triggerBy': job.triggerBy,
        'git': {
            'event': 'pr',
            'commit': {
                'id': 'xxx123123',
                'branch': 'master',
                'msg': 'hello world',
                'url': 'https://11231231231'
            },
            'pr': {
                'title': 'pr title',
                'msg': 'pr message',
                'url': 'pr url',
                'number': 'pr number',
                'head': {
                    'name': 'head repo name',
                    'branch': 'head repo branch',
                    'commit': 'head repo commit'
                },
                'base': {
                    'name': 'base repo name',
                    'branch': 'base repo branch',
                    'commit': 'base repo commit'
                }
            }
        },
        'steps': job.steps
    }


def createHtml():
    currentDir = os.path.dirname(os.path.abspath(__file__))

    loader = FileSystemLoader(currentDir)
    env = Environment(loader=loader)
    tm = env.get_template('template.html')

    job = buildTemplateData()
    html = tm.render(job=job)
    print(html)

    msg = MIMEText(html, 'html', 'utf-8')
    msg['From'] = _format_addr('flow.ci <%s>' % FromAddr)
    msg['To'] = ToAddr

    subject = "flow.ci report"
    msg['Subject'] = Header(subject, 'utf-8').encode()
    return msg

def fetchFlowUsers():
    global ToAddr
    # TODO: fetch flow userlist from api
    pass

def fetchJobSteps():
    # TODO: fetch job steps from api
    pass

def send():
    try:
        server = createServer()
        server.set_debuglevel(1)

        if ToAddr == 'FLOW_USERS':
            fetchFlowUsers()

        if Credential != None:
            c = fetchCredential(Credential)
            if c == None:
                sys.exit('Cannot get credential')
            server.login(c['pair']['username'], c['pair']['password'])

        msg = createHtml()
        # server.sendmail(from_addr=FromAddr, to_addrs=ToAddr.split(','), msg=msg.as_string())
        # server.quit()
        print('[INFO] email been sent')
    except smtplib.SMTPException as e:
        print('[ERROR] on send email %s' % e)

createHtml()
