import os
import tornado.ioloop
import tornado.web
import fiftyone as fo
import fiftyone.zoo as foz
from fiftyone import ViewField as F

import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("FiftyOne App is running")

class FiftyOneHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def make_app():
    # Define the URL prefix
    url_prefix = os.getenv("URL_PREFIX", "/")

    return tornado.web.Application([
        (url_prefix, MainHandler),
        (url_prefix + "fiftyone", FiftyOneHandler),
    ])

if __name__ == "__main__":
    # Load dataset
    dataset = foz.load_zoo_dataset("quickstart")

    # Launch the FiftyOne app
    session = fo.launch_app(dataset, address='0.0.0.0', port=5151, remote=True)

    # Show the session
    session.show()

    # Update the session view
    session.view = (
        dataset
        .sort_by("uniqueness", reverse=True)
        .limit(25)
        .filter_labels("predictions", F("confidence") > 0.5)
    )

    # Start the Tornado server
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
