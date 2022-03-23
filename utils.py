import os
from github import Github


def create_verification_report(vresults, baseline_tag, candidate_tag):
    github_branch = os.environ['GITHUB_REF']
    github_actor = os.environ['GITHUB_ACTOR']
    github_workflow = os.environ['GITHUB_WORKFLOW']
    return f"""
<a href="https://logsight.ai/"><img src="https://logsight.ai/assets/img/logol.png" width="120"/></a>

# Report

[:bar_chart: Detailed online report]({vresults['link']})

## GitHub metadata

|  Name                  |    Value                          |
| ---------------------- | --------------------------------- |
| Github actor           | {github_actor}                    |
| Workflow               | {github_workflow}                 |
| Baseline tag / branch  | {baseline_tag} / {github_branch}  |
| Candidate tag / branch | {candidate_tag} / {github_branch} |

## Deployment risk
+ :zap: {vresults['risk']}%

## Log records statistics

|        Total Count          |            Baseline            |             Compare             |                 % Change                 |
| :-------------------------: | :----------------------------: | :-----------------------------: | :--------------------------------------: |
| {vresults['totalLogCount']} | {vresults['baselineLogCount']} | {vresults['candidateLogCount']} | {vresults['candidateChangePercentage']}% |

## State analysis

| Name       | Total | 🔴 Failed % | :green_circle: Report % |
| :---        |    :----:   |          ---: |          ---: |
| :arrow_right: Added states    |   {vresults['addedStatesTotalCount']}     | {vresults['addedStatesFaultPercentage']} |  {vresults['addedStatesReportPercentage']} |
|  :arrow_left: Deleted states   |   {vresults['deletedStatesTotalCount']} | {vresults['deletedStatesFaultPercentage']} |  {vresults['addedStatesReportPercentage']} |
| :arrow_right_hook: Recurring states |   {vresults['recurringStatesTotalCount']}  |  {vresults['recurringStatesFaultPercentage']} |  {vresults['recurringStatesReportPercentage']}| 
| :arrows_counterclockwise: Freq. change states    |    {vresults['frequencyChangeTotalCount']}  | :arrow_up: {vresults['frequencyChangeFaultPercentage']['increase']} :arrow_down: {vresults['frequencyChangeFaultPercentage']['decrease']} |  :arrow_up: {vresults['frequencyChangeReportPercentage']['increase']} :arrow_down: {vresults['frequencyChangeReportPercentage']['decrease']}  |

# Documentation

+ <a href="https://docs.logsight.ai/#/">Logsight documentation</a>
    """


def create_github_issue(verification_report):
    # extracting all the input from environments
    title = "Logsight Stage Verifier [" \
            "baseline: " + os.environ['INPUT_BASELINE_TAG'][:6] + " | " + \
            "candidate:" + os.environ['INPUT_CANDIDATE_TAG'][:6] + \
            "]"
    token = os.environ['INPUT_GITHUB_TOKEN']
    labels = ['log-verification']
    # assignees = os.environ['GITHUB_ACTOR']

    # GitHub expects labels and assignees as list
    # but we supplied as string in yaml as list are not supposed in .yaml format
    # if labels and labels != '':
    #     labels = labels.split(',')  # splitting by , to make a list
    # else:
    #     labels = []  # setting empty list if we get labels as '' or None

    # if assignees and assignees != '':
    #     assignees = assignees.split(',')  # splitting by , to make a list
    # else:
    #     assignees = []  # setting empty list if we get labels as '' or None

    g = Github(token)
    # GITHUB_REPOSITORY is the repo name in owner/name format in Github Workflow
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])

    repo.create_issue(
        title=title,
        body=verification_report,
        labels=labels
    )
