import json
import unittest
from ddt import ddt, data, unpack
from config import test_data_file, MODAL, ENV
from lib.case_log import log_case_info, logging
from lib.read_excel import excel_to_list, get_test_data
from lib.send_request import req

test_data_list = excel_to_list(test_data_file, 'test_data', modal=MODAL)
print(test_data_list)
if ENV == 'test':
    HOST = ''
    BASE_URL = ''
elif ENV == 'release':
    HOST = ''
    BASE_URL = ''


@ddt
class RunCase(unittest.TestCase):
    def get_depend_params(self, depend, params):
        params_new = {}
        depend = json.loads(depend)
        for num, param in depend.items():
            d = get_test_data(test_data_list, serial=int(num))
            r = req(d['method'], d['url'], d['params'], d['headers'])
            params_new[param] = r[param]
        params_old = params
        for k, v in params_old.items():
            if not v:
                params_new.pop(k)
        params = dict(params_old, **params_new)
        return params

    def dict_compare(self, dict1, dict2):
        if len(dict1) != len(dict2):
            logging.error('实际结果中缺少字段')
            return False
        for i in dict1.keys():
            if i not in dict2.keys():
                logging.error('实际结果未包含该字段：{}'.format(i))
                return False
            elif type(dict1[i]) != type(dict2[i]):
                logging.error('实际结果中该字段值的类型与期望不符：{}'.format(i))
                return False
        return True

    @data(*test_data_list)
    @unpack
    def test_driver(self, **kwargs):
        serial, smoke, case_name, description, url, method, headers, params, depend, expect = kwargs.values()
        if depend is True:
            params = self.get_depend_params(depend, params)  # return a dict object
        res = req(method, url, params, headers)  # send request
        log_case_info(case_name, url, params, expect, res)  # create log file
        if self.dict_compare(expect, res):
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 2)


if __name__ == '__main__':
    unittest.main()
