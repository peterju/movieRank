import requests
import re
import bs4

# from bs4 import BeautifulSoup

url = "https://movies.yahoo.com.tw/chart.html"
html = requests.get(url)  # 利用 requests 套件取回網頁原始碼
if html.status_code != 200:  # 判斷回傳值決定是否正確擷取
    print("網址無效:", html.url)
    quit()
if not html.encoding == "utf-8":
    html.encoding = "utf-8"  # 指定網頁物件以utf-8編碼

# 以 Regular Expression 正規表示式來抓取網頁標題的方法
# 設定比對的樣板, 若附加 re.DOTALL 參數可讓任意字元.可比對換行字元
patten = re.compile("<title>(.*)</title>")
result = re.search(patten, html.text)
print(result.group(1))

# BeautifulSoup 採用解析器分析原始碼，回傳 bs4.BeautifulSoup 物件
# 速度快、文件容錯能力強
soup = bs4.BeautifulSoup(html.text, "lxml")
# 速度慢、最好的容錯性、以瀏覽器的方式分析文件、產生html5格式的文件
# soup = bs4.BeautifulSoup(html.text, 'html5lib')
# 速度中、文件容錯能力強
# soup = bs4.BeautifulSoup(html.text, 'html.parser')

# 輸出排版後的HTML內容至檔案
with open("pretty.html", "w", encoding="UTF-8") as f:
    f.write(soup.prettify())
# 以 BeautifulSoup 抓取網頁標題元素
print("-" * 26 + "\n" + soup.title.text + "\n" + "-" * 26)
# 改用 CSS 選擇器的 select 方法來抓到標題
print(soup.select("title")[0].text)

# 利用 find 方法尋找第一個符合條件的標籤，並傳回字串，也可以指定抓取的 id 與相關屬性
print(soup.find(id="mainURL").get("data-url"))
# 也可以這樣寫 print( soup.find(id='mainURL')["data-url"] )
# 也可以這樣寫 print( soup.find("",{"id":"mainURL"})["data-url"] )


# 使用 CSS 選擇器的 select_one 方法來進行順序挑選抓到名次
# nth-of-type(n) 的使用請參考：https://www.webdesigns.com.tw/CSS3-nth-of-type.asp
filmRank = soup.select_one(
    "div.rank_list.table.rankstyle1 > div:nth-of-type(2) > div:nth-of-type(1)"
).text
# 利用 find 方法抓取class 得知本周第 1 名相關標籤至 bs4.element.Tag 物件
filmName = soup.find("dl", "rank_list_box").dd.h2.text
# 使用 CSS 選擇器的 select_one 方法來進行順序挑選抓到日期
filmDate = soup.select_one(
    "div.rank_list.table.rankstyle1 > div:nth-of-type(2) > div:nth-of-type(5)"
).text
# 使用 CSS 選擇器的 select_one 方法來進行順序挑選抓到評價
filmRating = soup.select_one("div.td.starwithnum > h6").text

print("filmRank={}".format(filmRank))
print("filmName={}".format(filmName))
print("filmDate={}".format(filmDate))
print("filmRating={}".format(filmRating))

# 利用 find_all 方法抓取class得知本周第 2-20 名相關標籤至 bs4.element.ResultSet 物件
films = soup.find_all("div", "rank_txt")
#  films = soup.find_all("div",class_=’rank_txt’)
for film in films:
    print(film.text)
