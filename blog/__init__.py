import os
from flask import Flask

def create_app(test_config=None):
    app  = Flask(__name__, instance_relative_config=True) # new flask app instance

    # database set up
    app.config.from_mapping(
        SECRETE_KEY='Dev',
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite')
    )

    if test_config is None: # prod
        app.config.from_pyfile('config.py', silent=True)
    else:
        # for testing
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def indexPage():
        return "Blog posts!"
    
    from . import db
    db.init_app(app)

    return app