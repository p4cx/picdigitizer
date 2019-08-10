# picdigitizer
Tool to auto-crop old analog pictures and add a description in the digital files.
This application is very focused on my system. I'm sure, that you have to change something to use it properly.
   
Tool only used and tested under macOS!

#### What I used
Epson Perfection V30 Scanner on macOS Mojave 

#### Build
- Install `requirements.txt` for `pip`
- Set Permissions: `chmod +x ./build.sh ./scan.sh`
- Run `./build.sh`

#### Scan pictures
- Run `./scan.sh`
- Between each scan process, you have three seconds to change the picture.
- Make sure the lid stays open and the room is dark. For best results, cover the white part of the lid.

#### Usage
- After scanning you will found all the pictures in your new `./images` folder.
- 

#### Elements from other projects:
- _Command line scanning utility for OSX:_ [scanline](https://github.com/klep/scanline)
- _Sans serif font family for user interface environments:_ [source-sans-pro](https://github.com/adobe-fonts/source-sans-pro)