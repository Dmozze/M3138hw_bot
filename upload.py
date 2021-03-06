from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

SAMPLE_SPREADSHEET_ID = '1Pvi6QSRy6xWS-l-6L2I5LszqgWNOIDPaosX7UKKGpaA'
SAMPLE_RANGE_NAME = 'Ответы 38-39!A3:B'

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
    for row in values:
       if len(row) == 1 or row[1][-1] == '?':
           res.append(int(row[0]))
    print('array', res)
    return res
