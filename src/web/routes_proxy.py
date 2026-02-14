#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, current_app

def register_proxy_routes(app):

    @app.get("/proxy")
    def proxy():
        target = request.args.get("target")
        services = request.args.get("services")
        expand = request.args.get("expand_implies") == "1"
        seed = request.args.get("seed")

        if not target or not services:
            return "target and services required", 400

        return current_app.config["PROXY"].proxied_response(
            target=target,
            services=services.split(","),
            expand=expand,
            seed=seed
        )
