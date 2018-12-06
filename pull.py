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
    r = requests.get(SHEET_URL)
    list = r.text.split('$$')
    del list[-1]
    res = set()
    for i in range(len(list)):
        if list[i][-1] = 'F':
            res.add(i + 1)
    return res
