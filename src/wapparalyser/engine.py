#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import exrex
import random
from dataclasses import dataclass
from typing import Dict, List, Optional

from wapparalyser.models import Service

_REGEX_CHARS = re.compile(r"[\\^$.*+?()[\]{}|]")

@dataclass(frozen=True)
class Fingerprint:
    service: str
    headers: Dict[str, str]
    cookies: Dict[str, str]
    meta: Dict[str, str]
    html: List[str]
    scripts: List[str]
    js: Dict[str, str]
    implies: List[str]

class WapparalyserEngine:
    def __init__(self, services: List[Service], seed: Optional[int] = None):
        self.services = services
        self.random = random.Random(seed)

    def list_services(self) -> List[str]:
        return sorted(s.name for s in self.services)

    def emulate_service(self, name: str) -> Fingerprint:
        return self._fuzz(self._find_service(name))

    def emulate_random(self) -> Fingerprint:
        return self._fuzz(self.random.choice(self.services))

    def emulate_all(self) -> List[Fingerprint]:
        return [self._fuzz(s) for s in self.services]

    def emulate_stack(self, services: list[str], expand_implies: bool = False) -> Fingerprint:
        if expand_implies:
            services = self.expand_implies(services)

        fps = [self.emulate_service(name) for name in services]

        return Fingerprint(
            service=" + ".join(services),
            headers=self._merge_dicts(fp.headers for fp in fps),
            cookies=self._merge_dicts(fp.cookies for fp in fps),
            meta=self._merge_dicts(fp.meta for fp in fps),
            html=self._merge_lists(fp.html for fp in fps),
            scripts=self._merge_lists(fp.scripts for fp in fps),
            js=self._merge_dicts(fp.js for fp in fps),
            implies=self._merge_lists(fp.implies for fp in fps),
        )

    def expand_implies(self, services: List[str]) -> List[str]:
        expanded = set(services)
        queue = list(services)

        while queue:
            name = queue.pop()
            svc = self._find_service(name)
            for implied in svc.signature.implies:
                base = implied.split(";")[0]
                if base not in expanded:
                    expanded.add(base)
                    queue.append(base)

        return list(expanded)

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

    def _fuzz(self, service: Service) -> Fingerprint:
        sig = service.signature

        return Fingerprint(
            service=service.name,
            headers={k: self._materialize(v) or "1" for k, v in sig.headers.items()},
            cookies={k: self._materialize(v) or "1" for k, v in sig.cookies.items()},
            meta={k: self._materialize(v) or "true" for k, v in sig.meta.items()},
            html=sig.html,
            scripts=[
                self._materialize(s) or f"/static/{abs(hash(s)) & 0xffffffff}.js"
                for s in sig.scripts
            ],
            js=sig.js,
            implies=sig.implies,
        )

    @staticmethod
    def _materialize(pattern: str) -> Optional[str]:
        if not _REGEX_CHARS.search(pattern):
            return pattern
        try:
            return exrex.getone(pattern)
        except Exception:
            return None
