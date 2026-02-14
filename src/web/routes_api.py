#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, current_app

def register_api_routes(app):

    @app.get("/api/services")
    def list_services():
        return jsonify(current_app.config["EMU"].list_services())

    @app.post("/api/emulate")
    def emulate():
        data = request.get_json(silent=True)
        if not data:
            return {"error": "invalid json"}, 400

        services = data.get("services")
        if not services:
            return {"error": "services required"}, 400

        seed = data.get("seed")
        seed = int(seed) if isinstance(seed, str) and seed.isdigit() else None

        try:
            result = current_app.config["EMU"].emulate(
                services,
                expand=data.get("expand_implies", False),
                seed=seed
            )
            return jsonify(result)
        except ValueError as e:
            return {"error": str(e)}, 400

    @app.post("/api/export/nginx")
    def export_nginx():
        data = request.get_json(silent=True)
        if not data or not data.get("services"):
            return {"error": "services required"}, 400

        return {"nginx": current_app.config["EMU"].export_nginx(data["services"])}

    @app.post("/api/export/caddy")
    def export_caddy():
        data = request.get_json(silent=True)
        if not data or not data.get("services"):
            return {"error": "services required"}, 400

        return {"caddy": current_app.config["EMU"].export_caddy(data["services"])}
