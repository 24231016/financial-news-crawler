import requests
import re
import time
import datetime
from datetime import date
from bs4 import BeautifulSoup

keyword=["富旺","台翰","聖暉","岱宇","朋億","捷流","力士","信紘科","鈺齊","寶陞"]
headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
today = date.today()
now = datetime.datetime.now()
oneday = datetime.timedelta(days=1) 
yesterday = today-oneday
doc = open("%s點.txt"%now.strftime("%Y%m%d_%H"), "a+" ,encoding="UTF-8")

def spider():
    
    print("\n財訊快報 盤勢分析  " + today.strftime("%Y-%m-%d") + "\n")
    doc.write("\n財訊快報 盤勢分析  " + today.strftime("%Y-%m-%d") + "\n")
    inv()


    print("\n財訊快報 最新報紙  " + today.strftime("%Y-%m-%d") + "\n")
    doc.write("\n財訊快報 最新報紙  " + today.strftime("%Y-%m-%d") + "\n")
    for investor in keyword:  #財訊快報
        result = {}
        rep = requests.get('http://www.investor.com.tw/onlineNews/TodayNews.asp',headers = headers)
        rep.encoding='big5' #財訊快報 investor
        url = re.compile('<li class="TODAY_NEWS_TITLE"><a href="(.*?)">')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('"TODAY_NEWS_DATE">(.*?)<')
        datelist = re.findall(date1, rep.text)
        title = re.compile('<li class="TODAY_NEWS_TITLE"><a href=".*?">(.*?)</a></li>')
        titlelist = re.findall(title, rep.text)
        keywordsearch = re.compile(investor)
        for j in range(len(titlelist)):
            result[j] = "%s : %s \nhttp://www.investor.com.tw/onlineNews/%s"%(re.sub('/','-',datelist[j]),titlelist[j],urllist[j])
        key = re.findall(keywordsearch,str(result.values()))
        if key:
            for x in result.values():
                if investor in x:
                    print('\n' + investor + '\n' + x + '\n')    
        else:
            print(investor + " 無")        
        time.sleep(1)
    
    

    print("\n中央通訊社   " + today.strftime("%Y-%m-%d") + "\n")
    doc.write("\n中央通訊社   " + today.strftime("%Y-%m-%d") + "\n")
    for cna in keyword:  #中央通訊社
        rep = requests.get('https://www.cna.com.tw/search/hysearchws.aspx?q=' + cna,headers = headers)
        filterdata = re.compile('<ul id="jsMainList" class="mainList">(.*?)</ul>')
        rep1 = re.findall(filterdata, rep.text)
        url = re.compile('<li><a href="(.*?)"><div')
        urllist = re.findall(url, str(rep1))
        date1 = re.compile('class="date">(.*?)\s')
        datelist = re.findall(date1, str(rep1))
        title = re.compile('<h2>(.*?)</h2>')
        titlelist = re.findall(title, str(rep1))
        if titlelist:
            if (today.strftime("%Y/%m/%d") in datelist) or (yesterday.strftime("%Y/%m/%d") in datelist):
                for j in range(len(titlelist)):
                    if (datelist[j] != today.strftime("%Y/%m/%d")) and (datelist[j] != yesterday.strftime("%Y/%m/%d")):
                        break
                    print("\n" + cna + "  " + re.sub('/','-',datelist[j]) +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
                    doc.write("\n" + cna + "  " + re.sub('/','-',datelist[j]) +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
            else:
                print(cna + "  無")
                doc.write(cna + "  無\n")
        else:                
            print(cna + "  無")
            doc.write(cna + "  無\n")
        time.sleep(1)

    print("\n中時新聞網   " + today.strftime("%Y-%m-%d") + "\n")
    doc.write("\n中時新聞網   " + today.strftime("%Y-%m-%d") + "\n")
    for cn in keyword:  #中時新聞網
        rep = requests.get('https://www.chinatimes.com/search/' + cn,headers = headers)
        url = re.compile('"title"><a href="(.*?)"')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('datetime="(.*?)\s')
        datelist = re.findall(date1, rep.text)
        title = re.compile('"title"><a href=".*?">(.*?)</a></h3>')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if (today.strftime("%Y-%m-%d") in datelist) or (yesterday.strftime("%Y-%m-%d") in datelist):
                for j in range(len(titlelist)):
                    if (datelist[j] != today.strftime("%Y-%m-%d")) and (datelist[j] != yesterday.strftime("%Y-%m-%d")):
                        break
                    print("\n" + cn + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
                    doc.write("\n" + cn + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
            else:
                print(cn + "  無")
                doc.write(cn + "  無\n")
        else:                
            print(cn + "  無")
            doc.write(cn + "  無\n")
        time.sleep(1)

    print("\n經濟日報   " + today.strftime("%Y-%m-%d") + "\n")
    doc.write("\n經濟日報   " + today.strftime("%Y-%m-%d") + "\n")
    for money in keyword:  #經濟日報
        rep = requests.get('https://money.udn.com/search/result/1001/' + money,headers = headers)
        url = re.compile('<dt>\s\s+<a href="(.*?)"')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('"cat">經濟日報：(.*?)<')
        datelist = re.findall(date1, rep.text)
        title = re.compile('</i>\s\s+<h3>(.*?)</h3>')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if (today.strftime("%Y/%m/%d") in datelist) or (yesterday.strftime("%Y/%m/%d") in datelist):
                for j in range(len(titlelist)):
                    if (datelist[j] != today.strftime("%Y/%m/%d")) and (datelist[j] != yesterday.strftime("%Y/%m/%d")):
                        break
                    print("\n" + money + "  " + re.sub('/','-',datelist[j]) +" : " + re.sub('<(.*?)>','',titlelist[j]) + "\n" + urllist[j] + "\n")
                    doc.write("\n" + money + "  " + re.sub('/','-',datelist[j]) +" : " + re.sub('<(.*?)>','',titlelist[j]) + "\n" + urllist[j] + "\n")
            else:
                print(money + "  無")
                doc.write(money + "  無\n")
        else:                
            print(money + "  無")
            doc.write(money + "  無\n")
        time.sleep(1)

    print("\n台北時報   " + today.strftime("%Y-%m-%d") + "\n")
    doc.write("\n台北時報   " + today.strftime("%Y-%m-%d") + "\n")
    for TP in keyword:  #TaipeiNews
        rep = requests.get('https://www.taipeitimes.com/News/list?section=all&keywords=' + TP,headers = headers)
        url = re.compile('class="tit" href="(.*?)"')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('class="date_list.*?">(.*?)<')
        datelist = re.findall(date1, rep.text)
        title = re.compile('class="bf6">(.*?)<')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if (today.strftime("%Y-%m-%d") in datelist) or (yesterday.strftime("%Y-%m-%d") in datelist):
                for j in range(len(titlelist)):
                    if (datelist[j] != today.strftime("%Y-%m-%d")) and (datelist[j] != yesterday.strftime("%Y-%m-%d")):
                        break
                    print("\n" + TP + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
                    doc.write("\n" + TP + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
            else:
                print(TP + "  無")
                doc.write(TP + "  無\n")
        else:                
            print(TP + "  無")
            doc.write(TP + "  無\n")
        time.sleep(1)

    print("\n自立晚報   " + today.strftime("%Y-%m-%d") + "\n")
    doc.write("\n自立晚報   " + today.strftime("%Y-%m-%d") + "\n")
    for idn in keyword:  #自立晚報
        rep = requests.get('https://www.idn.com.tw/news/article_search.aspx?key_word=' + idn,headers = headers)
        url = re.compile('class="body_9b"><a href="(.*?)"')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('<td width="70" class="body_9g">(.*?)<')
        datelist = re.findall(date1, rep.text)
        title = re.compile('class="body_9b">(.*?)</a>')
        titlelist = re.findall(title, rep.text)
        re_h = re.compile('<(.*?)>')            
        
        if titlelist:
            if (today.strftime("%Y-%m-%d") in datelist) or (yesterday.strftime("%Y-%m-%d") in datelist):
                for j in range(len(titlelist)):
                    if (datelist[j] != today.strftime("%Y-%m-%d")) and (datelist[j] != yesterday.strftime("%Y-%m-%d")):
                        break
                    re_titlelist = re_h.sub('',titlelist[j])
                    print("\n" + idn + "  " + datelist[j] +" : " + re_titlelist + "\n" + "https://www.idn.com.tw/news/" + urllist[j] + "\n")
                    doc.write("\n" + idn + "  " + datelist[j] +" : " + re_titlelist + "\n" + "https://www.idn.com.tw/news/" + urllist[j] + "\n")
            else:
                print(idn + "  無")
                doc.write(idn + "  無\n")
        else:                
            print(idn + "  無")
            doc.write(idn + "  無\n")
        time.sleep(1)

    print("\n必聞網   " + today.strftime("%Y-%m-%d") + "\n")
    doc.write("\n必聞網   " + today.strftime("%Y-%m-%d") + "\n")
    for bi in keyword:  #必聞網
        rep = requests.get('https://www.biwennews.com/search.php?keyword=' + bi,headers = headers)
        url = re.compile('<h3 class="post-title">\s\s+<a href="(.*?)">')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('datetime="(.*?)\s')
        datelist = re.findall(date1, rep.text)
        title = re.compile('jpg" alt="(.*?)"')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if (today.strftime("%Y-%m-%d") in datelist) or (yesterday.strftime("%Y-%m-%d") in datelist):
                for j in range(len(titlelist)):
                    if (datelist[j] != today.strftime("%Y-%m-%d")) and (datelist[j] != yesterday.strftime("%Y-%m-%d")):
                        break
                    print("\n" + bi + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
                    doc.write("\n" + bi + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
            else:
                print(bi + "  無")
                doc.write(bi + "  無\n")
        else:                
            print(bi + "  無")
            doc.write(bi + "  無\n")
        time.sleep(1)

    print("\n聯合新聞網   " + today.strftime("%Y-%m-%d") + "\n")
    doc.write("\n聯合新聞網   " + today.strftime("%Y-%m-%d") + "\n")
    for udn in keyword:  #聯合新聞網
        rep = requests.get('https://udn.com/search/word/2/' + udn,headers = headers)
        url = re.compile('<div class="story-list__image ">\s\s+<a href="(.*?)"')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('<time class="story-list__time" >(.*?)\s')
        datelist = re.findall(date1, rep.text)
        title = re.compile('<h2>\s\s+<a href=".*" title="(.*?)"')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if (today.strftime("%Y-%m-%d") in datelist) or (yesterday.strftime("%Y-%m-%d") in datelist):
                for j in range(len(titlelist)):
                    if (datelist[j] != today.strftime("%Y-%m-%d")) and (datelist[j] != yesterday.strftime("%Y-%m-%d")):
                        break
                    print("\n" + udn + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
                    doc.write("\n" + udn + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
            else:
                print(udn + "  無")
                doc.write(udn + "  無\n")
        else:                
            print(udn + "  無")
            doc.write(udn + "  無\n")
        time.sleep(1)

    doc.close()
    print("\nOK,Spider is End .")

def inv():
    filterlist = []
    rep = requests.get('http://www.investor.com.tw/onlineNews/NewsList2.asp?UnitXsub=048&UnitX=02',headers = headers)
    rep.encoding='big5' #財訊快報 investor
    url = re.compile('"PAGE_NEWS_LIST_TI"><a href="(.*?)">')
    urllist = re.findall(url, rep.text)
    date1 = re.compile('LIST_AUTHOR"> (.*?)<')
    datelist = re.findall(date1, rep.text)
    title = re.compile('"PAGE_NEWS_LIST_TI"><a href=".*?">(.*?)</a></li>')
    titlelist = re.findall(title, rep.text)
    if titlelist:
        if today.strftime("%Y/%#m/%d") in datelist:
            for j in range(len(titlelist)):
                if datelist[j] != today.strftime("%Y/%#m/%d"):
                    break
                repx = requests.get("http://www.investor.com.tw/onlineNews/%s"%urllist[j],headers = headers)
                repx.encoding='big5'
                soup = BeautifulSoup(repx.text,'html.parser')
                repx1 = soup.find_all("div", class_="highslide-gallery ARTICLES_STYLE")
                for inv in keyword:
                    filterkey = re.findall(inv, str(repx1))
                    if filterkey:
                        filterlist.append("%s  %s  %s\nhttp://www.investor.com.tw/onlineNews/%s"%(filterkey,titlelist[j],datelist[j],urllist[j]))
    if filterlist:
        for x in range(len(filterlist)):
            print(filterlist[x])
    else:
        print("無")



def main():
    spider()

if __name__ == '__main__':
    main()