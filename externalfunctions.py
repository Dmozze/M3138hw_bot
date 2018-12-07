import csv

def generate_csv_file(data):
    f = open('sheet.csv', 'w')
    with open('sheet.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

def update_tasks():
## TODO: Сделать нормальную тащилку задач
    res = {'17', '41', '47', '50', '62', '65', '69', '72', '73', '85', '86', '87', '109', '112', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132'}
    return res
