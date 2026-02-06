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

        services = data.get("services")
        expand = data.get("expand_implies", False)
        seed = data.get("seed")

        if not services:
            return jsonify({"error": "services required"}), 400

        if seed:
            engine = WapparalyserEngine(engine.services, seed=int(seed))

        if isinstance(services, list):
            fp = engine.emulate_stack(services, expand_implies=expand)
        else:
            fp = engine.emulate_service(services)

        result = Normalizer().normalize(fp)

        return jsonify(result)

    @app.route("/proxy", methods=["GET"])
    def proxy():
        engine = current_app.config["ENGINE"]

        target = request.args.get("target")
        services = request.args.get("services")
        expand = request.args.get("expand_implies") == "1"
        seed = request.args.get("seed")

        if not target or not services:
            return "target and service required", 400

        if seed:
            engine = WapparalyserEngine(engine.services, seed=int(seed))

        service_list = services.split(",")

        # fetch upstream site
        upstream = requests.get(target, timeout=10)

        # choose service to emulate
        fp = engine.emulate_stack(service_list, expand_implies=expand)

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
