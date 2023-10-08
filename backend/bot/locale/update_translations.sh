#!/bin/bash

cd "$(dirname "$0")"
xgettext -d exampleQAbot -o exampleQAbot.pot ../exampleQAbot.py
msgmerge --update ./en/LC_MESSAGES/exampleQAbot.po exampleQAbot.pot
msgmerge --update ./tr/LC_MESSAGES/exampleQAbot.po exampleQAbot.pot
msgfmt ./en/LC_MESSAGES/exampleQAbot.po -o ./en/LC_MESSAGES/exampleQAbot.mo
msgfmt ./tr/LC_MESSAGES/exampleQAbot.po -o ./tr/LC_MESSAGES/exampleQAbot.mo
