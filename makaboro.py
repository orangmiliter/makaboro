import requests
import csv
import argparse
from bs4 import BeautifulSoup
from datetime import datetime
from cookies import cookie

waktu = datetime.now()
tahun = waktu.year
bulan = waktu.month
hari = waktu.day
#
parser = argparse.ArgumentParser()
parser.add_argument("--start", help="Input page start ", nargs='+')
parser.add_argument("--stop", help="input page stop", nargs='+')
parser.add_argument("--output", help="Output file Name", nargs='+')

args = parser.parse_args()
startJoin = ''.join(args.start)
start = str(startJoin)
stopJoin = ''.join(args.stop)
stop = str(stopJoin)
outputJoin = ''.join(args.output)
output = str(outputJoin)

start = int(start)
stop = int(stop)

with open('output/zoneH-{}-{}-{}-{}.csv'.format(tahun, bulan, hari, output), 'a') as csvfile:
    writecsv = csv.writer(csvfile)
    writecsv.writerow(["Institusi", "Halaman Terdeface", "Attacker", "Tebas Index", "Kejadian", "Arsip"])

    print("[+] wait, It's Working...")

    for i in range(start, stop+1):
        url = 'http://www.zone-h.org/archive/filter=1/special=1/domain=go.id/fulltext=1/page=%s' % i
        sess = requests.session()

        # log.progress("Wait, It's Working...")

        myCookie = {
            'ZHE':cookie['ZHE'],
            'ZH':cookie['ZH'],
            'PHPSESSID':cookie['PHPSESSID']
        }

        data = sess.get(url, cookies=myCookie)
        data2 = data.content
        bs = BeautifulSoup(data2, 'lxml')
        table_body = bs.find('table')
        rows = table_body.find_all('tr', class_=None)[1:]

        for row in rows:
            kolom = row.findAll('td')

            if len(kolom) > 1:
                halaman = kolom[7].text.encode('utf-8')
                attacker = kolom[1].text.encode('utf-8)
                tebas = kolom[2].text.replace("H", "Y").replace("", "T").replace("TYT", "Y") #wkwkwkgoblok
                kejadian = kolom[0].text.replace('/', '-')
                arsip = kolom[9].find('a').get('href')
                writecsv.writerow([None, halaman, attacker, tebas, str('%s 00:00:00' % kejadian), str('www.zone-h.org%s' % arsip)])

    print("[✔] Done")
