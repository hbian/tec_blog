## 多线程和多进程比较
[多线程和多进程比较](https://www.liaoxuefeng.com/wiki/897692888725344/923057354442720)

多线程编程，模型复杂，容易发生冲突，必须用锁加以隔离，同时，又要小心死锁的发生。
Python解释器由于设计时有GIL全局锁，导致了多线程无法利用多核。多线程的并发在Python中就是一个美丽的梦。

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
        check_res.append(process_pool.apply_async(ping_ip, (ip,)))

    process_pool.close()
    process_pool.join()

    for ip in check_res:
        if ip.get()[1]:
            print ip.get()[0]

```

对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了。

请注意输出的结果，task 0，1，2，3是立刻执行的，而task 4要等待前面某个task完成后才执行，这是因为Pool的默认大小在我的电脑上是4，因此，最多同时执行4个进程。这是Pool有意设计的限制，并不是操作系统的限制。

process_pool.apply_async 会返回函数返回值， 通过get进行获取