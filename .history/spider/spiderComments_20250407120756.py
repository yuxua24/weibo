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
        'Cookie':'SINAGLOBAL=1139663897103.056.1665663045813; UOR=,,login.sina.com.cn; XSRF-TOKEN=KtBvgmv_E_xz6tXecy8aXUCt; login_sid_t=21ac5180d59b66e852a1bdd51c07c991; cross_origin_proto=SSL; _s_tentry=weibo.com; Apache=9843086827913.645.1691305673041; ULV=1691305673044:17:1:1:9843086827913.645.1691305673041:1681187066075; wb_view_log=1920*10801; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5V8K5qGyCrwGNY_OGZyV-n5JpX5o275NHD95QNeoeRe05Xe0MRWs4DqcjVi--4iK.Ri-isi--fiK.pi-2Ri--Xi-zRiKy2i--fiK.7iKn0i--4i-zpi-ihP7tt; SSOLoginState=1691305688; SCF=AsgHzaOR1bpjw8Hrr2jBXHXlx-poji6oDUSYps9xJdaN4I3YujAxtvuB-sHstj9sI1715awPIp4c3jrJCSKi_Oo.; SUB=_2A25JyzaJDeRhGeFM6FoS8CrPzDSIHXVqoS9BrDV8PUNbmtANLWz4kW9NQMc5ghU_rpqoaEe8yK-gCmUdceGx4u7-; ALF=1722841688; WBPSESS=P4aOuTPLj_7JdYdRZmhiB8bOEDR0t13rm6FdGGg-L5Rc6JXM2Ot4b_qQl1mSKTL8bBmEY2LOFz37q7GfDYn4t0xGCbO_tiSBh9BKdhvEkhzEQPbL_v_fignVIkaOk4ki9Cs60UzbTDs7c8nulOdDxA=='
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