import hashlib
import random
import requests
import json
import time
from urllib.parse import urlencode

# 接口地址
url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
# 请求头
headers = {
    'Host': 'fanyi.youdao.com',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://fanyi.youdao.com',
    'Referer': 'http://fanyi.youdao.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
    'Cookie':'OUTFOX_SEARCH_USER_ID_NCOO=960614636.8457044; OUTFOX_SEARCH_USER_ID="1404351459@10.169.0.82"; _ga=GA1.2.1097949216.1585277385; UM_distinctid=17212d6d7891ba-0c1c42cdc246ea-c373667-1fa400-17212d6d78aac6; JSESSIONID=aaaQQoD-N9zmc4uBTt8kx; ___rl__test__cookies=1592301402666'
}

def get_md5(s):
    '''
    生成MD5
    :param s: 原始字符串
    :return: MD5加密串
    '''
    hash = hashlib.md5()
    hash.update(s.encode('utf-8'))
    return hash.hexdigest()

def get_salt(time_stamp):
    '''
    生成salt
    :param time_stamp: 时间戳
    :return:
    '''
    rand_int = int(random.random() * 10) # random.randint(0, 9)也可以
    salt = str(time_stamp) + str(rand_int)
    return salt

def get_sign(keyword, salt):
    '''
    获取sign参数
    :param keyword: 关键词
    :param salt: salt
    :return:
    '''
    source_str = "fanyideskweb" + keyword + salt + "Tbh5E8=q6U3EXe+&L[4c@"
    result = get_md5(source_str)
    return result

def get_param_data(keyword):
    '''
    构造请求参数
    :param keyword: 关键词
    :return:
    '''
    ts = int(time.time() * 1000)
    salt = get_salt(ts)
    sign = get_sign(keyword, salt)
    data = {
        'i': keyword,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'ts': str(ts),
        'bv': 'd17d9dd026a611df0315b4863363408c',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION',
    }

    return urlencode(data)

def translate(keyword):
    '''
    请求翻译接口, 获取翻译结果
    :param keyword: 关键词
    :return:
    '''
    param_data = get_param_data(keyword)
    try:
        resp = requests.post(url, headers=headers, data=param_data, verify=False)
        data = json.loads(resp.text).get('translateResult')[0][0]
        result = data.get('tgt')
        return result
    except:
        return '无结果'


if __name__ == '__main__':
    while True:
        keyword = input('请输入要翻译的单词:')
        result = translate(keyword)
        print(f'结果:{result}\n')