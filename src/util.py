import os
import json
import sys
import base64
import http.client

ServerUrl = os.environ.get('FLOWCI_SERVER_URL')
FlowName = os.environ.get("FLOWCI_FLOW_NAME")

JobBuildNumber = os.environ.get("FLOWCI_JOB_BUILD_NUM")
JobStatus = os.environ.get("FLOWCI_JOB_STATUS")
JobTrigger = os.environ.get("FLOWCI_JOB_TRIGGER")
JobTriggerBy = os.environ.get("FLOWCI_JOB_TRIGGER_BY")
JobStartAt = os.environ.get("FLOWCI_JOB_START_AT")
JobFinishAt = os.environ.get("FLOWCI_JOB_FINISH_AT")

AgentToken = os.environ.get('FLOWCI_AGENT_TOKEN')
AgentJobDir = os.environ.get('FLOWCI_AGENT_JOB_DIR')

HttpHeaders = {
    "Content-type": "application/json",
    "AGENT-TOKEN": AgentToken
}

class Job:
    def __init__(self):
        self.flowName = FlowName
        self.number = JobBuildNumber
        self.status = JobStatus
        self.trigger = JobTrigger
        self.triggerBy = JobTriggerBy
        self.startAt = JobStartAt
        self.finishAt = JobFinishAt

def getVar(name, required=True):
    val = os.environ.get(name)
    if required and val is None:
        sys.exit("{} is missing".format(name))
    return val


def createHttpConn(url):
    if url.startswith("http://"):
        return http.client.HTTPConnection(url.lstrip("http://"))

    return http.client.HTTPConnection(url.lstrip("https://"))


def fetchCredential(name):
    try:
        path = "/api/credential/{}".format(name)
        conn = createHttpConn(ServerUrl)
        conn.request(method="GET", url=path, headers=HttpHeaders)

        response = conn.getresponse()
        if response.status is 200:
            body = response.read()
            return json.loads(body)

        return None
    except Exception as e:
        print(e)
        return None

def fetchFlowUsers():
    try:
        path = "/api/flow/{}/users".format(FlowName)
        conn = createHttpConn(ServerUrl)
        conn.request(method="GET", url=path, headers=HttpHeaders)

        if response.status is 200:
            body = response.read()
            return json.loads(body)

        return None
    except Exception as e:
        print(e)
        return None

def fetchJobSteps():
    try:
        path = "/api/flow/{}/job/{}/steps".format(FlowName, JobBuildNumber)
        conn = createHttpConn(ServerUrl)
        conn.request(method="GET", url=path, headers=HttpHeaders)

        if response.status is 200:
            body = response.read()
            return json.loads(body)

        return None
    except Exception as e:
        print(e)
        return None
