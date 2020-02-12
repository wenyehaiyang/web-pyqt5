#!/usr/bin/env python
# -*- coding:utf-8 -*-
import http.server
import os
import queue
from functools import partial
from asyncBase_native import runTask  # 这是我写的一个线程装饰器，被装饰的函数在被调用时会另外加载线程执行，具体代码请移步我的github嘿嘿

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
