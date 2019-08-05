import sys
import os
import tkinter as tk
from PIL import ImageTk, Image


def picture_window(path, window_size):
    window = tk.Tk()
    window.title(path)
    window.geometry(str(window_size) + "x" + str(window_size))
    window.configure(bg='grey')

    image = Image.open(path)
    image_width, image_height = image.size
    if image_height >= image_width:
        image_width = int(image_width/(image_height/window_size * 2 / 3))
        image_height = int(image_height/(image_height/window_size * 2 / 3))
    else:
        image_height = int(image_height/(image_width/window_size))
        image_width = int(image_width/(image_width/window_size))

    canvas = tk.Canvas(window, height=image_height, width=image_width)

    resize_image = image.resize((image_width, image_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(resize_image)
    canvas.create_image(image_width/2, image_height/2, image=photo)
    canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    window.mainloop()


def create_sub_dirs(path):
    sub_dirs = ["/orig_photos", "/crop_photos", "/desc_photos"]
    try:
        for folder in sub_dirs:
            if not os.path.exists(path + folder):
                os.mkdir(path + folder)
    except OSError:
        print("Creation of the directory %s failed" % path)
        exit(0)


def sort_files(path_list):
    picture_path_list = []
    for path in path_list:
        if path[-3:] == "jpg" or path[-3:] == "JPG":
            picture_path_list.append(path)
    return picture_path_list


def get_file_paths(path):
    return [os.path.join(path, fn) for fn in next(os.walk(path))[2]]


def main(argv):
    if len(argv) == 2:
        path = argv[0]
        window_size = int(argv[1])
        if os.path.exists(path) and window_size > 0:
            create_sub_dirs(path)
            picture_paths = sort_files(get_file_paths(path))
            for path in picture_paths:
                picture_window(path, window_size)
        else:
            print("Your path is not valid or your screen size integer is smaller than 0")
            exit(0)
    else:
        print("You must have exact 2 arguments:\n1. Path to your picture folder\n2. Window size for x and y as one integer"
              "\nExample: python3 main.py /path/to/your/picture/folder 800")


if __name__ == "__main__":
    main(sys.argv[1:])
