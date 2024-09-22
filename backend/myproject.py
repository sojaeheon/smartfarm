from flask import Flask
app = Flask(__name__)

@app.route("/api/", methods=['GET'])
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)