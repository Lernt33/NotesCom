from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template()

if __name__ == '__main__':
    app.run('127.0.0.1',port=80,debug=False)
