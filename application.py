from flask import Flask, request, render_template
from src import page_menu, page_payment
import os
import json
from google.oauth2.service_account import Credentials
import gspread

application = Flask(__name__)

key_json_string = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
credentials_info = json.loads(key_json_string)
credentials = Credentials.from_service_account_info(credentials_info)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('1871ZjkgBWblqwsxkTxWSDqGy73M18Z27Qx9LPM_AIF0')
ws_menu = spreadsheet.worksheet('menu_available')
ws_order = spreadsheet.worksheet('order_contents')

@application.route("/")
def page_route():
  return 'hello'


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
