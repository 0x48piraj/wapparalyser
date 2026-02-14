#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template

def register_ui_routes(app):

    @app.get("/")
    def index():
        return render_template("index.html")
