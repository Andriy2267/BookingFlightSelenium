# captcha_solver.py

import requests
import time

API_KEY = "31ca8432ab089060215b8fe6030f84ee"

def solve_funcaptcha(site_key, page_url):
    create_task_url = "http://2captcha.com/in.php"
    payload = {
        "key": API_KEY,
        "method": "funcaptcha",
        "publickey": site_key,
        "pageurl": page_url,
        "json": 1
    }

    response = requests.post(create_task_url, data=payload)
    result = response.json()
    if result["status"] != 1:
        raise Exception("2Captcha error: " + result["request"])

    captcha_id = result["request"]
    get_result_url = "http://2captcha.com/res.php"

    for _ in range(20):
        time.sleep(5)
        r = requests.get(get_result_url, params={
            "key": API_KEY,
            "action": "get",
            "id": captcha_id,
            "json": 1
        })
        result = r.json()
        if result["status"] == 1:
            return result["request"]
        elif result["request"] != "CAPCHA_NOT_READY":
            raise Exception("2Captcha error: " + result["request"])

    raise Exception("2Captcha timeout: no result")
