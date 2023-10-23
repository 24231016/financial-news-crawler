import requests

headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
rep = requests.get('https://www.chinatimes.com/search/台積電?chdtv', headers=headers)
print(rep)
doc = open("hello.txt", "a+" ,encoding="UTF-8")
doc.write(rep.text)