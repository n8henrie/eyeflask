from flask import Flask
import os
import os.path

__version__ = "0.1.3"


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    config_name = "eyeflask.cfg"

    # Use user specified config file if provided.
    if config:
        config_path = os.path.abspath(config)

    # Load from `instance` folder
    # http://flask.pocoo.org/docs/0.10/config/#instance-folders
    else:
        config_path = config_name

    try:
        app.config.from_pyfile(config_path)
    except FileNotFoundError:
        sample_conf = os.path.join(os.path.dirname(__file__), "extras",
                                   "eyeflask-sample.cfg")
        no_conf_msg = ("Unable to load your config file.\n"
                       "Either specify one with the `-c` flag, or put one "
                       "named `{}` in the Flask\n"
                       "instance folder at the path  below. You may have to "
                       "create the instance\n"
                       "folder if it doesn't already "
                       "exist.\n".format(config_name))
        print(no_conf_msg)
        print("Sample config: {}".format(sample_conf))
        print("Instance folder: {}\n".format(app.instance_path))
        raise

    app.debug_log_format = '\n'.join([
        80 * '-',
        '%(asctime)s %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:',
        '%(message)s',
        80 * '-'
        ])

    from .server import server
    app.register_blueprint(server)

    return app
