import random,datetime
from flask import Flask
from pymongo import MongoClient
import os
from flask import (
    render_template, request, session, redirect, jsonify
)
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash
from . import dataops

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
    client = MongoClient("mongodb://divesh:divesh123@ds123012.mlab.com:23012/typetest",connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1)
    db = client.typetest
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def sendLoginMail(mailid):
        mailid=mailid.lower()
        with app.app_context():
            pwdlink = "cdtype.herokuapp.com/?user=%s&hash=%s"%(mailid,generate_password_hash(mailid[::-1]))
            msg = Message(subject="CDTYPE login details",
                          sender=app.config.get("MAIL_USERNAME"),
                          recipients=[mailid], # replace with your email for testing
                          body="Please click the following link to login "+pwdlink
                          )
            mail.send(msg)


    def get_user(email):
        email=email.lower()
        user = list(db.scores.find({'email':email}))
        if len(user)<=0:
            error = 'no user found'
            return False
        # print ('found ', user)
        return user[0]

    def check_and_update_speed(email,speed):
        email=email.lower()
        try:
            speed = float(speed)
        except:
            speed = 0.0
        user = list(db.scores.find({'email':email}))[0]
        try:
            old_speed = float(user['speed'])
        except:
            old_speed = 0.0

        new_params = dataops.process_history(user)
        db.scores.update({'email':email}, {'$set': { 'averages':new_params }})
        if speed > old_speed:
            db.scores.update({'email':email},{'$set':{'speed':speed,'achieved_on': datetime.datetime.now()}})



    @app.route('/createuser')
    def create_user():
        return render_template('create_user.html')

    @app.route('/postscore',methods=['POST'])
    def post_score():
        mailid = session.get('user_mail')
        if (mailid):
            try:
            # if 2:
                d = request.get_json()
                hash = dataops.decryptStringWithXORFromHex(d['hash'],'secretkeeeeey')
                speed = int(hash[:len(hash)//10])
                if speed > 160:
                    return 'false'
                from . import parser
                text = db.scores.find_one({'email':mailid},{'text':1})
                db.scores.update({'email':mailid},{'$set':{ 'text': ''}})
                res = parser.process_list(d,text)
                assert(res[0])
                db.scores.update({'email':mailid},{'$push':{ 'history':{ 'speed':speed,'achieved_on': datetime.datetime.now(), 'data':res[2]}}})

                if not res[2]['bot']:
                    check_and_update_speed(mailid,res[1])
                    return jsonify(res[2],res[3])
                else:
                    return 'false'
            except Exception as e:
                print(e)
                import traceback
                traceback.print_exc()
                return 'false'
        return 'false'

    @app.route('/statistics')
    def statistics():
        return render_template('statistics.html')

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
                mail=mail.lower()
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
            #try except here
            name = request.form.get('name')
            email = request.form.get('email')
            dept = request.form.get('team')
            print(email, "mila")
            email=email.lower()
            user = get_user(email)
            if user:
                return render_template("sign_up.html",text= True, duplicate=True)
            if name and email and dept:
                sendLoginMail(email)
                db.scores.insert({'email': email, 'name':name, 'dept':dept, 'created_at':datetime.datetime.now()})
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
                email = request.form['email'].lower()
                dept = request.form['team']
                speed = float(request.form.get('speed',0))
                user = get_user(email)
                if user:
                    check_and_update_speed(email,float(speed))
                else:
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
                        session.permanent = True
                        return redirect('/')
                    else:
                        session.clear()
                else:
                    session.clear()

        texts = db.texts.find();
        textlist = list(texts)
        scores = [ x for x in list(db.scores.find()) if x.get('speed')]
        chosen_text = random.choice(textlist)['text']
        # chosen_text =  'asdfasdfasdfasdfasdf'
        email = session.get('user_mail')
        if email:
            db.scores.update({'email':email},{'$set':{ 'text': chosen_text}})

        return render_template("index.html",
            scores= sorted(scores, key=lambda x : x.get('speed'),reverse=True),
            email = email,
            text = chosen_text)

    return app
