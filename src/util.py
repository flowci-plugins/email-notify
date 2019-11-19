import os
import json
import sys
import base64
import http.client
from datetime import datetime

JobTriggerScheduler = "SCHEDULER"
JobTriggerApi = "API"
JobTriggerManual = "MANUAL"
JobTriggerPush = "PUSH"
JobTriggerPrOpen = "PR_OPENED"
JobTriggerPrMerged = "PR_MERGED"
JobTriggerTag = "TAG"

ServerUrl = os.environ.get('FLOWCI_SERVER_URL')
FlowName = os.environ.get("FLOWCI_FLOW_NAME")

JobBuildNumber = os.environ.get("FLOWCI_JOB_BUILD_NUM")
JobStatus = os.environ.get("FLOWCI_JOB_STATUS")
JobTrigger = os.environ.get("FLOWCI_JOB_TRIGGER")
JobTriggerBy = os.environ.get("FLOWCI_JOB_TRIGGER_BY")
JobStartAt = os.environ.get("FLOWCI_JOB_START_AT")
JobFinishAt = os.environ.get("FLOWCI_JOB_FINISH_AT")
JobSteps = os.environ.get("FLOWCI_JOB_STEPS")

AgentToken = os.environ.get('FLOWCI_AGENT_TOKEN')
AgentJobDir = os.environ.get('FLOWCI_AGENT_JOB_DIR')

GitEvent = os.environ.get('FLOWCI_GIT_EVENT')

GitCommitBranch = os.environ.get('FLOWCI_GIT_BRANCH')
GitCommitID = os.environ.get('FLOWCI_GIT_COMMIT_ID')
GitCommitMessage = os.environ.get('FLOWCI_GIT_COMMIT_MESSAGE')
GitCommitTime = os.environ.get('FLOWCI_GIT_COMMIT_TIME')
GitCommitURL = os.environ.get('FLOWCI_GIT_COMMIT_URL')

GitPrTitle = os.environ.get('FLOWCI_GIT_PR_TITLE')
GitPrMessage = os.environ.get('FLOWCI_GIT_PR_MESSAGE')
GitPrURL = os.environ.get('FLOWCI_GIT_PR_URL')
GitPrTime = os.environ.get('FLOWCI_GIT_PR_TIME')
GitPrNumber = os.environ.get('FLOWCI_GIT_PR_NUMBER')

GitPrHeadRepoName = os.environ.get('FLOWCI_GIT_PR_HEAD_REPO_NAME')
GitPrHeadRepoBranch = os.environ.get('FLOWCI_GIT_PR_HEAD_REPO_BRANCH')
GitPrHeadRepoCommit = os.environ.get('FLOWCI_GIT_PR_HEAD_REPO_COMMIT')

GitPrBaseRepoName = os.environ.get('FLOWCI_GIT_PR_BASE_REPO_NAME')
GitPrBaseRepoBranch = os.environ.get('FLOWCI_GIT_PR_BASE_REPO_BRANCH')
GitPrBaseRepoCommit = os.environ.get('FLOWCI_GIT_PR_BASE_REPO_COMMIT')

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
        self.duration = "-"
        self.steps = []

        self.gitCommit = GitCommit()
        self.gitPr = GitPr()

        if JobStartAt != None and JobFinishAt != None:
            start = datetime.strptime(JobStartAt, "%Y-%m-%d %H:%M:%S.%f")
            finish = datetime.strptime(JobFinishAt, "%Y-%m-%d %H:%M:%S.%f")
            self.duration = abs(finish - start).microseconds

        if JobSteps != None:
            items = JobSteps.split(";")
            for item in items:
                if item != '':
                    self.steps.append(Step(item))

class Step:
    def __init__(self, strItem):
        pair = strItem.split("=")
        self.name = pair[0]
        self.status = pair[1]

class GitCommit:
    def __init__(self):
        self.id = GitCommitID
        self.branch = GitCommitBranch
        self.message = GitCommitMessage
        self.time = GitCommitTime
        self.url = GitCommitURL

class GitPr:
    def __init__(self):
        self.title = GitPrTitle
        self.message = GitPrMessage
        self.url = GitPrURL
        self.number = GitPrNumber
        self.time = GitPrTime
        self.head = GitPrHeadRepo()
        self.base = GitPrBaseRepo()

class GitPrHeadRepo:
    def __init__(self):
        self.name = GitPrHeadRepoName
        self.branch = GitPrHeadRepoBranch
        self.commit = GitPrHeadRepoCommit

class GitPrBaseRepo:
    def __init__(self):
        self.name = GitPrBaseRepoName
        self.branch = GitPrBaseRepoBranch
        self.commit = GitPrBaseRepoCommit

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
        response = conn.getresponse()

        if response.status is 200:
            body = response.read()
            return json.loads(body)

        return None
    except Exception as e:
        print(e)
        return None
