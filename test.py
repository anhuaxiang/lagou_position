import time
import re

def add(x, y):
    assert isinstance(x, int), 'x需整数'
    assert isinstance(y, int), 'x需整数'
    return x+y


print(add(1, 2))
print(type(type(1)))

s = 0
start_time = time.time()
for i in range(1, pow(10, 1)+1):
    s += i
print(s, time.time()-start_time)


def timing(fun):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        a = fun(*args, **kwargs)
        print(f'函数执行时间为{time.time() - start_time}')
        return a
    return wrapper


@timing
def fun01(a: int, b: int):
    assert a < b, 'a需小于b'
    s = 0
    for i in range(a, b, 1):
        s += i
    return s


print(fun01(1, 11))


pa = re.compile('[\d]+')
a = re.match(pa, 'dfdsf12')
b = re.search(pa, 'fdafadsf2')
if a:
    print(a.group())
else:
    print('匹配不成功')

if b:
    print(b.group())
else:
    print('搜索不成功')

import psutil
info = psutil.net_if_addrs()
for k, v in info.items():
    for item in v:
        if item[0] == 2 and not item[1] == '127.0.0.1':
            print(k, item[1])