from flask import g, Flask, request
import sqlite3

DATABASE = 'airmon.sq3'

app = Flask(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route("/airmon", methods=["POST"])
def airmon():
    xs = request.form
    ip = request.remote_addr
    print xs
    if 'mac' not in xs:
        return 'Invalid input', 200
    conn = g.db
    c = conn.cursor()
    c.execute('SELECT location FROM mac WHERE mac=?', (xs['mac'], ))
    loc = c.fetchone()
    if loc is None:
        loc = 'No location'
    else:
        loc = loc[0]
    c.execute('insert into log values (?, datetime("now"), ?, ?, ?, ?)',
            (xs['mac'], xs['pm25'], xs['t'], xs['h'], xs['co2']))
    conn.commit()
    c.close()
    return loc, 200

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False     # JSON in UTF-8
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=8080, threaded=False)
