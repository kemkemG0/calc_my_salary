import time
import re
import argparse
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--month", required=True, help="month")
parser.add_argument("-p", "--pay", required=True, help="job pays per hour")
args = parser.parse_args()

month = args.month
pay = int(args.pay)

path = 'timehistory.log'

ymd_pattern = re.compile(
    '[0-9]{4}/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])')
hm_pattern = re.compile('[0-9]{2}:[0-9]{2}')


hi_dict = {}
bye_dict = {}

sum = timedelta()

with open(path) as f:
    for s_line in f:
        if not '@Kenshin Tanaka' in s_line:
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
            if not ymd in hi_dict:
                hi_dict[ymd] = hm
            else:
                if hi_dict[ymd] > hm:
                    hi_dict[ymd] = hm
        else:
            if not ymd in bye_dict:
                bye_dict[ymd] = hm
            else:
                if bye_dict[ymd] < hm:
                    bye_dict[ymd] = hm

for ymd, bye_hm in bye_dict.items():
    if not ymd in hi_dict:
        continue
    hi_hm = hi_dict[ymd]

    bye_hm = datetime.strptime(bye_hm, '%H:%M')
    hi_hm = datetime.strptime(hi_hm, '%H:%M')

    sum += (bye_hm - hi_hm)

hours = sum.days * 24 + sum.seconds/3600

print('働いた時間:', '{:.1f}'.format(hours), '時間')
print('給料:', int(hours*pay), '円')
