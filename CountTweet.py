import os
import json
from datetime import datetime, timedelta


dir_path = os.path.dirname(os.path.realpath(__file__))
total = 0
ht1 = 0
ht2 = 0
ht3 = 0
ht4 = 0
ht5 = 0
ht6 = 0
ht7 = 0
ht8 = 0
ft = 0
fc = 0
at = 0
ac = 0


outData = list()
outputFileName = ("{}/data/tweetCountByHashtags".format(dir_path))

date_start = datetime(2016,11,8,16).strftime('%Y-%m-%d-%H')
date_start = datetime.strptime(str(date_start), '%Y-%m-%d-%H')
timeLines = [date_start - timedelta(hours=x) for x in range(0, 62 * 24)]
date_list = ','.join([str(each_time.strftime("%m%d")) for each_time in timeLines])
days = [str(each_time.strftime("%Y-%m-%d-%H")) for each_time in timeLines]

for day in days:
    YEAR, MONTH, DAY, HOUR = day.split('-')
    inputDirLocation = ("{}/data/stance/{}{}{}{}_keywords.json".format(dir_path, YEAR, MONTH, DAY, HOUR))
    data = []
    with open(inputDirLocation) as file:
        data = data + json.load(file)
    file.close();
    for item in data:
        total += 1
        if (item['ht1'] > 0):
            ht1 += 1
        if (item['ht2'] > 0):
            ht2 += 1
        if (item['ht3'] > 0):
            ht3 += 1
        if (item['ht4'] > 0):
            ht4 += 1
        if (item['ht5'] > 0):
            ht5 += 1
        if (item['ht6'] > 0):
            ht6 += 1
        if (item['ht7'] > 0):
            ht7 += 1
        if (item['ht8'] > 0):
            ht8 += 1
        if (item['ht1'] + item['ht2'] > 0):
            ft += 1
        if (item['ht3'] + item['ht4'] > 0):
            fc += 1
        if (item['ht5'] + item['ht6'] > 0):
            at += 1
        if (item['ht7'] + item['ht8'] > 0):
            ac += 1

outData.append(['Total', str(total)])
outData.append(['Trump2016', str(ht1)])
outData.append(['MakeAmericaGreatAgain', str(ht2)])
outData.append(['ImWithHer', str(ht3)])
outData.append(['Hillary2016', str(ht4)])
outData.append(['NeverTrump', str(ht5)])
outData.append(['DumpTrump', str(ht6)])
outData.append(['DropOutHillary', str(ht7)])
outData.append(['NeverHillary', str(ht8)])
outData.append(['FavorTrump', str(ft)])
outData.append(['FavorClinton', str(fc)])
outData.append(['AgainstTrump', str(at)])
outData.append(['AgainstClinton', str(ac)])

outString = ""

for l in outData:
    outString += " ".join(l)
    outString += "\n"

with open(outputFileName, 'w') as f:
    f.write(outString)
    f.close()