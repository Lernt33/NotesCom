from flask import Flask,render_template,url_for,request,redirect,flash,session
app = Flask(__name__)

@app.route('/')
def index():
    # if session['logged_in']:
    return render_template('index.html')
@app.route('/mynotes')
def mynotes():
    return render_template('mynotes.html')

@app.route('/reg')
def register():
    return render_template('reg.html')

@app.route('/log')
def log():
    return render_template('log.html')
@app.route('/logout')
def logout():
    return redirect(url_for('index'))
@app.route('/admin')
def admin():
    return render_template('AdminPanel.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
