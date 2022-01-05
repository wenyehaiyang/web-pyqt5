# ================= ENGLISH =====================

# PyQt5 builds interactive web&python application through QWebEngineView and QWebChannel
### PyQt5 builds interactive web&python application through QWebEngineView and QWebChannel

First of all, let's talk about the benefits of building interactive web & Python applications through QWebEngineView and QWebChannel. Ha ha, everything needs to be created

1. It can greatly shorten your development cycle. As we all know, web development technology and cycle are excellent, and UI is also one of the tedious and time-consuming development work in our development process. If the UI and some logic of python application can be realized by web technology, it will save too much time;
2. This can make python application and web technology deeply integrate and expand the application scope of python. Web engineers can easily cooperate with python engineers to develop applications with python advantages and web technology advantages.

Code address: https://github.com/wenyehaiyang/web-pyqt5

## content

1. Preparation environment
2. Register QWebChannel in QWebEngineView
3. Register QWebChannel on html front page
4. Write the function to be called in QWebEngineView (parameters can be attached)
5. On the html front-end page, call the corresponding QWebEngineView function through QWebChannel
6. Call HTML front-end code at QWebEngineView end and execute javascript code
7. In addition, QWebEngineView loads the local html file, so it uses the file protocol. If it is to design other static resource requests, it is suggested that you can use http.server of python to monitor the local port, which can be realized

Start codeword^^

##1. Preparation environment:

(1) Install python, that's not to say. There are many online tutorials.
(2) Install pyqt5. Before pyqt5 5.12, pyqt5 package contains QWebEngineView. You can install pyqt5 = = 5.11 or earlier directly. After installation, you can import from pyqt5.qtwebenginewidges import QWebEngineView. After pyqt5 is installed, you need to install pyqtwebengine (pip install PyQtWebEngine) shows that pyqtwebengine can adapt to multiple versions of pyqt5. It is recommended to be the same as pyqt5.
(3) Download qwebchannel.js at https://doc.qt.io/qt-5.9/qtwebengine-webingenewidgets-markdowneditor-resources-qwebchannel-js.html. (PS: This is the official website address. If the address fails, you can find qwebchannel.js in Baidu qwebchannel.js)

##2. QWebEngineView end
```
Look directly at the code hee hee:

    #!/usr/bin/env python
    # -*- coding:utf-8 -*-
    import sys
    import os
    import time
    import urllib.request

    from PyQt5.QtWidgets import QApplication, QDesktopWidget
    from PyQt5.QtCore import QObject, pyqtSlot, QUrl, Qt, QPoint
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from httpSeve.server_tool import http_server_main

    __Author__ = '''wenye'''


    class CallHandler(QObject):

        def __init__(self):
            super(CallHandler, self).__init__()

        @pyqtSlot(str, result=str)  # The first parameter is the type of parameter carried during callback
        def init_home(self, str_args):
            print('call received')
            print('resolving......init home..')
            print(str_args)  # View parameters
            # #####
            # The corresponding processing logic is written here, for example:
            msg = 'Received from python News'
            view.page().runJavaScript("alert('%s')" % msg)
            view.page().runJavaScript("window.say_hello('%s')" % msg)
            return 'hello, Python'


    class WebEngine(QWebEngineView):
        def __init__(self):
            super(WebEngine, self).__init__()
            self.setContextMenuPolicy(Qt.NoContextMenu)  # Set right-click menu rule to custom right-click menu
            # self.customContextMenuRequested.connect(self.showRightMenu)  # The custom right-click menu will be loaded and displayed here. Don't we skip the details here

            self.setWindowTitle('QWebChannel Interact with the front end')
            self.resize(1100, 650)
            cp = QDesktopWidget().availableGeometry().center()
            self.move(QPoint(cp.x() - self.width() / 2, cp.y() - self.height() / 2))

        def closeEvent(self, evt):
            self.page().profile().clearHttpCache()  # Clear the cache of QWebEngineView
            super(WebEngine, self).closeEvent(evt)


    if __name__ == '__main__':
        # Loader main window
        app = QApplication(sys.argv)
        view = WebEngine()
        channel = QWebChannel()
        handler = CallHandler()  # Instantiate the front-end processing object of QWebChannel
        channel.registerObject('PyHandler', handler)  # Register the front-end processing object in the front-end page as the PyHandler object, which will be named PyHandler 'when accessed by the front-end
        view.page().setWebChannel(channel)  # Mount the front-end processing object
        url_string = urllib.request.pathname2url(os.path.join(os.getcwd(), "index.html"))  # Load local html file
        # Of course, you can load the url of the Internet line, or listen to the local port by yourself, and then load the resources of the local port service
        # url_string = 'localhost:64291'   # Load local html file
        # print(url_string, '\n', os.path.join(os.getcwd(), "index.html"))
        view.load(QUrl(url_string))
        time.sleep(2)
        view.show()
        sys.exit(app.exec_())
```
##2, HTML terminal

(1) Create a new index.html, and put qwebchannel.js in the index.html directory (other directories can also be imported correctly in HTML);
(2) Register the QWebChannel instance in index.html.
Look at the code directly
```
    <!DOCTYPE html>
    <html lang=en>
    <head>
        <meta charset=utf-8>
        <meta http-equiv=X-UA-Compatible content="IE=edge">
        <meta name=viewport content="width=device-width,initial-scale=1">
        <title>PyQt5 adopt QWebEngineView and QWebChannel Build interactive browser</title>
        <style>body {
            margin: 0;
        }</style>
        <script src="qwebchannel.js"></script><!--Load qwebchannel.js-->
        <script>
        window.onload = function () {
            try {
                new QWebChannel(qt.webChannelTransport, function (channel) {
                    //Mount the instance of QWebChannel to window.PyHandler, and then call it through window.PyHandler in javascript
                    window.PyHandler = channel.objects.PyHandler;
                });
            } catch (e) {
                window.console.log(e)
            }
        }
        </script>
    </head>
    <body>
    <button onclick="window.PyHandler.init_home('This is from the front end python News')">Click to python Callback</button>
    <div id="app"></div>
    <script>
        //Mount the method to window for easy access from webengine view
        window.say_hello = function (msg) {
            document.getElementById('app').append("This is from python Message received by:"+msg);
        }
    </script>
    </body>
    </html>
```
##The effect is as follows:


3. Add: if you load the web file from the local port, you can use http.server to listen to the local port

Look directly at the code hee hee:
```
    #!/usr/bin/env python
    # -*- coding:utf-8 -*-
    import http.server
    import os
    import queue
    from functools import partial
    from httpServe.asyncBase_native import runTask  # This is a thread decorator I wrote. When the decorated function is called, another thread will be loaded for execution. Please move to my github for specific code

    __Author__ = '''wenye&hunan'''

    # Define paths to avoid errors on different operating systems
    STATIC_PATH_MAIN = os.path.join(os.getcwd(), 'dist', 'mainpage')  # Splicing the static file path to be served here

    PORT_MAIN = 64291  # For the listening port, the url loaded by the load function of QWebEngineView is: localhost: port \ main

    Handler = http.server.SimpleHTTPRequestHandler
    # queue
    q_line_main = queue.Queue()  # This queue is used to hold the handle of the server and operate the server. You can import this queue in the application specific logic


    @runTask
    def http_server_main():
        handler_class = partial(Handler, directory=STATIC_PATH_MAIN)
        handler_class.protocol_version = "HTTP/1.0"
        with http.server.ThreadingHTTPServer(("", PORT_MAIN), handler_class) as httpd:
            q_line_main.put(httpd)
            print("serving at port", PORT_MAIN)
            httpd.serve_forever()
```
Code address: https://github.com/wenyehaiyang/web-pyqt5 
# ================ CHINESE ====================

# 通过QWebEngineView和QWebChannel搭建交互式web&python应用
### 首先来说说通过QWebEngineView和QWebChannel搭建交互式web&python应用的好处哈哈，万事皆是有需要才有创造嘛哈哈
1、可以大幅缩短您的开发周期，众所周知，web开发技术和周期都非常优秀，而UI也是我们开发过程中繁琐费时的开发工作之一，如果python应用的UI和部分逻辑可以用web技术实现那将节省太多太多时间；
2、这可以让python应用和web技术深入融合，开拓python的运用范围，web工程师可以轻松与python工程师合作开发出具有python优势和web技术优势的应用。
###### 代码地址：[https://github.com/wenyehaiyang/web-pyqt5](https://github.com/wenyehaiyang/web-pyqt5)

## 仓库说明：
```
clone仓库以后，按照本文安装好环境，运行PyQt5exploreJSPY.py
```
## 内容
1、准备环境
2、在QWebEngineView注册QWebChannel
3、在html前端页面注册QWebChannel
4、在QWebEngineView端写待调用函数（可附带参数）
5、在html前端页面通过QWebChannel调用对应的QWebEngineView端的函数
6、在QWebEngineView端调用HTML前端代码，执行javascript代码
7、补充本文中QWebEngineView加载的是本地html文件相当于是使用的是file协议，如果是设计其他静态资源请求等，建议可以利用python的http.server监听本地端口，即可实现

## 开始码字^^
##### 1、准备环境：
（1）安装python，这就不多说了，网上很多教程嘿嘿。
（2）安装pyqt5，在pyqt5 5.12版本之前pyqt5包内包含QWebEngineView，可以直接pip install pyqt5==5.11或者之前的版本，安装完毕就可以导入了from PyQt5.QtWebEngineWidgets import QWebEngineView；在之后的版本，安装pyqt5之后，需要另外安装pyqtwebengine（pip install PyQtWebEngine），说明一下PyQtWebEngine可以适配多个版本的pyqt5，推荐与pyqt5版本一致。
（3）下载qwebchannel.js，下载地址：[https://doc.qt.io/qt-5.9/qtwebengine-webenginewidgets-markdowneditor-resources-qwebchannel-js.html](https://doc.qt.io/qt-5.9/qtwebengine-webenginewidgets-markdowneditor-resources-qwebchannel-js.html)。PS：这是官网地址，如果地址失效可以百度qwebchannel.js找到
##### 2、QWebEngineView端
直接看代码嘻嘻：

```
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import time
import urllib.request

from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, Qt, QPoint
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from httpSeve.server_tool import http_server_main

__Author__ = '''wenye'''


class CallHandler(QObject):

    def __init__(self):
        super(CallHandler, self).__init__()

    @pyqtSlot(str, result=str)  # 第一个参数即为回调时携带的参数类型
    def init_home(self, str_args):
        print('call received')
        print('resolving......init home..')
        print(str_args)  # 查看参数
        # #####
        # 这里写对应的处理逻辑比如：
        msg = '收到来自python的消息'
        view.page().runJavaScript("alert('%s')" % msg)
        view.page().runJavaScript("window.say_hello('%s')" % msg)
        return 'hello, Python'


class WebEngine(QWebEngineView):
    def __init__(self):
        super(WebEngine, self).__init__()
        self.setContextMenuPolicy(Qt.NoContextMenu)  # 设置右键菜单规则为自定义右键菜单
        # self.customContextMenuRequested.connect(self.showRightMenu)  # 这里加载并显示自定义右键菜单，我们重点不在这里略去了详细带吗

        self.setWindowTitle('QWebChannel与前端交互')
        self.resize(1100, 650)
        cp = QDesktopWidget().availableGeometry().center()
        self.move(QPoint(cp.x() - self.width() / 2, cp.y() - self.height() / 2))

    def closeEvent(self, evt):
        self.page().profile().clearHttpCache()  # 清除QWebEngineView的缓存
        super(WebEngine, self).closeEvent(evt)


if __name__ == '__main__':
    # 加载程序主窗口
    app = QApplication(sys.argv)
    view = WebEngine()
    channel = QWebChannel()
    handler = CallHandler()  # 实例化QWebChannel的前端处理对象
    channel.registerObject('PyHandler', handler)  # 将前端处理对象在前端页面中注册为名PyHandler对象，此对象在前端访问时名称即为PyHandler'
    view.page().setWebChannel(channel)  # 挂载前端处理对象
    url_string = urllib.request.pathname2url(os.path.join(os.getcwd(), "index.html"))  # 加载本地html文件
    # 当然您可以加载互联网行的url，也可自行监听本地端口，然后加载本地端口服务的资源，后面有介绍嘻嘻
    # url_string = 'localhost:64291'   # 加载本地html文件
    # print(url_string, '\n', os.path.join(os.getcwd(), "index.html"))
    view.load(QUrl(url_string))
    time.sleep(2)
    view.show()
    sys.exit(app.exec_())

```
##### 2、HTML端
（1）新建index.html，并将qwebchannel.js放在index.html目录（其他目录也可以，在HTML中正确引入即可）；
（2）在index.html中注册QWebChannel实例。
直接看代码哈哈：

```
<!DOCTYPE html>
<html lang=en>
<head>
    <meta charset=utf-8>
    <meta http-equiv=X-UA-Compatible content="IE=edge">
    <meta name=viewport content="width=device-width,initial-scale=1">
    <title>PyQt5通过QWebEngineView和QWebChannel搭建交互式浏览器</title>
    <style>body {
        margin: 0;
    }</style>
    <script src="qwebchannel.js"></script><!--加载qwebchannel.js-->
    <script>
    window.onload = function () {
        try {
            new QWebChannel(qt.webChannelTransport, function (channel) {
                //将QWebChannel的实例挂载到window.PyHandler，后面在javascript中通过window.PyHandler即可调用
                window.PyHandler = channel.objects.PyHandler;
            });
        } catch (e) {
            window.console.log(e)
        }
    }
    </script>
</head>
<body>
<button onclick="window.PyHandler.init_home('这是从前端发到python的消息')">点击向python回调</button>
<div id="app"></div>
<script>
    //将方法挂载到window便于从webengineview访问
    window.say_hello = function (msg) {
        document.getElementById('app').append("这是从python端收到的消息:"+msg);
    }
</script>
</body>
</html>
```
###### 效果见我的博文：https://blog.csdn.net/weixin_43866138/article/details/104281399

###### 3、补充：如果您从本地端口加载web文件，可以使用http.server监听本地端口
直接看代码嘻嘻：

```
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import http.server
import os
import queue
from functools import partial
from httpServe.asyncBase_native import runTask  # 这是我写的一个线程装饰器，被装饰的函数在被调用时会另外加载线程执行，具体代码请移步我的github嘿嘿

__Author__ = '''wenye&hunan'''

# 定义路径，以免在不同操作系统出错
STATIC_PATH_MAIN = os.path.join(os.getcwd(), 'dist', 'mainpage')  # 在这里拼接需要服务的静态文件路径

PORT_MAIN = 64291  # 监听的端口，对于的QWebEngineView的load函数加载的url即为：localhost:PORT_MAIN

Handler = http.server.SimpleHTTPRequestHandler
# 队列
q_line_main = queue.Queue()  # 这个队列用于盛放服务器的句柄，用于操作服务器，可在应用具体逻辑中导入此队列


@runTask
def http_server_main():
    handler_class = partial(Handler, directory=STATIC_PATH_MAIN)
    handler_class.protocol_version = "HTTP/1.0"
    with http.server.ThreadingHTTPServer(("", PORT_MAIN), handler_class) as httpd:
        q_line_main.put(httpd)
        print("serving at port", PORT_MAIN)
        httpd.serve_forever()

```
###### 代码地址：[https://github.com/wenyehaiyang/web-pyqt5](https://github.com/wenyehaiyang/web-pyqt5)
