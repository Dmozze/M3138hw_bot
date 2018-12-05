import requests

def pull():
    r = requests.get('https://docs.google.com/spreadsheets/d/1z5JfDt0nUjpKEcLX3Ws9LaQe_I7NFwPGQkuS_HIOr9M/edit?usp=sharing')
    list = r.text.split(',00E')
    del list[-1]
    res = []
    for i in list:
        res.append({'count_of_tasks': ''.join(j for j in i[-2::1] if j.isdigit())})
    list = ''.join(r.text.split(',00E')).split(',00')
    for i in range(len(list) - 1):
        print(type(res[i]))
        res[i].update({'last_task': ''.join(j for j in list[i][-3::1] if j.isdigit())})
    return res
