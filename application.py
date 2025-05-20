from flask import Flask, request, render_template
from src import page_menu, page_payment
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread


application = Flask(__name__)


SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

key_json_string = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
credentials_info = json.loads(key_json_string)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, SCOPES)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('1871ZjkgBWblqwsxkTxWSDqGy73M18Z27Qx9LPM_AIF0')
ws_menu = spreadsheet.worksheet('menu_available')
ws_order = spreadsheet.worksheet('order_contents')


@application.route("/")
def page_route():
  return str(ws_menu.get('A1:G1'))


@application.route("/payment", methods=['POST'])
def page_order_payment():
  order_state = [request.form[menu] for menu in ws_menu.get('A1:G1')[0]+ws_menu.get('A4:H4')[0]]
  table_num = request.form['table_num']
  return page_payment.page_payment(order_state, table_num)


@application.route("/payment/order_complete", methods=['POST'])
def page_order_complete():
  order_state = [request.form[menu] for menu in ws_menu.get('A1:G1')[0]+ws_menu.get('A4:H4')[0]]
  table_num = request.form['table_num']
  orderer_name = request.form['orderer_name']
  total_price = request.form['total_price']
  ws_order.append_row([table_num, orderer_name, total_price, ''] + order_state)
  return render_template('page_complete.html', table=table_num)


@application.route("/<table_num>")
def page_menu_select(table_num):
  return page_menu.page_menu(table_num)

