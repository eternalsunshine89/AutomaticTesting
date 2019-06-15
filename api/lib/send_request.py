import requests


def req(method, url, data='', headers=''):
    if method == 'get':
        res = requests.get(url=url, params=data, headers=headers)
        return res.json()
    elif method == 'post':
        res = requests.post(url=url, json=data, headers=headers)
        return res.json()
    else:
        print('不支持的请求方法')


if __name__ == '__main__':
    req('get', 'https://www.baidu.com')