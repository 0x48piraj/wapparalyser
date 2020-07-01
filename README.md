# Wapparalyser

![License](https://img.shields.io/github/license/0x48piraj/wapparalyser)
![Version: 1.0](https://img.shields.io/badge/version-1.0-blue.svg)
![Commits](https://img.shields.io/github/commit-activity/y/0x48piraj/wapparalyser)

<p align="center">
    <img alt="Wapparalyser Logo" src="assets/logo.jpg"><br>
    <i>Fuzzing 'n' Fooling Wappalyzer</i>
</p>

Wapparalyser is a security tool for blue-teams which defeats [Wappalyzer](https://www.wappalyzer.com/), a common red-team tool that uncovers the technologies used on websites.

Wapparalyser was presented at BSides Delhi 2019. The command-line tool is built on Python and will have an interactive web-app in near future. It transparently intercepts all the static detections that Wappalyzer uses in order to camouflage, modify and defeat the tool in real-time.

Wapparalyser has been completely written from the ground-up, after reverse-enginnering Wappalyzer to it's core and thus, it is highly flexible and automatically adapts without manually inserting any new heuristics/fingerprints.

#### Features

◆ Emulating services
● Random
● All
● Certain tech-stack (e.g. MEAN, LAMP, LAMB, DONKEY?)

➔ In-built small fuzzer for Wappalyzer
● Blind
● metadata|js|scripts|html|headers|cookies

Some additional features:

- No website modification or lengthy patches
- Simple user interface and several logging features
- Modes: front-end, back-end & combined
- Emulates any service (currently, 1123)
- Undetectable to attackers