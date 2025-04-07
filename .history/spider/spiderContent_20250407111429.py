import time
import requests
import csv
import os
import re
from datetime import datetime
def init():
    if not os.path.exists('articleData.csv'):
        with open('articleData.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'id',
                'likeNum',
                'commentsLen',
                'reposts_count',
                'region',
                'content',
                'contentLen',
                'created_at',
                'type',
                'detailUrl',# followBtnCode>uid + mblogid
                'authorAvatar',
                'authorName',
                'authorDetail',
                'isVip' # v_plus
            ])

def wirterRow(row):
        with open('articleData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

def get_json(url,params):
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Cookie':'SINAGLOBAL=1139663897103.056.1665663045813; UOR=,,login.sina.com.cn; XSRF-TOKEN=KtBvgmv_E_xz6tXecy8aXUCt; login_sid_t=21ac5180d59b66e852a1bdd51c07c991; cross_origin_proto=SSL; _s_tentry=weibo.com; Apache=9843086827913.645.1691305673041; ULV=1691305673044:17:1:1:9843086827913.645.1691305673041:1681187066075; wb_view_log=1920*10801; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5V8K5qGyCrwGNY_OGZyV-n5JpX5o275NHD95QNeoeRe05Xe0MRWs4DqcjVi--4iK.Ri-isi--fiK.pi-2Ri--Xi-zRiKy2i--fiK.7iKn0i--4i-zpi-ihP7tt; SSOLoginState=1691305688; SCF=AsgHzaOR1bpjw8Hrr2jBXHXlx-poji6oDUSYps9xJdaN4I3YujAxtvuB-sHstj9sI1715awPIp4c3jrJCSKi_Oo.; SUB=_2A25JyzaJDeRhGeFM6FoS8CrPzDSIHXVqoS9BrDV8PUNbmtANLWz4kW9NQMc5ghU_rpqoaEe8yK-gCmUdceGx4u7-; ALF=1722841688; WBPSESS=P4aOuTPLj_7JdYdRZmhiB8bOEDR0t13rm6FdGGg-L5Rc6JXM2Ot4b_qQl1mSKTL8bBmEY2LOFz37q7GfDYn4t0xGCbO_tiSBh9BKdhvEkhzEQPbL_v_fignVIkaOk4ki9Cs60UzbTDs7c8nulOdDxA=='
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response,type):
    for article in response:
        id = article['id']
        likeNum = article['attitudes_count']
        commentsLen = article['comments_count']
        reposts_count = article['reposts_count']
        try:
            region = article['region_name'].replace('发布于 ','')
        except:
            region = '无'
        content = article['text_raw']
        contentLen = article['textLength']
        created_at = datetime.strptime(article['created_at'],"%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        type = type
        try:
            detailUrl = 'https://weibo.com/' + str(article['user']['id']) +'/'+ str(article['mblogid'])
        except:
            detailUrl = '无'
        authorAvatar = article['user']['avatar_large']
        authorName = article['user']['screen_name']
        authorDetail = 'https://weibo.com' + article['user']['profile_url']
        if  article['user']['v_plus']:
            isVip = article['user']['v_plus']
        else:
            isVip = 0
        wirterRow([
                id,
                likeNum,
                commentsLen,
                reposts_count,
                region,
                content,
                contentLen,
                created_at,
                type,
                detailUrl,
                authorAvatar,
                authorName,
                authorDetail,
                isVip
            ])

def start(typeNum=10,pageNum=2):
    articleUrl = 'https://weibo.com/ajax/feed/hottimeline'
    init()
    typeNumCount = 0
    with open('./spider/nav   Data.csv','r',encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for nav in reader:
            if typeNumCount > typeNum:return
            for page in range(0,pageNum):
                time.sleep(2)
                print('正在爬取类型：' + nav[0] + '中的第' + str(page + 1) + '页数据')
                params = {
                    'group_id':nav[1],
                    'containerid':nav[2],
                    'max_id':page,
                    'count':10,
                    'extparam':'discover|new_feed'
                }
                response = get_json(articleUrl,params)
                parse_json(response['statuses'],nav[0])
            typeNumCount += 1

if __name__ == '__main__':
    start()