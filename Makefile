Release.zip: clean Scrambler.py Engine.py Themes.py Assets
	pyinstaller Scrambler.py -w -F -i Assets/favi.ico
	7z a Release.zip ./dist/* Assets

clean:
	rm -rf __pycache__ dist build *.spec *.exe Release.zip