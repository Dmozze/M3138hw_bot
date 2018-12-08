import csv

def generate_csv_file(data):
    f = open('sheet.csv', 'w')
    with open('sheet.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)
