import requests
from bs4 import BeautifulSoup
import datetime

odds_url_base = 'https://www.boatrace.jp/owpc/pc/race/'
today = datetime.date.today().strftime('%Y%m%d')

# 浜名湖を指定
jcd = '06'
# レース番号を指定
rno = 1
# 3連単などを指定
odds_mode = 'odds3t'

odds_url_param = f'?rno={rno}&jcd={jcd}&hd={today}'
odds_url = odds_url_base + odds_mode + odds_url_param

# HTMLを取得
response = requests.get(odds_url)
response.raise_for_status()  # エラーチェック

with open('output.html', 'wb') as file:
    file.write(response.content)

# BeautifulSoupで解析
soup = BeautifulSoup(response.content, 'html.parser')

# テーブルを見つける
tables = soup.find_all('table')

# テーブル情報を抽出
data = []
for table in tables:
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # 空のエントリを除外

# 結果を表示
for row in data:
    print(row)
