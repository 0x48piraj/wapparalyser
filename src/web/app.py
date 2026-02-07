#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wapparalyser.loader import load_services
from wapparalyser.engine import WapparalyserEngine
from web.routes import register_routes
from web.headless import register_proxy_only

HEADLESS = os.getenv("WAPPARALYSER_HEADLESS") == "1"

def create_app():
    app = Flask(__name__)

    # load engine
    apps_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "signatures",
        "apps.json"
    )

    services = load_services(apps_path)
    engine = WapparalyserEngine(services)

    # attach engine to app
    app.config["ENGINE"] = engine

    if HEADLESS:
        register_proxy_only(app)
    else:
        register_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8005, debug=True)
