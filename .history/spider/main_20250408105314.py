from spiderContent import start as contentStart
from spiderComments import start as commentsStart
import os
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('mysql+pymysql://root:123456@127.0.0.1/weibo_project?charset=utf8mb4')

def delete_2023_data():
    """删除数据库中 2023 年的数据"""
    try:
        with engine.connect() as conn:
            # 删除 article 表中 2023 年的数据
            conn.execute("""
                DELETE FROM article 
                WHERE created_at BETWEEN '2023-01-01' AND '2023-12-31'
            """)
            print("已删除 article 表中 2023 年的数据")

            # 删除 comments 表中 2023 年的数据
            conn.execute("""
                DELETE FROM comments 
                WHERE created_at BETWEEN '2023-01-01' AND '2023-12-31'
            """)
            print("已删除 comments 表中 2023 年的数据")
    except Exception as e:
        print(f"删除数据时出错: {e}")
  
def save_to_sql():
    try:
        articleOldPd = pd.read_sql('select * from article', engine)
        articleNewPd = pd.read_csv('./spider/articleData.csv')
        concatPd = pd.concat([articleNewPd,articleOldPd],join='inner')
        concatPd = concatPd.drop_duplicates(subset='id', keep='last')
        concatPd.to_sql('article',con=engine, if_exists='replace',index=False)

        commentOldPd = pd.read_sql('select * from comments', engine)
        commentNewPd = pd.read_csv('./spider/commentsData.csv')
        concatCommentPd = pd.concat([commentNewPd, commentOldPd], join='inner')
        concatCommentPd = concatCommentPd.drop_duplicates(subset='content', keep='last')
        concatCommentPd.to_sql('comments',con=engine, if_exists='replace',index=False)
    except:
        articleNewPd = pd.read_csv('./spider/articleData.csv')
        commentNewPd = pd.read_csv('./spider/commentsData.csv')
        articleNewPd.to_sql('article', con=engine, if_exists='replace',index=False)
        commentNewPd.to_sql('comments', con=engine, if_exists='replace',index=False)

    # os.remove('./spider/articleData.csv')
    # os.remove('./spider/commentsData.csv')



def main():
    print('正在爬取文章内容...')
    contentStart(2,2)
    print('正在爬取评论内容...')
    commentsStart()
    print('爬取完毕正在存储中...')
    save_to_sql()


if __name__ == '__main__':
    main()