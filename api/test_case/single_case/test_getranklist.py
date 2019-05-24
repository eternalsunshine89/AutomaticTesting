"""牛市首页四个排行榜接口"""
import unittest
from lib.send_request import req

test_data = {
    'url': 'http://stest.eyee.com/capi/exchange/rank/open/getranklist',
    'method': 'post',
    'data': {
        'type': 1,
        'page': 1,
        'size': 10
    },
    'except_result': 5
}


class GetRankList(unittest.TestCase):
    def tearDown(self):
        global test_data
        test_data['data']['type'] += 1

    def test_hot_list(self):
        """type为1，page和size默认"""
        res = req(test_data['method'], url=test_data['url'], json=test_data['data'])
        self.assertEqual(res['code'], 1511200)
        self.assertGreaterEqual(len((res['data']['list'])), test_data['except_result'], msg='返回的数据小于5条')

    def test_increase_list(self):
        """type为2，page和size默认"""
        res = req(test_data['method'], url=test_data['url'], json=test_data['data'])
        self.assertEqual(res['code'], 1511200)
        self.assertGreaterEqual(len((res['data']['list'])), test_data['except_result'], msg='返回的数据小于5条')

    def test_decrease_list(self):
        """type为3，page和size默认"""
        res = req(test_data['method'], url=test_data['url'], json=test_data['data'])
        self.assertEqual(res['code'], 1511200)
        self.assertGreaterEqual(len((res['data']['list'])), 11, msg='返回的数据小于5条')

    def test_new_list(self):
        """type为4，page和size默认"""
        res = req(test_data['method'], url=test_data['url'], json=test_data['data'])
        self.assertEqual(res['code'], 1511200)
        self.assertGreaterEqual(len((res['data']['list'])), 11, msg='返回的数据小于5条')
