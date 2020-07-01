#!/usr/bin/env python
import json, ast
from pprint import pprint
import strgen, exrex
import rstr # https://bitbucket.org/leapfrogdevelopment/rstr/src
import re, random
import os, sys, argparse, textwrap, requests, datetime, operator
import urllib.request

if sys.platform.lower() == "win32":
    os.system('color')
    class style():
        BLACK = lambda x: '\033[30m' + str(x)
        RED = lambda x: '\033[31m' + str(x)
        GREEN = lambda x: '\033[32m' + str(x)
        YELLOW = lambda x: '\033[33m' + str(x)
        BLUE = lambda x: '\033[34m' + str(x)
        MAGENTA = lambda x: '\033[35m' + str(x)
        CYAN = lambda x: '\033[36m' + str(x)
        WHITE = lambda x: '\033[37m' + str(x)
        UNDERLINE = lambda x: '\033[4m' + str(x)
        RESET = lambda x: '\033[0m' + str(x)
else:
    class style():
        BLACK = ""
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""
        UNDERLINE = ""
        RESET = ""

counter = 0
banner = textwrap.dedent('''\
    .===================================================================.
    ||      Wapparalyzer - Command-line tool for fuzzing Wappalyzer    ||
    '==================================================================='
    ''')

cookieJSblob = """document.cookie = "%s=%s""" # name:val pair
metadJSblob  = """<meta %s='%s'>""" # attr:val pair
scriptJSblob = """<script src="%s"></script>"""
htmlJSblob   = """%s""" # blob, sometimes []
jsJSblob     = """<script type="text/javascript">%s</script>"""

def tryLoad(file):
    try:
        return open(file.strip(), 'w')
    except:
        print(style.RED('Permission Denied: {}'.format(file)) + style.RESET(''))
        sys.exit(0)

def UpdateJSON():
    blob_url = "https://raw.githubusercontent.com/AliasIO/Wappalyzer/master/src/apps.json"
    try:
        urllib.request.urlretrieve(blob_url, 'source/apps.json')
        print(style.GREEN("[+] Updated the source from AliasIO/Wappalyzer ...") + style.RESET(''))
    except Exception as e:
        print(style.RED("Error: {}\nExiting.".format(e)) + style.RESET(''))

def regex2str(value): # input => str
    if value is not None:
        # ret = ""
        ret = exrex.getone(value)
        return ret
        # while len(ret) < len(value) + 15: # dirty way for retricting rstr from exploding, tweaking left
        #     try:
        #         ret = rstr.xeger(value)
        #         return ret
        #     except:
        #         pass
    else:
        return None

def metaParse(idict): # input => dict
    if idict is not None:
        meta_dict = json.loads(idict) if isinstance(idict, str) else idict
        key, value = next(iter(meta_dict.keys())), next(iter(meta_dict.values()))
        value = regex2str(value)
        return value
    else:
        return None

def get_data(data):
    name, serv = data[0], data[1]
    return name, serv.get('website'), serv.get('implies'), serv.get('headers'), serv.get('meta'), serv.get('html'), serv.get('js'), serv.get('script'), serv.get('cookies')

def brain(bools, data):
 if bools.fuzz:
    print("[*] Fuzzer param was selected ...")
    for service in apps.items():
        # tdqm implementation
        name, website, imply, headers, meta, html, js, scripts, cookies = get_data(service)
        print(meta)
        #meta = metaParse(meta)
        #html = regex2str(html)
        # client, server
        
    print("Total number of services found in apps.json : %d" % counter)
 elif bools.random:
    print("[*] Random flag was selected ...")
    service = apps[list(apps)[random.randrange(0, len(apps))]]
    print("[*] Selected random service, generating fuzzing data ...")
    print("[+] Done.")
 elif bools.list_all:
    print(style.CYAN("[+] Parsing successful, Wappalyzer instance correctly initialized.") + style.RESET(''))
    print(style.YELLOW("[*] Listing all the services ...") + style.RESET(''))
    for num, service in enumerate(apps.items()):
        name, website, imply, headers, meta, html, js, scripts, cookies = get_data(service)
        print("SERVICE [%s] => %s (%s)" % (style.GREEN(num + 1)+style.RESET(''), style.CYAN(name)+style.RESET(''), style.GREEN(website)+style.RESET('')))
        print("    ---- Implies => %s\n    ---- HTTP Headers => %s\n    ---- METADATA => %s\n    ---- HTML => %s\n    ---- JS => %s\n    ---- SCRIPTS => %s\n    ---- Cookies => %s" % (style.RED(imply)+style.RESET(''), style.YELLOW(headers)+style.RESET(''), style.CYAN(meta)+style.RESET(''), style.YELLOW(html)+style.RESET(''), style.RED(js)+style.RESET(''), style.YELLOW(scripts)+style.RESET(''), style.MAGENTA(cookies)+style.RESET('')))
    print(style.YELLOW("[*] Total number of services found in apps.json : {}".format(style.GREEN(num + 1)+style.RESET('')))  + style.RESET(''))
    print(style.GREEN("[+] Comamnd successful, Exiting.") + style.RESET(''))
    sys.exit(1)
 else:
    print("No parameter was provided (use [-h] flag for help), exiting ...")
    sys.exit(1)


parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=style.GREEN(banner) + style.RESET(''), usage=style.GREEN("wapparalyzer ") + style.YELLOW("[-h]") + style.RESET(''))
optional = parser._action_groups.pop() # popped opt args
optional = parser.add_argument_group('Options')

optional.add_argument("-f", "--fuzz-all", dest="fuzz", action='store_true', help= style.GREEN("Fuzzing Wappalyzer") + style.RESET(''))
optional.add_argument("-r", "--random", dest="random", action='store_true', help= style.GREEN("Emulate random services") + style.RESET(''))
optional.add_argument("-l", "--list-all", dest="list_all", action='store_true', help= style.GREEN("Listing all services") + style.RESET(''))
optional.add_argument("-e", "--emulate", dest="emulate", metavar=style.CYAN("Emulate specific service") + style.RESET(''), help= style.GREEN("Emulate a service from list (use --list-all)") + style.RESET(''))
optional.add_argument("-t", "--type", dest="stype", metavar=style.CYAN("metadata|js|scripts|html|headers|cookies") + style.RESET(''), help= style.GREEN("Service fuzz types") + style.RESET(''))
optional.add_argument("-im", "--imply", dest="imply", metavar=style.CYAN("Apache|Python|PHP|Perl") + style.RESET(''), help= style.GREEN("Imply language / tech-stack") + style.RESET(''))
# optional.add_argument("-in", "--inject", dest="inject", metavar=style.CYAN("'/path/to/file'") + style.RESET(''), help= style.GREEN("Inject file path") + style.RESET(''))
optional.add_argument("-o", "--out", dest="output", metavar=style.CYAN("html|txt") + style.RESET(''), help= style.GREEN("Output file format type") + style.RESET(''))
optional.add_argument("-u", "--update", dest="update", action='store_true', help= style.GREEN("Fetching Latest Wappalyzer Mapping") + style.RESET(''))

args = parser.parse_args()
print(style.GREEN(banner) + style.RESET(''))
out_file = args.output

if args.update: # UPDATE AND QUIT #
    UpdateJSON()
    sys.exit(1)

print(style.YELLOW("[*] Loading AliasIO/Wappalyzer JSON ...")+style.RESET(''))
with open('source/apps.json') as f:
    data = json.load(f)
apps = data['apps']

if not out_file: # (not None)
    client, server = brain(args, data)
    print(out) # server part / html
    # write evrything to stdout directory
if out_file:
    client, server = brain(args, data)
    out_file = tryLoad(out_file)
    out_file.write(out)
    print('Written to {}'.format(out_file))