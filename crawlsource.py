import requests
import re
import time
import datetime
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

def spider():
    now = datetime.datetime.now()
    rep = requests.get('https://money.udn.com/search/result/1001/%E4%B8%96%E8%B1%90', headers=headers)
    doc = open("hello.txt", "a+" ,encoding="UTF-8")
    print(rep.text)
    doc.write(rep.text)

def main():
    spider()

if __name__ == '__main__':
    main()
