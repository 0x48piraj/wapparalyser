#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import urllib.request
from typing import Dict, List

from wapparalyser.models import Service, Signature

WAPPALYZER_URL = "https://raw.githubusercontent.com/AliasIO/Wappalyzer/master/src/apps.json"

def _as_list(value) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]

def _as_dict(value) -> Dict[str, str]:
    if isinstance(value, dict):
        return {str(k): str(v) for k, v in value.items()}
    return {}

def load_services(path: str) -> List[Service]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    services: List[Service] = []

    for name, raw in data.get("apps", {}).items():
        signature = Signature(
            headers=_as_dict(raw.get("headers")),
            cookies=_as_dict(raw.get("cookies")),
            meta=_as_dict(raw.get("meta")),
            html=_as_list(raw.get("html")),
            scripts=_as_list(raw.get("script")),
            js=_as_dict(raw.get("js")),
            implies=_as_list(raw.get("implies")),
            excludes=_as_list(raw.get("excludes")),
        )

        services.append(
            Service(
                name=name,
                icon=raw.get("icon"),
                website=raw.get("website"),
                categories=raw.get("cats", []),
                signature=signature,
            )
        )

    return services

def update_signatures(path: str) -> None:
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    urllib.request.urlretrieve(WAPPALYZER_URL, path)
    print("[+] Updated Wappalyzer signatures")
