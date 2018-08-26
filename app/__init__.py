import random,datetime
from flask import Flask
from pymongo import MongoClient
import os
from flask import (
    render_template, request, session, redirect
)
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash

def create_app(database_uri=None, debug=True):
    app = Flask(__name__, instance_relative_config=True)
    app.debug = debug

    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": 'localizedtypingolympics@gmail.com',
        "MAIL_PASSWORD": 'd1i2v3e4s5h6'
    }

    app.config.from_mapping(
        SECRET_KEY='flaskycordovadev',
    )
    app.config.update(mail_settings)
    mail = Mail(app)
    # connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1
    client = MongoClient("mongodb://divesh:divesh123@ds123012.mlab.com:23012/typetest",connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1)
    db = client.typetest
    speed_results = db.scores
    # var r = Math.floor(Math.random() * n);
    # var randomElement = db.myCollection.find(query).limit(1).skip(r);
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def sendLoginMail(mailid):
        with app.app_context():
            pwdlink = "cdtype.herokuapp.com/?user=%s&hash=%s"%(mailid,generate_password_hash(mailid[::-1]))
            msg = Message(subject="CDTYPE login details",
                          sender=app.config.get("MAIL_USERNAME"),
                          recipients=[mailid], # replace with your email for testing
                          body="Please click the following link to login "+pwdlink
                          )
            mail.send(msg)


    @app.route('/createuser')
    def create_user():
        return render_template('create_user.html')

    @app.route('/postscore',methods=['POST'])
    def post_score():
        mailid = session.get('user_mail')
        if (mailid):
            check_and_update_speed(mailid,request.form.get('speed',0.0))
        return 'false'

    def get_user(email):
        user = list(db.scores.find({'email':email}))
        if len(user)!=1:
            error = 'no user found'
            return False
        print ('found ', user)
        return user[0]

    def check_and_update_speed(email,speed):
        try:
            speed = float(speed)
        except:
            speed = 0.0
        user = list(db.scores.find({'email':email}))[0]
        try:
            old_speed = float(user['speed'])
        except:
            old_speed = 0.0

        print ('found speed', old_speed)
        if speed > old_speed:
            db.scores.update({'email':email},{'$set':{'speed':speed,'achieved_on': datetime.datetime.now()}})


    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect("/", code=302)

    @app.route('/login',methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':
            mail= request.form.get('email')
            print ( mail, 'm')
            if mail:
                l = list(db.scores.find({'email':mail}))
                if len(l) > 0:
                    print(mail,'mf')
                    sendLoginMail(mail)
                    return render_template("login.html",success = True)
                else:
                    return render_template("login.html", error = True,success = False)

        return render_template("login.html")

    @app.route('/signup', methods=('GET', 'POST'))
    def signup():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            dept = request.form.get('team')
            print(email, "mila")
            user = get_user(email)
            if user:
                return render_template("sign_up.html",text= True, duplicate=True)
            if name and email and dept:
                sendLoginMail(email)
                db.scores.insert({'email': email, 'name':name, 'dept':dept})
                return render_template("sign_up.html",text= True, success=True)
            else:
                return render_template("sign_up.html",error= True)

        return render_template("sign_up.html")

    @app.route('/', methods=('GET', 'POST'))
    def hello():
        #Admin user creation
        if request.method == 'POST':
            if(request.form.get('pwd')=='cordova'):
                username = request.form['name']
                email = request.form['email']
                dept = request.form['team']
                speed = float(request.form.get('speed',0))
                user = get_user(email)
                if user:
                    check_and_update_speed(email,float(speed))
                else:
                    print ('speedtype',type(speed))
                    db.scores.insert({'email': email, 'name':username, 'speed':speed, 'achieved_on': datetime.datetime.now(), 'dept':dept})
                    print('created user with', request.form)
                    user = get_user(email)
                session.clear()
                session['user_mail'] = user['email']

        if request.method == 'GET':
            email = request.args.get('user')
            if(email):
                hash_result = check_password_hash(request.args.get('hash'),email[::-1])
                print (hash_result,'hashres')
                if hash_result:
                    user = get_user(email)
                    if user:
                        session['user_mail'] = user['email']
                        return redirect('/')
                    else:
                        session.clear()
                else:
                    session.clear()

        texts = db.texts.find();
        textlist = list(texts)
        scores = [ x for x in list(speed_results.find()) if x.get('speed')]
        chosen_text = random.choice(textlist)['text']
        return render_template("index.html",
            scores= sorted(scores, key=lambda x : x.get('speed'),reverse=True),
            mailid = session.get('user_mail'),
            text = chosen_text)

    return app
