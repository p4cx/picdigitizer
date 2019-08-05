import sys
import os
import tkinter as tk
from PIL import ImageTk, Image


WINDOW_SIZE = 800


def picture_window(path):
    window = tk.Tk()
    window.title(path)
    window.geometry(str(WINDOW_SIZE) + "x" + str(WINDOW_SIZE))
    window.configure(bg='grey')

    image = Image.open(path)
    image_width, image_height = image.size
    if image_height >= image_width:
        image_width = int(image_width/(image_height/WINDOW_SIZE * 2 / 3))
        image_height = int(image_height/(image_height/WINDOW_SIZE * 2 / 3))
    else:
        image_height = int(image_height/(image_width/WINDOW_SIZE))
        image_width = int(image_width/(image_width/WINDOW_SIZE))
        print("1", image_width, image_height, (image_width/WINDOW_SIZE))

    canvas = tk.Canvas(window, height=image_height, width=image_width)

    resize_image = image.resize((image_width, image_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(resize_image)
    canvas.create_image(image_width/2, image_height/2, image=photo)
    canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    window.mainloop()


def create_sub_dirs(path):
    sub_dirs = ["/orig_photos", "/crop_photos", "desc_photos"]
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
    path = argv[0]
    if os.path.exists(path):
        create_sub_dirs(path)
        picture_paths = sort_files(get_file_paths(path))
        for path in picture_paths:
            picture_window(path)
    else:
        print("Your path is not valid!")
        exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
