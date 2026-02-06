#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap
import argparse
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wapparalyser.loader import load_services
from wapparalyser.style import Style
from wapparalyser.engine import WapparalyserEngine
import wapparalyser.output as output

DEFAULT_APPS_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "signatures",
    "apps.json"
)

BANNER = textwrap.dedent('''\
    .===================================================================.
    ||      Wapparalyzer - Command-line tool for fuzzing Wappalyzer    ||
    '==================================================================='
    ''')

style = Style()

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=style.wrap(style.GREEN, BANNER), usage=style.wrap(style.GREEN, "wapparalyzer [-h]"))

    parser.add_argument("-l", "--list", action="store_true", help=style.wrap(style.GREEN, "List all available services"))
    parser.add_argument("-r", "--random", action="store_true", help=style.wrap(style.GREEN, "Emulate a random service"))
    parser.add_argument("-e", "--emulate", metavar="SERVICE", help=style.wrap(style.GREEN, "Emulate a specific service by name"))
    parser.add_argument("-f", "--fuzz", action="store_true", help=style.wrap(style.GREEN, "Fuzz all known Wappalyzer signatures"))
    parser.add_argument("-t", "--type", metavar="TYPE", choices=["headers", "html", "js", "meta", "cookies", "scripts"], help=style.wrap(style.GREEN, "Restrict fuzzing to a specific detection type"))
    parser.add_argument("-o", "--output", metavar="FILE", help=style.wrap(style.GREEN, "Write output to a file instead of stdout"))
    parser.add_argument("-u", "--update", action="store_true", help=style.wrap(style.GREEN, "Update Wappalyzer signatures from upstream"))

    return parser.parse_args()

def main():
    args = parse_args()

    # exit early
    if args.update:
        from wapparalyser.loader import update_signatures
        update_signatures(DEFAULT_APPS_PATH)
        return 0

    # load services
    try:
        services = load_services(DEFAULT_APPS_PATH)
    except IOError as exc:
        sys.stderr.write("[-] Failed to load apps.json: {}\n".format(exc))
        return 1

    engine = WapparalyserEngine(services)

    # dispatch actions
    if args.list:
        services = engine.list_services()
        for idx, name in enumerate(services, 1):
            print("[{}] {}".format(idx, name))
        return 0

    elif args.random:
        result = engine.emulate_random()

    elif args.emulate:
        result = engine.emulate_service(args.emulate, mode=args.type)

    elif args.fuzz:
        result = engine.fuzz(mode=args.type)

    else:
        sys.stderr.write("[-] No action specified. Use -h for help.\n")
        return 1

    # render output
    if args.output:
        output.write_to_file(result, args.output)
    else:
        output.write_to_stdout(result)

    return 0

if __name__ == "__main__":
    sys.exit(main())
