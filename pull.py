import requests

SHEET_URL = 'https://docs.google.com/spreadsheets/d/1z5JfDt0nUjpKEcLX3Ws9LaQe_I7NFwPGQkuS_HIOr9M/edit?usp=sharing'

def update_score():
    r = requests.get(SHEET_URL)
    list = r.text.split(',00E')
    del list[-1]
    res = []
    for i in list:
        res.append(int(''.join([j for j in i[-2::1] if j.isdigit()])))
    return res

def update_last_task():
    r = requests.get(SHEET_URL)
    list = ''.join(r.text.split(',00E')).split(',00')
    del list[-1]
    res =[]
    for i in list:
        res.append(int(''.join([j for j in i[-3::1] if j.isdigit()])))
    return res

def update_tasks():
    res = {17, 41, 47, 50, 62, 65, 69, 72, 73, 85, 86, 87, 109, 112, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132}
    ## FIXME:Баг с таблицами
    '''r = requests.get(SHEET_URL)
    with open('output', 'w') as f:
        print(r.text, file=f)
    list = r.text.split('@@@@')
    print(len(list))
    del list[-1]
    print(len(list))
    res = set()
    index = 0
    for i in list:
        if i[-1] == 'T' or i[-1] == 'F':
             index+=1
        print(i[-1], index)
        if i[-1] == 'F':
            res.add(i)'''
    return res
