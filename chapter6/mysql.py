"""
When you have a problem connecting to mysql server, the following page might help (or not,,,)
https://askubuntu.com/questions/1029177/error-1698-28000-access-denied-for-user-rootlocalhost-at-ubuntu-18-04
"""
import datetime
import random
import re
from urllib.request import urlopen
import pymysql
from bs4 import BeautifulSoup

with pymysql.connect(host='localhost', user='root', passwd=None,
                     db='mysql') as conn, conn.cursor() as curr:
    curr.execute('USE scraping')
    random.seed(datetime.datetime.now())

    def store(title, content):
        curr.execute(
            f'INSERT INTO pages (title, content) VALUES ("{title}", "{content}")'
        )
        curr.connection.commit()

    def getlinks(article_url):
        html = urlopen('http://en.wikipedia.org' + article_url)
        bs = BeautifulSoup(html, 'html.parser')
        print(bs.find('h1').find('span').get_text())
        title = bs.find('h1').find('span').get_text()
        content = bs.find('div', {
            'id': 'mw-content-text'
        }).find('p').get_text()
        store(title, content)
        return bs.find('div', {
            'id': 'bodyContent'
        }).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))

    links = getlinks('/wiki/Kevin_Bacon')
    while len(links) > 0:
        new_article = links[random.randint(0, len(links) - 1)].attrs['href']
        print(new_article)
        links = getlinks(new_article)
