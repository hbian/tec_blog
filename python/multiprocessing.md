## 多线程和多进程比较
本文是对廖雪峰大神的文章进行的自己总结[多线程和多进程比较](https://www.liaoxuefeng.com/wiki/897692888725344/923057354442720)

多线程编程，模型复杂，容易发生冲突，必须用锁加以隔离，同时，又要小心死锁的发生。Python解释器由于设计时有GIL全局锁，导致了多线程无法利用多核。多线程的并发在Python中就是一个美丽的梦。
个人在多年的工作中也确实是没有遇到需要些多线程的机会，有些小的脚本会用下多进程，对于高IO的用过协程去处理，更工程化一些的代码直接采取的分布式(pyspark)处理提高效率


### 使用多线程和多进程需要考虑的问题
任务切换： 操作系统在切换进程或者线程时也是一样的，它需要先保存当前执行的现场环境（CPU寄存器状态、内存页等），然后，把新任务的执行环境准备好（恢复上次的寄存器状态，切换内存页等），才能开始执行。这个切换过程虽然很快，但是也需要耗费时间。如果有几千个任务同时进行，操作系统可能就主要忙着切换任务，根本没有多少时间去执行任务了，这种情况最常见的就是硬盘狂响，点窗口无反应，系统处于假死状态。

所以，多任务一旦多到一个限度，就会消耗掉系统所有的资源，结果效率急剧下降，所有任务都做不好。

计算密集型 vs. IO密集型

计算密集型任务的特点是要进行大量的计算，消耗CPU资源，比如计算圆周率、对视频进行高清解码等等，全靠CPU的运算能力。这种计算密集型任务虽然也可以用多任务完成，但是任务越多，花在任务切换的时间就越多，CPU执行任务的效率就越低，所以，要最高效地利用CPU，计算密集型任务同时进行的数量应当等于CPU的核心数。

计算密集型任务由于主要消耗CPU资源，因此，代码运行效率至关重要。Python这样的脚本语言运行效率很低，完全不适合计算密集型任务。对于计算密集型任务，最好用C语言编写。

第二种任务的类型是IO密集型，涉及到网络、磁盘IO的任务都是IO密集型任务，这类任务的特点是CPU消耗很少，任务的大部分时间都在等待IO操作完成（因为IO的速度远远低于CPU和内存的速度）。对于IO密集型任务，任务越多，CPU效率越高，但也有一个限度。常见的大部分任务都是IO密集型任务，比如Web应用。

IO密集型任务执行期间，99%的时间都花在IO上，花在CPU上的时间很少，因此，用运行速度极快的C语言替换用Python这样运行速度极低的脚本语言，完全无法提升运行效率。对于IO密集型任务，最合适的语言就是开发效率最高（代码量最少）的语言，脚本语言是首选，C语言最差。


## 多线程编程示例

如果要启动大量的子进程，可以用进程池的方式批量创建子进程.

示例从一个ip池中通过ping获取仍然可用ip， 通过多进程的方式提高效率
```
import subprocess
import argparse
from multiprocessing import Pool 

ip_range_dict = dict()
ip_range_dict["10.121.49"] = [["10.121.49.101", "10.121.49.159"], ["10.121.49.163", "10.121.49.194"]]
ip_range_dict["10.72.84"] = [["10.72.84.11", "10.72.84.134"]]
ip_range_dict["10.72.83"] = [["10.72.83.21", "10.72.83.136"]]

def ping_ip(ip):

    response = subprocess.call("ping -c 2 -W 1 {} >/dev/null  ".format(ip), shell=True)
    if response != 0:
        return (ip, True)
    else:
        return (ip, False)

def get_ip_from_range(ip_range):

    for ip_range in ip_range_dict[ip_range]:
        for ip_last_pos in xrange(int(ip_range[0].split(".")[-1]), int(ip_range[1].split(".")[-1])):
            ip = ip_range[0].split(".")[:3]
            ip.append(str(ip_last_pos))
            yield ".".join(ip)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--ip", dest="ip_range", help = "ip range to find available ip 10.121.49, 10.72.84, 10.72.83", required=True)

    args = parser.parse_args()

    ip_range = args.ip_range

    available_ip = list()
    process_pool = Pool(4)
    check_res = list()

    for ip in get_ip_from_range(ip_range):
        # apply_async会返回任务的retrun结果
        check_res.append(process_pool.apply_async(ping_ip, (ip,)))

    process_pool.close()
    process_pool.join()

    for ip in check_res:
        if ip.get()[1]:
            #通过get方法获得任务的retrun结果
            print ip.get()[0]

```

对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了。

请注意输出的结果，task 0，1，2，3是立刻执行的，而task 4要等待前面某个task完成后才执行，这是因为Pool的默认大小在我的电脑上是4，因此，最多同时执行4个进程。这是Pool有意设计的限制，并不是操作系统的限制。

process_pool.apply_async 会返回函数返回值， 通过get进行获取