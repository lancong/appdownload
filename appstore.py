# -*- coding: utf-8 -*-

'''

现在以豌豆荚网站为基础构建的app搜索,默认结果以app的名称为准

'''
import threading

import config
import baseutil


# 豌豆荚搜索及下载
# http://www.wandoujia.com/search?key=GO%E6%A1%8C%E9%9D%A2&source=search
class AppStore_wandoujia(object):
    def __init__(self):
        # self.appInfo = appinfo.AppInfo()
        self.appName = ""
        self.targetDir = ""
        self.logFileName = ""
        self.isSave = True

    APPSTROE_WNADOUJIA = "http://www.wandoujia.com/search"

    # 设置文件存储目录
    def setSaveFilePlace(self, targetDir=config.APP_SAVE_PATH):
        self.targetDir = targetDir

    # 得到下载正确的日志文件名称
    def getsucceedfilename(self):
        return str(baseutil.getTime_yyyymmdd()) + "_appdown_succeed.log"

    # 得到下载失败的日志文件名称
    def getfailedfilename(self):
        return str(baseutil.getTime_yyyymmdd()) + "_appdown_failed.log"

    # 得到没有找到的app文件名称
    def getnotfindfilename(self):
        return str(baseutil.getTime_yyyymmdd()) + "_appdown_notfind.log"

    # 生成搜索属性或者链接
    def generalSearchParm(self):
        encodeAppName = baseutil.URLEncoder(self.appName)
        return self.APPSTROE_WNADOUJIA + "?key=" + encodeAppName + "&source=search"

    # 判断搜索结果是否可以下载
    def judgeResult(self):
        searchResult = baseutil.openUrl(self.generalSearchParm())
        allResults = searchResult.find("ul", {"id": "j-search-list"})
        # print(allResults)

        if baseutil.valid(allResults):
            firstSearchResult = allResults.find("li")
            if baseutil.valid(firstSearchResult):
                flagAttrs = firstSearchResult.attrs
                if "data-pn" in flagAttrs:
                    packageName = flagAttrs['data-pn']
                    namePflag = firstSearchResult.find("h2", {"class": "app-title-h2"})
                    if baseutil.valid(namePflag):
                        infos = namePflag.find("a")
                        if baseutil.valid(infos):
                            resultAppName = infos.attrs['title'].lower().strip()
                            nameapp = self.appName
                            if self.appName.lower().strip() == resultAppName:
                                url = firstSearchResult.find("a", {"class": "i-source install-btn "})['href']
                                return url.replace("binding", "download")
                                # return infos.attrs["href"]
            else:
                return ""

    # 设置搜索app名称
    def setSearchAppName(self, appName):
        self.appName = appName.strip()

    # 设置是否保存下载结果(默认开启)
    def setSaveResult(self, isSave):
        self.isSave = isSave

    # 执行下载
    def execute(self):
        if baseutil.valid(self.targetDir):
            downUrl = self.judgeResult()
            if (baseutil.valid(downUrl)):
                # print(self.appName + ",下载地址: " + downUrl)
                isSucceed = baseutil.downLoadFile(downUrl, self.targetDir + baseutil.getTime_yyyymmdd(), self.appName)

                pos1 = downUrl.index("apps") + 5
                pos2 = downUrl.index("download") - 1
                packageName = downUrl[pos1:pos2]

                data = ""
                retext = "成功"
                if isSucceed:
                    retext = "成功"
                    data = str(
                            baseutil.getTime_yyyymmddhhmmss()) + "," + self.appName + "," + packageName + ",下载" + retext
                    baseutil.writeText(data, config.LOG_SAVE_PATH + baseutil.getTime_yyyymmdd(),
                                       self.getsucceedfilename(), "a", True)
                else:
                    retext = "失败或者错误"
                    data = str(
                            baseutil.getTime_yyyymmddhhmmss()) + "," + self.appName + "," + packageName + ",下载" + retext
                    baseutil.writeText(data, config.LOG_SAVE_PATH + baseutil.getTime_yyyymmdd(),
                                       self.getfailedfilename(), "a", True)

                print(str(baseutil.getTime_yyyymmddhhmmss()) + "," + self.appName + ",下载" + retext)

            else:
                data = str(baseutil.getTime_yyyymmddhhmmss()) + "," + self.appName + ",未找到,取消下载"
                baseutil.writeText(data, config.LOG_SAVE_PATH + baseutil.getTime_yyyymmdd(), self.getnotfindfilename(),
                                   "a", True)
                print(data)
        else:
            print(str(baseutil.getTime_yyyymmddhhmmss()) + " 请设置下载文件存储路径!!!")

    pass


if __name__ == '__main__':
    # --- base func test
    appStore = AppStore_wandoujia()
    appStore.setSearchAppName("QQ")
    # print(appStore.judgeResult())
    appStore.setSaveFilePlace()
    appStore.execute()

    # --- app package name get
    # text = "http://www.wandoujia.com/apps/com.ttlm.mljf/binding"
    # pos2 = text.replace("binding","download")
    # print(pos2)

    pass
