from eyeflask import create_app
from werkzeug.serving import WSGIRequestHandler
import argparse


def run():
    """Run EyeFlask with the built-in Flask server.

    Running with the Flask server will be problematic in high traffic
    circumstances; consider investigating gunicorn or a gunicorn / nginx combo
    if you encounter difficulties or are running outside of a simple private
    home network environment.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config",
                        help="Path to the eyeflask config file")
    parser.add_argument("-b", "--bind", default="0.0.0.0",
                        help="Interface to bind")
    parser.add_argument("-p", "--port", type=int, default=59278,
                        help="Port to bind, should probably remain 59278")
    parser.add_argument("-d", "--debug", action="store_true",
                        help=("Turn on debugging. Do *not* run this on a "
                              "publically accessible server, as the Flask "
                              "debugger can run arbitrary code."))
    parser.add_argument("--notthreaded", action="store_false", dest="threaded",
                        help="Turn off Flask server's `threaded` option")
    args = parser.parse_args()

    # Flask server doesn't work right without specifying HTTP/1.1
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app = create_app(args.config)

    app.run(host=args.bind, port=args.port, debug=args.debug,
            threaded=args.threaded)


if __name__ == "__main__":
    run()
