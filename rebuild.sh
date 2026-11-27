#!/bin/sh
# Regénère le site puis rafraîchit la copie d'aperçu locale
cd "$(dirname "$0")" && python3 build.py && rm -rf "$1" && cp -R docs "$1"
