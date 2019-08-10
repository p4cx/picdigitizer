#!/bin/bash


mkdir ./res
mkdir ./scanner
wget https://github.com/adobe-fonts/source-sans-pro/raw/release/TTF/SourceSansPro-Regular.ttf -P ./res 
wget https://github.com/klep/scanline/blob/master/build/Products/Debug/scanline?raw=true -O ./scanner/scanline
chmod +x ./scanner/scanline