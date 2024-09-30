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

def main(place_no: int):
    today = datetime.date.today().strftime('%Y%m%d')

    # 全レース場に対してスクレイピングすると回線に問題が出るので1レース場に限定する
    # races = get_boat_data.fetch_all_race_info(today)
    # place_no_list = [race["jcd"] for race in races]
    place_no = place_no

    rounds = 12

    report_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for round in range(1, rounds + 1):
            report = ReportDTO()
            report.race_url = get_race_url(round, place_no, today)
            result = biyori.check_is_target_race(round, place_no, today, '0', browser)
            if result == False:
                report.message = 'this is not target: place'+ str(place_no) + '&round' + str(round)
                report_list.append(report)
                continue
            data = biyori.fetch_frame_info(round, place_no, today, '1', browser)
            report.data = data
            report_list.append(report)
        browser.close()

    for report in report_list:
        if report.message is None:
            if report.data.is_target():
                report.message = '対象データです'
            else:
                report.message = 'データを抽出しましたが、条件に合致しませんでした。'

    subject = 'bot実行結果 会場NO:' + str(place_no) + ' 日付:' + today
    msg = ''

    for r in report_list:
        msg += 'Race URL: ' + r.race_url + '\n'
        msg += 'Message: ' + r.message + '\n'
        if r.data:
            msg += 'Data: ' + pformat(r.data) + '\n'
        msg += '-' * 40 + '\n'

    mail.send(subject, msg)


    valid_data_list = [r for r in report_list if r.message == '対象データです']

    if valid_data_list == []:
        print('csv対象データなし。')
        return

    csv_file_path = 'csv/output.csv'
    isFile = os.path.exists(csv_file_path)
    with open(csv_file_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        if not isFile:
            header = valid_data_list[0].get_csv_header_list()
            writer.writerow(header)

        for r in valid_data_list:
            body = r.get_csv_body_list()
            writer.writerow(body)

def get_race_url(rno, jcd, today):
    if rno < 10:
        rno = '0' + str(rno)
    if jcd < 10:
        jcd = '0' + str(jcd)
    url_base = 'https://www.boatrace.jp/owpc/pc/race/racelist'
    url_param = f'?rno={rno}&jcd={jcd}&hd={today}'
    return url_base + url_param

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('place_no', type=int, help='The place number')

    args = parser.parse_args()
    main(args.place_no)
