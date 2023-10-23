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
doc = open("%s點.html"%now.strftime("%Y%m%d_%H"), "a+" ,encoding="UTF-8")

def spider():
    
    print("\n---------------------財訊快報 盤勢分析  %s---------------------\n"%today.strftime("%Y-%m-%d"))
    doc.write("""<br>---------------------財訊快報 盤勢分析  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
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
                        doc.write("""<br>%s<a href="http://www.investor.com.tw/onlineNews/%s" target="_blank">%s  </a>%s<br> """%(filterkey,urllist[j],titlelist[j],datelist[j]))
                        filterlist.append("%s  %s  %s\nhttp://www.investor.com.tw/onlineNews/%s"%(filterkey,titlelist[j],datelist[j],urllist[j]))
    if filterlist:
        for x in range(len(filterlist)):
            print(filterlist[x])
    else:
        print("無")


    print("\n---------------------財訊快報 最新報紙  %s---------------------\n"%today.strftime("%Y-%m-%d"))
    doc.write("""<br>---------------------財訊快報 最新報紙  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
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
                    doc.write("""<br>%s<a href="http://www.investor.com.tw/onlineNews/%s" target="_blank">%s  </a>%s<br> """%(investor,urllist[j],titlelist[j],re.sub('/','-',datelist[j])))
        else:
            print(investor + " 無")        
        time.sleep(1)
    
    print("\n---------------------工商時報  %s---------------------\n"%today.strftime("%Y-%m-%d"))
    doc.write("""<br>---------------------工商時報  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
    for ctee in keyword:  #工商時報
        rep = requests.get('https://search.ctee.com.tw/multiindexsearch/' + ctee,headers = headers)
        url = re.compile('"sharelink":"(.*?)"')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('"mmddhhmm":"(.*?) ')
        datelist = re.findall(date1, rep.text)
        title = re.compile('"title":"(.*?)"')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if (today.strftime("%m/%d") in datelist) or (yesterday.strftime("%m/%d") in datelist):
                try:
                    for j in range(len(titlelist)):
                        if (datelist[j] != today.strftime("%m/%d")) and (datelist[j] != yesterday.strftime("%m/%d")):
                            break
                        print("\n" + ctee + "  " + re.sub('/','-',datelist[j]) +" : " + re.sub('<(.*?)>','',titlelist[j]) + "\n" + urllist[j] + "\n")
                        doc.write("""<br>%s<a href="%s" target="_blank">%s  </a>%s<br> """%(ctee,urllist[j],re.sub('<(.*?)>','',titlelist[j]),re.sub('/','-',datelist[j])))
                except:
                    pass
            else:
                print(ctee + "  無")
        else:                
            print(ctee + "  無")
        time.sleep(1)

    print("\n---------------------中央通訊社   %s---------------------\n"%today.strftime("%Y-%m-%d"))
    doc.write("""<br>---------------------中央通訊社  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
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
                    doc.write("""<br>%s<a href="%s" target="_blank">%s  </a>%s<br> """%(cna,urllist[j],titlelist[j],re.sub('/','-',datelist[j])))
            else:
                print(cna + "  無")
        else:                
            print(cna + "  無")
        time.sleep(1)

    # print("\n---------------------中時新聞網   %s---------------------\n"%today.strftime("%Y-%m-%d"))
    # doc.write("""<br>---------------------中時新聞網  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
    # for cn in keyword:  #中時新聞網
    #     rep = requests.get('https://www.chinatimes.com/search/' + cn,headers = headers)
    #     url = re.compile('"title"><a href="(.*?)"')
    #     urllist = re.findall(url, rep.text)
    #     date1 = re.compile('datetime="(.*?)\s')
    #     datelist = re.findall(date1, rep.text)
    #     title = re.compile('"title"><a href=".*?">(.*?)</a></h3>')
    #     titlelist = re.findall(title, rep.text)
    #     if titlelist:
    #         if (today.strftime("%Y-%m-%d") in datelist) or (yesterday.strftime("%Y-%m-%d") in datelist):
    #             for j in range(len(titlelist)):
    #                 if (datelist[j] != today.strftime("%Y-%m-%d")) and (datelist[j] != yesterday.strftime("%Y-%m-%d")):
    #                     break
    #                 print("\n" + cn + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
    #                 doc.write("""<br>%s<a href="%s" target="_blank">%s  </a>%s<br> """%(cn,urllist[j],titlelist[j],datelist[j]))
    #         else:
    #             print(cn + "  無")
    #     else:                
    #         print(cn + "  無")
    #     time.sleep(1)

    print("\n---------------------經濟日報   %s---------------------\n"%today.strftime("%Y-%m-%d"))
    doc.write("""<br>---------------------經濟日報  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
    for money in keyword:  #經濟日報
        rep = requests.get('https://money.udn.com/search/result/1001/' + money,headers = headers)
        url = re.compile('<div class="story__content ">\s\s+<a href="(.*?)"')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('<time>(.*?) ')
        datelist = re.findall(date1, rep.text)
        title = re.compile('<h3 class="story__headline">\s\s+(.*?)</h3>')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if (today.strftime("%Y-%m-%d") in datelist) or (yesterday.strftime("%Y-%m-%d") in datelist):
                for j in range(len(urllist)):
                    if (datelist[j] != today.strftime("%Y-%m-%d")) and (datelist[j] != yesterday.strftime("%Y-%m-%d")):
                        break
                    print("\n" + money + "  " + re.sub('/','-',datelist[j]) +" : " + re.sub('<(.*?)>','',titlelist[j]) + "\n" + urllist[j] + "\n")
                    doc.write("""<br>%s<a href="%s" target="_blank">%s  </a>%s<br> """%(money,urllist[j],re.sub('<(.*?)>','',titlelist[j]),re.sub('/','-',datelist[j])))
            else:
                print(money + "  無")
        else:                
            print(money + "  無")
        time.sleep(1)

    print("\n---------------------台北時報   %s---------------------\n"%today.strftime("%Y-%m-%d"))
    doc.write("""<br>---------------------台北時報  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
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
                    doc.write("""<br>%s<a href="%s" target="_blank">%s  </a>%s<br> """%(TP,urllist[j],titlelist[j],datelist[j]))
            else:
                print(TP + "  無")
        else:                
            print(TP + "  無")
        time.sleep(1)

    print("\n---------------------自立晚報   %s---------------------\n"%today.strftime("%Y-%m-%d"))
    doc.write("""<br>---------------------自立晚報  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
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
                    doc.write("""<br>%s<a href="%s" target="_blank">%s  </a>%s<br> """%(idn,"https://www.idn.com.tw/news/" + urllist[j],re_titlelist,datelist[j]))
            else:
                print(idn + "  無")
        else:                
            print(idn + "  無")
        time.sleep(1)

    print("\n---------------------必聞網   %s---------------------\n"%today.strftime("%Y-%m-%d"))
    doc.write("""<br>---------------------必聞網  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
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
                    doc.write("""<br>%s<a href="%s" target="_blank">%s  </a>%s<br> """%(bi,urllist[j],titlelist[j],datelist[j]))
            else:
                print(bi + "  無")
        else:                
            print(bi + "  無")
        time.sleep(1)

    print("\n---------------------精實新聞   %s---------------------\n"%today.strftime("%Y-%m-%d"))
    doc.write("""<br>---------------------精實新聞  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
    for dj in keyword:  #精實新聞
        rep = requests.get('https://www.moneydj.com/KMDJ/search/list.aspx?_Query_=' + dj,headers = headers)
        url = re.compile('<td><a href="..(.*?)"')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('100px;">(.*?) ')
        datelist = re.findall(date1, rep.text)
        title = re.compile('>(.*?)</a></td><td align="center"')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if (today.strftime("%Y-%m-%d") in datelist) or (yesterday.strftime("%Y-%m-%d") in datelist):
                for j in range(len(titlelist)):
                    if (datelist[j] != today.strftime("%Y-%m-%d")) and (datelist[j] != yesterday.strftime("%Y-%m-%d")):
                        break
                    print("\n" + dj + "  " + re.sub('/','-',datelist[j]) +" : " + re.sub('<(.*?)>','',titlelist[j]) + "\n" + "https://www.moneydj.com/KMDJ" +urllist[j] + "\n")
                    doc.write("""<br>%s<a href="%s" target="_blank">%s  </a>%s<br> """%(dj,"https://www.moneydj.com/KMDJ" + urllist[j],re.sub('<(.*?)>','',titlelist[j]),re.sub('/','-',datelist[j])))
            else:
                print(dj + "  無")
        else:                
            print(dj + "  無")
        time.sleep(1)

    print("\n---------------------自由時報   " + today.strftime("%Y-%m-%d") + "---------------------\n")
    doc.write("""<br>---------------------自由時報  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
    for ltn in keyword:  
        rep = requests.get('https://search.ltn.com.tw/list?keyword=' + ltn,headers = headers)
        url = re.compile('class="cont" href="(.*?)"')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('<span class="time">(.*?)<')
        datelist = re.findall(date1, rep.text)          
        title = re.compile('class="ph" title="(.*?)"')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if ('小時' in datelist[0]) or ('分鐘' in datelist[0]) or ('1天' in datelist[0]):
                for j in range(len(titlelist)):
                    if ('小時' in datelist[j]) or ('分鐘' in datelist[j]) or ('1天' in datelist[j]):         
                        print("\n" + ltn + "  " + today.strftime("%Y-%m-%d") +" : " + re.sub('<(.*?)>','',titlelist[j]) + "\n" + urllist[j] + "\n")
                        doc.write("""<br>%s<a href="%s" target="_blank">%s  </a>%s<br> """%(ltn,urllist[j],titlelist[j],today.strftime("%Y-%m-%d")))
            else:
                print(ltn + "  無")
        else:                
            print(ltn + "  無")
        time.sleep(1)

    print("\n---------------------ETtoday   %s---------------------\n"%today.strftime("%Y-%m-%d"))
    doc.write("""<br>---------------------ETtoday  %s---------------------<br>"""%today.strftime("%Y-%m-%d"))
    for ettoday in keyword:  #ETtoday
        rep = requests.get('https://www.ettoday.net/news_search/doSearch.php?keywords=' + ettoday,headers = headers)
        url = re.compile('<h2><a href="(.*?)"')
        urllist = re.findall(url, rep.text)
        date1 = re.compile('</a> / (.*?) ')
        datelist = re.findall(date1, rep.text)
        title = re.compile('">(.*?)</a></h2>')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            if (today.strftime("%Y-%m-%d") in datelist) or (yesterday.strftime("%Y-%m-%d") in datelist):
                for j in range(len(titlelist)):
                    if (datelist[j] != today.strftime("%Y-%m-%d")) and (datelist[j] != yesterday.strftime("%Y-%m-%d")):
                        break
                    print("\n" + ettoday + "  " + datelist[j] +" : " + titlelist[j] + "\n" + urllist[j] + "\n")
                    doc.write("""<br>%s<a href="%s" target="_blank">%s  </a>%s<br> """%(ettoday,urllist[j],titlelist[j],datelist[j]))
            else:
                print(ettoday + "  無")
        else:                
            print(ettoday + "  無")
        time.sleep(1)

    html2 = """
    </div>
    </body>
    </html>"""
    doc.write(html2)
    doc.close()
    print("\nOK,Spider is End .")


def main():
    spider()

if __name__ == '__main__':
    html1 = """
        <html>
        <head></head>
        <style>
        body {
            background-color: #2b2b2b;
            color: #ccc;
        }
        a {
            background-color: transparent;
            text-decoration: none;
            outline: 0;
        }
        a:link {
            color:#FF0000;
            text-decoration:underline;
        }
        a:visited {
            color:#00FF00;
            text-decoration:none;
        }
        a:hover {
            color:#000000;
            text-decoration:none;
        }
        a:active {
            color:#FFFFFF;
            text-decoration:none;
        }
        </style>
        <body>
        <div>"""
    doc.write(html1)
    main()