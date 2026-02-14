#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random

from wapparalyser.models import Evidence, EvidenceType

VERSION_RE = re.compile(r'\\;version:\\(\d+)')
CONF_RE = re.compile(r'\\;confidence:(\d+)')

CAPTURE_RE = re.compile(r'\((?:\?:)?[^)]*\\d[^)]*\)')

def strip_modifiers(pattern: str):
    has_version = False

    if VERSION_RE.search(pattern):
        has_version = True
        pattern = VERSION_RE.sub("", pattern)

    if CONF_RE.search(pattern):
        pattern = CONF_RE.sub("", pattern)

    # numeric capture groups
    if CAPTURE_RE.search(pattern):
        has_version = True

    return pattern.strip(), has_version

def fake_version(rng: random.Random, key: str) -> str:
    """
    Derive stable per-technology randomness.

    Gotcha:
        hash() is randomized per process for security.

    :param rng: Base RNG for reproducibility.
    :type rng: random.Random
    :param key: String key to derive a stable pseudo-version.
    :type key: str
    :return: Version-like string "major.minor.patch", e.g., "7.3.15".
    :rtype: str
    """

    local = random.Random(rng.randint(0, 2**32 - 1) ^ hash(key))
    return f"{local.randint(0,9)}.{local.randint(0,20)}.{local.randint(0,30)}"

class RuleCompiler:
    def __init__(self, rng: random.Random):
        self.rng = rng

    def compile(self, service):
        sig = service.signature
        out = []

        # headers
        for k, v in (sig.headers or {}).items():
            pattern, has_version = strip_modifiers(v)
            out.append(self._header(service.name, k, pattern, has_version))

        # cookies
        for k, v in (sig.cookies or {}).items():
            out.append(Evidence(EvidenceType.COOKIE, service.name, k, "1"))

        # meta
        for k, v in (sig.meta or {}).items():
            pattern, has_version = strip_modifiers(v)
            out.append(self._meta(service.name, k, pattern, has_version))

        # scripts
        for s in (sig.scripts or []):
            pattern, _ = strip_modifiers(s)
            out.append(self._script(service.name, pattern))

        # html
        for h in (sig.html or []):
            pattern, has_version = strip_modifiers(h)
            out.append(self._html(service.name, pattern, has_version))

        # js globals
        for prop in (sig.js or {}).keys():
            out.append(Evidence(EvidenceType.JS, service.name, prop, None))

        return out

    def _header(self, tech, name, pattern, has_version):
        value = tech
        if has_version:
            value = f"{tech}/{fake_version(self.rng, tech)}"
        return Evidence(EvidenceType.HEADER, tech, name, value)

    def _meta(self, tech, name, pattern, has_version):
        value = tech
        if has_version:
            value += f" {fake_version(self.rng, tech)}"
        return Evidence(EvidenceType.META, tech, name, value)

    PATH = re.compile(r'([a-z0-9.-]+\.[a-z]{2,}/[^\s"\']+)', re.I)
    DOMAIN = re.compile(r'([a-z0-9.-]+\.[a-z]{2,})', re.I)

    TAG = re.compile(r'<\s*([a-z0-9-]+)', re.I)
    CLASS = re.compile(r'class=["\']([a-zA-Z0-9 _-]{2,})["\']')

    ALT_TAG = re.compile(r'<\(\?:([^>]+)\)')
    URL_TOKEN = re.compile(r'([a-z0-9.-]+\.[a-z]{2,}[^\s"\'<>]*)', re.I)

    def _script(self, tech, pattern):

        m = self.PATH.search(pattern)
        if m:
            return Evidence(EvidenceType.SCRIPT, tech, None, f"https://{m.group(1)}")

        m = self.DOMAIN.search(pattern)
        if m:
            return Evidence(EvidenceType.SCRIPT, tech, None, f"https://{m.group(1)}/{tech}.js")

        name = re.sub(r'[^a-z0-9]', '', tech.lower())
        return Evidence(EvidenceType.SCRIPT, tech, None, f"/static/{name}/{name}.min.js")

    def _html(self, tech, pattern, has_version):
        # HTML comment
        if "<!--" in pattern:
            text = tech
            if has_version:
                text += f" {fake_version(self.rng, tech)}"
            return Evidence(EvidenceType.COMMENT, tech, None, text)

        # determine tag
        tag = None

        # literal tag
        m = self.TAG.search(pattern)
        if m:
            tag = m.group(1).lower()

        # alternation tag
        if not tag:
            alt = self.ALT_TAG.search(pattern)
            if alt:
                options = alt.group(1).split("|")
                priority = ["iframe","embed","script","link","meta","param","img"]
                for p in priority:
                    if p in options:
                        tag = p
                        break
                else:
                    tag = options[0]

        if not tag:
            tag = "div"

        # collect attributes
        attrs = []

        # class extraction
        m = self.CLASS.search(pattern)
        if m:
            cls = m.group(1).split()[0]
            attrs.append(f'class="{cls}"')

        # inject URL token if detection depends on it
        token = self.URL_TOKEN.search(pattern)
        if token:
            url = "https://" + token.group(1)

            if tag in ("script","iframe","embed","img"):
                attrs.append(f'src="{url}"')

            elif tag == "link":
                attrs.append(f'href="{url}"')

            elif tag == "meta":
                attrs.append(f'content="{url}"')

        # stealth marker
        attrs.append('data-wapparalyser="true"')
        attrs.append(f'data-tech="{tech}"')

        # frankenstein element
        attr_str = " ".join(attrs)
        return Evidence(EvidenceType.HTML, tech, None, f"<{tag} {attr_str}></{tag}>")
