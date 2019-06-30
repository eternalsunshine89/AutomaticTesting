# coding=utf-8
import os
import time
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageChops


class Picture(object):
    """截图以及图片处理"""
    def compare_images(self, path_one, path_two, path_diff):
        """对比两张截图并返回两张截图中不同的区域以便观察"""
        image_one = Image.open(path_one)
        image_two = Image.open(path_two)
        try:
            diff = ImageChops.difference(image_one, image_two)
            if diff.getbbox() is None:
                print("We are the same!")
            else:
                diff.save(path_diff)
        except ValueError as e:
            print(e, "错误，图片位深度可能与要求不符！")


class Document(object):
    def __init__(self, path):
        self.path = path

    # 返回指定目录下按改动时间排序最新文件(不作用于文件夹)
    def get_latest_file(self, postfix='.apk'):
        # 列出目标目录下所有文件和文件夹并将其保存到列表
        lists = os.listdir(self.path)
        # 将所有文件按其最后修改时间排序
        lists.sort(key=lambda x: os.path.getmtime(self.path + "\\" + x))
        # 获取最新的文件保存到latest
        for i in list(range(1, len(lists) + 1)):
            latest = os.path.join(self.path, lists[-i])
            if os.path.isdir(latest):
                continue
            else:
                if postfix in latest:
                    os.rename(latest, latest.replace(' ', ''))
                    time.sleep(1)
                    return latest
                else:
                    print('没有后缀名为%s的文件' % postfix)


class Compression(object):

    """压缩文件和文件夹"""
    def compress_dir(self, new_file_path, dir_path):
        # 压缩后文件存放路径
        new_file = new_file_path + '\\' + time.strftime('%Y%m%d%H%M%S') + '.zip'
        z = ZipFile(new_file, 'w', ZIP_DEFLATED)
        for root, dirs, files in os.walk(dir_path):
            # 去掉父级目录，只压缩指定文件目录的文件夹及内部文件
            fpath = root.replace(dir_path, '')
            fpath = fpath and fpath + os.sep or ''
            for file in files:
                z.write(os.path.join(root, file), fpath + file)
        z.close()


if __name__ == '__main__':
    a = Document(os.path.abspath(os.path.dirname(__file__)))
    a.get_latest_file()
