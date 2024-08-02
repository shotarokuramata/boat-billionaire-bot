import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def fetch_all_race_info(today):
    url = 'https://www.boatrace.jp/owpc/pc/race/index?hd=' + today

    # HTMLを取得
    response = requests.get(url)
    response.raise_for_status()  # エラーチェック

    with open('test.html', 'wb') as file:
        file.write(response.content)

    soup = BeautifulSoup(response.content, 'html.parser')

    # 特定の文字列を含む要素を検索
    def contains_text(tag):
        return tag.name == 'a' and '/owpc/pc/race/beforeinfo' in tag.get('href', '')

    elements = soup.find_all(contains_text)

    query_params_list = []
    for e in elements:
        href = e.get('href')
        # URLを解析してクエリパラメータを抽出
        parsed_url = urlparse(href)
        query_params = parse_qs(parsed_url.query)
        query_params_str = {k: v[0] if isinstance(v, list) else v for k, v in query_params.items()}
        query_params_list.append(query_params_str)

    return query_params_list



def fetch_before_info(rno, jcd, today):
    url_base = 'https://www.boatrace.jp/owpc/pc/race/beforeinfo'

    url_param = f'?rno={rno}&jcd={jcd}&hd={today}'
    url = url_base + url_param

    # HTMLを取得
    response = requests.get(url)
    response.raise_for_status()  # エラーチェック

    with open('output.html', 'wb') as file:
        file.write(response.content)

    data = get_exhibition_times(response.content)

    # 結果を返却
    return data

def get_exhibition_times(content):
    # BeautifulSoupで解析
    soup = BeautifulSoup(content, 'html.parser')

    # テーブルを見つける
    table = soup.find('table', class_='is-w748')

    # テーブル情報から展示タイムのみを抽出(面倒だから固定値)
    exhibition_time_index = 4
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if exhibition_time_index < len(cols):
            data.append(cols[exhibition_time_index].text.strip())

    return data


def fetch_frame_info(race_no, place_no, today):
    url_base = 'https://kyoteibiyori.com/race_shusso.php'

    url_param = f'?place_no={place_no}&race_no={race_no}&hiduke={today}'
    url = url_base + url_param + '&slider=1'

    # HTMLを取得
    response = requests.get(url)
    response.raise_for_status()  # エラーチェック

    with open('output2.html', 'wb') as file:
        file.write(response.content)

    data = get_escape_info(response.content)

    # 結果を返却
    return data

def get_escape_info(content):
    # BeautifulSoupで解析
    soup = BeautifulSoup(content, 'html.parser')

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
