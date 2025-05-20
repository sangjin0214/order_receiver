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
      <p><h2 class="main-title">'''+table_num+'''번 테이블 주문</h2></p><br><br>
      <form action="/payment" method="post">
        '''+template_menu()+'''<br>
        <input type="hidden" name="table_num" value="'''+table_num+'''">
        <input type="submit" value="결제">
      </form>
    </body>
  </html>'''
  return template


def template_menu():
  template = 'Main<br>\n'
  for menu, available in zip(ws_menu.get('A1:G1')[0], ws_menu.get('A2:G2')[0]):
    if int(available):
      template += '        '+menu+' : <select name="'+menu+'''">
          <option value="0" selected>0</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select><br>\n'''
    else:
      template += '        '+menu+' : 품절<input type="hidden" name="'+menu+'" value="0"><br>\n'
  template += '        <br>Drinks<br>\n'
  for menu, available in zip(ws_menu.get('A4:H4')[0], ws_menu.get('A5:H5')[0]):
    if int(available):
      template += '        '+menu+' : <select name="'+menu+'''">
          <option value="0" selected>0</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
          <option value="6">6</option>
          <option value="7">7</option>
          <option value="8">8</option>
          <option value="9">9</option>
          <option value="10">10</option>
        </select><br>\n'''
    else:
      template += '        '+menu+' : 품절<input type="hidden" name="'+menu+'" value="0"><br>\n'
  return template


