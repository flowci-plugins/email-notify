# email-report

## Description

It will send job report via email

## Inputs

- `FLOWCI_EMAIL_SMTP` (required): smtp server, ex: 'smtp.163.com' 
- `FLOWCI_EMAIL_SSL`: enable ssl for smtp, default is `true`
- `FLOWCI_EMAIL_FROM` (required): from email address 
- `FLOWCI_EMAIL_TO` (required): receiver's email address, ex: `xx@163.com,xxx@qq.com`. The value `FLOW_USERS` to send email to all flow users
- `FLOWCI_EMAIL_CREDENTIAL`: 'AUTH' credential name for smtp username and password  

## How to use it

```yml
#  Example that togeher with git clone plugin

envs:
  FLOWCI_GIT_URL: "https://github.com/FlowCI/spring-petclinic-sample.git"
  FLOWCI_GIT_BRANCH: "master"
  FLOWCI_GIT_REPO: "spring-petclinic"

steps:
  - name: clone
    plugin: 'gitclone'
    allow_failure: false

  - name: email result
    tail: true
    envs:
        FLOWCI_EMAIL_SMTP: "smtp.163.com"
        FLOWCI_EMAIL_SSL: true
        FLOWCI_EMAIL_FROM: "xxxx@163.com"
        FLOWCI_EMAIL_TO: "xxx@qq.com,xxx@gmail.com"
        FLOWCI_EMAIL_CREDENTIAL: "your auth credential name"
    plugin: email-report 
```