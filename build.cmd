@echo off
pyinstaller Scrambler.py -w -F -i Assets/favi.ico
7z a Release.zip ./dist/* Assets