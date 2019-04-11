# [Python3入门之线程实例常用方法及属性设置](https://www.cnblogs.com/chengd/articles/7766735.html)

> 作者: chengd
>
> 链接: https://www.cnblogs.com/chengd/articles/7766735.html

## **什么是线程**

​    **线程是CPU分配资源的基本单位。但一个程序开始运行，这个程序就变成了一个进程，而一个进程相当于一个或者多个线程。当没有多线程编程时，一个进程也是一个主线程，但有多线程编程时，一个进程包含多个线程，包括主线程。使用线程可以实现程序的并发。**

## **python3中线程模块**

​    **python3对多线程支持的是 threading 模块，应用这个模块可以创建多线程程序，并且在多线程间进行同步和通信。在python3 中，可以通过两种方法来创建线程（下面列子将以直接在线程中运行函数为主）：**

​    **1.用 threading.Thread 直接在线程中运行函数**

```python
import time
import threading

def thread_run(name):
    print("%s's first thread!!!"% name)
    time.sleep(5)

mike = threading.Thread(target=thread_run, args=('Mike', ))
jone = threading.Thread(target=thread_run, args=('jone', ))

mike.start()
jone.start()
```

​    **2.通过继承 threading.Thread 类 来创建线程** 

```python
import time
import threading

class mythread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("%s's first thread!!!"% self.name)
        time.sleep(5)

mike = mythread('mike')
jone = mythread('jone')

mike.start()
jone.start()
```



## **线程threading.Thread实例常用方法**

**可以通过help(threading.Thread)查看线程实例所有方法**

### **1. start()**

​    **help解释：Start the thread's activity**

​    **启动线程**

### **2. join()**

​    **help解释：Wait until the thread terminates**

​    **阻塞线程直至线程终止，然后在继续运行**

```python
import time
import threading

def thread_run(name):
    time.sleep(2)
    print("%s's first thread!!!"% name)


mike = threading.Thread(target=thread_run, args=('Mike', ))
jone = threading.Thread(target=thread_run, args=('jone', ))

mike.start()
jone.start()
mike.join()    #阻塞子线程mike直到mike线程执行完毕
jone.join()    #阻塞子线程jone直到jone线程执行完毕
print('main thread is running!!!')

执行结果：
jone's first thread!!!
Mike's first thread!!!
main thread is running!!!
```

​    **如果上面列子不执行join()，主线程先执行，然后才会执行子线程mike和jone**

```python
import time
import threading

def thread_run(name):
    time.sleep(2)
    print("%s's first thread!!!"% name)


mike = threading.Thread(target=thread_run, args=('Mike', ))
jone = threading.Thread(target=thread_run, args=('jone', ))

mike.start()
jone.start()
#mike.join()    #阻塞子线程mike
#jone.join()    #阻塞子线程jone
print('main thread is running!!!')
执行结果：
main thread is running!!!
jone's first thread!!!
Mike's first thread!!!
```



### 3. isAlive = is_alive(self)

​    help解释：Return whether the thread is alive.

​    这个方法用于判断线程是否运行。

​        1.当线程未调用 start()来开启时，isAlive()会返回False

​        2.但线程已经执行后并结束时，isAlive()也会返回False

```python
import time
import threading

def thread_run(name):
    time.sleep(2)
    print("%s's first thread!!!"% name)


mike = threading.Thread(target=thread_run, args=('Mike', ))
jone = threading.Thread(target=thread_run, args=('jone', ))

mike.start()
jone.start()
print('isAlive status: %s'% mike.isAlive())
print('is_alive status: %s' %mike.is_alive())
print('main thread is running!!!')
执行结果：
isAlive status: True
is_alive status: True
main thread is running!!!
Mike's first thread!!!
jone's first thread!!!
```



### 4. name

​    help解释：A string used for identification purposes only.

​    name属性表示线程的线程名 默认是 Thread-x  x是序号，由1开始，第一个创建的线程名字就是 Thread-1

```python
import time
import threading

def thread_run(name):
    print("%s's first thread!!!"% name)
    time.sleep(5)

mike = threading.Thread(target=thread_run, args=('Mike', ), name='Thread-mike')    #name设置线程名
jone = threading.Thread(target=thread_run, args=('jone', ))    #默认线程name是Thread-X

mike.start()
jone.start()
print(mike.name)    #打印线程名
print(jone.name)    #打印线程名
执行结果：
Mike's first thread!!!
jone's first thread!!!
Thread-mike
Thread-1
```



### 5. setName()

​    用于设置线程的名称name

```python
import time
import threading

def thread_run(name):
    print("%s's first thread!!!"% name)
    time.sleep(5)

mike = threading.Thread(target=thread_run, args=('Mike', ))
jone = threading.Thread(target=thread_run, args=('jone', ))    #默认线程name是Thread-X

mike.setName('Thread-mike')    #name设置线程名
mike.start()
jone.start()
print(mike.name)    #打印线程名
print(jone.name)    #打印线程名
执行结果：
Mike's first thread!!!
jone's first thread!!!
Thread-mike
Thread-2
```



### 6. getName()

​    获取线程名称name

```python
import time
import threading

def thread_run(name):
    print("%s's first thread!!!"% name)
    time.sleep(5)

mike = threading.Thread(target=thread_run, args=('Mike', ))
jone = threading.Thread(target=thread_run, args=('jone', ))    #默认线程name是Thread-X

mike.setName('Thread-mike')    #name设置线程名
mike.start()
jone.start()
print(mike.getName())    #打印线程名
print(jone.getName())    #打印线程名
```



### 7. **daemon**

​    help解释：A boolean value indicating whether this thread is a daemon thread

​    当 daemon = False 时，线程不会随主线程退出而退出（默认时，就是 daemon = False）

​    当 daemon = True 时，当主线程结束，其他子线程就会被强制结束

```python
import time
import threading

def thread_mike_run(name):
    time.sleep(1)
    print('mike thread is running 1S')
    time.sleep(5)
    print("%s's first thread!!!"% name)

def thread_jone_run(name):
    time.sleep(2)
    print("%s's first thread!!!"% name)


mike = threading.Thread(target=thread_mike_run, args=('Mike', ), daemon=True)    #设置daemon为True
#mike = threading.Thread(target=thread_mike_run, args=('Mike', ))
jone = threading.Thread(target=thread_jone_run, args=('jone', ))


mike.start()
jone.start()
print('main thread')    #由于线程没有join()，所以主线程会先运行；而jone的daemon为false，所以主线程会等待jone线程运行完毕；但是mike的daemon为True，所以主线程不会等待mike线程
执行结果：
main thread
mike thread is running 1S    #mike线程只执行了1S的print，5S的为执行就直接退出了
jone's first thread!!!
```



### 8. setDaemon()

​    用于设置daemon值

```python
import time
import threading

def thread_mike_run(name):
    time.sleep(1)
    print('mike thread is running 1S')
    time.sleep(5)
    print("%s's first thread!!!"% name)

def thread_jone_run(name):
    time.sleep(2)
    print("%s's first thread!!!"% name)


mike = threading.Thread(target=thread_mike_run, args=('Mike', ))
jone = threading.Thread(target=thread_jone_run, args=('jone', ))

mike.setDaemon(True)    #设置daemon为True
mike.start()
jone.start()
print('main thread')    #由于线程没有join()，所以主线程会先运行；而jone的daemon为false，所以主线程会等待jone线程运行完毕；但是mike的daemon为True，所以主线程不会等待mike线程
执行结果：
main thread
mike thread is running 1S
jone's first thread!!!
```

