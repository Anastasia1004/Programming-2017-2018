from flask import Flask
from flask import render_template, request, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html'), request.args

@app.route('/form/')
def data():
    with open ('form.txt', mode='a', encoding = 'utf-8') as f:
         for key in request.args:
            f.write(key)
            f.write('--')
            f.write(request.args[key])
            f.write(' ')
         f.write('Sent. ')
         
    return render_template('form.html')

@app.route('/stats/')
def stats():
    with open ('form.txt', mode='r', encoding = 'utf-8') as f:
        statistics1 = {}
        statistics2 = {}
        statistics3 = {}
        statistics4 = {}
        for line in f.read().split(' '):
            if 'жИза' in line or 'жизА' in line:
                if line not in statistics1:
                    statistics1[line] = 1
                else:
                    statistics1[line] += 1
            if 'гУглить' in line or 'гуглИть' in line:
                if line not in statistics2:
                    statistics2[line] = 1
                else:
                    statistics2[line] += 1
            if 'возраст' in line or 'пол_ж' in line or 'пол_м' in line or 'родился' in line or 'жил' in line:
                if line not in statistics3:
                    statistics3[line] = 1
                else:
                    statistics3[line] += 1
            if 'школьник' in line or '9_классов' in line or '11_классов' in line or 'студент' in line or 'высшее' in line:
                if line not in statistics4:
                    statistics4[line] = 1
                else:
                    statistics4[line] += 1
    with open ('stats.txt', mode='w', encoding = 'utf-8') as f:
        for i in statistics1:
            f.write(i)
            f.write(' ')
            f.write(str(statistics1[i]))
            f.write('\n')
        f.write('\n\n\n')
        for i in statistics2:
            f.write(i)
            f.write(' ')
            f.write(str(statistics2[i]))
            f.write('\n')
        f.write('\n\n\n')
        for i in statistics3:
            f.write(i)
            f.write(' ')
            f.write(str(statistics3[i]))
            f.write('\n')
        f.write('\n\n\n')
        for i in statistics4:
            f.write(i)
            f.write(' ')
            f.write(str(statistics4[i]))
            f.write('\n')
        f.write('\n\n\n')
    with open ('stats.txt', mode='r', encoding = 'utf-8') as f:
        stats = f.readlines()
        
        return render_template('stats.html', stats = stats)  

@app.route('/json/')
def json1():
    with open ('form.txt', mode='r', encoding = 'utf-8') as f:
        with open('jsondata.json', mode='r+', encoding = 'utf-8') as k:
            mass = f.read().split(' ')
            for i in mass:
                json.dump(i, k, ensure_ascii = False)
                k.write(' ')
            show = k.readlines()

            return render_template('forjson.html', show = show)
        

@app.route('/search/')
def search():
    return render_template('search.html'), request.args

@app.route('/results/')
def results():
    k = 0
    arr = []
    with open ('form.txt', mode='r', encoding = 'utf-8') as f:
        answers1 = f.read()
        answers = answers1.split('Sent. ')
        for line in answers:
            m = 0
            for key in request.args:
                if 'родился' in key or 'жил' in key or 'возраст' in key:
                    if request.args[key] != '' and request.args[key] in line:
                        m += 1
                    else:
                        m = m
                else:
                    if key in line:
                        m += 1 
                    else:
                        m = m
            if m == 2:
                k += 1
                arrline = line + '\n'
                arr.append(arrline)
            else:
                continue
        lenans = len(answers)-1
        return render_template('results.html', lenans = lenans, k = k, arr = arr)
        
                    
    

if __name__ == '__main__':
    app.run(debug=True)
