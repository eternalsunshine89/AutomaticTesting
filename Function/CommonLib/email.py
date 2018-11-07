# coding: utf-8
import os
import smtplib
import sys
import time
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from selenium import webdriver


class SendEmail(object):
    def __init__(self, username, password, state='debug', file_path=None, html_path=None):
        self.username = username
        self.password = password
        self.state = state
        self.file_path = file_path
        self.html_path = html_path

    def get_latest_file(self, get_path=None):
        """获取指定目录下按改动时间排序最新文件"""
        # 列出目录下所有文件和文件夹保存到lists
        lists = os.listdir(get_path)
        # 按时间排序
        lists.sort(key=lambda x: os.path.getmtime(get_path + "\\" + x))
        # 获取最新的文件保存到latest
        latest = os.path.join(get_path, lists[-1])
        return latest

    def screen_shot(self):
        # 使用selenium的webdriver协议通过chrome驱动打开网页进行截图
        try:
            driver = webdriver.Chrome()
        except Exception:
            print("未找到chromedriver")
            return sys.exit()
        driver.get(self.get_latest_file(self.html_path))
        time.sleep(1)
        driver.fullscreen_window()
        time.sleep(1)
        driver.save_screenshot(self.html_path + '\\%s.png' % time.strftime('%Y%m%d%H%M%S'))
        driver.quit()

    def create_email(self):
        """创建并发送邮件，测试报告通过邮件附件的形式发出"""
        username = self.username
        password = self.password
        smtpserver = 'smtp.ym.163.com'
        sender = username
        receiver = ''
        if self.state == 'normal':
            receiver = 'eternalsunshine89@163.com'
        elif self.state == 'debug':
            receiver = 'eternalsunshine89@163.com'
        # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
        subject = '测试报告'
        subject = Header(subject, 'utf-8').encode()

        # 构造邮件对象MIMEMultipart对象
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        # 插入图片
        self.screen_shot()
        with open(self.get_latest_file(self.html_path), 'rb') as sendimagefile:
            image = MIMEImage(sendimagefile.read())
        image.add_header('Content-ID', self.html_path)
        msg.attach(image)

        # 构造文字内容
        mail_img = """
        <p><img src='cid:%s'></p>
        """ % self.html_path
        text = MIMEText(mail_img, 'html', 'utf-8')
        msg.attach(text)

        # 构造附件
        if self.file_path is not None:
            with open(self.get_latest_file(self.file_path), 'rb') as file:
                sendfile = file.read()
            text_att = MIMEText(sendfile, 'base64', 'utf-8')
            text_att["Content-Type"] = 'application/octet-stream'
            # 以下附件可以重命名成aaa.txt
            text_att["Content-Disposition"] = 'attachment; filename="test_report.zip"'
            msg.attach(text_att)

        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, 25)
        # 我们用set_debuglevel(path)就可以打印出和SMTP服务器交互的所有信息。
        # smtp.set_debuglevel(path)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver.split(','), msg.as_string())
        smtp.quit()


if __name__ == '__main__':
    a = SendEmail('eternalsunshine89@163.com', 'wzc6851498',
                  html_path=r'C:\Users\etern\MyProject\AutoTest\FunctionTest\testReport')
    a.screen_shot()
    a.create_email()
