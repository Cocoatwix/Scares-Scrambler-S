# Scares Scrambler

The place where all current/future Scares Scrambler stuff will
happen (at least, in it's current form).

Current Version: [v1.22](https://github.com/Cocoatwix/Scares-Scrambler-Class-Rebuild/releases/tag/v1.22)
In development:  v1.3

[Romanian Translation by TheTechnoGuy18](https://github.com/TheTechnoGuy18/ScaresScrambler_Custom)

Currently Planned Features: A bunch, but Scare'm not writing them
right now.

# Don't know what a "GitHub" is?

Go to the [releases tab](https://github.com/Cocoatwix/Scares-Scrambler-Class-Rebuild/releases) to download Scares Scrambler for you're comptuer Now!

# Ancient artifacts?

Look at the very first of the [commits in this repo](https://github.com/Cocoatwix/Scares-Scrambler-Class-Rebuild/commits/master).

All previously private testing versions and older releases were uploaded as commits.

# What need?

- [Python >=3.5][1]
- Tkinter           (comes with all prebuilt versions of Python)
- [Pyinstaller][2]  (optional, for building)
- 7-Zip or p7zip    (optional, for building)
- GNU make          (optional, for building on Linux)
- [Pillow][3]       (required on MacOS)

[1]: https://www.python.org/
[2]: https://www.pyinstaller.org/
[3]: https://python-pillow.org/

```bash
# Install Pyinstaller (not system dependent):
pip3 install pyinstaller

# Install Pillow (required to run on MacOS):
pip3 install Pillow

# Install p7zip (Ubuntu, Debian, Linux Mint):
sudo apt-get update
sudo apt-get install p7zip-full p7zip-rar

# Install p7zip (Arch, Manjaro, Artix Linux):
sudo pacman -Sy p7zip
```

# How run without build?

```
python3 Scrambler.py
```

# How build?

## Linux

Open the console of your choice, and navigate to where you
have extracted a source .zip file or whereever you have
cloned the repository.

Running `make` will create a `Release.zip` file that contains
a binary and `Assets`.

## Windows

Using GNU make is a bit harder on Windows, so Scott've included
a `build.cmd` file.

Install [7-Zip][3] and add it to the `PATH`:

- Press Windows+R, type `sysdm.cpl`, and press enter.
- Click on the `Advanced` tab.
- Click on the `Environment Variables...` button.
- Add or edit the `PATH` variable **for your user**
  (under "User variables") to include
  `C:\Program Files\7-Zip` or `C:\Program Files (x86)\7-Zip`.

(this only has to be done once per system.)

[3]: https://7-zip.org/download.html

Double-clicking `build.cmd` will now create a `Release.zip`
file that contains a binary and `Assets`.
