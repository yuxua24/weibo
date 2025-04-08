import requests
import csv
import os
import numpy as np
def init():
    if not os.path.exists('navData.csv'):
        with open('navData.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'typeName',
                'gid',
                'containerid'
            ])

def wirterRow(row):
        with open('navData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)
            print("写入成功")

def get_html(url):
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Cookie':'SCF=AkJxNyYT1-5RVVjecrxMBEiTtWcAzcfIkYKfZ4hnBHBDe8zWqYW_OJfzx0Cbq9gwAjgWxPno1rPqlfFDOZnXoM4.; SUB=_2A25K9z3ZDeRhGeFI71IR9CjIyDqIHXVpjT8RrDV8PUNbmtANLWLMkW9NfTRDyWmcWYEFaRdz6sTDf9bOFWk92aQa; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFcxJGphFqlqWo56EE1HyKf5JpX5KzhUgL.FoMcSh57ShqXe0q2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSoB7ehBcShec; ALF=02_1746590345; WBPSESS=VTEPjf_RFwWTHzUC-69fIAQjGPjChq0qRWT2n14MX-UBuwtg-rq5-y7UxqsOi43gg1qVMAN5JhOmpEBwQQ8NLhwNPTxJ9c6Fd0EVi1zO3ofW3WwX37GTXxqodPEKLmvDoJtKba_sJATweqKrrUz-8w==; XSRF-TOKEN=essmYgf_OXVzQ_oGEWOF-jOg; PC_TOKEN=4aaed72387'
    }
    params = {
        'is_new_segment':1,
        'fetch_hot':1
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response):
    navList = np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    for nav in navList:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        wirterRow([
            navName,
            gid,
            containerid,
        ])

if __name__ == '__main__':
    url = 'https://weibo.com/ajax/feed/allGroups'
    init()
    response = get_html(url)
    parse_json(response)