#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wapparalyser.models import Fingerprint, EvidenceType

class Renderer:

    def render(self, service, evidence):
        headers = {}
        cookies = {}
        meta = []
        scripts = []
        html = []
        js = {}

        for e in evidence:
            if e.type == EvidenceType.HEADER:
                headers.setdefault(e.key, e.value)

            elif e.type == EvidenceType.COOKIE:
                cookies[e.key] = e.value

            elif e.type == EvidenceType.META:
                meta.append((e.key, e.value))

            elif e.type == EvidenceType.SCRIPT:
                scripts.append(e.value)

            elif e.type == EvidenceType.HTML:
                html.append(e.value)

            elif e.type == EvidenceType.COMMENT:
                html.append(f"<!-- {e.value} -->")

            elif e.type == EvidenceType.JS:
                js[e.key] = ""

        return Fingerprint(
            service=service.name,
            headers=headers,
            cookies=cookies,
            meta=list(dict.fromkeys(meta)),
            html=list(dict.fromkeys(html)),
            scripts=list(dict.fromkeys(scripts)),
            js=dict(js),
            implies=service.signature.implies
        )
