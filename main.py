# -*- coding: utf-8 -*-

'''

下载程序主方法

'''
import codecs
import os
from time import sleep

import config
import baseutil
from appstore import AppStore_wandoujia

if __name__ == '__main__':

    filepath = config.APPLIST

    if os.path.exists(filepath) and os.path.isfile(filepath):
        texts = codecs.open(config.APPLIST, "r", "utf-8")
        appStore = AppStore_wandoujia()
        appStore.setSaveFilePlace()

        sumnum = baseutil.getfilelines(filepath)

        count = 0
        for text in texts:
            try:
                count += 1
                print("开始下载: " + text + " [" + str(count) + "/" + str(sumnum) + "]")
                appStore.setSearchAppName(text)
                appStore.execute()
                sleep(baseutil.general_randint(1, 9))
            except:
                # print(text + ",下载错误")
                pass

        texts.close()
        pass
