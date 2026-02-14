#!/usr/bin/env python
# -*- coding: utf-8 -*-

import certifi
import requests
from flask import Response, make_response
from typing import List, Optional

from web.wrapper import ResponseWrapper

class ProxyService:
    def __init__(self, emulation_service):
        self.emu = emulation_service

    def proxied_response(self, target: str, services: List[str], expand: bool, seed: Optional[int]) -> Response:
        try:
            # fetch upstream site
            upstream = requests.get(target, timeout=10, allow_redirects=True, stream=True, verify=certifi.where())
        except requests.RequestException:
            return "Upstream request failed", 502

        payload = self.emu.emulate(services, expand, seed)
        wrapper = ResponseWrapper(payload)

        content_type = upstream.headers.get("content-type", "").lower()
        raw = upstream.content

        if "text/html" in content_type:
            encoding = upstream.encoding or "utf-8"
            text = raw.decode(encoding, errors="replace")
            # apply HTML injections
            modified = wrapper.apply_html(text)
            body = modified.encode(encoding)
        else:
            body = raw

        # build response
        response = make_response(body, upstream.status_code)

        HOP_BY_HOP = {
            "content-length",
            "content-encoding",
            "transfer-encoding",
            "connection",
            "etag",
            "accept-ranges"
        }

        # copy upstream headers
        for k, v in upstream.headers.items():
            if k.lower() not in HOP_BY_HOP:
                response.headers[k] = v

        # apply synthetic headers
        response = wrapper.apply_headers(response)

        return response
