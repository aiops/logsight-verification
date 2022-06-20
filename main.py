import argparse
import copy
import time

import logsight.exceptions
from logsight.compare import LogsightCompare
from logsight.authentication import LogsightAuthentication

from utils import create_verification_report, create_github_issue

SECONDS_SLEEP = 10

# Instantiate the parser
parser = argparse.ArgumentParser(description='Logsight Init')
parser.add_argument('--username', type=str, help='URL of logsight')
parser.add_argument('--password', type=str, help='Basic auth username')
parser.add_argument('--repository', type=str, help='Repository name')
parser.add_argument('--baseline_tag', type=str, help='Baseline tag')
parser.add_argument('--candidate_tag', type=str, help='Compare tag')
parser.add_argument('--risk_threshold', type=int, help='Risk threshold (between 0 and 100)')
args = parser.parse_args()
EMAIL = args.username
PASSWORD = args.password
BASELINE_TAGS = {"version": args.baseline_tag, "repository": args.repository}
CANDIDATE_TAGS = {"version": args.candidate_tag, "repository": args.repository}
RISK_THRESHOLD = args.risk_threshold
auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)
time.sleep(SECONDS_SLEEP)
compare = LogsightCompare(auth.token)
flag = 0
while True:
    try:
        r = compare.compare(baseline_tags=BASELINE_TAGS,
                            candidate_tags=CANDIDATE_TAGS)
        break
    except logsight.exceptions.Conflict as conflict:
        time.sleep(SECONDS_SLEEP)
        print("Conflict, sleeping..")
    except Exception as e:
        time.sleep(SECONDS_SLEEP)
        if flag == 0:
            BASELINE_TAGS = copy.deepcopy(CANDIDATE_TAGS)
            flag += 1
        elif flag == 1:
            CANDIDATE_TAGS = copy.deepcopy(BASELINE_TAGS)
            flag += 1
        else:
            print("Both tags do not exist! We cant perform verification!")
            exit(0)

report = create_verification_report(vresults=r,
                                    baseline_tags=BASELINE_TAGS,
                                    candidate_tags=CANDIDATE_TAGS)
print(report)

if r['risk'] >= RISK_THRESHOLD:
    create_github_issue(report, r)
    exit(1)
else:
    exit(0)
