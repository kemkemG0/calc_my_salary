import time
import re
import argparse
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--month", required=False,
                    help="month", default=datetime.now().month)
parser.add_argument("-p", "--pay", required=False,
                    help="job pays per hour", default=2000)
parser.add_argument("-n", "--name", required=False,
                    help="name", default="Kenshin Tanaka")
args = parser.parse_args()

month = args.month
pay = int(args.pay)
name = args.name

path = 'timehistory.log'

ymd_pattern = re.compile(
    '[0-9]{4}/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])')
hm_pattern = re.compile('[0-9]{2}:[0-9]{2}')


hi_dict = {}
bye_dict = {}

sum = timedelta()


with open(path) as f:
    for s_line in f:
        if not f'@{name}' in s_line:
            continue
        ymd = ymd_pattern.search(s_line)
        hm = hm_pattern.search(s_line)

        if not ymd or not hm:
            continue
        ymd = ymd.group()
        hm = hm.group()
        if int(ymd.split('/')[1]) != int(month):
            continue

        if 'おはよう' in s_line or '出勤' in s_line:
            hi_dict[ymd] = hm
        else:
            bye_dict[ymd] = hm
        if ymd in hi_dict and ymd in bye_dict:
            _hi_hm = datetime.strptime(hi_dict[ymd], '%H:%M')
            _bye_hm = datetime.strptime(bye_dict[ymd], '%H:%M')
            assert(_hi_hm <= _bye_hm)

for ymd, bye_hm in bye_dict.items():
    if not ymd in hi_dict:
        continue
    hi_hm = hi_dict[ymd]
    print(ymd, f"\n   出勤　{hi_hm}    退勤　{bye_hm}")

    bye_hm = datetime.strptime(bye_hm, '%H:%M')
    hi_hm = datetime.strptime(hi_hm, '%H:%M')

    sum += (bye_hm - hi_hm)

hours = sum.days * 24 + sum.seconds/3600

print('出勤日数: ', len(bye_dict), '日')
print('時間:', '{:.1f}'.format(hours), '時間')
print('給料:', int(hours*pay), '円')
