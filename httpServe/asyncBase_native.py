import threading
import functools

"""本地异步任务装饰器，
用Thread类进行简单封装，执行中等耗时CPU任务，不带线程列队，执行完毕自动回收，
由于没有线程管理，短时间创建大量线程会增加进程管理负担，影响执行效率，所以不可频繁调用"""


def runTask(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper
