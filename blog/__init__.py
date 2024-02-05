# init.py file for seeting up the app and gettting it running.

import os
from flask import Flask

def create_app(test_config=None):
    app  = Flask(__name__, instance_relative_config=True) # new flask app instance

    # database set up
    app.config.from_mapping(
        SECRET_KEY='dev',
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
    
    # for database
    from . import db
    db.init_app(app)

    # for endpoints 
    from . import auth
    app.register_blueprint(auth.blueprint)

    from . import blog
    app.register_blueprint(blog.blog_blueprint)

    app.add_url_rule('/', endpoint='index')

    return app