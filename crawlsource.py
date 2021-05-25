import requests
import re
import time
import datetime
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

def spider():
    now = datetime.datetime.now()
    rep = requests.get('http://www.investor.com.tw/onlineNews/TodayNews.asp', headers=headers)
    rep.encoding='big5' #財訊快報 investor
    doc = open("hello.txt", "a+" ,encoding="UTF-8")
    print(rep.text)
    doc.write(rep.text)

def main():
    spider()

if __name__ == '__main__':
    main()
