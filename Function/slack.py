import slackweb
from time import sleep
import csv
from Function.api_common_function import *


# 获取测试结果
def get_test_result():
    # 读report
    path = os.path.split(os.path.realpath(__file__))[0] + '/../Reports/html/data/behaviors.csv'
    result = {
        'PASSED': 0,
        'FAILED': 0,
        'BROKEN': 0,
        'SKIPPED': 0
    }
    with open(path)as f:
        reader = csv.DictReader(f)
        column = [row for row in reader]
        for i in column:
            result['PASSED'] = result['PASSED'] + int(i['PASSED'])
            result['FAILED'] = result['FAILED'] + int(i['FAILED'])
            result['BROKEN'] = result['BROKEN'] + int(i['BROKEN'])
            result['SKIPPED'] = result['SKIPPED'] + int(i['SKIPPED'])
    result['Total'] = int(result['PASSED']) + int(result['FAILED']) + int(result['BROKEN']) + int(result['SKIPPED'])
    return result


# 和slack交互
def slack_report(type, env='test'):
    sleep(3)
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    result = get_test_result()
    id = get_job_id(type)
    if type == 'api':
        title = "Api Test Report"
    elif type == 'kyc':
        if env == 'test':
            title = "Compliance Service Test Report (test)"
        else:
            title = "Compliance Service Test Report (sanbox)"
    elif type == 'app':
        title = "App Test Report"
    elif type == 'cabinet':
        title = "Cabinet Test Report"
    elif type == 'connect':
        title = "Cabital Connect Test Report"
    elif type == 'web':
        title = "Web Test Report"
    elif type == 'accounting':
        title = "Accounting Test Report"
    elif type == 'infinni':
        title = "Infinni Games Test Report"
    else:
        title = "Test Report"
    attachment = [
        {
            "title": title,
            "text": "ToTal Test Cases number: _{}_,"
                    "\n Pass Test Cases number: _{}_,"
                    "\n Failed Test Cases number: _{}_,"
                    "\n Broken Test Cases number: _{}_,"
                    "\n Detailed report address is https://cabital.gitlab.io/-/team_qa/Test/-/jobs/{"
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
        elif type == 'app':
            if i['name'] == 'AppTest':
                id_list.append(i['id'])
        elif type == 'cabinet':
            if i['name'] == 'CabinetTest':
                id_list.append(i['id'])
        elif type == 'connect':
            if i['name'] == 'ConnectTest':
                id_list.append(i['id'])
        elif type == 'web':
            if i['name'] == 'WebTest':
                id_list.append(i['id'])
        elif type == 'accounting':
            if i['name'] == 'AccountingTest':
                id_list.append(i['id'])
        elif type == 'infinni':
            if i['name'] == 'Infinni Games Test':
                id_list.append(i['id'])
    return id_list[0]

