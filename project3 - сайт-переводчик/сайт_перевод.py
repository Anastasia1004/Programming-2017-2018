import os
import re
import urllib
from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html'), request.args

@app.route('/translate/')
def translate():
    with open ('input.txt', mode='w', encoding = 'utf-8') as f:
        for key in request.args:
            f.write(request.args[key])
    dictionary = {}
    asterix = ''
    with open('slovarik.txt', 'r', encoding = 'utf-8') as f:
        letter = re.findall('{(.*?)}', f.read())
        for i in letter:
            pairs = i.split(', ')
            for pair in pairs:
                words = pair.split(': ')
                for num, w in enumerate(words):
                    w = w.replace("'", '')
                    dictionary[words[0].replace("'", '')] = words[1].replace("'", '')
    with open ('output.txt', mode='w', encoding = 'utf-8') as f:
        os.system('mystem.exe ' + 'input.txt ' + 'output.txt ' + '-c -d -i')
    vowels = ['а','у','е','ы','о','э','я','и','ю','i', 'ѣ', 'Ѣ', 'І']
    with open ('output.txt', mode='r', encoding = 'utf-8') as f:
        wordsinfo = f.read().split(' ')
        if '' in wordsinfo:
            wordsinfo.remove('')
        if '\n' in wordsinfo:
            wordsinfo.remove('\n')
        text = ''
        for numwi, wordinfo in enumerate(wordsinfo):
            wordform = re.findall('(.*?){',wordinfo)[0]
            lemma = re.findall('{(.*?)=', wordinfo)[0]
            checked_key = 0
            for key in dictionary:
                checked_key += 1
                if lemma == key:
                    forchange = ''
                    beginchange = ''
                    ending = wordform
                    for numw, w in enumerate(wordform):
                        for numl, l in enumerate(lemma):
                            if numw == numl and wordform[numw] == lemma[numl]:
                                forchange += wordform[numw]
                                beginchange = dictionary[key][:len(forchange)]
                                ending = wordform[numw+1:]
                    if '=S,' in wordinfo:
                        if '=дат' in wordinfo  or '=пред' in wordinfo:
                            for num, i in enumerate(ending):
                                if i == 'и' and num != len(ending)-1 and ending[num+1] in vowels:
                                    ending = ending.replace(ending[num+1], 'ѣ')
                                if i == 'и' and num == len(ending)-1:
                                    if len(ending) == 1:
                                        ending = ending.replace(i, 'ѣ')
                                    else:
                                        ending = ending.replace(ending[num-1]+i, ending[num-1]+'ѣ')
                                else:
                                    if i == 'и' and ending[num+1] not in vowels:
                                        ending = ending.replace(i+ending[num+1], 'ѣ'+ending[num+1])
                                if i != 'и': 
                                    for vowel in vowels: 
                                        if i == vowel:
                                            ending = ending.replace(i, 'ѣ')
                    finalword = beginchange + ending
                    if '=A=' in wordinfo:
                        if '=S,' in wordsinfo[numwi+1]:
                            if ',сред' in wordsinfo[numwi+1] or ',жен' in wordsinfo[numwi+1]:
                                finalword = finalword.replace('ие', 'iя')
                                finalword = finalword.replace('ые', 'ыя')
                                finalword = finalword.replace('иеся', 'iяся')

                    m = 0
                    for vowel in vowels:
                        if finalword.endswith(vowel) == False:
                            m+=1
                    if m == 13:
                        if finalword.endswith('ъ') == False and finalword.endswith('ь') == False:
                            finalword = finalword+'ъ'
                    for vowel in vowels:
                        if 'и'+vowel in finalword:
                            finalword = finalword.replace('и'+vowel,'i'+vowel)
                    text += finalword+' '
                    break
                else:
                    if checked_key == len(dictionary):
                        for numw, w in enumerate(wordform):
                            for numl, l in enumerate(lemma):
                                if numw == numl and wordform[numw] == lemma[numl]:
                                    start = wordform[:numw+1]
                                    ending = wordform[numw+1:]
                        if '=S,' in wordinfo:
                            if '=дат' in wordinfo or '=пред' in wordinfo:
                                for num, i in enumerate(ending):
                                    if i == 'и' and num != len(ending)-1 and ending[num+1] in vowels:
                                        ending = ending.replace(ending[num+1], 'ѣ')
                                    if i == 'и' and num == len(ending)-1:
                                        if len(ending) == 1:
                                            ending = ending.replace(i, 'ѣ')
                                        else:
                                            ending = ending.replace(ending[num-1]+i, ending[num-1]+'ѣ')
                                    else:
                                        if i == 'и' and ending[num+1] not in vowels:
                                            ending = ending.replace(i+ending[num+1], 'ѣ'+ending[num+1])
                                    if i != 'и': 
                                        for vowel in vowels: 
                                            if i == vowel:
                                                ending = ending.replace(i, 'ѣ')
                        finalword = start + ending
                        if '=A=' in wordinfo:
                            if '=S,' in wordsinfo[numwi+1]:
                                if ',сред' in wordsinfo[numwi+1] or ',жен' in wordsinfo[numwi+1]:
                                    finalword = finalword.replace('ие', 'iя')
                                    finalword = finalword.replace('ые', 'ыя')
                                    finalword = finalword.replace('иеся', 'iяся')
                        
                        m = 0
                        for vowel in vowels:
                            if finalword.endswith(vowel) == False:
                                m+=1
                        if m == 13:
                            if finalword.endswith('ъ') == False and finalword.endswith('ь') == False:
                                finalword = finalword+'ъ'
                        for vowel in vowels:
                            if 'и'+vowel in wordform:
                                finalword = finalword.replace('и'+vowel,'i'+vowel)
                        asterix = ' (*точность перевода не гарантирована, слова нет в словаре)'
                        text += finalword + '(*) '
                    else:
                        continue
                    
            
    return render_template('translate.html', text = text, asterix = asterix)


@app.route('/mad/')
def breakingmad():
    dictionary = {}
    asterix = ''
    with open('slovarik.txt', 'r', encoding = 'utf-8') as f:
        letter = re.findall('{(.*?)}', f.read())
        for i in letter:
            pairs = i.split(', ')
            for pair in pairs:
                words = pair.split(': ')
                for num, w in enumerate(words):
                    w = w.replace("'", '')
                    dictionary[words[0].replace("'", '')] = words[1].replace("'", '')
    url = 'http://breakingmad.me/ru/collection/7289'
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')
    with open ('pagecode.txt', 'w', encoding = 'utf-8') as f:
        f.write(text)
    with open ('pagecode.txt', 'r', encoding = 'utf-8') as f:
        d = f.read()
        header = re.findall('<h2>(.*?)</h2>', d)[0]
        story1 = re.findall('<p class="leads">(Как.*?)</p>', d)[0]
        extracts = re.findall('<.*?>', story1)
        for i in extracts:
            story1 = story1.replace(i, ' ')
        story2 = re.findall('<p>(Там.*?)</p>', d)[0]
        story3 = re.findall('<p>(В полиции.*?)</p>', d)[0]
        story4 = re.findall('<p>("Ожившего.*?помешало.)', d)[0]
        story = ''
        story = story + story1 + ' ' + story2  + ' ' + story3  + ' ' + story4
        page_text = header + '. ' + story
    with open('page_text_raw.txt', 'w', encoding = 'utf-8') as p:
        p.write(page_text)
    with open ('page_text.txt', mode='w', encoding = 'utf-8') as f:
        os.system('mystem.exe ' + 'page_text_raw.txt ' + 'page_text.txt ' + '-c -d -i')
    vowels = ['а','у','е','ы','о','э','я','и','ю','i', 'ѣ', 'Ѣ', 'І']
    with open ('page_text.txt', mode='r', encoding = 'utf-8') as f:
        wordsinfo = f.read().split(' ')
        if '' in wordsinfo:
            wordsinfo.remove('')
        if '\n' in wordsinfo:
            wordsinfo.remove('\n')
        text = ''
        for numwi, wordinfo in enumerate(wordsinfo):
            if '}' not in wordinfo:
                wordform = wordinfo
                lemma = wordinfo
            else:
                wordform = re.findall('(.*?){',wordinfo)[0]
                lemma = re.findall('{(.*?)=', wordinfo)[0]
            checked_key = 0
            for key in dictionary:
                checked_key += 1
                if lemma == key:
                    forchange = ''
                    beginchange = ''
                    ending = wordform
                    for numw, w in enumerate(wordform):
                        for numl, l in enumerate(lemma):
                            if numw == numl and wordform[numw] == lemma[numl]:
                                forchange += wordform[numw]
                                beginchange = dictionary[key][:len(forchange)]
                                ending = wordform[numw+1:]
                    if '=S,' in wordinfo:
                        if '=дат' in wordinfo  or '=пред' in wordinfo:
                            for num, i in enumerate(ending):
                                if i == 'и' and num != len(ending)-1 and ending[num+1] in vowels:
                                    ending = ending.replace(ending[num+1], 'ѣ')
                                if i == 'и' and num == len(ending)-1:
                                    if len(ending) == 1:
                                        ending = ending.replace(i, 'ѣ')
                                    else:
                                        ending = ending.replace(ending[num-1]+i, ending[num-1]+'ѣ')
                                else:
                                    if i == 'и' and ending[num+1] not in vowels:
                                        ending = ending.replace(i+ending[num+1], 'ѣ'+ending[num+1])
                                if i != 'и': 
                                    for vowel in vowels: 
                                        if i == vowel:
                                            ending = ending.replace(i, 'ѣ')
                    finalword = beginchange + ending
                    if '=A=' in wordinfo:
                        if '=S,' in wordsinfo[numwi+1]:
                            if ',сред' in wordsinfo[numwi+1] or ',жен' in wordsinfo[numwi+1]:
                                finalword = finalword.replace('ие', 'iя')
                                finalword = finalword.replace('ые', 'ыя')
                                finalword = finalword.replace('иеся', 'iяся')

                    m = 0
                    for vowel in vowels:
                        if finalword.endswith(vowel) == False:
                            m+=1
                    if m == 13:
                        if finalword.endswith('ъ') == False and finalword.endswith('ь') == False:
                            finalword = finalword+'ъ'
                    for vowel in vowels:
                        if 'и'+vowel in finalword:
                            finalword = finalword.replace('и'+vowel,'i'+vowel)
                    if '}.' in wordinfo:
                        finalword += '.'
                    if '},' in wordinfo:
                        finalword += ','
                    if '}"' in wordinfo or '}»' in wordinfo:
                        finalword = '"' + finalword + '"'
                    if '}",' in wordinfo:
                        finalword = '"' + finalword + '",'
                    text += finalword+' '
                    break
                else:
                    if '24' in wordinfo or '–' in wordinfo or ' ' in wordinfo:
                        text += wordinfo+' '
                        break
                    else:
                        start = ''
                        ending = ''
                        if checked_key == len(dictionary):
                            for numw, w in enumerate(wordform):
                                for numl, l in enumerate(lemma):
                                    if numw == numl and wordform[numw] == lemma[numl]:
                                        start = wordform[:numw+1]
                                        ending = wordform[numw+1:]
                            if '=S,' in wordinfo:
                                if '=дат' in wordinfo or '=пред' in wordinfo:
                                    for num, i in enumerate(ending):
                                        if i == 'и' and num != len(ending)-1 and ending[num+1] in vowels:
                                            ending = ending.replace(ending[num+1], 'ѣ')
                                        if i == 'и' and num == len(ending)-1:
                                            if len(ending) == 1:
                                                ending = ending.replace(i, 'ѣ')
                                            else:
                                                ending = ending.replace(ending[num-1]+i, ending[num-1]+'ѣ')
                                        else:
                                            if i == 'и' and ending[num+1] not in vowels:
                                                ending = ending.replace(i+ending[num+1], 'ѣ'+ending[num+1])
                                        if i != 'и': 
                                            for vowel in vowels: 
                                                if i == vowel:
                                                    ending = ending.replace(i, 'ѣ')
                            finalword = start + ending
                            if '=A=' in wordinfo:
                                if '=S,' in wordsinfo[numwi+1]:
                                    if ',сред' in wordsinfo[numwi+1] or ',жен' in wordsinfo[numwi+1]:
                                        finalword = finalword.replace('ие', 'iя')
                                        finalword = finalword.replace('ые', 'ыя')
                                        finalword = finalword.replace('иеся', 'iяся')
                        
                            m = 0
                            for vowel in vowels:
                                if finalword.endswith(vowel) == False:
                                    m+=1
                            if m == 13:
                                if finalword.endswith('ъ') == False and finalword.endswith('ь') == False:
                                    finalword = finalword+'ъ'
                            for vowel in vowels:
                                if 'и'+vowel in wordform:
                                    finalword = finalword.replace('и'+vowel,'i'+vowel)
                            if '}.' in wordinfo:
                                finalword += '.'
                            if '},' in wordinfo:
                                finalword += ','
                            if '}"' in wordinfo or '}»' in wordinfo:
                                finalword = '"' + finalword + '"'
                            if '}",' in wordinfo:
                                finalword = '"' + finalword + '",'
                            asterix = ' (*точность перевода не гарантирована, многих упомянутых слов нет в словаре)'
                            text += finalword + ' '
                        else:
                            continue
    text = text.replace('""ъ"",', '"покойного",') ##Программе почему-то не нравятся эти слова, хотя между ними нет ничего общего. 
    text = text.replace('"ъ"', '"Умерший"')##Моя теория в том, что ее моральные принципы не позволяют шутить над смертью.
    text = text.replace('. ъ', '. Ожившего')
    endtext = ''
    a = text.split(' ')
    for num, i in enumerate(a):
        if num > 0 and a[num-1].endswith('.') == True:
            i = i.title()
        endtext += i+' '
                                                                                      
    with open('mad.txt', 'w', encoding = 'utf-8') as ans:
        ans.write(endtext)                         
                                                

    return render_template('mad.html', endtext = endtext, asterix = asterix)

    
 
if __name__ == '__main__':
    app.run(debug=True)
