import random,datetime
from flask import Flask
from pymongo import MongoClient
import os
from flask import (
    render_template, request, session
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
            pwdlink = "cdtype.herokuapp.com/?user=divesh.naidu@collegedunia.com&hash=%s"%generate_password_hash(mailid[::-1])
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
            return
        user = list(db.scores.find({'email':email}))[0]
        old_speed = float(user['speed'])
        print ('found speed', old_speed)
        if speed > old_speed:
            db.scores.update({'email':email},{'$set':{'speed':speed,'achieved_on': datetime.datetime.now()}})

    @app.route('/', methods=('GET', 'POST'))
    def hello():
        if request.method == 'POST':
            if(request.form['pwd']=='cordova'):
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

        texts = db.texts.find();
        textlist = list(texts)
        chosen_text = random.choice(textlist)['text']
        return render_template("index.html",
            scores= sorted(list(speed_results.find()), key=lambda x : x['speed'],reverse=True),
            mailid = session.get('user_mail'),
            text = chosen_text)

    return app
