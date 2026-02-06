#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import urllib.request

WAPPALYZER_URL = "https://raw.githubusercontent.com/AliasIO/Wappalyzer/master/src/apps.json"


def load_services(path):
    with open(path, "r") as f:
        data = json.load(f)

    services = []
    for name, raw in data.get("apps", {}).items():
        services.append({
            "name": name,
            "raw": raw
        })
    return services


def update_signatures(path):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    urllib.request.urlretrieve(WAPPALYZER_URL, path)
    print("[+] Updated Wappalyzer signatures")
