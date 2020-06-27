#!/usr/bin/env python
import json
from pprint import pprint
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

def tryLoad(file):
    try:
        return open(file.strip(), 'w')
    except:
        print(style.RED('Permission Denied: {}'.format(file)) + style.RESET(''))
        sys.exit(0)

def UpdateJSON():
    blob_url = "https://raw.githubusercontent.com/AliasIO/Wappalyzer/master/src/apps.json"
    try:
        urllib.request.urlretrieve(blob_url, 'src/apps.json')
        print(style.GREEN("[+] Updated the source from AliasIO/Wappalyzer ...") + style.RESET(''))
    except Exception as e:
        print(style.RED("Error: {}\nExiting.".format(e)) + style.RESET(''))
        sys.exit(1)

def get_data(service): # I think I was drunk o_O
    try:
        name, website = (service[0], service[1]['website'])
        imply = service[1]['implies']
    except KeyError:
        imply = None
    try:
        headers = service[1]['headers']
    except KeyError:
        headers = None
    try:
        meta = service[1]['meta']
    except KeyError:
        meta = None
    try:
        html = service[1]['html']
    except KeyError:
        html = None
    try:
        js = service[1]['js']
    except KeyError:
        js = None
    try:
        scripts = service[1]['script']
    except KeyError:
        scripts = None
    try:
        cookies = service[1]['cookies']
    except KeyError:
        cookies = None
    return name, website, imply, headers, meta, html, js, scripts, cookies

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=style.GREEN(banner) + style.RESET(''), usage=style.GREEN("wapparalyzer ") + style.YELLOW("[-h]") + style.RESET(''))
optional = parser._action_groups.pop() # popped opt args
optional = parser.add_argument_group('Options')

optional.add_argument("-f", "--fuzz-all", dest="fuzz", action='store_true', help= style.GREEN("Fuzzing Wappalyzer") + style.RESET(''))
optional.add_argument("-r", "--random", dest="random", action='store_true', help= style.GREEN("Emulate random services") + style.RESET(''))
optional.add_argument("-l", "--list-all", dest="list_all", action='store_true', help= style.GREEN("Listing all services") + style.RESET(''))
optional.add_argument("-e", "--emulate", dest="emulate", metavar=style.CYAN("Service") + style.RESET(''), help= style.GREEN("Emulate a service from list (use --list-all)") + style.RESET(''))
optional.add_argument("-t", "--type", dest="stype", metavar=style.CYAN("metadata|js|scripts|html|headers|cookies") + style.RESET(''), help= style.GREEN("Service fuzz types") + style.RESET(''))
optional.add_argument("-im", "--imply", dest="imply", metavar=style.CYAN("Apache|Python|PHP|Perl") + style.RESET(''), help= style.GREEN("Imply language / tech-stack") + style.RESET(''))
# optional.add_argument("-in", "--inject", dest="inject", metavar=style.CYAN("'/path/to/file'") + style.RESET(''), help= style.GREEN("Inject file path") + style.RESET(''))
optional.add_argument("-o", "--out", dest="output", metavar=style.CYAN("html|txt") + style.RESET(''), help= style.GREEN("Output file format type") + style.RESET(''))
optional.add_argument("-u", "--update", dest="update", action='store_true', help= style.GREEN("Fetching Latest Wappalyzer Mapping") + style.RESET(''))

args = parser.parse_args()
print(style.GREEN(banner) + style.RESET(''))
out_file = args.output
# UPDATE AND QUIT #
if args.update:
    UpdateJSON()
    sys.exit(1)

print(style.YELLOW("[*] Loading AliasIO/Wappalyzer JSON ...")+style.RESET(''))
with open('src/apps.json') as f:
    data = json.load(f)
apps = data['apps']


def regex2str(input): # input => dict
    value = next(iter(input.values())) # value => dict_keys --> str
    while True:
        try:
            ret = rstr.xeger(value)
            if len(ret) < len(input) + 15: # dirty way for retricting rstr from exploding
                return ret
                break;
        except:
            pass

def brain(bools, data):
 if bools.fuzz:
    print("[*] Fuzzer param was selected ...")
    for service in data['apps'].items():
        # tdqm implementation
        name, website, imply, headers, meta, html, js, scripts, cookies = get_data(service)
        meta = next(iter(input.keys())) + regex2str(meta)
        html = regex2str(html)
        client, server
        

    print("Total number of services found in apps.json : %d" % counter)

 elif bools.list_all:
    print(style.CYAN("[+] Parsing successful, Wappalyzer instance correctly initialized.") + style.RESET(''))
    print(style.YELLOW("[*] Listing all the services ...") + style.RESET(''))
    for num,service in enumerate(data['apps'].items()):
        name, website, imply, headers, meta, html, js, scripts, cookies = get_data(service)
        print("SERVICE NAME [%s] => %s (%s)" % (style.GREEN(num + 1)+style.RESET(''), style.CYAN(name)+style.RESET(''), style.GREEN(website)+style.RESET('')))
        print("    ---- Implies => %s\n    ---- HTTP Headers => %s\n    ---- METADATA => %s\n    ---- HTML => %s\n    ---- JS => %s\n    ---- SCRIPTS => %s\n    ---- Cookies => %s" % (style.RED(imply)+style.RESET(''), style.YELLOW(headers)+style.RESET(''), style.CYAN(meta)+style.RESET(''), style.YELLOW(html)+style.RESET(''), style.RED(js)+style.RESET(''), style.YELLOW(scripts)+style.RESET(''), style.MAGENTA(cookies)+style.RESET('')))
    print(style.YELLOW("[*] Total number of services found in apps.json : {}".format(style.GREEN(num + 1)+style.RESET('')))  + style.RESET(''))
    print(style.GREEN("[+] Comamnd successful, Exiting.") + style.RESET(''))
    sys.exit(1)
 elif bools.random:
    print("[*] Random flag was selected ...")
    rand = random.randrange(0, len(apps))
    service = apps[list(apps)[rand]]
    print("[*] Selected random service, generating fuzzing data ...")
    print("[+] Done.")

 else:
    print("No parameter was provided (use [-h] flag for help), exiting ...")
    sys.exit(1)


if not out_file: # (not None)
    client, server = brain(args, data)
    print(out) # server part / html
    # write evrything to stdout directory
if out_file:
    client, server = brain(args, data)
    out_file = tryLoad(out_file)
    out_file.write(out)
    print('Written to {}'.format(out_file))