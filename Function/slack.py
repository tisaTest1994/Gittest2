import slackweb
from time import sleep
import csv
from Function.api_common_function import *


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
def slack_report(type):
    sleep(2)
    slackUrl = get_json()['slackUrl']
    slack = slackweb.Slack(url=slackUrl)
    result = get_test_result()
    id = get_job_id()
    if type == 'api':
        title = "Api Test Report"
    elif type == 'kyc':
        title = "Compliance Service Test Report"
    elif type == 'ui':
        title = "Ui Test Report"
    else:
        title = "Test Report"
    attachment = [
        {
            "title": title,
            "text": "ToTal Test Cases number: _{}_,"
                    "\n Pass Test Cases number: _{}_,"
                    "\n Failed Test Cases number: _{}_,"
                    "\n Broken Test Cases number: _{}_,"
                    "\n Detailed report address is https://cabital.gitlab.io/-/Test/-/jobs/{"
                    "}/artifacts/Reports/html/index.html".format(result["Total"], result["PASSED"], result["FAILED"], result['BROKEN'],id),
            "ts": time.time()
        }
    ]
    slack.notify(attachments=attachment)


# 获得build id
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

