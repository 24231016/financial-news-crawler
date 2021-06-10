import requests
import re
import time
import datetime
from datetime import date
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
keyword=["客思達","台翰","聖暉","岱宇","朋億","捷流","力士","信紘科","鈺齊","寶陞"]
today = date.today()
now = datetime.datetime.now()
oneday = datetime.timedelta(days=1) 
yesterday = today-oneday
def spider():
    now = datetime.datetime.now()
    rep = requests.get('https://www.taipeitimes.com/News/list?section=all&keywords=捷流', headers=headers)
    # rep.encoding='big5' #財訊快報 investor
    doc = open("hello.txt", "a+" ,encoding="UTF-8")
    doc.write(rep.text)

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

def main():
    spider()

if __name__ == '__main__':
    main()
