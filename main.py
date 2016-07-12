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

    if os.path.exists(config.APPLIST) and os.path.isfile(config.APPLIST):
        texts = codecs.open(config.APPLIST, "r", "utf-8")
        appStore = AppStore_wandoujia()
        appStore.setSaveFilePlace()
        for text in texts:
            try:
                appStore.setSearchAppName(text)
                appStore.execute()
                sleep(baseutil.general_randint(1, 9))
            except:
                # print(text + ",下载错误")
                pass

        texts.close()
        pass
