import codecs
import os
import re
import time

dictionary = {}
for root, dirs, files in os.walk('C:/Users/student/Desktop/thai_pages', topdown = False):
    for file in files:
        with codecs.open(os.path.join(root, file), 'r', encoding = 'utf-8') as f:
            name = f.read()
            time.sleep(2)
            pairs = re.findall('/id/.*?>(.*?)</a>', name)#.*?</td><td>(.*?)</td></tr>', name)
            for pair1 in pairs:
                try:
                    pair2 = re.findall(pair1+'.*?</td><td>(.*?)</td></tr>', name)[0]
                    pair = pair1 + ' ' + pair2
                except:
                    pair = ''
                if len(pair) > 300:
                    pair = ''
                else:
                    if 'bpat' in pair:
                        if 'alternate spelling of' not in pair:
                            delete = re.findall('bpat<span.*?<td>', pair)[0]
                            pair = pair.replace(delete, '')
                        else:
                            pair = ''
                    if 'bpan' in pair:
                        if 'alternate spelling of' not in pair:
                            delete = re.findall('bpan.*?<td>', pair)[0]
                            pair = pair.replace(delete, '')
                        else:
                            pair = ''
                if pair == '':
                    continue
                else:
                    if '>' not in pair:
                        words = pair.split(' ', maxsplit=1)
                        for num, i in enumerate(words):
                            dictionary[words[0]] = words[1]
                    
print(dictionary)



