# Wapparalyser

<p align="center">
    <b>Wapparalyser - FnF A.K.A. Fuzzing 'n' Fooling Wappalyzer</b><br><br>
    <img alt="Wapparalyser Logo" src="assets/logo.svg"><br>
</p>

**Wapparalyser** is a security tool for blue-teams which was released after my talk at BSides Delhi 2019. It defeats [Wappalyzer](https://www.wappalyzer.com/), a common red-team tool that uncovers the technologies used on websites.

It supports emulating services (random or specific tech-stack, e.g. MEAN, LAMP, LAMB, DONKEY...). It also has an in-built small fuzzer for Wappalyzer (`metadata|js|scripts|html|headers|cookies`).