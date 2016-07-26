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
from appstore import appstore_wandoujia, appstore_360


# 下载工作
def downappbyfile(downlist):
    filepath = downlist

    if os.path.exists(filepath) and os.path.isfile(filepath):
        texts = codecs.open(filepath, "r", "utf-8")

        appStore = ""
        if config.appstore_choice == 1:
            # 豌豆荚应用商店下载
            appStore = appstore_wandoujia()
        elif config.appstore_choice == 2:
            # 360应用商店下载
            appStore = appstore_360()

        appStore = appstore_360()
        appStore.setsavefileplace()

        sumnum = baseutil.getfilelines(filepath)

        count = 0
        for text in texts:
            try:
                count += 1
                print("开始下载 [" + str(count) + "/" + str(sumnum) + "] " + text)

                appStore.setsearchappname(text)
                appStore.execute()
                sleep(baseutil.general_randint(1, 9))
            except:
                # print(text + ",下载错误")
                pass

        texts.close()


# 下载工作
def downappbylist(appnames):
    appStore = ""
    if config.appstore_choice == 1:
        # 豌豆荚应用商店下载
        appStore = appstore_wandoujia()
    elif config.appstore_choice == 2:
        # 360应用商店下载
        appStore = appstore_360()

    appStore.setsavefileplace()

    # 当前执行任务总数
    sumnum = len(appnames)

    count = 0
    for appname in appnames:
        try:
            count += 1

            print(baseutil.getTime_yyyymmddhhmmss() + " 开始下载 [" + str(count) + "/" + str(sumnum) + "] -->> " + appname)

            appStore.setsearchappname(appname)
            # appStore.execute()
            sleep(baseutil.general_randint(1, 9))
        except:
            # print(text + ",下载错误")
            pass

    pass


if __name__ == '__main__':

    # 开始时间
    starttime = time()

    # 支持多下载列表
    downlists = [config.appdown_list1]
    # downlists = [config.appdown_list1, config.appdown_list6]

    # 所有文件读取 writer
    downappnamelists = []
    # 读取所有列表的名称信息
    for list in downlists:
        if os.path.exists(list) and os.path.isfile(list):
            texts = codecs.open(list, "r", "utf-8")
            downappnamelists.append(texts)
            # texts.close()

    # 所有需要下载 appname
    appnames = []

    if baseutil.validList(downappnamelists):
        for downappnamelist in downappnamelists:
            for downappname in downappnamelist:
                appnames.append(downappname)
            downappnamelist.close()

    # 需要下载的条目数
    appnamessize = len(appnames)
    # 通过除最大线程最到一个余数,以余数判断每个任务列表的下载条目数
    restnum = appnamessize % config.max_thread

    # 单个任务列表的下载条目数
    signal_num = 0
    if restnum == 0:
        signal_num = int(appnamessize / config.max_thread)
    else:
        signal_num = int(appnamessize / config.max_thread) + 1

    # 任务执行列表list
    tasklist = [[]]
    # 生成存储任务列表的list
    for num in range(config.max_thread):
        tasklist.append([])

    # 将任务分发至list
    count = 0
    index = 0
    for appname in appnames:
        count += 1
        tasklist[index].append(appname)
        if count == signal_num:
            count = 0
            index += 1

    print("\t\n********** line **********\t\n")

    print(baseutil.getTime_yyyymmddhhmmss() + " 当前下载任务总数:" + str(appnamessize))
    print(baseutil.getTime_yyyymmddhhmmss() + " 当前下载线程总数:" + str(config.max_thread) + "\t\n")

    # print("********** line **********\t\n")

    sleep(3)

    # print(len(tasklists))

    # for lists in tasklists:
    #     # print(len(lists))
    #     for name in lists:
    #         print(name)

    try:
        threads = []

        for downlist in tasklist:
            th = threading.Thread(target=downappbylist, args=(downlist,))
            th.start()
            threads.append(th)

        for th in threads:
            th.join()

        print("\t\n" + baseutil.getTime_yyyymmddhhmmss() + " down app task finished !!!")
    except:
        print("\t\n" + baseutil.getTime_yyyymmddhhmmss() + " down app task error !!!")

    endtime = time()
    totaltime = endtime - starttime

    print(baseutil.getTime_yyyymmddhhmmss() + "下载总耗时：{0:.5f} 秒".format(totaltime) + "\t\n")
