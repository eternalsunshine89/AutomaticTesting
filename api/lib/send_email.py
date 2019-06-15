import smtplib  # 用于建立smtp连接
from email.mime.text import MIMEText  # 邮件需要专门的MIME格式
from email.mime.multipart import MIMEMultipart  # 混合MIME格式，支持上传附件
from email.header import Header  # 支持中文邮件主题
from config import *


def send_email(report, count_num, pass_num, fail_num, error_num, rate):
    # 实例化支持上传附件的MIME格式邮件类
    msg = MIMEMultipart()

    # 添加邮件正文内容
    content = """
                <h3 text="#000000">接口自动化测试结果如下，报告详情见附件（注：请下载后使用chrome浏览器打开）</h3><br>
                <table border="1" cellspacing="0" cellpadding="3" width="1000" align="left">
                <tr bgcolor="#6495ED" align="center">
                    <th>用例总数</th>
                    <th>通过用例数</th>
                    <th>失败用例数</th>
                    <th>错误用例数</th>
                    <th>通过率</th>
                </tr>
                <tr align="center">
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}%</td>
                </tr>
            """.format(count_num, pass_num, fail_num, error_num, rate)
    mail_content = MIMEText(content, 'html', 'utf-8')
    msg.attach(mail_content)

    # 组装Email的头部信息
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = Header(subject, 'utf-8')  # 用Header支持中文邮件主题

    # 添加邮件的附件
    with open(report, 'rb') as f_att:
        mail_att = MIMEText(f_att.read(), 'html', 'utf-8')
    mail_att["Content-Type"] = 'application/octet-stream'
    mail_att.add_header("Content-Disposition", "attachment", filename="接口测试报告.html")
    msg.attach(mail_att)

    # 发送邮件
    try:
        smtp = smtplib.SMTP_SSL(smtp_server)  # smtp服务器地址 使用SSL模式
        smtp.login(smtp_user, smtp_password)  # 使用用户名和SMTP授权码登录邮箱
        smtp.sendmail(sender, receiver, msg.as_string())
        logging.info("邮件发送完成！")
    except Exception as e:
        logging.error(e)
    finally:
        smtp.quit()
