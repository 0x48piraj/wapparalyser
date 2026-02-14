#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flask import make_response

from web.wrapper import ResponseWrapper

class ProxyService:
    def __init__(self, emulation_service):
        self.emu = emulation_service

    def proxied_response(self, target, services, expand, seed):
        try:
            # fetch upstream site
            upstream = requests.get(target, timeout=10)
        except requests.RequestException:
            return "Upstream request failed", 502

        payload = self.emu.emulate(services, expand, seed)
        wrapper = ResponseWrapper(payload)

        content_type = upstream.headers.get("content-type", "")

        if "text/html" in content_type:
            # apply HTML injections
            body = wrapper.apply_html(upstream.text)
        else:
            body = upstream.content

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
