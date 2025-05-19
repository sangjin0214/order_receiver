from flask import Flask, request, render_template
#from src import page_menu, page_payment
import os
import json
from google.oauth2.service_account import Credentials
import gspread
'''
application = Flask(__name__)

key_json_string = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
credentials_info = json.loads(key_json_string)
credentials = Credentials.from_service_account_info(credentials_info)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('1871ZjkgBWblqwsxkTxWSDqGy73M18Z27Qx9LPM_AIF0')
ws_menu = spreadsheet.worksheet('menu_available')
ws_order = spreadsheet.worksheet('order_contents')
'''
print("Debug: Imports complete")

application = Flask(__name__)

print("Debug: Flask app instance created")

# gspread 초기화 코드 블록을 다시 살리고 디버그 메시지 추가
try:
    print("Debug: Starting gspread initialization")
    key_json_string = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    print(f"Debug: Got key string. Is None? {key_json_string is None}") # Config Vars가 설정되었다면 None이 아니어야 함

    if key_json_string: # 환경 변수가 있어야만 다음 단계 진행
        print("Debug: key_json_string is not None, proceeding.")
        credentials_info = json.loads(key_json_string)
        print("Debug: JSON loaded")
        credentials = Credentials.from_service_account_info(credentials_info)
        print("Debug: Credentials created")
        client = gspread.authorize(credentials)
        print("Debug: gspread client authorized")
        # 스프레드시트 열기 및 워크시트 가져오기 부분도 try...except로 감싸볼까?
        try:
            print("Debug: Attempting to open spreadsheet...")
            # 키 값 다시 한번 정확히 확인!
            spreadsheet = client.open_by_key('1871ZjkgBWblqwsxkTxWSDqGy73M1M18Z27Qx9LPM_AIF0') # <--- 이 줄에서 오류가 났을 가능성!
            print("Debug: Spreadsheet opened successfully!")
            ws_menu = spreadsheet.worksheet('menu_available')
            print("Debug: Menu worksheet obtained")
            ws_order = spreadsheet.worksheet('order_contents')
            print("Debug: Order worksheet obtained")
            print("Debug: Gspread initialization complete!")

        except gspread.exceptions.SpreadsheetNotFound:
             print("ERROR: Spreadsheet not found. Check Key and Sharing settings.")
             client, spreadsheet, ws_menu, ws_order = None, None, None, None # 실패 시 변수 초기화
             # 여기서 앱 시작을 막을지 결정
             # raise # 오류를 다시 발생시켜서 앱 시작을 중단시킬 수도 있어

        except Exception as e: # 스프레드시트 열기 또는 워크시트 가져오기 중 다른 오류
             print(f"ERROR: An error occurred opening spreadsheet or getting worksheet: {e}")
             import traceback
             traceback.print_exc()
             client, spreadsheet, ws_menu, ws_order = None, None, None, None # 실패 시 변수 초기화
             # raise # 오류 발생 시 앱 시작 중단

    else: # key_json_string이 None일 경우
         print("ERROR: GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable not set. Cannot initialize gspread.")
         client, spreadsheet, ws_menu, ws_order = None, None, None, None # 변수들 초기화


except json.JSONDecodeError:
    print("ERROR: GOOGLE_APPLICATION_CREDENTIALS_JSON is not valid JSON.")
    client, spreadsheet, ws_menu, ws_order = None, None, None, None # 변수들 초기화
    # raise # 오류 발생 시 앱 시작 중단

except Exception as e: # JSON 로드나 인증 과정 중 예상 못한 다른 오류
    print(f"ERROR: An unexpected error occurred during gspread initial authentication: {e}")
    import traceback
    traceback.print_exc()
    client, spreadsheet, ws_menu, ws_order = None, None, None, None # 변수들 초기화
    # raise # 오류 발생 시 앱 시작 중단

@application.route("/")
def page_route():
  return 'hello'

'''
@application.route("/payment", method=['POST'])
def page_payment():
  order_state = [request.form[menu] for menu in ws_menu.get('A1:G1')+ws_menu.get('A4:H4')]
  table_num = request.form['table_num']
  return page_payment.page_payment(order_state, table_num)


@application.route("/payment/order_complete", method=['POST'])
def page_complete():
  order_state = [request.form[menu] for menu in ws_menu.get('A1:G1')+ws_menu.get('A4:H4')]
  table_num = request.form['table_num']
  orderer_name = request.form['orderer_name']
  total_price = request.form['total_price']
  ws_order.append_row([table_num, orderer_name, total_price, '', ''] + order_state)
  return render_template('./src/page_complete.html', table=table_num)


@application.route("/<table_num>")
def page_menu(table_num):
  return page_menu.page_menu(table_num)
'''
