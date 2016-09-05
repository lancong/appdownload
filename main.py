# -*- coding: utf-8 -*-

'''

下载程序主方法

'''
import codecs
import os
import threading
from time import sleep, time

import config
import baseutil
from appstore import AppStore_WanDouJia, AppStore_360


# 下载工作
def downappbyfile(downlist):
    filepath = downlist

    if os.path.exists(filepath) and os.path.isfile(filepath):
        texts = codecs.open(filepath, "r", "utf-8")

        appStore = ""
        if config.appstore_choice == 1:
            # 豌豆荚应用商店下载
            appStore = AppStore_WanDouJia()
        elif config.appstore_choice == 2:
            # 360应用商店下载
            appStore = AppStore_360()

        appStore = AppStore_360()
        appStore.setsavefileplace()

        sumnum = baseutil.getfilelines(filepath)

        count = 0
        for text in texts:
            try:
                count += 1
                print("download [" + str(count) + "/" + str(sumnum) + "] " + text)

                appStore.setsearchappname(text)
                appStore.execute()
                sleep(baseutil.randnum(1, 9))
            except:
                # print(text + ",下载错误")
                pass

        texts.close()


# 下载工作
def downappbylist(appnames):
    appStore = ""
    if config.appstore_choice == 1:
        # 豌豆荚应用商店下载
        appStore = AppStore_WanDouJia()
    elif config.appstore_choice == 2:
        # 360应用商店下载
        appStore = AppStore_360()

    appStore.setsavefileplace()

    # 当前执行任务总数
    sumnum = len(appnames)

    count = 0
    for appname in appnames:
        try:
            count += 1

            baseutil.printlog("download [" + str(count) + "/" + str(
                    sumnum) + "] " + appname)

            appStore.setsearchappname(appname)
            appStore.execute()

            sleep(baseutil.randnum(1, 9))

        except:
            # print(text + ",下载错误")
            pass
    pass


def main():
    # 开始时间
    starttime = time()
    # 下载列表
    downfilelist = config.appdown_list1
    # 文件检查
    if not baseutil.isfileexist(downfilelist):
        baseutil.printlog("not find download list:" + str(downfilelist))
        return

    downfilelist = codecs.open(downfilelist, "r", "utf-8")

    appnames = downfilelist.readlines()
    # 任务分发
    tasklist = baseutil.dispatchtask(appnames, config.max_thread)

    downfilelist.close()

    sleep(3)

    try:
        threads = []

        for downlist in tasklist:
            th = threading.Thread(target=downappbylist, args=(downlist,))
            th.start()
            threadname = th.getName()
            # print("thread name: " + threadname + " is running ...")
            threads.append(th)

        for th in threads:
            th.join()

            # baseutil.printlog(threadname + " down app task finished !!!")
    except:

        baseutil.printlog("down app task error !!!")

    endtime = time()
    totaltime = endtime - starttime

    baseutil.printlog("cost time ：{0:.5f} s".format(totaltime) + "\t\n")


if __name__ == '__main__':
    main()
