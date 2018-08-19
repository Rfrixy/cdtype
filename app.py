from flask import Flask
from flask_pymongo import PyMongo

from flask import (
    render_template
)

def create_app(database_uri=None, debug=True):
    app = Flask(__name__)
    app.debug = debug

    app.config["MONGO_URI"] = "mongodb://divesh:divesh123@ds123012.mlab.com:23012/typetest"
    mongo = PyMongo(app)
    # set up your database
    # app.engine = create_engine(database_uri)

    # add your modules
    # app.register_module(frontend)

    # other setup tasks
    @app.route('/')
    def hello():
        scores = mongo.db.scores.find({})
        return render_template("index.html",
            scores= sorted(list(scores), key=lambda x : x['speed'],reverse=True))

    return app

if __name__ == "__main__":
    app = create_app()
    # app = create_app(config.DATABASE_URI, debug=True)
    app.run()
