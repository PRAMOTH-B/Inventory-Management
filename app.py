from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'inventory_db'

mysql = MySQL(app)

user=""

#default landing page
def default_route():
    return render_template("index.html")

app.add_url_rule('/', 'default_route', default_route)

#authenticate the user from the data on database(basic authentication)
@app.route("/authenticate", methods=['POST'])
def authenticate():
    global user
    user = request.form['uid']
    pwd = request.form['pwd']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE name=%s AND password=%s", (user, pwd,))
    result = cur.fetchone()
    cur.close()
    if result:
        # User exists, redirect to content page
        return redirect('/index')
    else:
        # User doesn't exist, show error message
        return render_template('index.html', error="Wrong Username or Password!!")
    
@app.route("/register")
def register():
     return render_template("register.html")

#account creation and also creating table for the particular user's data
@app.route("/create_account",methods=['POST','GET'])
def create_account():
     if request.method=="POST":
          name=request.form['uid']
          pwd=request.form['pwd']
          cur = mysql.connection.cursor()
          cur.execute("SELECT * FROM users WHERE name=%s", (name,))
          result = cur.fetchone()
          if result:
               return render_template("/register.html",error="User already Exists with same name!")
          else:
               cur.execute("INSERT INTO users(name,password)VALUES(%s,%s)",(name,pwd,))
               cur.execute(f"CREATE TABLE IF NOT EXISTS {name} (name VARCHAR(200), type VARCHAR(200), count INTEGER, cost_per_unit FLOAT, selling_price FLOAT)")
               mysql.connection.commit()
               return redirect("/")
          cur.close()
          


#add inventory form and current inventory check
@app.route("/index",methods=['POST','GET'])
def index():
        cur=mysql.connection.cursor()
        cur.execute(f"SELECT * FROM {user}")
        mysql.connection.commit()
        result=cur.fetchall()
        cur.close()
        return render_template("ic.html",products=result)

#adding product and redirects to samepage

@app.route("/add_product", methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        count = request.form['count']
        cost_per_unit = request.form['cost_per_unit']
        selling_price = request.form['selling_price']

        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO {user} (name, type, count, cost_per_unit, selling_price) VALUES (%s, %s, %s, %s, %s)", (name, type, count, cost_per_unit, selling_price))
        mysql.connection.commit()
        cur.close()

        return redirect("/index")
    
# search page
@app.route("/search")
def search():
     return render_template("search.html")
#displays the search element in the search module
@app.route("/search_product",methods=['POST'])
def search_product():
     if request.method == 'POST':
          product=request.form['search']
          cur=mysql.connection.cursor()
          cur.execute(f"SELECT * FROM {user} WHERE name=%s",(product,))
          mysql.connection.commit()
          result=cur.fetchall()
          cur.close()
          return render_template("search.html",products=result)
     
@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    cur=mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {user}")
    mysql.connection.commit()
    result=cur.fetchall()
    cur.close()
    data_set={}
    for row in result:
         cp=row[3]
         sp=row[4]
         item=row[0]
         profit=((sp-cp)/cp)*100
         data_set=dict(data_set,item=)

         
    

if __name__ == '__main__':
    app.run(debug=True)
