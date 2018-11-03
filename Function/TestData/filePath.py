import os


pkg_name = 'com.excelliance.dualaid'
launch_activity = 'com.excelliance.kxqp.ui.HelloActivity'


# 路径管理
class Path(object):
    BASE = os.path.abspath(os.path.dirname(__file__))

    path = {
        'apk_path': r'Z:\daily_review_SKZS',  # 应用安装目录
        'log_path': os.path.join(os.path.dirname(BASE), 'testLog'),
        'anr_log_path': os.path.join(os.path.dirname(BASE), r'testLog\anrLog'),
        'crash_log_path': os.path.join(os.path.dirname(BASE), r'testLog\crashLog'),
        'image_path': os.path.join(os.path.dirname(BASE), 'screenshot'),
        'report_path': os.path.join(os.path.dirname(BASE), 'testReport'),
        'data_save_path': r'Z:\daily_review_SKZS\daily_review_files\result',
    }


if __name__ == '__main__':
    print(Path.path['log_path'])
    print(Path.path['image_path'])
    print(Path.path['report_path'])
    print(Path.path['anr_log_path'])
    print(Path.path['crash_log_path'])