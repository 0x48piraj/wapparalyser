#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flask import request, current_app, make_response

from web.wrapper import ResponseWrapper
from wapparalyser.engine import WapparalyserEngine
from wapparalyser.normalizer import Normalizer

DEFAULT_UPSTREAM = "https://example.com"

def proxy_handler():
    engine = current_app.config["ENGINE"]

    target = request.args.get("target")
    services = request.args.get("services")
    expand = request.args.get("expand_implies") == "1"
    seed = request.args.get("seed")

    if not target or not services:
        return "target and services required", 400

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
