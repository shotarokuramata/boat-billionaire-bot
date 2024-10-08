import datetime
import time
import argparse
from pprint import pformat
from playwright.sync_api import sync_playwright

import get_boat_data
import get_kyotei_biyori as biyori
from dto.data import RaceDataDTO
from dto.report import ReportDTO
import mail
import csv
import os
import main as m
import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

def main():
    today = m.get_today()
    csv_file_path = m.get_csv_path(today)

    isFile = os.path.exists(csv_file_path)
    if not isFile:
        print('no file exists')
        exit()


    df = pd.read_csv(csv_file_path)

    race_result_urls = df['race_url'].str.replace('racelist', 'raceresult')

    # レース結果情報を取得してcsvに追記
    result_info_list = []
    environment_info_list = []
    for race in race_result_urls:
        result_info = get_boat_data.fetch_result_info(race)
        result_info_list.append(result_info['race_result'])
        environment_info_list.append(result_info['race_environment'])
    rh = get_result_header()
    re = get_environment_header()
    result_info_df = pd.DataFrame(result_info_list, columns=rh)
    environment_info_df = pd.DataFrame(environment_info_list, columns=re)

    df = pd.concat([df, result_info_df], axis=1)
    df = pd.concat([df, environment_info_df], axis=1)

    df.to_csv('csv/' + today + '_result.csv', index=False)

    mail.send('レース結果', '本日の分析対象レースの結果を添付します。', 'csv/' + today + '_result.csv')

def get_result_header() -> list:
    append_header_list = [
        'rank_1',
        'rank_2',
        'rank_3',
        'rank_4',
        'rank_5',
        'rank_6'
    ]
    return append_header_list

def get_environment_header() -> list:
    append_header_list = [
        'race_distance',
        'wind_speed',
        'wind_direction',
        'wave',
        'won_by'
    ]
    return append_header_list

if __name__ == '__main__':
    main()
