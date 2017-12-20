import urllib.request
import re
import json

def make_dict():
    preurl = 'http://www.dorev.ru/ru-index.html?l=' 
    posturls = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'dd', 'de', 'df']
    for posturl in posturls:
        url = preurl + posturl
        print(url)
        response = urllib.request.urlopen(url)
        text = response.read().decode('cp1251')
        words = re.findall(';</td><td class="uu">(.*?)</td><td></td><td class="uu">(.*?)(</| |<span class="u0"><span class="u1">(.*?)</span><span class="u(2|3)">(.*?)</span></span>(.*?)(<|,| ))', text)
        slovarik = {}
        with open('slovar.txt', 'w', encoding = 'utf-8') as f:
            for element in words:
                for c, i in enumerate(element):
                    if len(i)>20 or i == '2' or i == '3' or i == ' ' or i == "'" or i == ',' or i == '<' or i == '</':
                        continue
                    else:
                        f.write(str(i))
                        if c == 0:
                            f.write(' ')
                        else:
                            continue
                f.write(',')
        with open('slovar.txt', 'r', encoding = 'utf-8') as f:
            dorev = f.read().replace('&#1110;', 'i')
            dorev = dorev.replace('&#1123;', 'ѣ')
            dorev = dorev.replace('&#1139;', 'ѳ')
            dorev = dorev.replace('&#1130;', 'Ѣ')
            dorev = dorev.replace('&#1122;', 'Ѣ')
            dorev = dorev.replace('&#1030;', 'І')
            dorev1 = dorev.replace('&#1138;', 'Ѳ')
            pairs = dorev1.split(',')
            for i in pairs:
                pair = i.split(' ')
                for p in enumerate(pair):
                    slovarik[pair[0]] = pair[-1]
            with open('slovarik.txt', 'a+', encoding = 'utf-8') as f:
                f.write(str(slovarik))                
                return f

make_dict()
