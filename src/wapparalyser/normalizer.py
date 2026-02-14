#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Normalizer:
    """
    Compatibility shim.

    Converts Fingerprint into payload dict expected by ResponseWrapper.
    """

    def normalize(self, fp):
        return {
            "headers": fp.headers,
            "cookies": fp.cookies,
            "meta": [f'<meta name="{k}" content="{v}">' for k, v in fp.meta],
            "scripts": [f'<script src="{s}"></script>' for s in fp.scripts],
            "js": [
                "<script>\n" + "\n".join(self._expand_js(k)) + "\n</script>"
                for k in fp.js
            ],
            "html": fp.html,
        }

    def _expand_js(self, key: str):
        """
        Expands JS dotted paths into nested globals.
        """

        parts = key.split(".")
        base = "window"
        out = []

        for part in parts:
            if not part.isidentifier():
                break

            base = f"{base}.{part}"
            out.append(f"{base} = {base} || {{}};")

        return out
