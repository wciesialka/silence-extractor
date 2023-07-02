# silence-extractor

Removes any parts of a video with a volume over a certain threshold, leaving only the silent parts of the video.

## requirements

* ffmpeg
* Python 3.7+
* requirements from [requirements.txt](requirements.txt)

## running

Either run using `pipenv run python main.py` or run `pip3 install --user -r requirements.txt` to install dependencies followed by `python3 main.py`. I found that ffmpeg may not run correctly when using `pipenv`, so I suggest the second option.

## license

Check [LICENSE](LICENSE) for details

## authors

* Willow Ciesialka
