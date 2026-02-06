#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import exrex
import json

import re

_REGEX_CHARS = re.compile(r"[\\^$.*+?()[\]{}|]")

class WapparalyserEngine(object):
    def __init__(self, services):
        """
        services: list of dicts
        {
            "name": "...",
            "raw": { Wappalyzer signature }
        }
        """
        self.services = services

    def list_services(self):
        return [s["name"] for s in self.services]

    def emulate_random(self):
        return self._fuzz_service(random.choice(self.services))

    def emulate_service(self, name, mode):
        for service in self.services:
            if service["name"].lower() == name.lower():
                return self._fuzz_service(service, mode)
        raise ValueError("Unknown service: {}".format(name))

    def fuzz(self, mode=None):
        return [self._fuzz_service(s, mode) for s in self.services]

    def _fuzz_service(self, service, mode=None):
        """
        Generate a synthetic fingerprint payload for a single service.
        """
        raw = service["raw"]

        payload = {
            "service": service["name"],
            "headers": {},
            "meta": {},
            "html": [],
            "js": {},
            "scripts": [],
            "cookies": {},
            "implies": raw.get("implies")
        }

        if mode in (None, "headers"):
            payload["headers"] = self._fuzz_headers(raw.get("headers"))

        if mode in (None, "meta"):
            payload["meta"] = self._fuzz_meta(raw.get("meta"))

        if mode in (None, "html"):
            payload["html"] = self._fuzz_html(raw.get("html"))

        if mode in (None, "js"):
            payload["js"] = self._fuzz_js(raw.get("js"))

        if mode in (None, "scripts"):
            payload["scripts"] = self._fuzz_scripts(raw.get("script"))

        if mode in (None, "cookies"):
            payload["cookies"] = self._fuzz_cookies(raw.get("cookies"))

        return payload

    def _materialize(self, pattern):
        """
        Materialize a regex into a concrete string when possible.
        """
        if not pattern or not isinstance(pattern, str):
            return None
        if not _REGEX_CHARS.search(pattern):
            return pattern
        try:
            return exrex.getone(pattern)
        except Exception:
            return None

    def _fuzz_headers(self, headers):
        """
        Generate HTTP headers that satisfy presence-based detections.
        """
        out = {}
        if not isinstance(headers, dict):
            return out

        for k, v in headers.items():
            if isinstance(v, str) and _REGEX_CHARS.search(v):
                out[k] = self._materialize(v) or v
            else:
                out[k] = v or "1"
        return out

    def _fuzz_meta(self, meta):
        """
        Generate meta tag key/value pairs from detection rules.
        """
        if not meta:
            return {}

        if isinstance(meta, str):
            try:
                meta = json.loads(meta)
            except Exception:
                return {}

        out = {}
        for k, v in meta.items():
            if v in ("", None):
                out[k] = "true"
            else:
                out[k] = self._materialize(v) or v

        return out

    def _fuzz_html(self, html):
        """
        Pass through HTML detection patterns for later normalization.
        """
        if not html:
            return []

        return html if isinstance(html, list) else [html]

    def _fuzz_js(self, js):
        """
        JavaScript rules are presence checks only.
        """
        if isinstance(js, dict):
            return js
        return {}

    def _fuzz_scripts(self, scripts):
        """
        Generate fake script URLs.
        """
        out = []
        if not scripts:
            return out

        items = scripts if isinstance(scripts, list) else [scripts]

        for pattern in items:
            if not isinstance(pattern, str):
                continue

            materialized = self._materialize(pattern)
            if materialized:
                # ensure it looks like a URL
                if not materialized.startswith(("http://", "https://", "//")):
                    materialized = "//" + materialized
                out.append(materialized)
            else:
                out.append("/static/{}.js".format(abs(hash(pattern)) & 0xffffffff))

        return out

    def _fuzz_cookies(self, cookies):
        """
        Cookies are name presence only.
        NO JS. NO HTML.
        """
        out = {}
        if not isinstance(cookies, dict):
            return out

        for name, value in cookies.items():
            if value in ("", None, True):
                out[name] = "1"
            else:
                out[name] = self._materialize(value) or "1"
        return out
