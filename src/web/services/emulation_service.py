#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wapparalyser.engine import WapparalyserEngine
from wapparalyser.normalizer import Normalizer

class EmulationService:
    def __init__(self, engine: WapparalyserEngine):
        self.engine = engine
        self.normalizer = Normalizer()

    def _headers_for(self, services):
        return self.engine.emulate_stack(services).headers

    def list_services(self):
        return [
            {
                "name": s.name,
                "icon": s.icon,
                "categories": s.categories,
                "implies": s.signature.implies,
            }
            for s in self.engine.services
        ]

    def emulate(self, services, expand=False, seed=None):
        engine = self.engine
        if seed:
            engine = WapparalyserEngine(engine.services, seed=int(seed))

        if isinstance(services, list):
            fp = engine.emulate_stack(services, expand_implies=expand)
        else:
            fp = engine.emulate_service(services)

        return self.normalizer.normalize(fp)

    def export_nginx(self, services):
        headers = self._headers_for(services)
        lines = ["location / {", "  proxy_pass http://upstream;"]
        for k, v in headers.items():
            lines.append(f'  proxy_set_header {k} "{v}";')
        lines.append("}")
        return "\n".join(lines)

    def export_caddy(self, services):
        headers = self._headers_for(services)
        return "\n".join(f'header {k} "{v}"' for k, v in headers.items())
