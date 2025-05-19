import os
import json
from google.oauth2.service_account import Credentials
import gspread


key_json_string = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
credentials_info = json.loads(key_json_string)
credentials = Credentials.from_service_account_info(credentials_info)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('1871ZjkgBWblqwsxkTxWSDqGy73M18Z27Qx9LPM_AIF0')
ws_order = spreadsheet('order_contents')
ws_menu = spreadsheet('menu_available')


def page_menu(table_num):
  menu_available = template_menu()
  template = '''
  <html>
    <head>
      <p>'''+table_num+'''번 테이블 주문</p><br><br><br>
    </head>
    <body>
      <form action="/payment" method="post">
        '''+template_menu()+'''<br>
        <input tpye="hidden" name="table_num" value="'''+table_num+'''">
        <input type="submit" value="결제">
      </form>
    </body>
  </html>'''
  return template


def template_menu():
  template = 'Main<br>\n'
  for menu, available in zip(ws_menu.get('A1:G1'), ws_menu.get('A2:G2')):
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
  for menu, available in zip(ws_menu.get('A4:H4'), ws_menu.get('A5:H5')):
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
  
