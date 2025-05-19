import os
import json
from google.oauth2.service_account import Credentials
import gspread


key_json_string = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
credentials_info = json.loads(key_json_string)
credentials = Credentials.from_service_account_info(credentials_info)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('1871ZjkgBWblqwsxkTxWSDqGy73M18Z27Qx9LPM_AIF0')
ws_menu = spreadsheet('menu_available')


def page_payment(order_state, table_num):
  template = '''
  <html>
    <head>
      <p>'''+table_num+'''번 테이블 주문 사항</p><br><a href="/'''+table_num+'''">메뉴 선택 페이지로 돌아가기</a><br><br><br>
    </head>
    <body>
      다음 주문 내역을 확인하고 [우리은행 1002-859-834337 (예금주 엄상진)]로 주문 금액을 입금한 후, 입금자명을 입력하고 완료를 눌러주세요.<br><br>
      <form action="/payment/order_complete" method="post">
        '''+template_bill(order_state)+'''<br>
        입금자명 : <input type="text" name="orderer_name"><br><br>
        <input tpye="hidden" name="table_num" value="'''+table_num+'''">
        <input type="submit" value="완료">
      </form>
    </body>
  </html>'''
  return template


def template_bill(order_state):
  template = '주문 내역'
  sum = 0
  for menu, amount, price in zip(ws_menu.get('A1:G1')+ws_menu.get('A4:H4'), order_state, ws_menu.get('A3:G3')+ws_menu.get('A6:H6')):
    if int(amount):
      template += '<br>\n        '+menu+'('+price+'\) x '+amount
      sum += int(price) * int(amount)
    template += '<input type="hidden" name="'+menu+'" value="'+amount+'">'
  template += '<br>\n        Total : '+str(sum)+'\<br>'
  return template
