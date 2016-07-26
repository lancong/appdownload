# -*- coding: utf-8 -*-

'''

base tools class

'''

import os
import random
import time
import codecs
import urllib

import requests
import sys

from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.request import urlretrieve, Request


# open url and return beautifulsoup
def openUrl(url):
    session = requests.session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    req = session.get(url, headers=headers)
    req.encoding = "utf-8"
    return BeautifulSoup(req.text, "html.parser")


# write text to file (default mode 'w')
def writeText(data, fileParentPath, fileName, mode="w", newline=False):
    mkdirs(fileParentPath)

    nowFilePath = os.path.join(fileParentPath, fileName)
    writer = None
    try:
        writer = codecs.open(nowFilePath, mode, "utf-8")
        writer.write(data)
        if newline:
            writer.write("\n")
        writer.flush()
    except:
        print("write file to " + nowFilePath + " error")
    finally:
        if writer is not None:
            writer.close()
    return


def getfilelines(filepath):
    texts = codecs.open(filepath, "r", "utf-8")
    try:
        count = 0
        if os.path.exists(filepath) and os.path.isfile(filepath):
            for text in texts:
                count += 1
    finally:
        texts.close()
    return count


# create new dir
def mkdirs(path):
    path = path.strip()
    path = path.rstrip("/")
    if not os.path.exists(path):
        os.makedirs(path)


def readTextAll(filePath):
    if os.path.exists(filePath):
        file = open(filePath)
        lines = iter(file)
        if valid(lines):
            return lines


def readTextAll2(filePath):
    if os.path.exists(filePath):
        return open(filePath).readlines()


def readTextAll3(filePath):
    if os.path.exists(filePath):
        reader = codecs.open(filePath, "r", "utf-8")
        # reader.close()
        return reader


# read text from file
def readText(filePath):
    if os.path.exists(filePath) and os.path.isfile(filePath):
        return open(filePath).readline()
    else:
        return ""


def valid(obj):
    if obj != "" and obj is not None:
        return True
    return False


def validList(obj):
    if obj is not None and len(obj) > 0:
        return True
    return False


# download file
# def downLoadFile(downUrl, filePath, fileName, suffix=".apk"):
#     return True

# download file
def downLoadFile(downUrl, filePath, fileName, suffix=".apk"):
    mkdirs(filePath)
    try:
        path = os.path.join(filePath, fileName + suffix)
        # 下载方法
        # local_down, headers = urlretrieve(downUrl, path, schedule)
        local_down, headers = urlretrieve(downUrl, path)
        down = open(local_down)
        down.close()
        # print("\t\n")
        # urlretrieve(downUrl, path, schedule)
        return True
    except:
        # print(getTime_yyyymmddhhmmss() + " " + fileName + " 下载错误")
        return False


# download file2
def downLoadFile2(downUrl, filePath, fileName, suffix=".apk"):
    mkdirs(filePath)
    try:
        path = os.path.join(filePath, fileName + suffix)
        # 下载方法

        r = requests.get(downUrl)
        with open(path, "wb") as file:
            file.write(r.content)
        return True
    except:
        # print(getTime_yyyymmddhhmmss() + " " + fileName + " 下载错误")
        return False


# a:已经下载的数据大小; b:数据大小; c:远程文件大小;
def schedule(a, b, c):
    per = 100.0 * a * b / c
    if per > 100: per = 100
    print('{:.2f}%'.format(per))
    sys.stdout.flush()


def URLEncoder(obj):
    return quote(str(obj))


# 得到时间格式 20160202
def getTime_yyyymmdd():
    return time.strftime("%Y%m%d", time.localtime(time.time()))


# 得到时间格式 2016-02-02
def getTime_yyyymmdd2():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


# 得到时间格式 19:24:25
def getTime_hhmmss():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))


# 得到时间格式 2016-02-02 11:22:22
def getTime_yyyymmddhhmmss():
    return time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(time.time()))


# 得到时间格式 20160202112222
def getTime_yyyymmddhhmmss2():
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))


# 生成随机整形数字
def general_randint(min, max):
    return random.randint(min, max)


if __name__ == '__main__':

    filePath = "/Users/Lan/AndroidTemp/appList.txt"
    texts = readTextAll3(filePath)
    count = 0
    for text in texts:
        count += 1
        print(text)
    print(count)
    pass
