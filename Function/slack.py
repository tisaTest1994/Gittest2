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
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    result = get_test_result()
    id = get_job_id(type)
    if type == 'api':
        title = "Api Test Report"
    elif type == 'kyc':
        title = "Compliance Service Test Report"
    elif type == 'ui':
        title = "Ui Test Report"
    elif type == 'cabinet':
        title = "Cabinet Test Report"
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
def get_job_id(type):
    headers = {
        "PRIVATE-TOKEN": get_json()['PRIVATE-TOKEN']
    }
    r = requests.request('GET', url='https://gitlab.com/api/v4/projects/25201898/jobs', headers=headers)
    id_list = []
    for i in r.json():
        if type == 'api':
            if i['name'] == 'ApiTest':
                id_list.append(i['id'])
        elif type == 'kyc':
            if i['name'] == 'KycTest':
                id_list.append(i['id'])
        elif type == 'ui':
            if i['name'] == 'UiTest':
                id_list.append(i['id'])
        elif type == 'cabinet':
            if i['name'] == 'CabinetTest':
                id_list.append(i['id'])
    return id_list[0]

