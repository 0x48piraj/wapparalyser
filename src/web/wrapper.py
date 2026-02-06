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

    def apply_html(self, body):
        injections = []

        injections.extend(self.payload.get("meta", []))
        injections.extend(self.payload.get("scripts", []))
        injections.extend(self.payload.get("js", []))
        injections.extend(self.payload.get("html", []))

        if not injections:
            return body

        block = STEALTH_STYLE + "\n" + "\n".join(injections)

        if "</head>" in body:
            return body.replace("</head>", block + "\n</head>")
        elif "</body>" in body:
            return body.replace("</body>", block + "\n</body>")
        else:
            return body + block
