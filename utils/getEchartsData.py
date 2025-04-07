from utils import getPublicData
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image                   # 图片处理
import numpy as np
from snownlp import SnowNLP

def getTypeList():
    typeList = list(set([x[8] for x in getPublicData.getAllData()]))
    return typeList

def getArticleCharOneData(defaultType):
    articleList = getPublicData.getAllData()
    xData = []
    rangeNum = 1000
    for item in range(1,15):
        xData.append(str(rangeNum * item)+ '-' + str(rangeNum*(item+1)))
    yData = [0 for x in range(len(xData))]
    for article in articleList:
        if article[8] != defaultType:
            for item in range(14):
                if int(article[1]) < rangeNum*(item+2):
                    yData[item] += 1
                    break
    return xData,yData

def getArticleCharTwoData(defaultType):
    articleList = getPublicData.getAllData()
    xData = []
    rangeNum = 1000
    for item in range(1,15):
        xData.append(str(rangeNum * item)+ '-' + str(rangeNum*(item+1)))
    yData = [0 for x in range(len(xData))]
    for article in articleList:
        if article[8] != defaultType:
            for item in range(14):
                if int(article[2]) < rangeNum*(item+2):
                    yData[item] += 1
                    break
    return xData,yData

def getArticleCharThreeData(defaultType):
    articleList = getPublicData.getAllData()
    xData = []
    rangeNum = 50
    for item in range(1, 30):
        xData.append(str(rangeNum * item) + '-' + str(rangeNum * (item + 1)))
    yData = [0 for x in range(len(xData))]
    for article in articleList:
        if article[8] != defaultType:
            for item in range(29):
                if int(article[2]) < rangeNum * (item + 2):
                    yData[item] += 1
                    break
    return xData, yData

def getGeoCharDataTwo():
    cityList = getPublicData.cityList
    commentList = getPublicData.getAllCommentsData()
    cityDic = {}
    for comment in commentList:
        if comment[3] == '无': continue
        for j in cityList:
            if j['province'].find(comment[3]) != -1:
                if cityDic.get(j['province'], -1) == -1:
                    cityDic[j['province']] = 1
                else:
                    cityDic[j['province']] += 1

    cityDicList = []
    for key, value in cityDic.items():
        cityDicList.append({
            'name': key,
            'value': value
        })
    return cityDicList


def getGeoCharDataOne():
    cityList = getPublicData.cityList
    articleList = getPublicData.getAllData()

    cityDic = {}
    for article in articleList:
        if article[4] == '无':continue
        for j in cityList:
                if j['province'].find(article[4]) != -1:
                    if cityDic.get(j['province'],-1) == -1:
                        cityDic[j['province']] = 1
                    else:
                        cityDic[j['province']] += 1

    cityDicList = []
    for key, value in cityDic.items():
        cityDicList.append({
            'name': key,
            'value': value
        })
    return cityDicList

def getCommetCharDataOne():
    commentList = getPublicData.getAllCommentsData()
    xData = []
    rangeNum = 20
    for item in range(1, 100):
        xData.append(str(rangeNum * item) + '-' + str(rangeNum * (item + 1)))
    yData = [0 for x in range(len(xData))]
    for comment in commentList:
            for item in range(99):
                if int(comment[2]) < rangeNum * (item + 2):
                    yData[item] += 1
                    break
    return xData, yData

def getCommetCharDataTwo():
    commentList = getPublicData.getAllCommentsData()
    genderDic = {}
    for i in commentList:
        if genderDic.get(i[6],-1) == -1:
            genderDic[i[6]] = 1
        else:
            genderDic[i[6]] += 1
    resultData = [{
        'name':x[0],
        'value':x[1]
    } for x in genderDic.items()]
    return resultData

def stopwordslist():
    stopwords = [line.strip() for line in open('./model/stopWords.txt',encoding='UTF-8').readlines()]
    return stopwords

def getContentCloud():
    text = ''
    stopwords = stopwordslist()
    articleList = getPublicData.getAllData()
    for article in articleList:
        text += article[5]
    cut = jieba.cut(text)
    newCut = []
    for word in cut:
        if word not in stopwords: newCut.append(word)
    string = ' '.join(newCut)
    img = Image.open('./static/content.jpg')  # 打开遮罩图片
    img_arr = np.array(img)  # 将图片转化为列表
    wc = WordCloud(
        width=1000, height=600,
        background_color='white',
        colormap='Blues',
        font_path='STHUPO.TTF',
        mask=img_arr,
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴

    # 显示生成的词语图片
    # plt.show()

    # 输入词语图片到文件

    plt.savefig('./static/contentCloud.jpg', dpi=500)

def getCommentContentCloud():
    text = ''
    stopwords = stopwordslist()
    commentsList = getPublicData.getAllCommentsData()
    for comment in commentsList:
        text += comment[4]
    cut = jieba.cut(text)
    newCut = []
    for word in cut:
        if word not in stopwords:newCut.append(word)
    string = ' '.join(newCut)
    img = Image.open('./static/comment.jpg')  # 打开遮罩图片
    img_arr = np.array(img)  # 将图片转化为列表
    wc = WordCloud(
        width=1000, height=600,
        background_color='white',
        colormap='Blues',
        font_path='STHUPO.TTF',
        mask=img_arr,
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴

    # 显示生成的词语图片
    # plt.show()

    # 输入词语图片到文件

    plt.savefig('./static/commentCloud.jpg', dpi=500)

def getYuQingCharDataOne():
    hotWordList = getPublicData.getAllCiPingTotal()
    xData = ['正面', '中性', '负面']
    yData = [0,0,0]
    for hotWord in hotWordList:
        emotionValue = SnowNLP(hotWord[0]).sentiments
        if emotionValue > 0.5:
            yData[0] +=1
        elif emotionValue == 0.5:
            yData[1] += 1
        elif emotionValue < 0.5:
            yData[2] += 1
    bieData = [{
        'name': '正面',
        'value': yData[0]
    }, {
        'name': '中性',
        'value': yData[1]
    }, {
        'name': '负面',
        'value': yData[2]
    }]
    return xData,yData,bieData

def getYuQingCharDataTwo():
    bieData1 = [{
        'name':'正面',
        'value':0
    },{
        'name':'中性',
        'value':0
    },{
        'name':'负面',
        'value':0
    }]
    bieData2 = [{
        'name': '正面',
        'value': 0
    }, {
        'name': '中性',
        'value': 0
    }, {
        'name': '负面',
        'value': 0
    }]

    commentList = getPublicData.getAllCommentsData()
    articleList = getPublicData.getAllData()

    for comment in commentList:
        emotionValue = SnowNLP(comment[4]).sentiments
        if emotionValue > 0.5:
            bieData1[0]['value'] += 1
        elif emotionValue == 0.5:
            bieData1[1]['value'] += 1
        elif emotionValue < 0.5:
            bieData1[2]['value'] += 1
    for article in articleList:
        emotionValue = SnowNLP(article[5]).sentiments
        if emotionValue > 0.5:
            bieData2[0]['value'] += 1
        elif emotionValue == 0.5:
            bieData2[1]['value'] += 1
        elif emotionValue < 0.5:
            bieData2[2]['value'] += 1

    return bieData1,bieData2

def getYuQingCharDataThree():
    hotWordList = getPublicData.getAllCiPingTotal()
    return [x[0] for x in hotWordList],[int(x[1]) for x in hotWordList]
