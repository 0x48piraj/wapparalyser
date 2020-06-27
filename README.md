# Wapparalyser

<p align="center">
    <b>Wapparalyser - FnF A.K.A. Fuzzing 'n' Fooling Wappalyzer</b><br><br>
    <img alt="Wapparalyser Logo" src="assets/logo.svg" width="400"><br>
</p>

**Wapparalyser** is a security tool for blue-teams which was released after my talk at BSides Delhi 2019. It defeats [Wappalyzer](https://www.wappalyzer.com/), a common red-team tool that uncovers the technologies used on websites.

It supports emulating services (random or specific tech-stack, yeah, MEAN, LAMP, LAMB, DONKEY ...anything). In-built small fuzzer for Wappalyzer supporting `metadata|js|scripts|html|headers|cookies` or blind.