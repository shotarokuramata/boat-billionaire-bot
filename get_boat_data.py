import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import re

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

def fetch_result_info(url):
    response = requests.get(url)
    response.raise_for_status()  # エラーチェック

    with open('output2.html', 'wb') as file:
        file.write(response.content)

    data = {}
    data['race_result'] = get_raceresult_info(response.content)
    data['race_environment'] = get_environment_info(response.content)
    return data

def get_raceresult_info(content):
    # BeautifulSoupで解析
    soup = BeautifulSoup(content, 'html.parser')


    # テーブルを見つける
    units = soup.find_all('div', class_='grid_unit')

    with open('output.txt', 'w', encoding='utf-8') as f:
        for unit in units:
            f.write(str(unit))
            f.write('\n')  # 各要素の間に空行を追加

    result_unit = units[0]
    result_data = get_result_info(result_unit)

    return result_data

def get_result_info(result_unit):
    tds = result_unit.find_all('td', class_=re.compile(r'is-boatColor\d+'))
    data = [item.get_text(strip=True) for item in tds]
    return data

def get_environment_info(content):
    # BeautifulSoupで解析
    soup = BeautifulSoup(content, 'html.parser')

    # 天気関連情報
    weather_html = soup.find('div', class_='weather1')
    data = {}
    wind_html = weather_html.find('div', class_='is-wind')
    data['wind_speed'] = wind_html.find('span', class_='weather1_bodyUnitLabelData').get_text(strip=True)
    wind_direction_div = weather_html.find('div', class_='is-windDirection')
    data['wind_direction'] = wind_direction_div.find('p').get('class')[1].replace('is-wind', '')

    wave_html = weather_html.find('div', class_='is-wave')
    data['wave'] = wave_html.find('span', class_='weather1_bodyUnitLabelData').get_text(strip=True)

    # その他レース情報
    race_distance = soup.find('h3', class_='title16_titleDetail__add2020')
    race_distance_text = race_distance.get_text(strip=True)
    race_distance_text = re.sub(r'\D', '', race_distance_text)
    data['race_distance'] = race_distance_text

    won_by_td = soup.find('td', class_='is-fs16')
    data['won_by'] = won_by_td.get_text(strip=True)

    return data
