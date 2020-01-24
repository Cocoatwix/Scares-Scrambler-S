# Scares-Scrambler-Class-Rebuild

The place where all current/future Scares Scrambler stuff will happen
(at least, in it's current form).

Current Release Build: 20

Current Beta Build: 9+10

Currently Planned Features: A bunch, but Scare'm not writing them right now.

# What need?

- Python3
- Tkinter (comes with all prebuilt versions of Python)
- Pyinstaller (optional, for building)

`pip3 install pyinstaller`

If you're running Python 3.8, as of now you need to install the
*development* version of Pyinstaller for the build to work at all:

`pip3 install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz`

# How run without build?

```
python3 Scares_Scrambler_Class_Rebuild.py
```

# How build?

```
pyinstaller Scares_Scrambler_Class_Rebuild.py -w -F -i Assets/favi.ico
```
