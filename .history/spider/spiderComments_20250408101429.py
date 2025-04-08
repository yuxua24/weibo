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
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Cookie':'SCF=AkJxNyYT1-5RVVjecrxMBEiTtWcAzcfIkYKfZ4hnBHBDe8zWqYW_OJfzx0Cbq9gwAjgWxPno1rPqlfFDOZnXoM4.; XSRF-TOKEN=zlpd3d-Pfw45mvffv7_Qyf8c; SUB=_2A25K9z3ZDeRhGeFI71IR9CjIyDqIHXVpjT8RrDV8PUNbmtANLWLMkW9NfTRDyWmcWYEFaRdz6sTDf9bOFWk92aQa; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFcxJGphFqlqWo56EE1HyKf5JpX5KzhUgL.FoMcSh57ShqXe0q2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSoB7ehBcShec; ALF=02_1746590345; WBPSESS=VTEPjf_RFwWTHzUC-69fIAQjGPjChq0qRWT2n14MX-UBuwtg-rq5-y7UxqsOi43gg1qVMAN5JhOmpEBwQQ8NLhwNPTxJ9c6Fd0EVi1zO3ofW3WwX37GTXxqodPEKLmvDoJtKba_sJATweqKrrUz-8w=='
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