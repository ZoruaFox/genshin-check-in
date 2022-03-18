import os
import time
import json
import random
import hashlib
import requests # pip install requests

def get_ds():
    salt = 'h8w582wxwgqvahcdkpvdhbh2w9casgfl'
    timestamp = str(int(time.time()))
    random_string_list = '0123456789abcdefghijklmnopqrstuvwxyz'
    random_string = ''.join(random.sample(random_string_list, 6))
    ds_string = 'salt=' + salt + '&t=' + timestamp + '&r=' + random_string
    ds_md5 = hashlib.md5(ds_string.encode(encoding='UTF-8')).hexdigest()
    ds = timestamp + ',' + random_string + ',' + ds_md5
    return ds

def get_game_info(cookies):
    req = requests.get("https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz=hk4e_cn", cookies=cookies)
    result = json.loads(req.text)
    return result

def cookie_str2dict(cookie_string):
    cookie = cookie_string.replace(" ","").split(";")
    cookies = {}
    for i in cookie:
        cookies[i.split("=")[0]] = i.split("=")[1]
    return cookies

def bbs_sign_reward(cookies, ds, game_info):
    url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign"
    headers = {
        'DS': ds,
        'x-rpc-app_version': '2.3.0',
        'x-rpc-client_type': '5',
        "x-rpc-device_id": "bd7f912e-908c-3692-a520-e70206823495"
    }
    post_data = {
        "act_id":"e202009291139501",
        "region":game_info['data']['list'][0]['region'],
        "uid":game_info['data']['list'][0]['game_uid']
    }
    req = requests.post(url=url, data = json.dumps(post_data), headers=headers, cookies=cookies)
    result = json.loads(req.text)
    return result
    
def main_handler(event, context):
    cookie_string = os.environ.get('cookie_string')
    if(cookie_string == None or cookie_string == ""):
        print("环境变量错误或为空！")
        exit()
    cookies = cookie_str2dict(cookie_string)
    game_info = get_game_info(cookies)
    if(game_info['retcode'] != 0):
        print("签到失败！")
        print(game_info)
    else:
        print("执行成功！")
        print(game_info)
        print(bbs_sign_reward(cookies, get_ds(), game_info))