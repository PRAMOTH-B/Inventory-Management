from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'inventory_db'

mysql = MySQL(app)

@app.route("/index",methods=['POST','GET'])
def index():
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM products")
        mysql.connection.commit()
        result=cur.fetchone()
        cur.close()
        return render_template("ic.html",products=result)

@app.route("/add_product", methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        count = request.form['count']
        cost_per_unit = request.form['cost_per_unit']
        selling_price = request.form['selling_price']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products (name, type, count, cost_per_unit, selling_price) VALUES (%s, %s, %s, %s, %s)", (name, type, count, cost_per_unit, selling_price))
        mysql.connection.commit()
        cur.close()

        return redirect("/index")

if __name__ == '__main__':
    app.run(debug=True)
