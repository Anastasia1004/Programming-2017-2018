import urllib.request
import re
import os
import shutil
import time
    
def date_number(d):
    date_number = d.replace(' января ', '.01.')
    date_number = date_number.replace(' февраля ', '.02.')
    date_number = date_number.replace(' марта ', '.03.')
    date_number = date_number.replace(' апреля ', '.04.')
    date_number = date_number.replace(' мая ', '.05.')
    date_number = date_number.replace(' июня ', '.06.')
    date_number = date_number.replace(' июля ', '.07.')
    date_number = date_number.replace(' августа ', '.08.')
    date_number = date_number.replace(' сентября ', '.09.')
    date_number = date_number.replace(' октября ', '.10.')
    date_number = date_number.replace(' ноября ', '.11.')
    date_number = date_number.replace(' декабря ', '.12.')
    date_number = date_number.replace(' Января ', '.01.')
    date_number = date_number.replace(' Февраля ', '.02.')
    date_number = date_number.replace(' Марта ', '.03.')
    date_number = date_number.replace(' Апреля ', '.04.')
    date_number = date_number.replace(' Мая ', '.05.')
    date_number = date_number.replace(' Июня ', '.06.')
    date_number = date_number.replace(' Июля ', '.07.')
    date_number = date_number.replace(' Августа ', '.08.')
    date_number = date_number.replace(' Сентября ', '.09.')
    date_number = date_number.replace(' Октября ', '.10.')
    date_number = date_number.replace(' Ноября ', '.11.')
    date_number = date_number.replace(' Декабря ', '.12.')
    return date_number


def meta_create(file): 
    with open (file, 'w', encoding='utf-8') as f:
        metadata = ('path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n')
        f.write(metadata)
    
def meta_add(file, path, header, created, source, publ_year):
    with open (file,'a', encoding='utf-8') as f:
        metadata = (path + '\t\t\t\t\t' + header + '\t' + created +'\tпублицистика\t\t\t\t\t\tнейтральный\tн-возраст\tн-уровень\tгородская\t' + source + '\tГородские известия\tpublisher\t' + publ_year + '\tгазета\tРоссия\tКурская область\tru\n')
        f.write(metadata)
    
        
def download_page(url, start_page, end_page):
    if os.path.exists('gorodskiye_izvestiya_kursk/metadata.csv'):
        shutil.move('gorodskiye_izvestiya_kursk/metadata.csv', './')
    if os.path.exists('metadata.csv'):
        with open ('metadata.csv', 'r', encoding='utf-8') as f:
            lastline = f.readlines()[-1]
            page = int(''.join(re.findall('gorodskiye_izvestiya_kursk/plain/(.*?).txt', lastline)))
            if page > start_page:
                start_page = page + 1
    else:
        meta_create('metadata.csv')
    for i in range(start_page, end_page):
        try:
            req = urllib.request.Request(url + str(i), headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
            with urllib.request.urlopen(req) as response:
                code = response.read().decode('cp1251')
                header = ''.join(re.findall('<h1>(.*?)</h1>', code))
                created = date_number(''.join(re.findall('</h1>(.*?)<', code, flags=re.DOTALL)))
                publ_year = created[6:10]
                publ_month = created[3:5]
                text = ''.join(re.findall('<span style="font-size:16px;">(.*?)</span>', code, flags=re.DOTALL))
                text = text.join(re.findall('<p>(.*?)<span', code, flags=re.DOTALL))
                text = re.sub('<.*?>', '', text)
                text = re.sub('Поделитесь с друзьями:  Последние новости', '', text)
                text = re.sub('Поделитесь с друзьями:', '', text)
                with open (str(i) + '.txt', 'w', encoding='utf-8') as f:
                    f.write('@au ' + 'Noname' + '\n')
                    f.write('@da ' + created + '\n')
                    f.write('@url ' + url + str(i) + '\n')
                    f.write(text)
                if not os.path.exists('gorodskiye_izvestiya_kursk/mystem-plain/' + publ_year + '/' + publ_month):
                    os.makedirs('gorodskiye_izvestiya_kursk/mystem-plain/' + publ_year + '/' + publ_month)
                if not os.path.exists('gorodskiye_izvestiya_kursk/mystem-xml/' + publ_year + '/' + publ_month):
                    os.makedirs('gorodskiye_izvestiya_kursk/mystem-xml/' + publ_year + '/' + publ_month)
                os.system('mystem.exe ' + str(i)+'.txt ' + 'gorodskiye_izvestiya_kursk/mystem-plain/'+publ_year+'/'+publ_month+'/'+str(i)+'.txt ' + '-n -d -i --generate-all')
                os.system('mystem.exe ' + str(i)+'.txt ' + 'gorodskiye_izvestiya_kursk/mystem-xml/'+publ_year+'/'+publ_month+'/'+str(i)+'.xml ' + '-n -d -i --format="xml" --generate-all')
                if not os.path.exists('gorodskiye_izvestiya_kursk/plain/' + publ_year + '/' + publ_month + '/' + str(i) +  '.txt'):
                    if not os.path.exists('gorodskiye_izvestiya_kursk/plain/' + publ_year + '/' + publ_month):
                        os.makedirs('gorodskiye_izvestiya_kursk/plain/' + publ_year + '/' + publ_month)
                    shutil.move(str(i) + '.txt', 'gorodskiye_izvestiya_kursk/plain/' + publ_year + '/' + publ_month)
                else:
                    os.remove('gorodskiye_izvestiya_kursk/plain/' + publ_year + '/' + publ_month + '/' + str(i) +  '.txt')
                    shutil.move(str(i) + '.txt', 'gorodskiye_izvestiya_kursk/plain/' + publ_year + '/' + publ_month)
                meta_add('metadata.csv', 'gorodskiye_izvestiya_kursk/plain/' + str(i) + '.txt', header, created, url + str(i), publ_year)
                print('Succesfully downloaded page ' + url + str(i))
        except:
            print('Error:  ' + url + str(i))
    shutil.move('metadata.csv', 'gorodskiye_izvestiya_kursk/metadata.csv')
    
download_page('http://gikursk.ru/news/', 1, 5000)

