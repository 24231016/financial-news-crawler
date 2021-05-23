import requests
import re
import time
from datetime import date

keyword=["台積電","岱宇","世豐","捷流","力士","耕興","泰福","寶陞"]

def spider():
    today = date.today()
    doc = open("hello_world.txt", "a+" ,encoding="UTF-8")
    for TP in keyword:  #TaipeiNews
        rep = requests.get('https://www.taipeitimes.com/News/list?section=all&keywords=' + TP)
        # rep.encoding='big5' #財訊快報 investor
        # print(rep.text)
        date = re.compile('date_list ">(.*?)<')
        datelist = re.findall(date, rep.text)
        title = re.compile('class="bf6">(.*?)<')
        titlelist = re.findall(title, rep.text)
        if titlelist:
            for j in range(len(titlelist)):
                if datelist[j] != today.strftime("%Y-%m-%d"):
                    break
                print(TP + "  " + datelist[j] +" : " + titlelist[j])
        else:                
            print(TP + "  無")
        time.sleep(2)
    

        # doc.write(rep.text)
    # for i in range(1,5):
    #     print("Now write " + str(i) + " page")
        # rep = requests.get('http://www.investor.com.tw/onlineNews/TodayNews.asp'+str(i)+"/")
        # url = re.compile('<h2><a href="(.*?)"')
        # img = re.compile('im=//(.*?)"')
    
        # time = re.compile('time">(.*?)<')
        # urllist = re.findall(url, rep.text)
        # imglist = re.findall(img, rep.text)
        # titlelist = re.findall(title, rep.text)
        # timelist = re.findall(time, rep.text)

        # for j in range(len(urllist)):
        #     if timelist[j] != today.strftime("%Y-%m-%d"):
        #         break
        #     print("標題: %s\nURL: %s\n時間: %s\n圖片: %s\n"%(titlelist[j],urllist[j],timelist[j],imglist[j]))
        #     doc.write("標題: %s\nURL: %s\n時間: %s\n圖片: %s\n"%(titlelist[j],urllist[j],timelist[j],imglist[j]))
        # if timelist[j] != today.strftime("%Y-%m-%d"):
        #         break
        
    doc.close()
    print("OK,Spider is End .")


def main():
    spider()

if __name__ == '__main__':
    main()