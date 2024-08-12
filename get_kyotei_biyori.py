from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import datetime

def fetch_frame_info(race_no, place_no, today):
    url_base = 'https://kyoteibiyori.com/race_shusso.php'
    url_param = f'?place_no={place_no}&race_no={race_no}&hiduke={today}'
    url = url_base + url_param + '&slider=1'

    # Playwrightを使用してHTMLを取得
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until='domcontentloaded')
        page.wait_for_selector('#raceBasic', timeout=60000)
        page.evaluate("window.stop();")
        content = page.content()
        browser.close()

    data = get_escape_info(content)

    # 結果を返却
    return data

def get_escape_info(content):
    # BeautifulSoupで解析
    soup = BeautifulSoup(content, 'html.parser')
    print(content)
    raceBasic = soup.find(id='raceBasic')
    print(raceBasic)
    # テーブルを見つける
    table = raceBasic.find('table', class_='table_fixed')

    print(table)

    # テーブル情報から展示タイムのみを抽出(面倒だから固定値)
    exhibition_time_index = 4
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if exhibition_time_index < len(cols):
            data.append(cols[exhibition_time_index].text.strip())

    return data

# 使用例
race_no = 12
place_no = 1
today = datetime.date.today().strftime('%Y%m%d')
data = fetch_frame_info(race_no, place_no, today)
print(data)
