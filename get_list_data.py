import os
import csv
import time
import requests
import pandas as pd


position = ['Python爬虫', '数据分析', '后端', '数据挖掘', '全栈开发', '运维开发', '高级开发工程师', '大数据', '机器学习', '架构师']
request_url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Connection': 'keep-alive',
    'Cookie': 'user_trace_token=20180926183010-df3e9065-10cc-4657-b02f-090076ff5d06; _ga=GA1.2.945176530.1537957812; LGUID=20180926183012-266ff349-c177-11e8-bb60-5254005c3644; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216619f4faba483-014916f4c9f73d-5e442e19-1327104-16619f4fabb58c%22%2C%22%24device_id%22%3A%2216619f4faba483-014916f4c9f73d-5e442e19-1327104-16619f4fabb58c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LG_LOGIN_USER_ID=f6b481957737bc30d6c674259eca10eff608af539f0753a3; index_location_city=%E5%8C%97%E4%BA%AC; WEBTJ-ID=20181010095705-1665bb11b3d228-020c216d2d3221-5e442e19-1327104-1665bb11b3e3c; _gid=GA1.2.1812894684.1539136626; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1538185111,1538219606,1538410588,1539136627; LGSID=20181010095707-cb2fbffa-cc2f-11e8-bba8-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3DUTF-8%26wd%3D%25E6%258B%2589%25E5%258B%25BE%26from%3Dcentbrowser; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; JSESSIONID=ABAAABAAAGFABEF6BD801ECDC05B0A4AA0BD07E4EB14A36; LGRID=20181010095717-d0c4eb74-cc2f-11e8-bba8-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1539136637; TG-TRACK-CODE=index_search; SEARCH_ID=d35e41d98f0849a99716356d82ccb990',
    'Host': 'www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36,',
}


def file_do(list_info, p):
    file_name = p + '.csv'
    file_size = None
    try:
        file_size = os.path.getsize(file_name)
    except:
        name = ['薪资', '学历要求', '工作经验', 'id']
        file_test = pd.DataFrame(columns=name, data=list_info)
        file_test.to_csv(file_name, encoding='gbk', index=False)
    if file_size:
        with open(file_name, 'a+', newline='') as file_test:
            writer = csv.writer(file_test)
            writer.writerows(list_info)


def get_info(p):
    for i in range(1, 31):
        data = {
            'first': 'true',
            'kd': p,
            'pn': i
        }
        request_result = requests.post(request_url, data=data, headers=headers)
        request_result.encoding = 'utf-8'
        print(f'第{i}页, 状态码为{request_result.status_code}')
        request_info = request_result.json()
        request_info = request_info['content']['positionResult']['result']
        print(len(request_info))
        list_info = []
        for j in range(0, len(request_info)):
            position_id = request_info[j]['positionId']
            salary = request_info[j]['salary']
            education = request_info[j]['education']
            work_year = request_info[j]['workYear']
            list_info.append([salary, education, work_year, position_id])
        print(list_info)
        file_do(list_info, p)
        time.sleep(2)


def main():
    for p in position:
        get_info(p)

if __name__ == '__main__':
    main()
