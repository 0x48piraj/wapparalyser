#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flask import (
    request,
    jsonify,
    current_app,
    render_template,
    make_response
)

from web.wrapper import ResponseWrapper
from wapparalyser.engine import WapparalyserEngine
from wapparalyser.normalizer import Normalizer

DEFAULT_UPSTREAM = "https://example.com"

def register_routes(app):

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/api/services", methods=["GET"])
    def list_services():
        engine = current_app.config["ENGINE"]

        services = []
        for s in engine.services:
            services.append({
                "name": s.name,
                "icon": s.icon,
                "categories": s.categories,
                "implies": s.signature.implies,
            })

        return jsonify(services)

    @app.route("/api/emulate", methods=["POST"])
    def emulate():
        engine = current_app.config["ENGINE"]
        data = request.get_json(force=True) or {}

        service = data.get("service")
        seed = data.get("seed")

        if not service:
            return jsonify({"error": "service required"}), 400

        if seed is not None:
            engine = WapparalyserEngine(engine.services, seed=int(seed))

        fp = engine.emulate_service(service)
        result = Normalizer().normalize(fp)

        return jsonify(result)

    @app.route("/proxy", methods=["GET"])
    def proxy():
        engine = current_app.config["ENGINE"]

        target = request.args.get("target")
        service = request.args.get("service")
        seed = request.args.get("seed")

        if not target or not service:
            return "target and service required", 400

        if seed is not None:
            engine = WapparalyserEngine(engine.services, seed=int(seed))

        # fetch upstream site
        upstream = requests.get(target, timeout=10)

        # choose service to emulate
        fp = engine.emulate_service(service)

        safe_payload = Normalizer().normalize(fp)
        wrapper = ResponseWrapper(safe_payload)

        # apply HTML injections
        body = wrapper.apply_html(upstream.text)

        # build response
        response = make_response(body, upstream.status_code)

        # copy upstream headers
        for k, v in upstream.headers.items():
            if k.lower() not in (
                "content-length",
                "transfer-encoding",
                "connection",
                "content-encoding"
            ):
                response.headers[k] = v

        # apply synthetic headers
        response = wrapper.apply_headers(response)

        return response
