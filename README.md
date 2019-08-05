# picdigitizer
Tool to auto-crop old analog pictures and add a description on the digital files.

#### USAGE
- Take a picture of the analog pictures. Make sure the background is as dark (black) as possible. Also, be sure to take the pictures in * .JPG format.
- Put all pictures in a folder and call the program with `python main.py /path/to/your/picture/folder 800` (use Python > 3)
- The tool will create a subfolder and then paste once the cropped images without the description and once with the entered description. The description is requested for each image after execution: Simply enter the description here, `Enter` and then the program jumps to the next image. Repeat until all pictures are through.
