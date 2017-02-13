from flask import g, Flask, request
import sqlite3
import re

DATABASE = 'airmon.sq3'
MAC_RE = re.compile(r'([0-9a-f]{2}:){5}[0-9a-f]{2}$')
app = Flask(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()
    g.indicator = {}

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
    if xs['mac'] in g.indicator:
        loc = '/*IND*/' + loc
    c.execute('insert into log values (?, datetime("now"), ?, ?, ?, ?, ?)',
            (xs['mac'], ip, xs['pm25'], xs['t'], xs['h'], xs['co2']))
    conn.commit()
    c.close()
    return loc, 200

@app.route("/ind/on/<mac>", methods=["GET"])
def indicator_on(mac):
    if not MAC_RE.match(mac):
        return '', 200
    g.indicator[mac] = True

@app.route("/ind/off/<mac>", methods=["GET"])
def indicator_off(mac):
    if not MAC_RE.match(mac):
        return '', 200
    if mac in g.indicator[mac]:
        del g.indicator[mac]

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False     # JSON in UTF-8
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=8080, threaded=False)
