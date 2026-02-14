#!/usr/bin/env python
# -*- coding: utf-8 -*-

STEALTH_STYLE = """
<style id="wapparalyser">
[data-wapparalyser="true"] {
  position: absolute !important;
  left: -99999px !important;
  top: -99999px !important;
  width: 0 !important;
  height: 0 !important;
  overflow: hidden !important;
  visibility: hidden !important;
  pointer-events: none !important;
}
</style>
"""

class ResponseWrapper(object):
    def __init__(self, payload):
        self.payload = payload

    def apply_headers(self, response):
        for name, value in self.payload.get("headers", {}).items():
            response.headers[name] = value
        return response

    def apply_html(self, body: str) -> str:
        head_injections = []
        body_injections = []

        head_injections.extend(self.payload.get("meta", []))
        head_injections.extend(self.payload.get("scripts", [])) # external JS

        body_injections.extend(self.payload.get("js", [])) # inline JS globals
        body_injections.extend(self.payload.get("html", [])) # DOM markers

        if not head_injections and not body_injections:
            return body

        head_block = STEALTH_STYLE + "\n" + "\n".join(head_injections)
        body_block = "\n".join(body_injections)

        lower = body.lower()

        # inject into head
        if "</head>" in lower:
            idx = lower.rfind("</head>")
            body = body[:idx] + head_block + body[idx:]
        else:
            body = head_block + body

        # inject into body
        lower = body.lower()
        if "</body>" in lower:
            idx = lower.rfind("</body>")
            body = body[:idx] + body_block + body[idx:]
        else:
            body += body_block

        return body
