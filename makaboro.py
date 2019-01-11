import requests, re, sys, os
import urllib2
import csv
import argparse
from pwn import *
from bs4 import BeautifulSoup
from datetime import datetime

waktu = datetime.now()
tahun = waktu.year
bulan = waktu.month
hari = waktu.day
#
parser = argparse.ArgumentParser()
parser.add_argument("--page", help="Input page target ", nargs='+')
parser.add_argument("--output", help="Input output name", nargs='+')

args = parser.parse_args()
argspace = ' '.join(args.page)
keyword = str(argspace)
argoutput = ' '.join(args.output)
keyword2 = str(argoutput)

url = '%s' % keyword
sess = requests.session()

log.progress("Wait, It's Working...")

#input cookie press f12, find ZHE and PHPSESSID
myCookie = {
    'ZHE':'931be96f0472188542f55e28feea8b96',
    'ZH':'931be96f0472188542f55e28feea8b96',
    'PHPSESSID':'ldupdnp10tsgo6jdqh84n5mh81'
}

data = sess.get(url, cookies=myCookie)
data2 = data.content
bs = BeautifulSoup(data2, 'lxml')
table_body = bs.find('table')
rows = table_body.find_all('tr', class_=None)[1:]

with open('output/zoneH-{}-{}-{}-{}.csv'.format(tahun, bulan, hari, keyword2), 'a') as csvfile:
    writecsv = csv.writer(csvfile)
    writecsv.writerow(["Halaman Terdeface", "Attacker", "Tebas Index", "Kejadian", "Arsip"])

    for row in rows:
        kolom = row.findAll('td')

        if len(kolom) > 1:
            halaman = kolom[7].text
            attacker = kolom[1].text
            tebas = kolom[2].text.replace("H", "Y").replace("", "T").replace("TYT", "Y") #wkwkwkgoblok
            kejadian = kolom[0].text
            arsip = kolom[9].find('a').get('href')
            writecsv.writerow([halaman, attacker, tebas, kejadian, str('www.zone-h.org%s' % arsip)])
log.info("Done !!")
