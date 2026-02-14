#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from typing import List, Optional

from wapparalyser.models import Fingerprint, Service
from wapparalyser.compiler import RuleCompiler
from wapparalyser.renderer import Renderer

class WapparalyserEngine:
    def __init__(self, services: List[Service], seed: Optional[int] = None):
        self.services = services
        self.random = random.Random(seed)

        self.compiler = RuleCompiler(self.random)
        self.renderer = Renderer()

    def list_services(self) -> List[str]:
        return sorted(s.name for s in self.services)

    def emulate_service(self, name: str) -> Fingerprint:
        return self._build(self._find_service(name))

    def emulate_random(self) -> Fingerprint:
        return self._build(self.random.choice(self.services))

    def emulate_all(self) -> List[Fingerprint]:
        return [self._build(s) for s in self.services]

    def emulate_stack(self, services: list[str], expand_implies: bool = False) -> Fingerprint:
        if expand_implies:
            services = self.expand_implies(services)

        fps = [self.emulate_service(name) for name in services]

        return Fingerprint(
            service=" + ".join(services),
            headers=self._merge_dicts(fp.headers for fp in fps),
            cookies=self._merge_dicts(fp.cookies for fp in fps),
            meta=self._merge_lists(fp.meta for fp in fps),
            html=self._merge_lists(fp.html for fp in fps),
            scripts=self._merge_lists(fp.scripts for fp in fps),
            js=self._merge_dicts(fp.js for fp in fps),
            implies=self._merge_lists(fp.implies for fp in fps),
        )

    def expand_implies(self, services: List[str]) -> List[str]:
        expanded = list(dict.fromkeys(services))
        seen = set(expanded)
        queue = list(expanded)

        while queue:
            name = queue.pop(0)
            svc = self._find_service(name)

            for implied in svc.signature.implies:
                if implied not in seen:
                    seen.add(implied)
                    expanded.append(implied)
                    queue.append(implied)

        return expanded

    def _merge_dicts(self, items):
        out = {}
        for d in items:
            out.update(d)
        return out

    def _merge_lists(self, items):
        out = []
        for lst in items:
            out.extend(lst)
        return out

    def _find_service(self, name: str) -> Service:
        for service in self.services:
            if service.name.lower() == name.lower():
                return service
        raise ValueError(f"Unknown service: {name}")

    def _build(self, service: Service) -> Fingerprint:
        evidence = self.compiler.compile(service)
        return self.renderer.render(service, evidence)
