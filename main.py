from flask import Flask, redirect, request, make_response
from data import db_session
from data.users import User
from data.words import Words
from data.variants import Variants
from flask import render_template
from forms.user import RegisterForm, TrainForm, LoginForm, AddForm
import os
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'training4secretkey'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def intro():
    return render_template('intro_page.html', source='../static/refs/ege_rus.jpg')


@app.route('/register', methods=['GET', 'POST'])
def reg():
    rform = RegisterForm()
    if rform.validate_on_submit():
        if rform.password.data != rform.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=rform,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == rform.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=rform,
                                   message="Такой пользователь уже есть")
        user = User(
            name=rform.name.data,
            power=rform.powers.data
        )
        user.set_password(rform.password.data)
        db_sess.add(user)
        db_sess.commit()
        res = make_response()
        res.set_cookie('UserName', rform.name.data)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=rform)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/gym', methods=['GET', 'POST'])
@login_required
def gym():
    if not current_user.is_authenticated or current_user.power:
        return render_template('ban.html')
    if request.method == 'POST':
        target = request.form.get('swords')
    tform = TrainForm()
    if tform.validate_on_submit():
        words = target.split()
        tform.fwords = ''
        db_sess = db_session.create_session()
        answ = [int(j) for j in tform.answers.data]
        right = []
        for i in range(5):
            if db_sess.query(Variants.is_right).filter(Variants.word == words[i]).first()[0]:
                right.append(i + 1)
        if answ == right:
            return render_template('base.html', tform=tform, words=words, message='Ответ правильный')
        return render_template('base.html', tform=tform, words=words, message='Ответ неверный')
    db_sess = db_session.create_session()
    amount = randint(2, 4)
    ma = len(list(db_sess.query(Words).filter(Words.id >= 1)))
    indexes = set()
    parents = set()
    while len(indexes) < amount:
        w = db_sess.query(Variants.id).filter((Variants.parent_id == randint(1, ma)) and
                                              Variants.is_right).first()[0]
        p = db_sess.query(Variants.parent_id).filter(Variants.id == w).first()[0]
        if p not in parents:
            indexes.add(w)
            parents.add(p)
    while len(indexes) < 5:
        w = db_sess.query(Variants.id).filter((Variants.parent_id == randint(1, ma)) and not
        Variants.is_right).first()[0]
        p = db_sess.query(Variants.parent_id).filter(Variants.id == w).first()[0]
        if p not in parents:
            indexes.add(w)
            parents.add(p)
    words = []
    for el in indexes:
        words.append(db_sess.query(Variants.word).filter(Variants.id == el).first()[0])
    tform.fwords = ' '.join(words)
    return render_template('base.html', words=words, tform=tform)


@app.route('/add_word', methods=['GET', 'POST'])
@login_required
def add():
    if not current_user.is_authenticated or not current_user.power:
        return render_template('ban.html')
    aform = AddForm()
    if aform.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Words).filter(Words.word == aform.word.data).first():
            return render_template('add.html', form=aform, message='Такое слово уже существует в базе данных')
        if aform.variant.data:
            if aform.variant.data.lower() != aform.word.data.lower():
                return render_template('add.html', form=aform, message='''Введённый вариант ударения
                 не относится к введённому слову''')
            word = Words(word=aform.word.data)
            db_sess.add(word)
            d = db_sess.query(Words.id).filter(Words.word == aform.word.data).first()[0]
            variant_r = Variants(word=aform.word.data, parent_id=d, is_right=True)
            variant_f = Variants(word=aform.variant.data, parent_id=d, is_right=False)
            db_sess.add(variant_r)
            db_sess.add(variant_f)
            db_sess.commit()
            redirect('/add_word')
        else:
            vowels = ['у', 'ё', 'е', 'ы', 'а', 'о', 'э', 'я', 'и', 'ю']
            word = Words(word=aform.word.data)
            db_sess.add(word)
            d = db_sess.query(Words.id).filter(Words.word == aform.word.data).first()[0]
            for i in range(len(aform.word.data)):
                if aform.word.data[i].lower() in vowels:
                    s = aform.word.data.lower()
                    if i != len(s) - 1:
                        if s[:i] + s[i].upper() + s[i + 1:] == aform.word.data:
                            variant = Variants(word=s[:i] + s[i].upper() + s[i + 1:], parent_id=d, is_right=True)
                        else:
                            variant = Variants(word=s[:i] + s[i].upper() + s[i + 1:], parent_id=d, is_right=False)
                        db_sess.add(variant)
                    else:
                        if s[:i] + s[i].upper() == aform.word.data:
                            variant = Variants(word=s[:i] + s[i].upper(), parent_id=d, is_right=True)
                        else:
                            variant = Variants(word=s[:i] + s[i].upper(), parent_id=d, is_right=False)
                        db_sess.add(variant)
            db_sess.commit()
            redirect('/add_word')
    return render_template('add.html', form=aform)


@app.route('/check')
def check():
    pass


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init(os.getcwd()+"\\db\\words.db")
    app.run(port=8081, host='localhost')


if __name__ == '__main__':
    print(os.getcwd())
    main()
