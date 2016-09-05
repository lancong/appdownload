# -*- coding: utf-8 -*-

'''

现在以豌豆荚网站为基础构建的app搜索,默认结果以app的名称为准

后添加360下载

'''

import config
import baseutil


# 360搜索及download
# http://zhushou.360.cn/search/index/?kw=%E5%A4%A9%E5%A4%A9%E5%8A%A8%E5%90%AC
class AppStore_360(object):
    def __init__(self):
        # self.appInfo = appinfo.AppInfo()
        self.appName = ""
        self.targetDir = ""
        self.logFileName = ""
        self.isSave = True

    appstroe_360 = "http://zhushou.360.cn/search/index/?kw="

    # 设置文件存储目录
    def setsavefileplace(self, targetDir=config.app_save_path):
        self.targetDir = targetDir

    # 得到download正确的日志文件名称
    def getsucceedfilename(self):
        return str(baseutil.getTime_yyyymmdd()) + "_appdown_succeed.log"

    # 得到download失败的日志文件名称
    def getfailedfilename(self):
        return str(baseutil.getTime_yyyymmdd()) + "_appdown_failed.log"

    # 得到没有找到的app文件名称
    def getnotfindfilename(self):
        return str(baseutil.getTime_yyyymmdd()) + "_appdown_notfind.log"

    # 生成搜索属性或者链接
    def generalsearchparm(self):
        encodeAppName = baseutil.URLEncoder(self.appName)
        return self.appstroe_360 + encodeAppName

    # 判断搜索结果是否可以download
    def judgeresult(self):
        searchResult = baseutil.openUrl(self.generalsearchparm())
        allResults = searchResult.find("div", {"class": "main"})
        # print(allResults)

        if baseutil.valid(allResults):
            h3falg = allResults.find("h3")
            if baseutil.valid(h3falg):
                titlename = h3falg.find("a")
                if baseutil.valid(titlename):
                    searchname = titlename['title']
                    if baseutil.valid(searchname) and (self.appName.lower().strip() == searchname.lower().strip()):
                        urlflag = allResults.find("div", {"class": "download comdown"})
                        if baseutil.valid(urlflag):
                            aflag = urlflag.find("a")
                            aflagattrs = aflag.attrs
                            if "href" in aflagattrs:
                                return aflag['href']
        return ""

    # 设置搜索app名称
    def setsearchappname(self, appName):
        self.appName = appName.strip()

    # 设置是否保存download结果(默认开启)
    def setsaveresult(self, isSave):
        self.isSave = isSave

    # 执行download
    def execute(self):
        if baseutil.valid(self.targetDir):
            downurl = self.judgeresult()
            if (baseutil.valid(downurl)):
                # print(self.appName + ",download地址: " + downurl)
                isSucceed = baseutil.downLoadFile(downurl, self.targetDir + baseutil.getTime_yyyymmdd(), self.appName)

                pos1 = downurl.rfind("/") + 1
                pos2 = downurl.rfind("_")
                packageName = downurl[pos1:pos2]

                if not baseutil.valid(packageName):
                    packageName = "unknow"

                data = ""
                retext = "succeed"
                if isSucceed:
                    retext = "succeed"
                    data = str(
                            baseutil.getTime_yyyymmddhhmmss()) + "," + self.appName + "," + packageName + ", download" + retext
                    baseutil.writeText(data, config.down_log_save_path + baseutil.getTime_yyyymmdd(),
                                       self.getsucceedfilename(), "a", True)
                else:
                    retext = "failed or error"
                    data = str(
                            baseutil.getTime_yyyymmddhhmmss()) + "," + self.appName + "," + packageName + ", download" + retext
                    baseutil.writeText(data, config.down_log_save_path + baseutil.getTime_yyyymmdd(),
                                       self.getfailedfilename(), "a", True)

                # print(str(baseutil.getTime_yyyymmddhhmmss()) + "," + self.appName + ", download" + retext)

            else:
                data = str(baseutil.getTime_yyyymmddhhmmss()) + "," + self.appName + ", not find, cancel download"
                baseutil.writeText(data, config.down_log_save_path + baseutil.getTime_yyyymmdd(),
                                   self.getnotfindfilename(),
                                   "a", True)
                # print(data)
        else:
            print(str(baseutil.getTime_yyyymmddhhmmss()) + " please set save path !!!")


# 豌豆荚搜索及download
# http://www.wandoujia.com/search?key=GO%E6%A1%8C%E9%9D%A2&source=search
class AppStore_WanDouJia(object):
    def __init__(self):
        # self.appInfo = appinfo.AppInfo()
        self.appName = ""
        self.targetDir = ""
        self.logFileName = ""
        self.isSave = True

    appstroe_wnadoujia = "http://www.wandoujia.com/search"

    # 设置文件存储目录
    def setsavefileplace(self, targetDir=config.app_save_path):
        self.targetDir = targetDir

    # 得到download正确的日志文件名称
    def getsucceedfilename(self):
        return str(baseutil.getTime_yyyymmdd()) + "_appdown_succeed.log"

    # 得到download失败的日志文件名称
    def getfailedfilename(self):
        return str(baseutil.getTime_yyyymmdd()) + "_appdown_failed.log"

    # 得到没有找到的app文件名称
    def getnotfindfilename(self):
        return str(baseutil.getTime_yyyymmdd()) + "_appdown_notfind.log"

    # 生成搜索属性或者链接
    def generalsearchparm(self):
        encodeAppName = baseutil.URLEncoder(self.appName)
        return self.appstroe_wnadoujia + "?key=" + encodeAppName + "&source=search"

    # 判断搜索结果是否可以download
    def judgeresult(self):
        searchResult = baseutil.openUrl(self.generalsearchparm())
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
    def setsearchappname(self, appName):
        self.appName = appName.strip()

    # 设置是否保存download结果(默认开启)
    def setsaveresult(self, isSave):
        self.isSave = isSave

    # 执行download
    def execute(self):
        if baseutil.valid(self.targetDir):
            downUrl = self.judgeresult()
            app_name = self.appName
            if (baseutil.valid(downUrl)):
                # print(self.appName + ",download地址: " + downUrl)
                isSucceed = baseutil.downLoadFile(downUrl, self.targetDir + baseutil.getTime_yyyymmdd(), app_name)

                pos1 = downUrl.index("apps") + 5
                pos2 = downUrl.index("download") - 1
                packageName = downUrl[pos1:pos2]

                data = ""
                retext = "succeed"

                if isSucceed:
                    retext = "succeed"
                    data = str(
                            baseutil.getTime_yyyymmddhhmmss()) + "," + app_name + "," + packageName + ",download" + retext
                    baseutil.writeText(data, config.down_log_save_path + baseutil.getTime_yyyymmdd(),
                                       self.getsucceedfilename(), "a", True)
                else:
                    retext = "failed or error"

                    data = str(
                            baseutil.getTime_yyyymmddhhmmss()) + "," + app_name + "," + packageName + ",download" + retext
                    baseutil.writeText(data, config.down_log_save_path + baseutil.getTime_yyyymmdd(),
                                       self.getfailedfilename(), "a", True)

                # baseutil.printlog(app_name + ", download" + retext)

            else:
                data = str(baseutil.getTime_yyyymmddhhmmss()) + "," + app_name + ", not find, cancel download"

                baseutil.writeText(data, config.down_log_save_path + baseutil.getTime_yyyymmdd(),
                                   self.getnotfindfilename(),
                                   "a", True)

                # baseutil.printlog(app_name + ' not failed or error')
        else:

            baseutil.printlog("please set save path !!!")


if __name__ == '__main__':
    # --- base func test
    # appStore = AppStore_wandoujia()
    # appStore.setSearchAppName("QQ")
    # # print(appStore.judgeResult())
    # appStore.setSaveFilePlace()
    # appStore.execute()

    # --- app package name get
    # text = "http://www.wandoujia.com/apps/com.ttlm.mljf/binding"
    # pos2 = text.replace("binding","download")
    # print(pos2)

    # --- appstore 360

    appstore360 = AppStore_360()
    appstore360.setsearchappname("360清理大师")
    # appstore360.judgeresult()
    appstore360.setsavefileplace()
    appstore360.execute()

    # --- app package name get
    # downurl = "http://m.shouji.360tpcdn.com/160713/18650ccdc58039cb3b219c27ee44e88f/com.tencent.mobileqq_390.apk"
    # index = downurl.rfind("_")
    # index2 = downurl.rfind("/")
    # print(downurl[index2 + 1:index])
    pass
