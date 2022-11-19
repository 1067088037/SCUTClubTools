default_pageSize = 500
default_start_date = "2022-07-01 00:00:00"

cookies = ''

query_params = {
    "service_name": "申请加入学生社团服务",
    "job_number": "",
    "unit_name": "",
    "procinst_id": "",
    "summary": "",
    "result": "",
    "currentNode": "",
    "blstart_date": "",
    "blend_date": "",
    "start_date": default_start_date,  # 开始日期
    "end_date": "",
    "status": "2",
    "pageNum": "1",
    "pageSize": ""
}


def get_cookies():
    return cookies.strip()


def get_query_params():
    return dict(query_params)
