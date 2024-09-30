
from bs4 import BeautifulSoup
import datetime
from playwright.sync_api import sync_playwright, Browser
from dto.data import RaceDataDTO

def check_is_target_race(race_no, place_no, today, slider, browser: Browser):
    url_base = 'https://kyoteibiyori.com/race_shusso.php'
    url_param = f'?place_no={place_no}&race_no={race_no}&hiduke={today}'
    # slider0なら基本情報 1なら枠別情報
    url = url_base + url_param + '&slider=' + slider

    # Playwrightを使用してHTMLを取得
    page = browser.new_page()
    page.goto(url, wait_until='domcontentloaded')
    page.wait_for_selector('#raceBasic', timeout=60000)
    page.evaluate("window.stop();")
    content = page.content()

    data = get_base_info(content)

    if data[0] < 5.0:
        return False

    if max(data) - min(data) >= 2.0:
        return False

    return True

def get_base_info(content):
    # BeautifulSoupで解析
    soup = BeautifulSoup(content, 'html.parser')
    raceBasic = soup.find(id='raceBasic')
    # テーブルを見つける(最初のテーブルのみ取得される)
    table = raceBasic.find('table', class_='table_fixed')

    # 全国勝率
    search_text = '勝率'
    found_rows = []
    get_next_row = False
    for row in table.find_all('tr'):
        if get_next_row:
            found_rows.append(row)
            get_next_row = False
            continue
        for cell in row.find_all(['td']):
            if search_text in cell.get_text():
                get_next_row = True

    # 見つけた行から値を抽出
    for row in found_rows:
        row_values = [cell.get_text(strip=True) for cell in row.find_all('td')]

    # 全国勝率の値のリストを返す(最初の項目は全国という文字列)
    row_values.pop(0)
    return [float(value) for value in row_values]

def fetch_frame_info(race_no, place_no, today, slider, browser: Browser) -> RaceDataDTO:
    url_base = 'https://kyoteibiyori.com/race_shusso.php'
    url_param = f'?place_no={place_no}&race_no={race_no}&hiduke={today}'
    # slider0なら基本情報 1なら枠別情報
    url = url_base + url_param + '&slider=' + slider

    # Playwrightを使用してHTMLを取得
    page = browser.new_page()
    page.goto(url, wait_until='domcontentloaded')
    page.wait_for_selector('#raceBasic', timeout=60000)
    page.evaluate("window.stop();")
    content = page.content()

    data = get_escaped_flame_info(content)

    # 結果を返却
    return data

def get_escaped_flame_info(content):
    # BeautifulSoupで解析
    soup = BeautifulSoup(content, 'html.parser')
    raceBasic = soup.find(id='raceBasic')
    # テーブルを見つける(最初のテーブルのみ取得される)
    table = raceBasic.find('table', class_='table_fixed')

    RaceData = RaceDataDTO()

    # 1年と半年の逃げ率と逃がし率
    search_text = '逃げ'
    found_rows = []
    get_next_row = False
    for row in table.find_all('tr'):
        if get_next_row:
            found_rows.append(row)
            get_next_row = False
            continue
        for cell in row.find_all(['td']):
            if search_text in cell.get_text():
                get_next_row = True

    # 見つけた行から値を抽出
    extracted_values = []
    for row in found_rows:
        row_values = [cell.get_text(strip=True) for cell in row.find_all('td')]
        extracted_values.append(row_values)

    RaceData.escape_last_year = from_percent_string_to_float(extracted_values[0][0])
    RaceData.escape_last_half_year = from_percent_string_to_float(extracted_values[0][1])
    RaceData.allow_escape_last_year = from_percent_string_to_float(extracted_values[1][0])
    RaceData.allow_escape_last_half_year = from_percent_string_to_float(extracted_values[1][1])

    # 刺され率
    search_text = '差され'
    found_rows = []
    get_next_row = False
    for row in table.find_all('tr'):
        if get_next_row:
            found_rows.append(row)
            get_next_row = False
            continue
        for cell in row.find_all(['td']):
            if search_text in cell.get_text():
                get_next_row = True

    # 見つけた行から値を抽出
    extracted_values = []
    for row in found_rows:
        row_values = [cell.get_text(strip=True) for cell in row.find_all('td')]
        extracted_values.append(row_values)

    # 直近1年の値のみ使用
    RaceData.pierce_last_year = from_percent_string_to_float(extracted_values[1][0])

    # 捲られ率,捲られ差
    search_text = '捲られ'
    found_rows = []
    get_next_row = False
    for row in table.find_all('tr'):
        if get_next_row:
            # 捲られ率の項目の後に空行があるため、空行をスキップ(コーディングミスってるっぽい)
            cells = row.find_all(['td'])
            if not cells or cells[0].get_text(strip=True) == '':
                continue
            found_rows.append(row)
            get_next_row = False
            continue
        for cell in row.find_all(['td']):
            if search_text in cell.get_text():
                get_next_row = True


    # 見つけた行から値を抽出
    extracted_values = []
    for row in found_rows:
        row_values = [cell.get_text(strip=True) for cell in row.find_all('td')]
        extracted_values.append(row_values)

    # 直近1年の捲られのみ使用
    RaceData.overtake_last_year = from_percent_string_to_float(extracted_values[2][0])


    # 直近10レースで1着の回数
    tables = raceBasic.find_all('table', class_='table_fixed')
    if len(tables) >= 6:
        table = tables[5]
    # テーブルが見つからない場合は処理を終了して結果を返す
    else:
        return RaceData

    rows = table.find_all('tr')
    # 1レーン目のデータだけ見る
    row = rows[5]
    row_values = [cell.get_text(strip=True) for cell in row.find_all('td')]
    RaceData.first_place_in_last_ten_race = row_values.count('1')

    return RaceData


def from_percent_string_to_float(string):
    # パーセント記号を取り除く
    percentage_str = string.replace('%', '')
    # 浮動小数点数に変換
    percentage_value = float(percentage_str)
    return percentage_value
