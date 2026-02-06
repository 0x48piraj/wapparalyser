#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import html

SAFE_HTML_TAGS = {
    "div", "span", "meta", "link", "section",
    "article", "header", "footer", "nav", "body"
}

SAFE_ATTR_NAMES = {
    "class", "id", "name", "content", "rel", "type"
}

class Normalizer(object):
    """
    Converts Wappalyzer detection rules into
    safe, non-executable fingerprint artifacts.
    """

    def normalize(self, payload):
        """
        Convert a fuzzed payload into response artifacts.
        """
        return {
            "headers": self._headers(payload.get("headers")),
            "cookies": self._cookies(payload.get("cookies")),
            "meta": self._meta(payload.get("meta")),
            "scripts": self._scripts(payload.get("scripts")),
            "js": self._js(payload.get("js")),
            "html": self._html(payload.get("html")),
        }

    def _headers(self, headers):
        return headers or {}

    def _cookies(self, cookies):
        # cookies are applied at HTTP layer
        return cookies or {}

    def _meta(self, meta):
        """
        Render meta tags from key/value pairs.
        """
        tags = []
        for k, v in meta.items():
            content = v or "true"
            tags.append(f'<meta name="{k}" content="{content}">')
        return "\n".join(tags)

    def _scripts(self, scripts):
        """
        Only external script URLs.
        No inline JS allowed here.
        """
        out = []
        for src in scripts or []:
            out.append('<script src="{}"></script>'.format(src))
        return out

    def _js(self, js_rules):
        """
        Emit inert JavaScript stubs for global object presence checks.
        """
        if not isinstance(js_rules, dict):
            return []

        lines = []
        created = set()

        for key in js_rules.keys():
            if not isinstance(key, str):
                continue

            parts = key.split(".")
            base = "window"

            for part in parts:
                if not part.isidentifier():
                    break

                path = f"{base}.{part}"
                if path not in created:
                    lines.append(f"{path} = {path} || {{}};")
                    created.add(path)

                base = path

        if not lines:
            return []

        return ["<script>\n" + "\n".join(lines) + "\n</script>"]

    def _html(self, html_rules):
        """
        Convert HTML detection regexes into minimal dummy markup.
        """
        out = []
        for rule in html_rules or []:
            dummy = self._dummy_element(rule)
            if dummy:
                out.append(dummy)
        return out

    def _is_safe_attr(self, name):
        return name in SAFE_ATTR_NAMES or name.startswith("data-")

    def _dummy_element(self, pattern):
        """
        Generate a minimal, valid HTML fragment that satisfies
        common Wappalyzer HTML regex signatures.
        """

        if not isinstance(pattern, str):
            return None

        # comment signatures
        if pattern.strip().startswith("<!--"):
            # Preserve comment literal safely
            comment = pattern.strip()
            if not comment.endswith("-->"):
                comment += " -->"
            return comment

        # tag detection
        tag = "div"
        m = re.search(r"<\s*([a-zA-Z][a-zA-Z0-9]*)", pattern)
        if m:
            tag = m.group(1).lower()

        if tag not in SAFE_HTML_TAGS:
            tag = "div"

        # attribute extraction
        attrs = {}

        for attr, val in re.findall(
            r'([a-zA-Z:-]+)\s*=\s*["\']([^"\']+)["\']',
            pattern
        ):
            attr = attr.lower()
            if self._is_safe_attr(attr):
                clean_val = re.sub(r"[\\^$.*+?()[\]{}|]", "", val)
                attrs[attr] = clean_val

        # text-node extraction
        text = None
        m = re.search(r">\s*([^<]{4,})", pattern)
        if m:
            candidate = m.group(1)
            # reject regex-heavy or unsafe text
            if not re.search(r"[\\^$.*+?()[\]{}|]", candidate):
                text = html.escape(candidate.strip())

        # always add a marker
        attrs.setdefault("data-wapparalyser", "true")

        # construct element
        attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())

        if tag in ("meta", "link", "input"):
            return f"<{tag} {attr_str}>"

        if text:
            return f"<{tag} {attr_str}>{text}</{tag}>"

        return f"<{tag} {attr_str}></{tag}>"
