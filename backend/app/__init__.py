from flask import Flask

app = Flask(__name__)

app.register_blueprint()

if __name__ == "__main__":
  app.run(host = '0.0.0.0', port = 6000, debug=True)