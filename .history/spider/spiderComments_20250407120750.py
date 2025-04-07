import requests
import csv
import os
from datetime import datetime
def init():
    if not os.path.exists('commentsData.csv'):
        with open('commentsData.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'articleId',
                'created_at',
                'like_counts',
                'region',
                'content',
                'authorName',
                'authorGender',
                'authorAddress',
                'authorAvatar'
            ])

def wirterRow(row):
        with open('commentsData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

def get_html(url,id):
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Cookie':'PS D:\外接项目\基于python的微博舆情监测系统\微博舆论> python -u "d:\外接项目\基于python的微博舆情监测系统\微博舆论\spider\main.py"
正在爬取文章内容...
正在爬取类型：热门中的第1页数据
Request URL: https://weibo.com/ajax/feed/hottimeline?group_id=102803&containerid=102803&max_id=0&count=10&extparam=discover%7Cnew_feed
Status Code: 200
Response Text: {"ok":1,"statuses":[{"visible":{"type":0,"list_id":0},"created_at":"Tue Apr 01 21:12:29 +0800 2025","id":5150729824114546,"idstr":"5150729824114546","mid":"5150729824114546","mblogid":"PlhIihgnE","user":{"id":7561554525,"idstr":"7561554525","pc_new":7,"screen_name":"鞠婧祎奶茶里有珍珠","profile_image_url":"https://tvax1.sinaimg.cn/crop.0.0.1023.1023.50/008fJvKRly8hzrw87l84aj30sg0sfjtw.jpg?KID=imgbed,tva&Expires=1744009490&ssig=AAkbL2CeMz","profile_url":"/u/7561554525","verified":true,"verified_type":0,"d'
    }
    params = {
        'is_show_bulletin':2,
        'id':id
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response,articleId):
    commentList = response['data']
    for comment in commentList:
        created_at = datetime.strptime(comment['created_at'],"%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        like_counts = comment['like_counts']
        authorName = comment['user']['screen_name']
        authorGender = comment['user']['gender']
        authorAddress = comment['user']['location'].split(' ')[0]
        authorAvatar = comment['user']['avatar_large']
        try:
            region = comment['source'].replace('来自','')
        except:
            region = '无'
        content = comment['text_raw']
        wirterRow([
            articleId,
            created_at,
            like_counts,
            region,
            content,
            authorName,
            authorGender,
            authorAddress,
            authorAvatar,
        ])

def start():
    init()
    url = 'https://weibo.com/ajax/statuses/buildComments'
    with open('./articleData.csv','r',encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for article in reader:
            articleId = article[0]
            response = get_html(url,articleId)
            parse_json(response,articleId)


if __name__ == '__main__':
    start()