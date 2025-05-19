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


def input_order(table_num, orderer_name, total_price, order_state):
  order_info = [table_num, orderer_name, total_price, '', ''] + order_state
  ws_order.append_row([table_num, orderer_name, total_price, '', ''] + order_state)
