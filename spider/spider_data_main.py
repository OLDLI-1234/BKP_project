import csv
import json
import re
import os
import sys
import requests
from pymysql import *
from utils.query import querys

# 房名 封面 市区 地区 详情地址 房型详情 建面 是否具有预售证 每平价格 房屋的装修情况（毛坯，简装修） 公司 房屋类型（别墅） 交房时间 开盘时间 标签 总价区间 售房情况（在售）  详情链接

def init():
    if not os.path.exists('./hourseInfoData.csv'):
        with open('./hourseInfoData.csv','w',encoding='utf-8',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'title',
                'cover',
                'city',
                'region',
                'address',
                'rooms_desc',
                'area_range',
                'all_ready',
                'price',
                'hourseDecoration',
                'company',
                'hourseType',
                'on_time',
                'open_date',
                'tags',
                'totalPrice_range',
                'sale_status',
                'detail_url'
            ])

def writerRow(row):
    with open('./hourseInfoData.csv', 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'cookie':'lianjia_uuid=75d60c76-ce9b-4101-ac09-57ac4f563814; _smt_uid=649be54d.ac72699; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218900f7b917a16-060e71bafc7b5a-26031f51-2073600-18900f7b918ef0%22%2C%22%24device_id%22%3A%2218900f7b917a16-060e71bafc7b5a-26031f51-2073600-18900f7b918ef0%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; _ga=GA1.2.1631881632.1687938384; _ga_4JBJY7Y7MX=GS1.2.1687938383.1.0.1687938383.0.0.0; _jzqx=1.1687944603.1688020170.2.jzqsr=xianyang%2Efang%2Elianjia%2Ecom|jzqct=/loupan/pg2/.jzqsr=bj%2Efang%2Elianjia%2Ecom|jzqct=/; _ga_6DHGZS4SHY=GS1.2.1688020170.2.1.1688021583.0.0.0; _gid=GA1.2.1320906752.1689149404; _jzqc=1; _jzqckmp=1; _jzqa=1.4022756256930896000.1687938382.1687938382.1687938382.1; _jzqa=1.4022756256930896000.1687938382.1687938382.1689150109.2; _jzqc=1; _jzqy=1.1687938382.1689150109.1.jzqsr=baidu.-; _jzqckmp=1; _qzjc=1; lianjia_ssid=03697d91-fb1e-4a6b-b9f9-ddf69b592d29; _jzqb=1.2.10.1689150109.1; _ga_KJTRWRHDL1=GS1.2.1689150113.1.1.1689150236.0.0.0; _ga_QJN1VP0CMS=GS1.2.1689150113.1.1.1689150237.0.0.0; _ga_RCTBRFLNVS=GS1.2.1689149407.9.1.1689150241.0.0.0; select_city=130600; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; lj_newh_session=eyJpdiI6ImprODRHSEFLbHh4cmxTdVJadEtwaFE9PSIsInZhbHVlIjoiVHRIbnBMMlI2R3ZWazVQdEgzMzU1Z1R0Z3U2K3haaWFIN0dtZkc1N0huazMzMFhlUDFJTDRtUndYakpQTFpBYVl6UjVXQlwvNUxodlZiSlRNQ291eUJnPT0iLCJtYWMiOiI3MzJmMDUxYzAyNDE5MjVkMDgyZDk0ZDVhNjI0NTM4NDUwY2U3MWU1NWQ4MzMwY2IxNmY5MjVmNDU2OGJhMDQxIn0%3D; digData=%7B%22key%22%3A%22loupan_index%22%7D; _qzja=1.333215935.1687940937448.1688884242924.1689150142200.1689150533981.1689150540623.0.0.0.9.5; _qzjb=1.1689150142200.3.0.0.0; _qzjto=3.1.0; _jzqb=1.3.10.1689150109.1; srcid=eyJ0IjoiXCJ7XFxcImRhdGFcXFwiOlxcXCI2Zjk1ODVhYWIyOWRiNWQzOGNkMjE3MjEzMzI4MmExZDViODE3MWM4ZmFjNmQ2MTliYzA2NDNkNzI5YzQ4YmJjMmY4MmUzOWNjYzhlMTA5ZDQyM2YzZTAyYTY5OGI4OTFiMThlZTQ5MGZjYjBkMGU4MTIxMDIyYmVhYzk4MDI1NGZmMGJjYmIzNjg3NTg1Zjg3ZTQxNWFmMjFiZTZhNzFhNDYxZTE4OGEyY2EwNGViYTk0MmFjZjVmZjVmZGU1YTQ5OTIzOThhZTFjMDVmMzg4YWExN2U3MWQ3YWZiZmY2ZmQyMzBmZjZhZjE4NTYwNWMwYmM3MGMwYzZkZjBlZGQyXFxcIixcXFwia2V5X2lkXFxcIjpcXFwiMVxcXCIsXFxcInNpZ25cXFwiOlxcXCIyOTAxNWJmNFxcXCJ9XCIiLCJyIjoiaHR0cHM6Ly9iZC5mYW5nLmxpYW5qaWEuY29tL2xvdXBhbi8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
        'Referer':'https://bd.fang.lianjia.com/loupan/pg2/'
    }
    response = requests.get(url,headers)
    if response.status_code == 200:
        return response.json()['data']['list']
    else:
        return None

def parse_data(hourseDataList,city,url):
    for hourseInfo in hourseDataList:
            title = hourseInfo['title']
            cover = hourseInfo['cover_pic']
            region = hourseInfo['district']
            address = hourseInfo['address']
            rooms_desc = json.dumps(hourseInfo['frame_rooms_desc'].replace('居', '').split('/'))
            area_range = json.dumps(hourseInfo['resblock_frame_area_range'].replace('㎡', '').split('-'))
            all_ready = hourseInfo['permit_all_ready']
            price = hourseInfo['average_price']
            hourseDecoration = hourseInfo['decoration']
            company = hourseInfo['developer_company'][0]
            hourseType = hourseInfo['house_type']
            on_time = hourseInfo['on_time']
            open_date = hourseInfo['open_date']
            tags = json.dumps(hourseInfo['tags'])
            totalPrice_range = json.dumps(hourseInfo['reference_total_price'].split('-'))
            sale_status = hourseInfo['process_status']
            detail_url = 'https://' + re.search('//(.*)/loupan/pg\d/\?_t=1', url).group(1) + hourseInfo['url']
            writerRow([
                title,
                cover,
                city,
                region,
                address,
                rooms_desc,
                area_range,
                all_ready,
                price,
                hourseDecoration,
                company,
                hourseType,
                on_time,
                open_date,
                tags,
                totalPrice_range,
                sale_status,
                detail_url
            ])

def save_to_sql():
    with open('./hourseInfoData.csv','r',encoding='utf-8') as reader:
        readerCsv = csv.reader(reader)
        next(readerCsv)
        for h in readerCsv:
            querys('''
                insert into hourse_info(title,cover,city,region,address,rooms_desc,area_range,all_ready,price,hourseDecoration,company,hourseType,on_time,open_date,tags,totalPrice_range,sale_status,detail_url)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''',[
                h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10], h[11], h[12], h[13], h[14], h[15],
                h[16], h[17]
            ])

def main():
    init()
    with open('./cityData.csv','r',encoding='utf-8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for city in reader:
                try:
                    for page in range(1, 10):
                        url = 'https:' + re.sub('pg1', 'pg' + str(page), city[1])
                        print('正在爬取 %s 城市的房屋数据正在第 %s 页 路径为：%s' % (
                            city[0],
                            page,
                            url
                        ))
                        hourseDetailList = get_data(url)
                        parse_data(hourseDetailList, city[0], url)
                except:
                    pass


if __name__ == '__main__':
    # main()
    save_to_sql()