from spiderContent import start as contentStart
from spiderComments import start as commentsStart
import os
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('mysql+pymysql://root:123456@127.0.0.1/weibo_project?charset=utf8mb4')

# def save_to_sql():
#     try:
#         articleOldPd = pd.read_sql('select * from article', engine)
#         articleNewPd = pd.read_csv('./articleData.csv')
#         concatPd = pd.concat([articleNewPd,articleOldPd],join='inner')
#         concatPd = concatPd.drop_duplicates(subset='id', keep='last')
#         concatPd.to_sql('article',con=engine, if_exists='replace',index=False)

#         commentOldPd = pd.read_sql('select * from comments', engine)
#         commentNewPd = pd.read_csv('./commentsData.csv')
#         concatCommentPd = pd.concat([commentNewPd, commentOldPd], join='inner')
#         concatCommentPd = concatCommentPd.drop_duplicates(subset='content', keep='last')
#         concatCommentPd.to_sql('comments',con=engine, if_exists='replace',index=False)
#     except:
#         articleNewPd = pd.read_csv('./articleData.csv')
#         commentNewPd = pd.read_csv('./commentsData.csv')
#         articleNewPd.to_sql('article', con=engine, if_exists='replace',index=False)
#         commentNewPd.to_sql('comments', con=engine, if_exists='replace',index=False)

#     os.remove('./articleData.csv')
#     os.remove('./commentsData.csv')

import re

def remove_emoji(text):
    """移除文本中的表情符号和特殊字符"""
    if isinstance(text, str):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # 表情符号
            "\U0001F300-\U0001F5FF"  # 符号和图形
            "\U0001F680-\U0001F6FF"  # 交通和地图符号
            "\U0001F1E0-\U0001F1FF"  # 国旗
            "\U00002500-\U00002BEF"  # 其他符号
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r'', text)
    return text

def clean_dataframe(df):
    """清理 DataFrame 中的所有字符串列，移除表情符号"""
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(remove_emoji)
    return df

def save_to_sql():
    try:
        # 读取旧数据
        articleOldPd = pd.read_sql('select * from article', engine)
        articleNewPd = pd.read_csv('./articleData.csv')
        commentOldPd = pd.read_sql('select * from comments', engine)
        commentNewPd = pd.read_csv('./commentsData.csv')

        # 清理新数据中的特殊字符
        articleNewPd = clean_dataframe(articleNewPd)
        commentNewPd = clean_dataframe(commentNewPd)

        # 合并数据并去重
        concatPd = pd.concat([articleNewPd, articleOldPd], join='inner')
        concatPd = concatPd.drop_duplicates(subset='id', keep='last')
        concatCommentPd = pd.concat([commentNewPd, commentOldPd], join='inner')
        concatCommentPd = concatCommentPd.drop_duplicates(subset='content', keep='last')

        # 插入到数据库
        concatPd.to_sql('article', con=engine, if_exists='replace', index=False)
        concatCommentPd.to_sql('comments', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error occurred: {e}")
        # 如果发生异常，直接插入新数据
        articleNewPd = pd.read_csv('./articleData.csv')
        commentNewPd = pd.read_csv('./commentsData.csv')

        # 清理新数据中的特殊字符
        articleNewPd = clean_dataframe(articleNewPd)
        commentNewPd = clean_dataframe(commentNewPd)

        articleNewPd.to_sql('article', con=engine, if_exists='replace', index=False)
        commentNewPd.to_sql('comments', con=engine, if_exists='replace', index=False)

    # 删除临时文件
    os.remove('./articleData.csv')
    os.remove('./commentsData.csv')



def main():
    print('正在爬取文章内容...')
    contentStart(2,2)
    print('正在爬取评论内容...')
    commentsStart()
    print('爬取完毕正在存储中...')
    save_to_sql()


if __name__ == '__main__':
    main()