import gspread

account = gspread.service_account(...)
f = account.open('cloud_storage')

def page_menu(table_num):
  template = '''
  <html>
    <head>
      <p>
