#!/bin/bash

sudo apt install ffmpeg -y
sudo apt install pyenv -y
pyenv install 3.13.2
eval "$(pyenv init -)"
python -m pip install yt-dlp
python -m pip install musicbrainzngs
python -m pip install youtube-search-python
python -m pip install mutagen
python ./script.py