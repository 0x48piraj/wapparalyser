#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web.proxy import proxy_handler

def register_proxy_only(app):
    app.add_url_rule(
        "/proxy",
        endpoint="proxy",
        view_func=proxy_handler,
        methods=["GET"],
    )
