#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

class Style(object):
    def __init__(self):
        self.enabled = self._supports_color()

        if self.enabled:
            self.BLACK = "\033[30m"
            self.RED = "\033[31m"
            self.GREEN = "\033[32m"
            self.YELLOW = "\033[33m"
            self.BLUE = "\033[34m"
            self.MAGENTA = "\033[35m"
            self.CYAN = "\033[36m"
            self.WHITE = "\033[37m"
            self.UNDERLINE = "\033[4m"
            self.RESET = "\033[0m"
        else:
            self.BLACK = ""
            self.RED = ""
            self.GREEN = ""
            self.YELLOW = ""
            self.BLUE = ""
            self.MAGENTA = ""
            self.CYAN = ""
            self.WHITE = ""
            self.UNDERLINE = ""
            self.RESET = ""

    def _supports_color(self):
        if sys.platform.lower() == "win32":
            try:
                os.system("color")
                return True
            except Exception:
                return False
        return True

    def wrap(self, color, text):
        return "{}{}{}".format(color, text, self.RESET)
