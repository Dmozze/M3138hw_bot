from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

SAMPLE_SPREADSHEET_ID = '1z5JfDt0nUjpKEcLX3Ws9LaQe_I7NFwPGQkuS_HIOr9M'
SAMPLE_RANGE_NAME = 'Лист1!G1:H1000'

def upload():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    res = []
    print(values)
    for row in values:
       if len(row) == 1 or row[1][-1] == '?':
           res.append(int(row[0]))
    return res
