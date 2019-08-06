import sys
import os
import math
import tkinter as tk
from PIL import ImageTk, Image


def crop_picture(path, sensibility, sub_dirs):
    raw_image = Image.open(path)
    rgb_raw_image = raw_image.convert("RGB")
    image_width, image_height = rgb_raw_image.size

    picture_start_point_x = run_trough_picture(rgb_raw_image, "W", 0, sensibility)
    picture_rotation_n_x = run_trough_picture(rgb_raw_image, "W", -int(image_width/10), sensibility)
    picture_rotation_s_x = run_trough_picture(rgb_raw_image, "W", int(image_width/10), sensibility)

    if picture_rotation_n_x >= picture_rotation_s_x:
        opposite = picture_rotation_n_x - picture_start_point_x
        rotation_value = math.tan(opposite / int(image_width / 10))
        rotated_image = raw_image.rotate(math.degrees(rotation_value), expand=True,
                                         fillcolor=rgb_raw_image.getpixel((0, 0)))
    else:
        opposite = picture_rotation_s_x - picture_start_point_x
        rotation_value = math.tan(opposite / int(image_width / 10))
        rotated_image = raw_image.rotate(math.degrees(-rotation_value), expand=True,
                                         fillcolor=rgb_raw_image.getpixel((0, 0)))

    cropped_image = rotated_image.crop((
        run_trough_picture(rotated_image, "W", 0, sensibility) + 20,
        run_trough_picture(rotated_image, "N", 0, sensibility) + 20,
        run_trough_picture(rotated_image, "E", 0, sensibility) - 20,
        run_trough_picture(rotated_image, "S", 0, sensibility) - 20
    ))

    path, filename = os.path.split(path)
    raw_image.save(path + sub_dirs[0] + "/" + filename)
    cropped_image_path = path + sub_dirs[1] + "/" + filename
    cropped_image.save(cropped_image_path)

    return cropped_image_path


def run_trough_picture(rgb_raw_image, position, start_pos, sensibility):
    image_width, image_height = rgb_raw_image.size
    if position == "W":
        pixel_x = 0
        pixel_y = int(image_height / 2) + start_pos
        r_old, g_old, b_old = rgb_raw_image.getpixel((pixel_x, pixel_y))
        for x in range(0, int(image_width / 2)):
            r, g, b = rgb_raw_image.getpixel((x, pixel_y))
            if (abs(r - r_old) >= sensibility) or (abs(g - g_old) >= sensibility) or (abs(b - b_old) >= sensibility):
                # print("POS:", position, ":", x, "/", pixel_y, "->", r, g, b)
                return x
            r_old, g_old, b_old = r, g, b

    elif position == "N":
        pixel_x = int(image_width / 2) + start_pos
        pixel_y = 0
        r_old, g_old, b_old = rgb_raw_image.getpixel((pixel_x, pixel_y))
        for y in range(0, int(image_height / 2)):
            r, g, b = rgb_raw_image.getpixel((pixel_x, y))
            if (abs(r - r_old) >= sensibility) or (abs(g - g_old) >= sensibility) or (abs(b - b_old) >= sensibility):
                # print("POS:", position, ":", pixel_x, "/", y, "->", r, g, b)
                return y
            r_old, g_old, b_old = r, g, b

    elif position == "E":
        pixel_x = image_width - 1
        pixel_y = int(image_height / 2) + start_pos
        r_old, g_old, b_old = rgb_raw_image.getpixel((pixel_x, pixel_y))
        for x in range(image_width - 1, int(image_width / 2), -1):
            r, g, b = rgb_raw_image.getpixel((x, pixel_y))
            if (abs(r - r_old) >= sensibility) or (abs(g - g_old) >= sensibility) or (abs(b - b_old) >= sensibility):
                # print("POS:", position, ":", x, "/", pixel_y, "->", r, g, b)
                return x
            r_old, g_old, b_old = r, g, b

    elif position == "S":
        pixel_x = int(image_width / 2) + start_pos
        pixel_y = image_height - 1
        r_old, g_old, b_old = rgb_raw_image.getpixel((pixel_x, pixel_y))
        for y in range(image_height - 1, int(image_height / 2), -1):
            r, g, b = rgb_raw_image.getpixel((pixel_x, y))
            if (abs(r - r_old) >= sensibility) or (abs(g - g_old) >= sensibility) or (abs(b - b_old) >= sensibility):
                # print("POS:", position, ":", pixel_x, "/", y, "->", r, g, b)
                return y
            r_old, g_old, b_old = r, g, b

    else:
        return 0


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


def create_sub_dirs(path, sub_dirs):
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
    if len(argv) == 3:
        path = argv[0]
        window_size = int(argv[1])
        sensibility = int(argv[2])
        sub_dirs = ["/orig_photos", "/crop_photos", "/desc_photos"]
        if os.path.exists(path) and window_size > 0:
            create_sub_dirs(path, sub_dirs)
            picture_paths = sort_files(get_file_paths(path))
            for path in picture_paths:
                cropped_image_path = crop_picture(path, sensibility, sub_dirs)
                picture_window(cropped_image_path, window_size)
        else:
            print("Your path is not valid or your screen size integer is smaller than 0")
            exit(0)
    else:
        print("You must have exact 3 arguments:"
              "\n1. Path to your picture folder"
              "\n2. Window size for x and y as one"
              "\n3. Sensibility for background"
              "\nExample: python3 main.py /path/to/your/picture/folder 800 10")


if __name__ == "__main__":
    main(sys.argv[1:])
