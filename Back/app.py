from flask import Flask,render_template,url_for,request,redirect,flash,session,make_response
import datetime,database
from admin.admin import admin
app = Flask(__name__)
app.config["SECRET_KEY"] = '9d9c6cb95afbc68b20c4fc3257f7bbe4dc7963fb'
app.permanent_session_lifetime = datetime.timedelta(days=90)
db =database.DataBase("db.db")
app.register_blueprint(admin, url_prefix='/admin')



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

@app.errorhandler(404)
def error(e):
    return '<style>body{background-color: green;h1{margin: auto;width: fit-content;}}</style><h1>Page not found</h1>',404
####################################################################################################
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if 'logged' in session:
            db.insert_notes(session['logged'],request.form['note'])
            flash('Successfully added','succes')
            return redirect(url_for('index'))
        else:
            flash("You have not logged in","warning")
            return redirect(url_for('index'))
    # if session['logged_in']:
    # print(db.get_notes())
    return render_template('index.html',notes=db.get_notes()[::-1])
@app.route('/mynotes')
def mynotes():
    if not 'logged' in session:
        flash('You are not logged in','bad')
        return redirect(url_for('log'))
    print(db.get_notes_by_email(session['logged']))
    return render_template('mynotes.html',notes=db.get_notes_by_email(session['logged'])[::-1])

@app.route('/profile/<id>')
def profile(id):
    if db.get_id(session['logged']) == str(id):
        return redirect(url_for('mynotes'))
    if db.exist_id(id):
        return f'profile for {id}'
    return '404',404
@app.route('/reg',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if request.form['pasw'] == request.form['pasw2']:
            if db.register_user(request.form['email'], request.form['pasw']):
                session['logged'] = request.form['email']
                return redirect(url_for('index'))
            else:
                flash("This mail is already registered",'bad')
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
