import os
import json
from datetime import datetime, timedelta


dir_path = os.path.dirname(os.path.realpath(__file__))


outData = list()
outputFileName = ("{}/data/temporalTweetCount.csv".format(dir_path))
outData.append(["Date","Total",
                "#trump2016", "#makeamericagreatagain",
                "#imwithher", "#hillary2016",
                "#nevertrump", "#dumptrump",
                "#dropouthillary", "#neverhillary",
                'FavorTrump', 'FavorClinton', 'AgainstTrump', 'AgainstClinton'])



d_s = datetime(2016,11,7).strftime('%Y-%m-%d')
d_s = datetime.strptime(str(d_s), '%Y-%m-%d')
tL = [d_s - timedelta(days=x) for x in range(0, 60)]
d_l = ','.join([str(each_time.strftime("%m%d")) for each_time in tL])
ds = [str(each_time.strftime("%Y-%m-%d")) for each_time in tL]

for d in ds:
    Y, M, D = d.split('-')
    date_start = datetime(int(Y),int(M),int(D),23).strftime('%Y-%m-%d-%H')
    date_start = datetime.strptime(str(date_start), '%Y-%m-%d-%H')
    timeLines = [date_start - timedelta(hours=x) for x in range(0, 1 * 24)]
    date_list = ','.join([str(each_time.strftime("%m%d")) for each_time in timeLines])
    days = [str(each_time.strftime("%Y-%m-%d-%H")) for each_time in timeLines]

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
    date = M+D
    outData.append([date,str(total), str(ht1), str(ht2), str(ht3), str(ht4), str(ht5), str(ht6), str(ht7), str(ht8), str(ft), str(fc), str(at), str(ac)])

outString = ""

for l in outData:
    outString += ",".join(l)
    outString += "\n"

with open(outputFileName, 'w') as f:
    f.write(outString)
    f.close()