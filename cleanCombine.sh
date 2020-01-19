#!/bin/bash
ffmpeg -safe 0 -f concat -i <(find ./video -type f -name '*' -printf "file '$PWD/%p'\n" | sort) -c copy ./output/$1_vid.mp4
rm -r ./video/*