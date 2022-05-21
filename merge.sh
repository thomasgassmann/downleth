#!/bin/bash

for i in `\ls out/*.ts | sort -V`; do echo "file '$i'"; done >> mylist.txt
ffmpeg -f concat -i mylist.txt -c copy -bsf:a aac_adtstoasc video.mp4
