from flask import Flask

app = Flask(__name__)


@app.route('/area')
def hello():
    return 'Server runnning'


if __name__ == '__main__':
    print("SERVER RUNNING")
    app.run(port=8000, debug=True)
