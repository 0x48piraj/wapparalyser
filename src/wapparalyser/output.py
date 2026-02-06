#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import List

from wapparalyser.engine import Fingerprint

def write_to_stdout(result: Fingerprint | List[Fingerprint]) -> None:
    if isinstance(result, list):
        for entry in result:
            _print_payload(entry)
            print("-" * 60)
    else:
        _print_payload(result)

def _print_payload(fp: Fingerprint) -> None:
    print("[*] Service:", fp.service)

    for name, section in (
        ("HEADERS", fp.headers),
        ("META", fp.meta),
        ("HTML", fp.html),
        ("JS", fp.js),
        ("SCRIPTS", fp.scripts),
        ("COOKIES", fp.cookies),
        ("IMPLIES", fp.implies),
    ):
        if not section:
            continue

        print(f"\n[+] {name}:")
        if isinstance(section, dict):
            for k, v in section.items():
                print(f"    {k}: {v}")
        else:
            for item in section:
                print(f"    {item}")

def write_to_file(result, path: str) -> None:
    with open(path, "w") as f:
        json.dump(result, f, default=lambda o: o.__dict__, indent=2)
    print("[+] Output written to {}".format(path))
