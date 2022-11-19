import urllib3
import json
from lxml import etree

import env

http = urllib3.PoolManager()


def default_headers():
    return {'Cookie': env.get_cookies()}


def http_request(method: str, url: str, headers: dict, body=None):
    res = http.request(method=method, url=url, headers=headers, body=body)
    return res.data.decode('UTF-8')


def http_json_request(method: str, url: str, body=''):
    headers_temp = default_headers().copy()
    headers_temp['Content-Type'] = 'application/json'
    return http_request(method, url, headers=headers_temp, body=body)


def get_task_list():
    body = json.dumps(env.get_query_params())
    return http_json_request('POST', 'https://ehall.scut.edu.cn/fp/fp/taskcenter/getYBSXList', body)


def get_form_url(task_id: str):
    body = json.dumps({"task_id": task_id, "pr": "done"})
    return http_json_request('POST', 'https://ehall.scut.edu.cn/fp/fp/taskcenter/getForm', body)


def get_task(url: str):
    url = 'https://ehall.scut.edu.cn/fp' + url
    response = http_request('GET', url, default_headers())
    html = etree.HTML(str(response).encode('UTF-8'))
    return html.xpath("//script[@id='dcstr']/text()")[0]
