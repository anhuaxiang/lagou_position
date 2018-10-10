import os
import re
import csv
import time
import requests
import pandas as pd
from lxml import etree
from get_list_data import headers


def read_csv(file_name):
    position_urls = []
    with open(file_name, 'r', newline='') as file_test:
        reader = csv.reader(file_test)
        i = 0
        for row in reader:
            if i != 0:
                url = 'https://www.lagou.com/jobs/' + row[-1]+'.html'
                position_urls.append(url)
            i += 1
    return position_urls


def write_file(content, file_name):
    with open(file_name, 'a+') as test_file:
        test_file.write(content)


def get_detail_info(position_urls):
    index = 1
    for url in position_urls:
        work_duty = ''
        work_requirement = ''
        response = requests.get(url, headers=headers)
        response = etree.HTML(response.text)
        content = response.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
        j = 0
        i = 0
        for i in range(len(content)):
            content[i] = content[i].replace('\xa0', ' ')
            if content[i][0].isdigit():
                if j == 0:
                    content[i] = content[i][2:].replace('、', ' ')
                    content[i] = re.sub('[；;.0-9。]', '', content[i])
                    work_duty = work_duty + content[i] + '/'
                    j += 1
                elif content[i][0] == '1' and not content[i][1].isdigit():
                    break
                else:
                    content[i] = content[i][2:].replace('、', ' ')
                    content[i] = re.sub('[、；;.0-9。]', '', content[i])
                    work_duty = work_duty + content[i] + '/'
        m = i
        write_file(work_duty, 'work_duty.txt')
        print(work_duty)
        j = 0
        for i in range(m, len(content)):
            content[i] = content[i].replace('\xa0', ' ')
            if content[i][0].isdigit():
                if j == 0:
                    content[i] = content[i][2:].replace('、', ' ')
                    content[i] = re.sub('[、；;.0-9。]', '', content[i])
                    work_requirement = work_requirement + content[i] + '/'
                    j += 1
                elif content[i][0] == '1' and not content[i][1].isdigit():
                    # 控制范围
                    break
                else:
                    content[i] = content[i][2:].replace('、', ' ')
                    content[i] = re.sub('[、；;.0-9。]', '', content[i])
                    work_requirement = work_requirement + content[i] + '/'
        write_file(work_requirement, 'work_requirement.txt')
        print(work_requirement)
        print('------------------分割线------------------------')
        print(f'----------------{index}-----------------------')
        print('------------------分割线------------------------')
        index += 1


def main():
    get_detail_info(read_csv('Python爬虫.csv'))


if __name__ == '__main__':
    main()