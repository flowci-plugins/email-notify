# email-notify

## Description

It will send job report via email

## Inputs

- `FLOWCI_SMTP_CONFIG` (required): smtp config name that created from 'settings' -> 'config'
- `FLOWCI_EMAIL_FROM` (required): from email address
- `FLOWCI_EMAIL_TO`: receiver's email address, ex: `xx@163.com,xxx@qq.com`. The value `FLOW_USERS` to send email to all flow users

## How to use it

```yml
#  Example: send email by sendgrid that created by default

envs:
  FLOWCI_GIT_URL: "https://github.com/FlowCI/spring-petclinic-sample.git"
  FLOWCI_GIT_BRANCH: "master"

notifications:
  - plugin: 'email-notify'
    envs:
      FLOWCI_SMTP_CONFIG: "sendgrid-demo"
      FLOWCI_EMAIL_FROM: "flow.ci.test@gmail.com"

steps:
  - name: clone
    plugin: 'gitclone'
    allow_failure: false
```
