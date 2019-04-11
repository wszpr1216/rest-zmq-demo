# [Python3入门之线程threading常用方法](https://www.cnblogs.com/chengd/articles/7770898.html)

> 作者: chengd
>
> 链接: https://www.cnblogs.com/chengd/articles/7770898.html

Python3 线程中常用的两个模块为：

- **_thread**
- **threading(推荐使用)**

thread 模块已被废弃。用户可以使用 threading 模块代替。所以，在 Python3 中不能再使用"thread" 模块。为了兼容性，Python3 将 thread 重命名为 "_thread"。

## 下面将介绍threading模块常用方法： 

### 1. threading.Lock()

​    如果多个线程共同对某个数据修改，则可能出现不可预料的结果，为了保证数据的正确性，需要对多个线程进行同步。

​    使用 Thread 对象的 Lock 和 Rlock 可以实现简单的线程同步，这两个对象都有 acquire 方法和 release 方法，对于那些需要每次只允许一个线程操作的数据，可以将其操作放到 acquire 和 release 方法之间。

​    来看看多个线程同时操作一个变量怎么把内容给改乱了(在windows下不会出现内容混乱情况，可能python在Windows下自动加上锁了；不过在Linux 下可以测试出内容会被改乱)：

```python
#!/usr/bin/env python3

import time, threading

# 假定这是你的银行存款:
balance = 0

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
执行结果：
[root@localhost ~]# python3 thread_lock.py 
5
[root@localhost ~]# python3 thread_lock.py 
5
[root@localhost ~]# python3 thread_lock.py 
0
[root@localhost ~]# python3 thread_lock.py 
8
[root@localhost ~]# python3 thread_lock.py 
-8
[root@localhost ~]# python3 thread_lock.py 
5
[root@localhost ~]# python3 thread_lock.py 
-8
[root@localhost ~]# python3 thread_lock.py 
3
[root@localhost ~]# python3 thread_lock.py 
5
```

​    我们定义了一个共享变量`balance`，初始值为`0`，并且启动两个线程，先存后取，理论上结果应该为`0`，但是，由于线程的调度是由操作系统决定的，当t1、t2交替执行时，只要循环次数足够多，`balance`的结果就不一定是`0`了。

​    如果我们要确保`balance`计算正确，就要给`change_it()`上一把锁，当某个线程开始执行`change_it()`时，我们说，该线程因为获得了锁，因此其他线程不能同时执行`change_it()`，只能等待，直到锁被释放后，获得该锁以后才能改。由于锁只有一个，无论多少线程，同一时刻最多只有一个线程持有该锁，所以，不会造成修改的冲突。创建一个锁就是通过`threading.Lock()`来实现：

```python
#!/usr/bin/env python3

import time, threading

balance = 0
lock = threading.Lock()

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()
t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
执行结果：
[root@localhost ~]# python3 thread_lock.py 
0
[root@localhost ~]# python3 thread_lock.py 
0
[root@localhost ~]# python3 thread_lock.py 
0
[root@localhost ~]# python3 thread_lock.py 
0
[root@localhost ~]# python3 thread_lock.py 
0
[root@localhost ~]# python3 thread_lock.py 
0
```

​    当多个线程同时执行`lock.acquire()`时，只有一个线程能成功地获取锁，然后继续执行代码，其他线程就继续等待直到获得锁为止。

​    获得锁的线程用完后一定要释放锁，否则那些苦苦等待锁的线程将永远等待下去，成为死线程。所以我们用`try...finally`来确保锁一定会被释放。

​    锁的好处就是确保了某段关键代码只能由一个线程从头到尾完整地执行，坏处当然也很多，首先是阻止了多线程并发执行，包含锁的某段代码实际上只能以单线程模式执行，效率就大大地下降了。其次，由于可以存在多个锁，不同的线程持有不同的锁，并试图获取对方持有的锁时，可能会造成死锁，导致多个线程全部挂起，既不能执行，也无法结束，只能靠操作系统强制终止。

###  2. threading.Rlock()

​    RLock允许在同一线程中被多次acquire。而Lock却不允许这种情况。注意：如果使用RLock，那么acquire和release必须成对出现，即调用了n次acquire，必须调用n次的release才能真正释放所占用的琐。

```python
import threading
lock = threading.Lock() 
#Lock对象
lock.acquire()
lock.acquire() 
#产生了死琐。
lock.release()
lock.release()
  
import threading
rLock = threading.RLock() 
#RLock对象
rLock.acquire()
rLock.acquire() 
#在同一线程内，程序不会堵塞。
rLock.release()
rLock.release()
```



### 3. threading.Condition()

​    可以把Condiftion理解为一把高级的琐，它提供了比Lock, RLock更高级的功能，允许我们能够控制复杂的线程同步问题。threadiong.Condition在内部维护一个琐对象（默认是RLock），可以在创建Condigtion对象的时候把琐对象作为参数传入。Condition也提供了acquire, release方法，其含义与琐的acquire, release方法一致，其实它只是简单的调用内部琐对象的对应的方法而已。Condition还提供wait方法、notify方法、notifyAll方法(特别要注意：这些方法只有在占用琐(acquire)之后才能调用，否则将会报RuntimeError异常。)：

​    acquire()/release()：获得/释放 Lock

​    wait([timeout]):线程挂起，直到收到一个notify通知或者超时（可选的，浮点数，单位是秒s）才会被唤醒继续运行。**wait()必须在已获得Lock前提下才能调用，否则会触发RuntimeError。调用wait()会释放Lock，直至该线程被Notify()、NotifyAll()或者超时线程又重新获得Lock.**

​    notify(n=1):通知其他线程，那些挂起的线程接到这个通知之后会开始运行，默认是通知一个正等待该condition的线程,最多则唤醒n个等待的线程。**notify()必须在已获得Lock前提下才能调用，否则会触发RuntimeError。notify()不会主动释放Lock。**

​    notifyAll(): 如果wait状态线程比较多，notifyAll的作用就是通知所有线程（这个一般用得少）

​    现在写个捉迷藏的游戏来具体介绍threading.Condition的基本使用。假设这个游戏由两个人来玩，一个藏(Hider)，一个找(Seeker)。游戏的规则如下：1. 游戏开始之后，Seeker先把自己眼睛蒙上，蒙上眼睛后，就通知Hider；2. Hider接收通知后开始找地方将自己藏起来，藏好之后，再通知Seeker可以找了； 3. Seeker接收到通知之后，就开始找Hider。Hider和Seeker都是独立的个体，在程序中用两个独立的线程来表示，在游戏过程中，两者之间的行为有一定的时序关系，我们通过Condition来控制这种时序关系。

```python
#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import threading, time

def Seeker(cond, name):
    time.sleep(2)
    cond.acquire()
    print('%s :我已经把眼睛蒙上了！'% name)
    cond.notify()                               # 黄色
    cond.wait()                                 # 橘黄
    for i in range(3):
        print('%s is finding!!!'% name)
        time.sleep(2)
    cond.notify()                               # 粉色
    cond.release()
    print('%s :我赢了！'% name)

def Hider(cond, name):
    cond.acquire()
    cond.wait()                                 # 黄色
    for i in range(2):
        print('%s is hiding!!!'% name)
        time.sleep(3)
    print('%s :我已经藏好了，你快来找我吧！'% name)
    cond.notify()                               # 橘黄
    cond.wait()                                 # 粉色
    cond.release()
    print('%s :被你找到了，唉~^~!'% name)


if __name__ == '__main__':
    cond = threading.Condition()
    seeker = threading.Thread(target=Seeker, args=(cond, 'seeker'))
    hider = threading.Thread(target=Hider, args=(cond, 'hider'))
    seeker.start()
    hider.start()
执行结果：
seeker :我已经把眼睛蒙上了！
hider is hiding!!!
hider is hiding!!!
hider :我已经藏好了，你快来找我吧！
seeker is finding!!!
seeker is finding!!!
seeker is finding!!!
seeker :我赢了！
hider :被你找到了，唉~^~!
```

​    上面不同颜色的notify和wait一一对应关系，通知--->等待；等待--->通知

### 4. threading.Semaphore和BoundedSemaphore

​    Semaphore：Semaphore 在内部管理着一个计数器。调用 acquire() 会使这个计数器 -1，release() 则是+1(可以多次release()，所以计数器的值理论上可以无限).计数器的值永远不会小于 0，当计数器到 0 时，再调用 acquire() 就会阻塞，直到其他线程来调用release()

```python
import threading, time


def run(n):
    # 获得信号量，信号量减一
    semaphore.acquire()
    time.sleep(1)
    print("run the thread: %s" % n)

    # 释放信号量，信号量加一
    semaphore.release()
    #semaphore.release()    # 可以多次释放信号量，每次释放计数器+1
    #semaphore.release()    # 可以多次释放信号量，每次释放计数器+1


if __name__ == '__main__':

    num = 0
    semaphore = threading.Semaphore(2)  # 最多允许2个线程同时运行(即计数器值)；在多次释放信号量后，计数器值增加后每次可以运行的线程数也会增加
    for i in range(20):
        t = threading.Thread(target=run, args=(i,))
        t.start()

while threading.active_count() != 1:
    pass  # print threading.active_count()
else:
    print('----all threads done---')
    print(num)
```

​    BoundedSemaphore：类似于Semaphore；不同在于BoundedSemaphore 会检查内部计数器的值，并保证它不会大于初始值，如果超了，就引发一个 ValueError。多数情况下，semaphore 用于守护限制访问（但不限于 1）的资源，如果 semaphore 被 release() 过多次，这意味着存在 bug

```python
import threading, time


def run(n):
    semaphore.acquire()
    time.sleep(1)
    print("run the thread: %s" % n)
    semaphore.release()
    # 如果再次释放信号量，信号量加一，这是超过限定的信号量数目，这时会报错ValueError: Semaphore released too many times
    #semaphore.release()


if __name__ == '__main__':

    num = 0
    semaphore = threading.BoundedSemaphore(2)  # 最多允许2个线程同时运行
    for i in range(20):
        t = threading.Thread(target=run, args=(i,))
        t.start()

while threading.active_count() != 1:
    pass  # print threading.active_count()
else:
    print('----all threads done---')
    print(num)
```



###  5. threading.Event

​    事件处理的机制：全局定义了一个“Flag”，如果“Flag”值为 False，那么当程序执行 event.wait 方法时就会阻塞；如果“Flag”值为True，那么执行event.wait 方法时便不再阻塞。

​    clear：将“Flag”设置为False
​    set：将“Flag”设置为True
​    用 threading.Event 实现线程间通信，使用threading.Event可以使一个线程等待其他线程的通知，我们把这个Event传递到线程对象中，

​    Event默认内置了一个标志，初始值为False。一旦该线程通过wait()方法进入等待状态，直到另一个线程调用该Event的set()方法将内置标志设置为True时，该Event会通知所有等待状态的线程恢复运行。

​    通过Event来实现两个或多个线程间的交互，下面是一个红绿灯的例子，即起动一个线程做交通指挥灯，生成几个线程做车辆，车辆行驶按红灯停，绿灯行的规则。

```python
import threading, time
import random

def light():
    if not event.isSet():    #初始化evet的flag为真
        event.set()    #wait就不阻塞 #绿灯状态
    count = 0
    while True:
        if count < 10:
            print('\033[42;1m---green light on---\033[0m')
        elif count < 13:
            print('\033[43;1m---yellow light on---\033[0m')
        elif count < 20:
            if event.isSet():
                event.clear()
            print('\033[41;1m---red light on---\033[0m')
        else:
            count = 0
            event.set()    #打开绿灯
        time.sleep(1)
        count += 1

def car(n):
    while 1:
        time.sleep(random.randrange(3, 10))
        #print(event.isSet())
        if event.isSet():
            print("car [%s] is running..." % n)
        else:
            print('car [%s] is waiting for the red light...' % n)
            event.wait()    #红灯状态下调用wait方法阻塞，汽车等待状态

if __name__ == '__main__':
    car_list = ['BMW', 'AUDI', 'SANTANA']
    event = threading.Event()
    Light = threading.Thread(target=light)
    Light.start()
    for i in car_list:
        t = threading.Thread(target=car, args=(i,))
        t.start()
```



### 6. threading.active_count()

​    返回当前存活的线程对象的数量；通过计算len(threading.enumerate())长度而来

​    The returned count is equal to the length of the list returned by enumerate().

```python
import threading, time


def run():
    thread = threading.current_thread()
    print('%s is running...'% thread.getName())    #返回线程名称
    time.sleep(10)    #休眠10S方便统计存活线程数量

if __name__ == '__main__':
    #print('The current number of threads is: %s' % threading.active_count())
    for i in range(10):
        print('The current number of threads is: %s' % threading.active_count())    #返回当前存活线程数量
        thread_alive = threading.Thread(target=run, name='Thread-***%s***' % i)
        thread_alive.start()
    thread_alive.join()
    print('\n%s thread is done...'% threading.current_thread().getName())
```



### 7. threading.current_thread()

​    Return the current Thread object, corresponding to the caller's thread of control.

​    返回当前线程对象

```python
>>> threading.current_thread
<function current_thread at 0x00000000029F6C80>
>>> threading.current_thread()
<_MainThread(MainThread, started 4912)>
>>> type(threading.current_thread())
<class 'threading._MainThread'>
```

​    继承线程threading方法；通过help(threading.current_thread())查看。

```python
import threading, time


def run(n):
    thread = threading.current_thread()
    thread.setName('Thread-***%s***' % n)    #自定义线程名称
    print('-'*30)
    print("Pid is :%s" % thread.ident)  # 返回线程pid
    #print('ThreadName is :%s' % thread.name)  # 返回线程名称
    print('ThreadName is :%s'% thread.getName())    #返回线程名称
    time.sleep(2)

if __name__ == '__main__':
    #print('The current number of threads is: %s' % threading.active_count())
    for i in range(3):
        #print('The current number of threads is: %s' % threading.active_count())    #返回当前存活线程数量
        thread_alive = threading.Thread(target=run, args=(i,))
        thread_alive.start()
    thread_alive.join()
    print('\n%s thread is done...'% threading.current_thread().getName())

执行结果：
Pid is :11792
ThreadName is :Thread-***0***
------------------------------
Pid is :12124
ThreadName is :Thread-***1***
------------------------------
Pid is :11060
ThreadName is :Thread-***2***

MainThread thread is done...
```



### 8. threading.enumerate()

​    Return a list of all Thread objects currently alive

​    返回当前存在的所有线程对象的列表

```python
import threading, time


def run(n):
    thread = threading.current_thread()
    thread.setName('Thread-***%s***' % n)
    print('-'*30)
    print("Pid is :%s" % thread.ident)  # 返回线程pid
    #print('ThreadName is :%s' % thread.name)  # 返回线程名称
    print('ThreadName is :%s'% threading.enumerate())    #返回所有线程对象列表
    time.sleep(2)

if __name__ == '__main__':
    #print('The current number of threads is: %s' % threading.active_count())
    threading.main_thread().setName('Chengd---python')
    for i in range(3):
        #print('The current number of threads is: %s' % threading.active_count())    #返回当前存活线程数量
        thread_alive = threading.Thread(target=run, args=(i,))
        thread_alive.start()
    thread_alive.join()
    print('\n%s thread is done...'% threading.current_thread().getName())
执行结果：
Pid is :12096
ThreadName is :[<_MainThread(Chengd---python, started 12228)>, <Thread(Thread-***0***, started 12096)>, <Thread(Thread-2, initial)>]
------------------------------
Pid is :10328
ThreadName is :[<_MainThread(Chengd---python, started 12228)>, <Thread(Thread-***0***, started 12096)>, <Thread(Thread-***1***, started 10328)>, <Thread(Thread-3, initial)>]
------------------------------
Pid is :6032
ThreadName is :[<_MainThread(Chengd---python, started 12228)>, <Thread(Thread-***0***, started 12096)>, <Thread(Thread-***1***, started 10328)>, <Thread(Thread-***2***, started 6032)>]

Chengd---python thread is done...
```



### 9.threading.get_ident()

​    返回线程pid

```python
import threading, time


def run(n):
    print('-'*30)
    print("Pid is :%s" % threading.get_ident())  # 返回线程pid

if __name__ == '__main__':
    threading.main_thread().setName('Chengd---python')    #自定义线程名
    for i in range(3):
        thread_alive = threading.Thread(target=run, args=(i,))
        thread_alive.start()
    thread_alive.join()
    print('\n%s thread is done...'% threading.current_thread().getName())    #获取线程名
```



### 10. threading.main_thread()

​    返回主线程对象，类似 threading.current_thread()；只不过一个是返回当前线程对象，一个是返回主线程对象

```python
import threading, time


def run(n):
    print('-'*30)
    print("Now Pid is :%s" % threading.current_thread().ident)  # 返回当前线程pid
    print("Main Pid is :%s" % threading.main_thread().ident)  # 返回主线程pid
    print('Now thread is %s...' % threading.current_thread().getName())  # 获取当前线程名
    print('Main thread is %s...' % threading.main_thread().getName())  # 获取主线程线程名

if __name__ == '__main__':
    threading.main_thread().setName('Chengd---python')    #自定义线程名
    for i in range(3):
        thread_alive = threading.Thread(target=run, args=(i,))
        thread_alive.start()
        time.sleep(2)
    thread_alive.join()

执行结果：
------------------------------
Now Pid is :8984
Main Pid is :3992
Now thread is Thread-1...
Main thread is Chengd---python...
------------------------------
Now Pid is :4828
Main Pid is :3992
Now thread is Thread-2...
Main thread is Chengd---python...
------------------------------
Now Pid is :12080
Main Pid is :3992
Now thread is Thread-3...
Main thread is Chengd---python...
```

[廖大线程讲解](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143192823818768cd506abbc94eb5916192364506fa5d000)

[线程常用模块方法](http://www.jb51.net/article/68066.htm)

[多线程之Condition()](http://blog.csdn.net/suipingsp/article/details/40303429)

[python—threading.Semaphore和BoundedSemaphore](http://blog.csdn.net/a349458532/article/details/51589460)

[python 多线程之信号机Semaphore示例](http://blog.sina.com.cn/s/blog_7f85f8a701014ux9.html)

[alex线程讲解](http://www.cnblogs.com/alex3714/articles/5230609.html)