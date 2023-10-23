import requests
import re
import time
import datetime
from datetime import date
from bs4 import BeautifulSoup

keyword=["富旺","台翰","聖暉","岱宇","朋億","捷流","力士","信紘科","鈺齊","寶陞"]
# keyword=["台積電"]
headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
today = date.today()
now = datetime.datetime.now()
oneday = datetime.timedelta(days=1) 
yesterday = today-oneday
print("\n經濟日報   " + today.strftime("%Y-%m-%d") + "\n")
for money in keyword:  #經濟日報
	rep = requests.get('https://money.udn.com/search/result/1001/' + money,headers = headers)
	# print(rep.text)
	doc = open("hello.txt", "a+" ,encoding="UTF-8")
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
		else:
			print(money + "  無")
	else:                
		print(money + "  無")
	time.sleep(1)
print("\nOK,Spider is End .")