import datetime
import json
import re
from json import JSONDecodeError

import env
import network


def init():
    if env.cookies is None or env.cookies == '':
        print('请输入从办事大厅获取的Cookies：', end='')
        env.cookies = str(input())

    if env.query_params['pageSize'] == '':
        print(f'请输入检索人数的上限（不填默认{env.default_pageSize}）：', end='')
        page_size = input()
        if page_size != '':
            env.query_params['pageSize'] = int(page_size)
        else:
            env.query_params['pageSize'] = env.default_pageSize

    if env.query_params['start_date'] == '':
        print(f'请输入检索的起始时间（不填默认{env.default_start_date}）：', end='')
        start_date = input()
        if start_date != '':
            env.query_params['start_date'] = start_date
        else:
            env.query_params['start_date'] = env.default_start_date

    try:
        task_src = dict(json.loads(network.get_task_list()))
        time = datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
        return open(f'./{time}.csv', mode='w+'), task_src
    except JSONDecodeError:
        print("Cookies不合法或已经过期")
        return None, None


def to_csv_row(task_info: dict):
    feedback_id = task_info['fk_id']  # 反馈ID
    applicant = task_info['SQR']  # 申请人
    student_id = task_info['XH']  # 学号
    school = task_info['XY']  # 学院
    major = task_info['ZY']  # 专业
    grade = task_info['NJ']  # 年级
    phone_number = task_info['LXDH']  # 联系电话
    politics_status = task_info['ZZMM']  # 政治面貌
    club_name = task_info['ST_TEXT']  # 申请加入社团
    return f"{feedback_id},{applicant},{student_id},{school}," \
           f"{major},{grade},{phone_number},{politics_status},{club_name}"


def main(csv_file: open, task_src: dict):
    task_list = list(task_src['list'])
    task_size = len(task_list)
    print(f"已探测到的数量 {task_size}")
    counter = 0
    for task in task_list:
        task_id = task['task_id']
        form_url = str(network.get_form_url(task_id))
        task_form = str(network.get_task(form_url))
        pattern = re.compile(r'"primary": \[(.*?)]')
        task_json_text = pattern.findall(task_form)[1]
        task_dict = json.loads(task_json_text)
        csv_row = to_csv_row(task_dict)
        csv_file.write(csv_row + "\n")
        counter += 1
        print(f"{counter % 10}", end=' ')
        if counter % 10 == 0:
            print(f"[{counter}]")
    csv_file.close()
    print(f"已读取{counter}份数据，内容被写入在{csv_file.name}")


if __name__ == '__main__':
    csv, res = init()
    if res is not None:
        main(csv, res)
    else:
        exit(-1)
