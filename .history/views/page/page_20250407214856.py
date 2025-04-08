from flask import Flask, session, render_template, redirect, Blueprint, request, flash
from utils import getHomeData, getTableData, getEchartsData
from snownlp import SnowNLP

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')

@pb.route('/home')
def home():
    username = session.get('username')
    topFiveComments = getHomeData.getHomeTopLikeCommentsData()
    articleLen, maxLikeAuthorName, maxCity = getHomeData.getTagData()
    xData, yData = getHomeData.getCreatedNumEchartsData()
    userCreatedDicData = getHomeData.getTypeCharData()
    commentUserCreatedDicData = getHomeData.getCommentsUserCratedNumEchartsData()
    return render_template('index.html',
                         username=username,
                         topFiveComments=topFiveComments,
                         articleLen=articleLen,
                         maxLikeAuthorName=maxLikeAuthorName,
                         maxCity=maxCity,
                         xData=xData,
                         yData=yData,
                         commentUserCreatedDicData=commentUserCreatedDicData,
                         userCreatedDicData=userCreatedDicData
                         )

@pb.route('/tableData')
def tabelData():
    username = session.get('username')
    hotWordList = getTableData.getTableDataPageData()
    
    # 获取用户输入的热词
    user_input = request.args.get('hotWord', '').strip()
    hotWord_exists = True
    
    # 处理热词选择
    if user_input:
        # 用户输入了热词，检查是否存在
        defaultHotWord = user_input
        defaultHotWordNum = 0
        
        # 检查热词是否存在
        found = False
        for hotWord, count in hotWordList:
            if defaultHotWord == hotWord:
                defaultHotWordNum = count
                found = True
                break
        
        if not found:
            hotWord_exists = False
            flash(f"未找到热词 '{defaultHotWord}' 的相关数据", 'warning')
    else:
        # 没有输入则使用第一个热词
        defaultHotWord = hotWordList[0][0] if hotWordList else ''
        defaultHotWordNum = hotWordList[0][1] if hotWordList else 0

    # 情感分析
    emotionValue = '未知'
    if defaultHotWord and hotWord_exists:
        sentiment = SnowNLP(defaultHotWord).sentiments
        if sentiment > 0.5:
            emotionValue = '正面'
        elif sentiment == 0.5:
            emotionValue = '中性'
        else:
            emotionValue = '负面'

    # 获取数据
    tableList = []
    xData, yData = [], []
    if hotWord_exists and defaultHotWord:
        tableList = getTableData.getTableData(defaultHotWord)
        xData, yData = getTableData.getTableDataEchartsData(defaultHotWord)

    return render_template('tableData.html',
                         username=username,
                         hotWordList=hotWordList,
                         defaultHotWord=defaultHotWord,
                         defaultHotWordNum=defaultHotWordNum,
                         emotionValue=emotionValue,
                         tableList=tableList,
                         xData=xData,
                         yData=yData,
                         hotWord_exists=hotWord_exists
                         )

@pb.route('/tableDataArticle')
def tableDataArticle():
    username = session.get('username')
    defaultFlag = False
    if request.args.get('flag'): defaultFlag = request.args.get('flag')
    tableData = getTableData.getTableDataArticle(defaultFlag)
    return render_template('tableDataArticle.html',
                         username=username,
                         defaultFlag=defaultFlag,
                         tableData=tableData
                         )

@pb.route('/articleChar')
def articleChar():
    username = session.get('username')
    typeList = getEchartsData.getTypeList()
    defaultType = typeList[0]
    if request.args.get('type'): defaultType = request.args.get('type')
    xData, yData = getEchartsData.getArticleCharOneData(defaultType)
    x1Data, y1Data = getEchartsData.getArticleCharTwoData(defaultType)
    x2Data, y2Data = getEchartsData.getArticleCharThreeData(defaultType)
    return render_template('articleChar.html',
                         username=username,
                         typeList=typeList,
                         defaultType=defaultType,
                         xData=xData,
                         yData=yData,
                         x1Data=x1Data,
                         y1Data=y1Data,
                         x2Data=x2Data,
                         y2Data=y2Data
                         )

@pb.route('/ipChar')
def ipChar():
    username = session.get('username')
    geoDataOne = getEchartsData.getGeoCharDataOne()
    geoDataTwo = getEchartsData.getGeoCharDataTwo()
    return render_template('ipChar.html',
                         username=username,
                         geoDataOne=geoDataOne,
                         geoDataTwo=geoDataTwo
                         )

@pb.route('/commentChar')
def commentChar():
    username = session.get('username')
    xData, yData = getEchartsData.getCommetCharDataOne()
    genderDicData = getEchartsData.getCommetCharDataTwo()
    return render_template('commentChar.html',
                         username=username,
                         xData=xData,
                         yData=yData,
                         genderDicData=genderDicData
                         )

@pb.route('/yuqingChar')
def yuqingChar():
    username = session.get('username')
    xData, yData, bieData = getEchartsData.getYuQingCharDataOne()
    bieData1, bieData2 = getEchartsData.getYuQingCharDataTwo()
    x1Data, y1Data = getEchartsData.getYuQingCharDataThree()
    return render_template('yuqingChar.html',
                         username=username,
                         xData=xData,
                         yData=yData,
                         bieData=bieData,
                         bieData1=bieData1,
                         bieData2=bieData2,
                         x1Data=x1Data[:10],
                         y1Data=y1Data[:10]
                         )

@pb.route('/contentCloud')
def contentCloud():
    username = session.get('username')
    return render_template('contentCloud.html',
                         username=username
                         )