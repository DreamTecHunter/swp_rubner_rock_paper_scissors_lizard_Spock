from flask import *
from flask_mysqldb import MySQL

db_name = "rpsls"
t_name = "rpsls"

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'swp-rubner'
app.config['MYSQL_PASSWORD'] = 'swp-rubner'
app.config['MYSQL_DB'] = 'swp_rubner_rpsls'

mysql = MySQL(app)


@app.route("/")
def hello():
    return "Welcome to the rpsls-flaskAPI!"


@app.route('/get', methods=['GET'])
def get():
    cursor = mysql.connection.cursor()
    cursor.execute("select * from rpsls_flask;")
    result = cursor.fetchall()
    return jsonify(result)


@app.route('/add', methods=['POST'])
def add():
    data = request.json
    data = [data[key] for key in data]
    print(data)
    curses = mysql.connection.cursor()
    curses.execute(
        "insert into rpsls_flask(name, hand, amount) values (%s, %s, %s) on duplicate key update amount = %s;",
        data + [data[-1]])
    mysql.connection.commit()
    return f'$ Stats: {data[1]} uploaded.'


if __name__ == '__main__':
    app.run(port=8888)
