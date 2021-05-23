import requests
import re
import time
from datetime import date
from bs4 import BeautifulSoup

keyword=["岱宇","世豐","捷流","力士","耕興","泰福","寶陞"]

def spider():
    today = date.today()
    doc = open("hello_world.txt", "a+" ,encoding="UTF-8")

    print("\n台北時報   " + today.strftime("%Y-%m-%d") + "\n")
    for TP in keyword:  #TaipeiNews
        rep = requests.get('https://www.taipeitimes.com/News/list?section=all&keywords=' + TP)
        # rep.encoding='big5' #財訊快報 investor
        # print(rep.text)
        url = re.compile('class="tit" href="(.*?)"')
        urllist = re.findall(url, rep.text)
        datetime = re.compile('date_list ">(.*?)<')
        datelist = re.findall(datetime, rep.text)
        title = re.compile('class="bf6">(.*?)<')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if today.strftime("%Y-%m-%d") in datelist:
                for j in range(len(titlelist)):
                    if datelist[j] != today.strftime("%Y-%m-%d"):
                        break
                    print("\n" + TP + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
            else:
                print(TP + "  無")
        else:                
            print(TP + "  無")
        time.sleep(2)

    print("\n自立晚報   " + today.strftime("%Y-%m-%d") + "\n")
    for idn in keyword:  #自立晚報
        rep = requests.get('https://www.idn.com.tw/news/article_search.aspx?key_word=' + idn)
        url = re.compile('class="body_9b"><a href="(.*?)"')
        urllist = re.findall(url, rep.text)
        datetime = re.compile('<td width="70" class="body_9g">(.*?)<')
        datelist = re.findall(datetime, rep.text)
        title = re.compile('class="body_9b">(.*?)</a>')
        titlelist = re.findall(title, rep.text)
        re_h = re.compile('<(.*?)>')            
        
        if titlelist:
            if today.strftime("%Y-%m-%d") in datelist:
                for j in range(len(titlelist)):
                    if datelist[j] != today.strftime("%Y-%m-%d"):
                        break
                    re_titlelist = re_h.sub('',titlelist[j])
                    print("\n" + idn + "  " + datelist[j] +" : " + re_titlelist + "\n" + "https://www.idn.com.tw/news/" + urllist[j] + "\n")
            else:
                print(idn + "  無")
        else:                
            print(idn + "  無")
        time.sleep(2)

    print("\n必聞網   " + today.strftime("%Y-%m-%d") + "\n")
    for bi in keyword:  #必聞網
        rep = requests.get('https://www.biwennews.com/search.php?keyword=' + bi)
        url = re.compile('<h3 class="post-title">\s\s+<a href="(.*?)">')
        urllist = re.findall(url, rep.text)
        datetime = re.compile('datetime="(.*?)\s')
        datelist = re.findall(datetime, rep.text)
        title = re.compile('alt="(.*?)"')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if today.strftime("%Y-%m-%d") in datelist:
                for j in range(len(titlelist)):
                    if datelist[j] != today.strftime("%Y-%m-%d"):
                        break
                    print("\n" + bi + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
            else:
                print(bi + "  無")
        else:                
            print(bi + "  無")
        time.sleep(2)

    print("\n聯合新聞網   " + today.strftime("%Y-%m-%d") + "\n")
    for udn in keyword:  #聯合新聞網
        rep = requests.get('https://udn.com/search/word/2/' + udn)
        url = re.compile('<div class="story-list__image ">\s\s+<a href="(.*?)"')
        urllist = re.findall(url, rep.text)
        datetime = re.compile('<time class="story-list__time" >(.*?)\s')
        datelist = re.findall(datetime, rep.text)
        title = re.compile('<h2>\s\s+<a href=".*" title="(.*?)"')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if today.strftime("%Y-%m-%d") in datelist:
                for j in range(len(titlelist)):
                    if datelist[j] != today.strftime("%Y-%m-%d"):
                        break
                    print("\n" + udn + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
            else:
                print(udn + "  無")
        else:                
            print(udn + "  無")
        time.sleep(2)

    doc.close()
    print("\nOK,Spider is End .")


def main():
    spider()

if __name__ == '__main__':
    main()