#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def write_to_stdout(result):
    if isinstance(result, list):
        for entry in result:
            _print_payload(entry)
            print("-" * 60)
    else:
        _print_payload(result)


def _print_payload(payload):
    print("[*] Service:", payload.get("service"))

    for section in ("headers", "meta", "html", "js", "scripts", "cookies"):
        items = payload.get(section)
        if not items:
            continue

        print("\n[+] {}:".format(section.upper()))

        if isinstance(items, dict):
            for k, v in items.items():
                print("    {}: {}".format(k, v))
        else:
            for item in items:
                print("    {}".format(item))


def write_to_file(result, path):
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    print("[+] Output written to {}".format(path))
