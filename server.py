from flask import Flask, request

app = Flask(__name__)

@app.route("/airmon", methods=["POST"])
def airmon():
    xs = request.form
    print xs
    return 'Hello World', 200

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False     # JSON in UTF-8
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=8080, threaded=False)
