import requests


def get_token():
    url = "http://stest.eyee.com/api/User/Login"
    data = {
        "deviceid": "h5",
        "os": "android",
        "param": "%7B%22mobile%22%3A%22%2B86-18217714191%22%2C%22password%22%3A%22670b14728ad9902aecba32e22fa4f6bd%22%7D",
        "sign": "5f4a002c5691a995533ed1a03ac809d1",
        "version": "3.3.4"
    }
    res = requests.post(url=url, json=data)
    token = res.json().get('data')['token']
    # print(token)
    return token


def req(method, url, json=""):
    headers = {
        'Content-Type': "application/json",
        'Authorization': get_token()
    }
    if method == "get":
        res = requests.get(url=url, params=json, headers=headers)
        # print(res.json())
        return res.json()
    elif method == "post":
        res = requests.post(url=url, json=json, headers=headers)
        # print(res.json())
        return res.json()
    else:
        print('不支持的请求方法')


if __name__ == '__main__':
    get_token()
