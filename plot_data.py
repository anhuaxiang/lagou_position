import re
import csv
import math
import jieba
import numpy as np
import pandas as pd
from pyecharts import TreeMap, Pie, Bar, WordCloud


def read_detail_data_from_csv(file_name, col=0):
    education = []
    with open(file_name, 'r', newline='') as file_test:
        reader = csv.reader(file_test)
        i = 0
        for row in reader:
            if i != 0:
                education.append(row[col])
            i += 1
    return education


def plot_education_tree():
    education = read_detail_data_from_csv('Python爬虫.csv', col=1)
    education_table = {}
    for x in education:
        education_table[x] = education.count(x)

    key = []
    values = []
    for k, v in education_table.items():
        key.append(k)
        values.append(v)

    data = []
    for i in range(len(key)):
        dict_01 = {'value': values[i], 'name': key[i]}
        data.append(dict_01)

    tree_map = TreeMap('矩形树图', width=1200, height=600)
    tree_map.add('学历要求', data, is_label_show=True, label_pos='inside')
    tree_map.render('tree.html')


def assort_salary(str_01):
    reg_str01 = "(\d+)"
    res_01 = re.findall(reg_str01, str_01)
    if len(res_01) == 2:
        a0 = int(res_01[0])
        b0 = int(res_01[1])
    else:
        a0 = int(res_01[0])
        b0 = int(res_01[0])
    return (a0+b0)/2


def plot_salary_bing():
    salary = read_detail_data_from_csv('Python爬虫.csv', col=0)
    salary_table = {}
    for x in salary:
        salary_table[x] = salary.count(x)
    key = ['5k以下', '5k-10k', '10k-20k', '20k-30k', '30k-40k', '40k以上']
    a0, b0, c0, d0, e0, f0 = [0, 0, 0, 0, 0, 0]
    for k, v in salary_table.items():
        ave_salary = math.ceil(assort_salary(k))
        print(ave_salary)
        if ave_salary < 5:
            a0 = a0 + v
        elif ave_salary in range(5, 10):
            b0 = b0 + v
        elif ave_salary in range(10, 20):
            c0 = c0 + v
        elif ave_salary in range(20, 30):
            d0 = d0 + v
        elif ave_salary in range(30, 40):
            e0 = e0 + v
        else:
            f0 = f0 + v
    values = [a0, b0, c0, d0, e0, f0]

    pie = Pie("薪资玫瑰图", title_pos='center', width=900)
    pie.add("salary", key, values, center=[40, 50], is_random=True, radius=[30, 75], rosetype="area",
            is_legend_show=False, is_label_show=True)
    pie.render(path='bing.html')


def plot_work_year_zhu():
    work_year = read_detail_data_from_csv('Python爬虫.csv', col=2)
    work_year_table = {}
    for x in work_year:
        work_year_table[x] = work_year.count(x)
    key = []
    value = []
    for k, v in work_year_table.items():
        key.append(k)
        value.append(v)
    bar = Bar('柱状图')
    bar.add('work_year', key, value, is_stack=True, center=(40, 60))
    bar.render('zhu.html')


def plot_detail_word_cloud(file_name):
    stopwords_path = 'stopword.txt'
    with open(file_name, encoding='gbk') as file:
        text = file.read()
        content = text
        content = re.sub('[,，.。\r\n]', '', content)
        segment = jieba.lcut(content)
        words_df = pd.DataFrame({'segment': segment})
        stopwords = pd.read_csv(stopwords_path, index_col=False, quoting=3, sep="\t", names=['stopword'], encoding='gbk')
        words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
        words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": np.size})
        words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
        test = words_stat.head(200).values
        codes = [test[i][0] for i in range(0, len(test))]
        counts = [test[i][1] for i in range(0, len(test))]
        wordcloud = WordCloud(width=1300, height=620)
        wordcloud.add(file_name.split('.')[0], codes, counts, word_size_range=[20, 100])
        wordcloud.render(file_name.split('.')[0] + "word_cloud.html")


if __name__ == '__main__':
    plot_education_tree()
    plot_salary_bing()
    plot_work_year_zhu()
    plot_detail_word_cloud('work_requirement.txt')
    plot_detail_word_cloud('work_duty.txt')
