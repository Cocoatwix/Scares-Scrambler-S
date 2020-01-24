Release.zip: clean Scrambler.py Engine.py Themes.py Assets
	pyinstaller Scrambler.py -w -F -i Assets/favi.xbm
	7z a Release.zip ./dist/* Assets

clean:
	rm -rf __pycache__ dist build *.spec *.exe Release.zip