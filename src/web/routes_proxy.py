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
        seed = int(seed) if isinstance(seed, str) and seed.isdigit() else None

        if not target or not services:
            return "target and services required", 400

        services_list = services.split(",")
        return current_app.config["PROXY"].proxied_response(
            target=target,
            services=services_list,
            expand=expand,
            seed=seed
        )
