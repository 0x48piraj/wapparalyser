#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask
from flask_cors import CORS

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wapparalyser.loader import load_services
from wapparalyser.engine import WapparalyserEngine
from web.services.emulation_service import EmulationService
from web.services.proxy_service import ProxyService

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

    emu = EmulationService(engine)
    proxy = ProxyService(emu)

    app.config["EMU"] = emu
    app.config["PROXY"] = proxy

    from web.routes_api import register_api_routes
    from web.routes_proxy import register_proxy_routes

    register_api_routes(app)
    register_proxy_routes(app)

    CORS(app, resources={
        r"/api/*": {"origins": "*"},
        r"/proxy": {"origins": "*"}
    })

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8005, debug=True)
