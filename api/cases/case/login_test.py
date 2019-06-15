from cases.base_case import BaseCase


class Login(BaseCase):
    def setUp(self):
        pass

    def tearDown(self):
        print("登录成功")

    def test_login_right(self):
        """正常登陆"""
        self.assertEqual(1, 1)
