# Wapparalyser

<p align="center">
    <img alt="Wapparalyser Logo" src="assets/logo.jpg"><br>
    <i>Fuzzing 'n' Fooling Wappalyzer</i>
</p>

Wapparalyser is a security tool for blue-teams which defeats [Wappalyzer](https://www.wappalyzer.com/), a common red-team tool that uncovers the technologies used on websites.

Wapparalyser was presented at BSides Delhi 2019. The command-line tool is built on Python and it has been completely written from the ground-up, after reverse-enginnering Wappalyzer to it's core and thus, it is highly flexible and automatically adapts without manually inserting any new heuristics/fingerprints. It intercepts all the static detections that Wappalyzer uses in order to camouflage, modify and defeat the tool in real-time.

Wapparalyser will have an interactive web-app in near future.

## Features

- Emulating services
   * All
   * Random
   * Certain tech-stack (e.g. MEAN, LAMP, LAMB, DONKEY?)
- In-built small fuzzer for Wappalyzer
   * Blind
   * metadata|js|scripts|html|headers|cookies

➔ **Some additional features**

- No website modification or lengthy patches
- Simple user interface and several logging features
- Modes: front-end, back-end & combined
- Emulates any service (currently, 1123)
- Undetectable to attackers


## Install

The project provides a script that will run a Wapparalyser instance isolated from the rest of your system by using file-less/memory-based execution.

```
curl -sSL https://raw.githubusercontent.com/0x48piraj/wapparalyser/master/src/cmdline/cli.py | python
```