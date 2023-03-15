# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
import random
import threading
import time
from optparse import OptionParser
from random import Random
from multiprocessing import Process
import os
from lxml import etree
import requests
import json

aid = []
fail = []
total = []
goal = []
start = []
finished_total = 0
threads = []
result_dict = {}
headers = {
    "cookie": "finger=-1260391586; _uuid=D51E6955-C238-C370-8571-73991591A3BA78608infoc; buvid3=D854CAA6-8795-4B65-82C3-F6617B20F17058502infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(JYYRlYRRJl0J'uY|~|RYumJ; sid=isi80p88; PVID=13; bsource=search_baidu; bfe_id=f027475b111b8c2b686328c826e4e281",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
}
new_result = {}

thread_file_path = "./thread_tracker.json"
result_file_path = "./results.json"
keywords_file_path = "./keywords.txt"

table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608
block_size = 0
keyword_list = []


def av2bv(x):
    x = (x ^ xor) + add
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[x // 58 ** i % 58]
    return ''.join(r)


def get_data(i):
    ##url = "https://comment.bilibili.com/" + str(oid[id]) + ".xml";
    global finished_total
    while aid[i] <= goal[i]:
        bvid = av2bv(aid[i])
        if bvid:
            cid = bvid_to_cid(bvid, i)
            if cid:
                url = "https://comment.bilibili.com/" + str(cid) + ".xml"
                # 发送请求
                try:
                    res = requests.get(url=url, headers=headers)
                    # 设置编码格式
                    s = res.text
                    # s.encoding='utf-8'

                    selector = etree.HTML(s.encode("utf-8"))
                    # 查看返回值。返回值200表明连接正常

                    if str(type(selector)) == '<class \'lxml.etree._Element\'>':
                        for item in selector.xpath('.'):
                            ss = item.xpath('.//d/text()')
                            tags = item.xpath('.//d/@p')
                        link = 'http://bilibili.com/video/av' + str(
                            aid[i])
                        id = 0
                        # 进行解码和打印输出
                        contents = {}
                        for i2 in range(len(ss)):
                            string = ss[i2].encode('raw_unicode_escape').decode()
                            for name in keyword_list:
                                if name in string:
                                    min = int(float(tags[i2].split(',')[0]) / 60)
                                    sec = int(float(tags[i2].split(',')[0])) % 60
                                    time = str(min) + '分' + str(sec) + '秒'
                                    contents[id] = {
                                        "content": string,
                                        "time": time,
                                    }
                                    id += 1
                        if len(contents.items()) > 0:
                            contents['link'] = link

                            result_dict[aid[i]] = contents
                            new_result[aid[i]] = contents

                except:
                    aid[i] -= 1
            else:
                fail[i] += 1
            total[i] += 1
        aid[i] += 1
        finished_total += 1


def save_progress():
    while True:
        time.sleep(10)

        [print(value) for (key, value) in new_result.items()]
        new_result.clear()

        thread_dict = {'block_size': block_size}

        for i in range(len(aid)):
            thread_dict['t' + str(i + 1)] = \
                {
                    "start": start[i],
                    "current": aid[i],
                    "goal": goal[i]
                }

        with open(thread_file_path, "w") as f:
            f.write(json.dumps(thread_dict, indent=4))

        with open(result_file_path, "w", encoding='utf-8') as f:
            f.write(json.dumps(result_dict, ensure_ascii=False, indent=4))

        cls()

        if print_progress() >= 100:
            break


# Press the green button in the gutter to run the script.
def aid_to_bvid(aid):
    url = "http://api.bilibili.com/x/web-interface/archive/stat?aid=" + str(aid)
    res = requests.get(url=url, headers=headers)
    json_dict = json.loads(res.text)
    data = json_dict["data"]
    if data:
        bvid = data["bvid"]
        return bvid
    return ""


def bvid_to_cid(bvid, i):
    url = "https://api.bilibili.com/x/player/pagelist?bvid=" + bvid + "&jsonp=jsonp"
    try:
        res = requests.get(url=url, headers=headers)
        dictory = json.loads(res.text)
        if "data" in dictory:
            data = dictory["data"][0]
            return data["cid"]
    except:
        return


def create_thread_file(thread_count, total_data, start_point):
    thread_dict = {}
    size = total_data[0] / thread_count[0]
    thread_dict['block_size'] = size

    for i in range(thread_count[0]):
        thread_dict['t' + str(i)] = \
            {
                "start": start_point[0] + size * i,
                "current": start_point[0] + size * i,
                "goal": start_point[0] + size * (i + 1)
            }

    json_object = json.dumps(thread_dict, indent=4)

    with open(thread_file_path, "w") as f:
        f.write(json_object)


def read_thread_file():
    global block_size
    with open(thread_file_path, 'r') as f:
        json_object = json.load(f)

    for (tid, data) in json_object.items():
        if tid == 'block_size':
            block_size = int(data)
        else:
            aid.append(int(data["current"]))
            goal.append(int(data["goal"]))
            start.append(int(data["start"]))
            fail.append(0)
            total.append(0)


def read_keywords_file():
    with open(keywords_file_path, 'r') as f:
        for line in f.readlines():
            keyword_list.append(line.replace('\n', ''))


def read_results_file():
    global result_dict
    if os.path.exists(result_file_path):
        with open(result_file_path, 'r') as f:
            result_dict = json.load(f)
    else:
        result_dict = {}


def main():
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('-s', metavar='N', type=int, nargs=1, default=[0], dest='start_aid',
                        help='where to start')
    parser.add_argument('-c', metavar='N', type=int, nargs=1, default=[1000000], dest='data_count',
                        help='how many data to be searched')
    parser.add_argument('-t', metavar='N', type=int, nargs=1, default=[10], dest='threads_count',
                        help='the number of threads for searching')

    parser.add_argument('--new', dest='newSearch', action='store_true',
                        default=False,
                        help='continue search')

    args = parser.parse_args()

    if args.newSearch or not os.path.exists(thread_file_path):
        create_thread_file(args.threads_count, args.data_count, args.start_aid)

    read_thread_file()
    read_keywords_file()
    read_results_file()

    for i in range(0, len(aid)):
        threads.append(threading.Thread(target=get_data, args=(i,)))
        threads[i].start()

    threads.append(threading.Thread(target=save_progress, ))
    threads[len(aid)].start()


def cls():
    print('\n' * 100)


def print_progress():
    for i in range(len(aid)):
        print("thread", i, end=": |")
        progress = int(((aid[i] - start[i]) / block_size) * 100)
        for j in range(progress):
            print("-", end="")
        for j in range(100 - progress):
            print(" ", end="")

        print("|", progress, "%", end=" ")
        print(aid[i] - 1, "/", goal[i], end=", ")
        print("miss rate:", "null" if total[i] == 0 else fail[i] / total[i])

    sum_aid = sum([aid[i] - 1 - start[i] for i in range(len(aid))])
    overall_progress = (sum_aid / (block_size * len(aid))) * 100
    print("overall:", overall_progress, "%")
    return overall_progress


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
