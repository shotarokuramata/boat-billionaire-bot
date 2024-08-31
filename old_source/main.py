import get_boat_data
import datetime


def main():
    today = datetime.date.today().strftime('%Y%m%d')

    races = get_boat_data.fetch_all_race_info(today)

    targets = []
    for race in races:
        data = get_boat_data.fetch_before_info(race['rno'], race['jcd'], today)
        if not data[0]:
            print('No before data:race ' + race['jcd'] + '#' + race['rno'] + 'R')
            continue

        result = check_is_first_lane_fastest(data)
        if result == False:
            print('first lane is not fastest:race ' + race['jcd'] + '#' + race['rno'] + 'R')
            continue
        targets.append(race)

    # print('target races are below')
    # for target in targets:
    #     print(target['jcd'] + '#' + target['rno'] + 'R')

    # 逃げ情報の解析はjsで構築されるテーブルへの対応が必要
    # escape_data = get_boat_data.fetch_frame_info(8, '03', today)



    for target in targets:
        print(target)


def check_is_first_lane_fastest(data):
    if data[0] == min(data):
        return True
    return False

def race_url(rno, jcd, today):
    url_base = 'https://www.boatrace.jp/owpc/pc/race/racelist'
    url_param = f'?rno={rno}&jcd={jcd}&hd={today}'
    return url_base + url_param

if __name__ == '__main__':
    main()
