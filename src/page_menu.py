import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

key_json_string = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
credentials_info = json.loads(key_json_string)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, SCOPES)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('1871ZjkgBWblqwsxkTxWSDqGy73M18Z27Qx9LPM_AIF0')
ws_menu = spreadsheet.worksheet('menu_available')
ws_order = spreadsheet.worksheet('order_contents')

def page_menu(table_num):
  template = '''
  <html>
    <head>
      <title>메뉴 선택 페이지</title>
    </head>
    <body>
      <p><h2 class="main-title">'''+table_num+'''번 테이블 주문</h2></p><br><br><br>
      <form action="/payment" method="post">
        '''+table_num+'''<br>
        <input type="hidden" name="table_num" value="'''+table_num+'''">
        <input type="submit" value="결제">
      </form>
    </body>
  </html>'''
  return str(ws_menu.get('A1:G1'))


