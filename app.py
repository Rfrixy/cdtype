from flask import Flask
from pymongo import MongoClient
from flask import (
    render_template
)

def create_app(database_uri=None, debug=True):
    app = Flask(__name__)
    app.debug = debug
    # connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1
    client = MongoClient("mongodb://divesh:divesh123@ds123012.mlab.com:23012/typetest",connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1)
    db = client.typetest
    speed_results = db.scores

    @app.route('/')
    def hello():
        return render_template("index.html",
            scores= sorted(list(speed_results.find()), key=lambda x : x['speed'],reverse=True))

    return app

if __name__ == "__main__":
    app = create_app()
    # app = create_app(config.DATABASE_URI, debug=True)
    app.run()
