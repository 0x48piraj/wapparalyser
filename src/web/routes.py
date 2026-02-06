#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flask import (
    request,
    current_app,
    make_response
)

from web.wrapper import ResponseWrapper
from wapparalyser.normalizer import Normalizer


DEFAULT_UPSTREAM = "https://example.com"


def register_routes(app):

    @app.route("/proxy", methods=["GET"])
    def proxy():
        engine = current_app.config["ENGINE"]

        target = request.args.get("target", DEFAULT_UPSTREAM)
        service = request.args.get("service")

        # fetch upstream site
        upstream = requests.get(target)

        # choose service to emulate
        if service:
            payload = engine.emulate_service(service)
        else:
            payload = engine.emulate_random()

        safe_payload = Normalizer().normalize(payload)
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

        # apply deception headers
        response = wrapper.apply_headers(response)

        return response
