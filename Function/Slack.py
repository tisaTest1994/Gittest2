import slackweb
import time
import csv
import requests
from Function.CommonFunction import *


# 获取测试结果
def get_test_result():
    # 读report
    with open('Reports/html/data/behaviors.csv')as f:
        f_csv = csv.reader(f)
        result = {}
        for row in f_csv:
            result['PASSED'] = row[5]
            result['FAILED'] = row[3]
            result['BROKEN'] = row[4]
            result['SKIPPED'] = row[6]
        result['Total'] = int(result['PASSED']) + int(result['FAILED']) + int(result['BROKEN']) + int(result['SKIPPED'])
    return result


# 和slack交互
def slack_report():
    slackUrl = get_json()['slackTestUrl']
    slack = slackweb.Slack(url=slackUrl)
    result = get_test_result()
    id = get_job_id()
    attachment = [
        {
            "title": "Api Test Report",
            "text": "ToTal Test Cases number: _{}_,"
                    "\n Pass Test Cases number: _{}_,"
                    "\n Failed Test Cases number: _{}_,"
                    "\n Broken Test Cases number: _{}_,"
                    "\n Skipped Test Cases number: _{}_"
                    "\n Detailed report address is https://cabital.gitlab.io/-/Test/-/jobs/{"
                    "}/artifacts/Reports/html/index.html".format(result["Total"], result["PASSED"], result["FAILED"],
                                                                 result["BROKEN"], result["SKIPPED"], id),
            "pretext": "_Api Test Report_",
            "ts": time.time()
        }
    ]
    slack.notify(attachments=attachment)


def get_job_id():
    headers = {
        "PRIVATE-TOKEN": get_json()['PRIVATE-TOKEN']
    }
    r = requests.request('GET', url='https://gitlab.com/api/v4/projects/25201898/jobs', headers=headers)
    job_id = {}
    for i in r.json():
        timestamp = int(time.mktime(time.strptime(str(i['created_at']).split('.')[0], "%Y-%m-%dT%H:%M:%S")))
        job_id[timestamp] = i['id']
    return job_id[max(job_id.keys())]