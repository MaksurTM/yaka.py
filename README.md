# yaka.py
Downloads images of a given search query and then creates a video with 10 images per second and a song.
By default the number of images is 698, about 1 minute and 8 seconds long in video.
These images are stored in `./images` and in `./img`(720p versions) and are deleted after the video is made unless `-k` is given.
`-n` can be used to change the amount of images.

## Dependencies
- firefox and geckodriver
- imagemagick
- ffmpeg
- audio.mp3 (needs to be in the same directory)
- selenium - `pip install selenium`
- pycurl - `pip install pycurl`

## Usage
Example: `python3 yaka.py Bread`
This will make a video using 698 images of bread. 
```
usage: yaka.py [-h] [-n NUMBER] [-k] QUERY

positional arguments:
  QUERY                 Target to download images of.

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER,            Number if images to download.
  -k, --keep            Won't delete downloaded images after video creation.
```
