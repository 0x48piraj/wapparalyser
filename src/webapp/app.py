from flask import Flask, render_template, request, redirect, session, url_for, make_response
from flask import jsonify
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from io import BytesIO
import base64
import re, os
import requests, json
import itertools
import string
import html

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

app = CustomFlask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run("0.0.0.0", port=8005, debug=True, threaded=True)