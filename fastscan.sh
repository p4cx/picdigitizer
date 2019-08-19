#!/bin/bash


mkdir ./images
while true; do
	./scanner/scanline -flatbed -resolution 400 -jpeg -dir ./images
	for value in 1
    do
    sleep 1
    echo ${value}
    done
done