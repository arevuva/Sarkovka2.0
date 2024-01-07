from flask import Flask, render_template, url_for, request, redirect, flash
import db
from userLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "xxxxxxxx"
login_manager = LoginManager(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('kovka.html',title='SarKovka')


@app.route('/interier', methods=['GET'])
def interier():
    return render_template('interier/interier.html', title='Интерьер')


@app.route('/exterier', methods=['GET'])
def exterier():
    return render_template('exterier/exterier.html', title='Экстерьер')


@app.route('/catalogs/<string:type>', methods=['GET'])
def type(type):
    goods = db.get_goods(type)
    return render_template('catalogs.html', goods = goods)




@app.route('/articles-list', methods=['GET'])
def articles():
    return render_template('articles-list/articleslist.html', title='Статьи')

@app.route('/articles-list/<string:article>', methods=['GET'])
def article(article):
    return render_template(f'articles-list/{article}.html', title=f'"{article}"')


@app.route('/onas', methods=['GET'])
def onas():
    return render_template('/o_nas/kovka_onas.html', title='О Sarkovka')


@app.route('/addappointment', methods=['POST'])
def add_message():
    tel = request.form["tel"]
    msg = request.form["message"]
    items = request.form["curitem"].split(', ')
    items = items=[] if items[0]=='' else items
    db.addappointment(tel,msg,items)
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)


@app.route('/adminrole', methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        user = db.getUserByLogin(request.form['login'])
        if user and check_password_hash(user[2], request.form['password']):
            userlogin=UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('admin'))
        else:
            if request.form['login']=='':
                flash('Введите логин')
            if request.form['password']=='':
                flash('Введите пароль пользователя')
            else:
                flash("Неправильный логин или пароль")
            return redirect(url_for('login'))
    if request.method=="GET":
        return render_template('au.html')


@app.route('/registration', methods=['GET', 'POST'])
@login_required
def reg():
    if request.method=="POST":
        login=request.form['login']
        password=request.form['password']
        user = db.getUserByLogin(request.form['login'])
        if user and password!=request.form['password1'] or request.form['login']=='' or request.form['password']=='':
            if user:
                flash('Администратор уже существует')
            if request.form['login']=='':
                flash('Введите логин')
            if request.form['password']=='':
                flash('Введите пароль пользователя')
            if request.form['password1']=='':
                flash('Введите пароль пользователя')
            else:
                flash("Пароли не совпадают")
            return redirect(url_for('reg')) 
        else:
            db.registration( login, generate_password_hash(password))
            return redirect(url_for('admin'))
            
    if request.method=="GET":
        return render_template('reg.html')


app.jinja_env.globals.update(getImgs=db.getImgs)
app.jinja_env.globals.update(getSkills=db.getSkills)


@app.route('/admininterface', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method=="GET":
        apps=db.getApps("false")
        employees=db.getEmp()
        return render_template('adminint.html', apps = apps, employees=employees)
    appid=request.form['appid']
    empid=request.form['select']
    db.admitapp(appid,empid)
    return redirect(url_for('admin'))

    


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        flash("Сначала авторизуйтесь")
        return redirect(url_for('login'))
    return response

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)