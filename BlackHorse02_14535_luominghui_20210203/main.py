import pandas as pd
import requests
from bs4 import BeautifulSoup


# 构造每一页的url，返回该页面的html代码
def get_html_content(url_base, page_id):
    url = url_base + str(page_id) + '.shtml'
    #print(url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'}
    html = requests.get(url, headers=headers, timeout=10)
    content = html.text
    return content


# 遍历指定范围页面的html代码，逐行获取表格中的数据，返回DataFrame格式的数据
def analyze_content(url_base, page_range):
    df = pd.DataFrame(columns=['id', 'brand', 'series', 'model', 'abstract', 'problems', 'time', 'status'])
    temp = {}
    for i in range(page_range):
        content = get_html_content(url_base, i + 1)
        bs = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
        tr_list = bs.find_all('tr')
        for tr in tr_list[1:]:
            td_list = tr.find_all('td')
            temp['id'] = td_list[0].string
            temp['brand'] = td_list[1].string
            temp['series'] = td_list[2].string
            temp['model'] = td_list[3].string
            temp['abstract'] = td_list[4].string
            temp['problems'] = td_list[5].string
            temp['time'] = td_list[6].string
            # 最后一个状态信息在td的em标签中
            temp['status'] = td_list[7].em.string
            df = df.append(temp, ignore_index=True)
            #print(temp)
        #print(df)
    return df


if __name__ == '__main__':
    url_base = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-'
    page_range = 10
    data = analyze_content(url_base, page_range)
    # 将DataFrame格式的数据输出到excel表格中
    data.to_excel('.\car_complain_20210204.xlsx', index=False)
    # 查看获取到的数据
    df = pd.read_excel('.\car_complain_20210204.xlsx')
    df.head()
