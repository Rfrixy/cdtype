from flask import Flask
from pymongo import MongoClient
import os
from flask import (
    render_template
)

def create_app(database_uri=None, debug=True):
    app = Flask(__name__, instance_relative_config=True)
    app.debug = debug

    # connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1
    client = MongoClient("mongodb://divesh:divesh123@ds123012.mlab.com:23012/typetest",connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1)
    db = client.typetest
    speed_results = db.scores
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return render_template("index.html",
            scores= sorted(list(speed_results.find()), key=lambda x : x['speed'],reverse=True))

    return app

# app = create_app()
# app = create_app(config.DATABASE_URI, debug=True)
# app.run()
