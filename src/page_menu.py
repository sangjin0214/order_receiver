import gspread


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
  return template




