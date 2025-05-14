from flask import Flask, request, render_template

application = Flask(__name__)


@application.route("/<table_num>")
def page_menu(table_num):
  return render_template('./src/page_menu.html', table_number=table_num)


@application.route("/payment", method=['POST'])
def page_payment():
  menu_price = []
  order_state = [request.form[''],request.form[''],request.form[''],request.form['']]
  sum = 0
  for p, s in menu_price, order_state:
    sum += p*s
  return render_template('./src/page_payment.html', table_number=table_num, price=sum, n=order_state[0], ... )


@application.route("/payment/order_complete", method=['POST'])
def page_complete():
  return render_template('./src/page_complete.html', table_number=table_num, name=orderer_name)
