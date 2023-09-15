import requests
import re
import bs4

url = "https://movies.yahoo.com.tw/chart.html?.tsrc=xl"
html = requests.get(url)                # 利用 requests 套件取回網頁原始碼
if html.status_code != 200:                # 判斷回傳值決定是否正確擷取
    print('網址無效:', html.url)
    quit()

# 以 Regular Expression 正規表示式來抓取網頁標題的方法
patten = re.compile('<title>(.*)</title>') # 設定比對的樣板, 若附加 re.DOTALL 參數可讓任意字元.可比對換行字元
result = re.search(patten, html.text)
print(result.group(1))

# BeautifulSoup 採用 html.parser 解析原始碼，回傳 bs4.BeautifulSoup 物件
soup = bs4.BeautifulSoup(html.text, 'html.parser')
# 以 BeautifulSoup 抓取網頁頁面標題的方法
print('-'*26+"\n"+soup.title.text+"\n"+'-'*26)

# 利用 find 方法抓取 id 與其相關屬性
print(soup.find(id='mainURL').get("data-url"))
# 也可以這樣寫 print(soup.find(id='mainURL')["data-url"])
# 也可以這樣寫 print(soup.find("",{"id":"mainURL"})["data-url"])

# 使用 CSS 選擇器的 select_one 方法來進行順序挑選抓到名次
filmRank = soup.select_one("div.rank_list.table.rankstyle1 > div:nth-of-type(2) > div:nth-of-type(1)").text
# 利用 find 方法抓取class 得知本周第 1 名相關標籤至 bs4.element.Tag 物件
filmName = soup.find("","rank_list_box").dd.h2.text
# 使用 CSS 選擇器的 select_one 方法來進行順序挑選抓到日期
filmDate = soup.select_one("div.rank_list.table.rankstyle1 > div:nth-of-type(2) > div:nth-of-type(5)").text
# 使用 CSS 選擇器的 select_one 方法來進行順序挑選抓到評價
filmRating = soup.select_one("div.td.starwithnum > h6").text

print("filmRank={}".format(filmRank))
print("filmName={}".format(filmName))
print("filmDate={}".format(filmDate))
print("filmRating={}".format(filmRating))

# 利用 find_all 方法抓取class得知本周第 2-20 名相關標籤至 bs4.element.ResultSet 物件
films = soup.find_all("","rank_txt")
for film in films:
    print(film.text)