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


def page_payment(order_state, table_num):
  template = '''
  <html>
    <head>
      <title>결제 페이지</title>
      <style>
        body {
          font-size: 60px;
        }
        input[type="text"] {
          width: 50%;
          height: 60px;
        }
        input[type="submit"] {
          width: 150px;
          height: 75px;
          font-size: 50px;
        }
      </style>
    </head>
    <body>
      <p><h2 class="main-title">'''+table_num+'''번 테이블 주문 사항</h2></p><br><a href="/'''+table_num+'''">메뉴 선택 페이지로 돌아가기</a><br><br><br>
      다음 주문 내역을 확인하고 [우리은행 1002-859-834337 (예금주 엄상진)]로 주문 금액을 입금한 후, 입금자명을 입력하고 완료를 눌러주세요.<br><br>
      <form action="/payment/order_complete" method="post">
        '''+template_bill(order_state)+'''<br>
        입금자명 : <input type="text" name="orderer_name"><br><br>
        <input type="hidden" name="table_num" value="'''+table_num+'''">
        <input type="submit" value="완료">
      </form>
    </body>
  </html>'''
  return template


def template_bill(order_state):
  template = '주문 내역'
  sum = 0
  for menu, amount, price in zip(ws_menu.get('A1:G1')[0]+ws_menu.get('A4:H4')[0], order_state, ws_menu.get('A3:G3')[0]+ws_menu.get('A6:H6')[0]):
    if int(amount):
      template += '<br>\n        '+menu+'('+price+'원) x '+amount
      sum += int(price) * int(amount)
    template += '<input type="hidden" name="'+menu+'" value="'+amount+'">'
  template += '<br>\n        >> Total : '+str(sum)+'원<input type="hidden" name="total_price" value="'+str(sum)+'"><br>'
  return template
