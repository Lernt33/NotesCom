from flask import Flask,render_template,url_for,request,redirect,flash,session,make_response
import datetime,sqlite3
# import additional_scripts.database
import database,crypting

app = Flask(__name__)
app.config["SECRET_KEY"] = '9d9c6cb95afbc68b20c4fc3257f7bbe4dc7963fb'
app.permanent_session_lifetime = datetime.timedelta(days=90)

db =database.DataBase("db.db")

dict = {'/':'index','/mynotes':'mynotes','/reg':'register','/log':'log','/logout':'logout','/admin':'admin'
        ,'/mynotes/':'mynotes','/reg/':'register','/log/':'log','/logout/':'logout','/admin/':'admin'
        }
####################################################################
# LANGUAGES
################################################################################


@app.before_request
def before_request():
    if not session.permanent: session['permanent'] = True
    print('before request')
    if not 'visit' in session or session['visit'] == False:
        if request.path.split('/')[1] !='static':
            requested_path = request.path
            print(requested_path)
            session['visit'] = True
        return redirect(url_for('language_and_redirect')+f'?url={requested_path}')
@app.route('/set_language_and_redirect/')
def language_and_redirect():
    print('Languaging')
    print('url - '+request.args['url'])
    print('languaging')
    response = make_response(redirect(url_for(dict[request.args['url']])))
    accept_language = request.headers.get('Accept-Language')
    preferred_language = accept_language.split(',')[0].strip() if accept_language else 'en'
    response.set_cookie('language', preferred_language)
    return response

####################################################################################################
@app.route('/')
def index():
    # if session['logged_in']:
    return render_template('index.html')
@app.route('/mynotes')
def mynotes():
    if not 'logged' in session:
        flash('You are not logged in','bad')
        return redirect(url_for('log'))
    return render_template('mynotes.html')

@app.route('/reg',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if request.form['pasw'] == request.form['pasw2']:
            if db.register_user(request.form['email'], request.form['pasw']):
                session['logged'] = request.form['email']
                return redirect(url_for('index'))
            else:
                flash("Такой email уже зарегестрирован",'bad')
        else:
            flash('пароли не совпадают','bad')
    return render_template('reg.html')

@app.route('/log',methods=['GET','POST'])
def log():
    if request.method == 'POST':
        if db.login_user(request.form['email'], request.form['pasw']):
            session['logged'] = request.form['email']
            return redirect(url_for('index'))
        flash("Incorrect user or password!",'bad!')
    return render_template('log.html')

@app.route('/logout')
def logout():
    del session['logged']
    session['visit'] = False
    return redirect(url_for('index'))
@app.route('/admin')
def admin():
    return render_template('AdminPanel.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
