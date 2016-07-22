# Android 应用下载及说明

>* 下载内容来源:豌豆荚

>* 下载匹配条件:从搜索结果的第一个搜索结果作匹配

- - - - - -

- 脚本文件组成

    - appstore.py (应用商店下载功能)

    - baseutil.py (常用方法)

    - config.py (下载的配置信息,如下载列表,下载存储路径,日志保存路径)

    - main.py (下载功能的主运行方法)
    

     **注:上述是下载脚本的四个文件,相互依赖,不可缺少**

<br/>

- 配置及声明:

    APPLIST:        下载清单路径(说明如下)

    APP_SAVE_PATH:  下载文件保存路径

    LOG_SAVE_PATH:  日志保存路径



    下载应用,需要提供一份应用名称清单,格式如下

    应用名称1
    应用名称2
    应用名称3
    ...

    如:

    天天动听
    酷狗音乐
    qq
    ...

    以上是下载文件的格式说明,需要在 config.py 文件中 APPLIST加入 下载清单路径


- 运行方式:

   可能通过命令行直接运行:

    python main.py


<br/>


***2016.07.22 Lann***

