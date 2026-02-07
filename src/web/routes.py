#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    request,
    jsonify,
    current_app,
    render_template
)

from web.proxy import proxy_handler
from wapparalyser.engine import WapparalyserEngine
from wapparalyser.normalizer import Normalizer

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

    @app.route("/api/export/nginx", methods=["POST"])
    def export_nginx():
        data = request.get_json(force=True)
        services = data.get("services")

        if not services:
            return jsonify({"error": "services required"}), 400

        base_engine = current_app.config["ENGINE"]
        engine = WapparalyserEngine(base_engine.services)

        fp = engine.emulate_stack(services)
        headers = fp.headers

        lines = [
            "location / {",
            "  proxy_pass http://upstream;",
        ]

        for k, v in headers.items():
            lines.append(f'  proxy_set_header {k} "{v}";')

        lines.append("}")

        return jsonify({"nginx": "\n".join(lines)})

    @app.route("/api/export/caddy", methods=["POST"])
    def export_caddy():
        data = request.get_json(force=True)
        services = data.get("services")

        if not services:
            return jsonify({"error": "services required"}), 400

        base_engine = current_app.config["ENGINE"]
        engine = WapparalyserEngine(base_engine.services)

        fp = engine.emulate_stack(services)

        lines = []
        for k, v in fp.headers.items():
            lines.append(f'header {k} "{v}"')

        return jsonify({"caddy": "\n".join(lines)})

    @app.route("/proxy", methods=["GET"])
    def proxy():
        return proxy_handler()
