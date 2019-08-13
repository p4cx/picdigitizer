import os
import sys
import tkinter as tk

from PIL import ImageTk, Image, ImageDraw, ImageFont

redo = False


class CheckImage:
    def __init__(self, window, image_path, window_size, font_path, description):
        def ok(event):
            top.destroy()

        def stop(event):
            global redo
            redo = True
            top.destroy()

        top = self.top = tk.Toplevel(window)
        top.configure(bg="Red")
        top.title(image_path)

        my_label = tk.Label(top,
                            text='Image Check - Press \'Enter\' to save this picture or \'ESC\' to cancel this '
                                 'operation.', borderwidth=5, relief=tk.SOLID, font=(font_path, 14))
        my_label.pack()

        check_image = Image.open(image_path)
        image_width, image_height = check_image.size
        if image_height >= image_width:
            image_width = int(image_width / (image_height / window_size * 3 / 2))
            image_height = int(image_height / (image_height / window_size * 3 / 2))
        else:
            image_height = int(image_height / (image_width / window_size))
            image_width = int(image_width / (image_width / window_size))

        canvas = tk.Canvas(top, height=image_height, width=image_width, bg="Red", bd=0, highlightthickness=0,
                           relief=tk.RIDGE)
        canvas.pack()
        resize_image = check_image.resize((image_width, image_height))
        photo = ImageTk.PhotoImage(resize_image)
        canvas.create_image(image_width / 2, image_height / 2, image=photo)

        text_label = tk.Label(top, text=description, borderwidth=5, relief=tk.SOLID, font=(font_path, 14))
        text_label.pack()

        top.update_idletasks()

        top.bind('<Return>', ok)
        top.bind('<Escape>', stop)

        top.mainloop()


def crop_picture(path, sensibility, sub_dirs, resize):
    raw_image = Image.open(path)
    image_width, image_height = raw_image.size
    rgb_raw_image = raw_image.convert("RGB")

    orientations = ["E", "S"]
    e_crop, s_crop = 0, 0

    for orientation in orientations:
        crop_points = []
        for x in range(1, 11):
            point_options = {
                1: 0,
                2: min(image_width, image_height) / 25,
                3: - min(image_width, image_height) / 25,
                4: min(image_width, image_height) / 25 * 2,
                5: - min(image_width, image_height) / 25 * 2,
                6: min(image_width, image_height) / 25 * 3,
                7: - min(image_width, image_height) / 25 * 3,
                8: min(image_width, image_height) / 25 * 4,
                9: - min(image_width, image_height) / 25 * 4,
                10: min(image_width, image_height) / 25 * 5,
                11: - min(image_width, image_height) / 25 * 5,
            }

            crop_point = run_trough_picture(rgb_raw_image, orientation, point_options.get(x, 0), sensibility)
            if crop_point is not None:
                crop_points.append(crop_point)
        print(crop_points)
        crop_points.remove(max(crop_points))
        crop_points.remove(max(crop_points))
        crop_points.remove(min(crop_points))
        crop_points.remove(min(crop_points))
        crop = sum(crop_points) / len(crop_points)
        if orientation == "E":
            e_crop = crop
        else:
            s_crop = crop

    cropped_image = rgb_raw_image.crop((
        0,
        0,
        e_crop - 10,
        s_crop - 10
    ))

    path, filename = os.path.split(path)
    if "jpeg" in filename:
        filename = filename[:-4]
    else:
        filename = filename[:-3]
    cropped_image_path = path + sub_dirs[1] + "/" + filename + "png"
    resize_width, resize_height = cropped_image.size
    if resize_height <= resize_width:
        resize_factor = resize_height / resize
    else:
        resize_factor = resize_width / resize
        print(resize_factor)

    resize_height = int(resize_height / resize_factor)
    resize_width = int(resize_width / resize_factor)
    print(resize_width, resize_height)
    resize_cropped_image = cropped_image.resize((resize_width, resize_height), Image.LANCZOS)
    resize_cropped_image.save(cropped_image_path)

    return cropped_image_path


def run_trough_picture(rgb_raw_image, position, start_pos, sensibility):
    image_width, image_height = rgb_raw_image.size

    if position == "E":
        ground_pixel_x = image_width - 5
        ground_pixel_y = int(image_height / 2) + start_pos
    else:
        ground_pixel_x = int(image_width / 2) + start_pos
        ground_pixel_y = image_height - 5

    ground_color_list = (rgb_raw_image.getpixel((ground_pixel_x, ground_pixel_y)),
                         rgb_raw_image.getpixel((ground_pixel_x + 2, ground_pixel_y)),
                         rgb_raw_image.getpixel((ground_pixel_x, ground_pixel_y + 2)),
                         rgb_raw_image.getpixel((ground_pixel_x + 2, ground_pixel_y + 2)))
    ground_color = tuple(map(lambda y: sum(y) / float(len(y)), zip(*ground_color_list)))
    r_old, g_old, b_old = ground_color

    if position == "E":
        for x in range(image_width - int(image_width / 3), int(image_width / 6), -5):
            r, g, b = rgb_raw_image.getpixel((x, int(image_height / 6) + start_pos))
            if (abs(r - r_old) >= sensibility) or (abs(g - g_old) >= sensibility) or (abs(b - b_old) >= sensibility):
                print("x:", x, 1, image_width - int(image_width / 3), int(image_width / 6))
                return x

    elif position == "S":
        print(image_height - int(image_height / 3), int(image_height / 6))
        for y in range(image_height - int(image_height / 4), int(image_height / 4), -5):
            r, g, b = rgb_raw_image.getpixel((int(image_width / 6) + start_pos, y))
            if (abs(r - r_old) >= sensibility) or (abs(g - g_old) >= sensibility) or (abs(b - b_old) >= sensibility):
                print("y:", y, 1)
                return y

    else:
        return 0


def create_desc_picture(description, path, sub_dirs, font_path, commands):
    font_size = 32

    image = Image.open(path)
    count_turn_left, count_turn_right = 0, 0
    for command in commands:
        if command is "turn_left":
            count_turn_left += 1
        elif command is "turn_right":
            count_turn_right += 1

    rotation_degree = (90 * count_turn_left) - (90 * count_turn_right)
    rotate_image = image.rotate(rotation_degree, expand=1)

    rotate_image.save(path)

    image_width, image_height = rotate_image.size

    text_image = Image.new('RGB', (image_width, font_size + 10), color=(255, 255, 255))
    text_image_width, text_image_height = text_image.size

    background_image = Image.new('RGB', (image_width + 40, image_height + 60 + text_image_height),
                                 color=(255, 255, 255))

    text_draw_font = ImageFont.truetype(font_path, font_size, encoding='unic')
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text((0, 0), description, font=text_draw_font, fill=(0, 0, 0))

    background_image.paste(rotate_image, (20, 20))
    background_image.paste(text_image, (20, image_height + 40))
    path, filename = os.path.split(path)
    new_path = path.rsplit("/", 1)[0]
    background_image_path = str(new_path) + sub_dirs[2] + "/" + filename[:-3] + "png"

    background_image.save(background_image_path)

    return background_image_path


def picture_window(path, sub_dirs, window_size):
    def save_description(event):
        image_path = create_desc_picture(description.get(), path, sub_dirs, font_path, commands)
        check_image = CheckImage(window, image_path, window_size, font_path, description.get())
        window.wait_window(check_image.top)
        global redo
        print(redo)
        if redo:
            redo = False
        else:
            window.destroy()

    def turn_left(event):
        commands.append("turn_left")
        command_text_var.set("Rotations: " + str(commands))
        window.update_idletasks()
        print(commands)

    def turn_right(event):
        commands.append("turn_right")
        command_text_var.set("Rotations: " + str(commands))
        window.update_idletasks()
        print(commands)

    def stop(event):
        print("Don't save picture.")
        window.destroy()

    commands = []

    window = tk.Tk()
    window.title(path)
    window.geometry('{}x{}+{}+{}'.format(
        window_size,
        window_size,
        int((window.winfo_screenwidth() / 2) - (window_size / 2)),
        int((window.winfo_screenheight() / 2) - (window_size / 2))
    ))

    font_path = os.getcwd() + '/res/SourceSansPro-Regular.ttf'

    image = Image.open(path)
    image_width, image_height = image.size
    if image_height >= image_width:
        image_width = int(image_width / (image_height / window_size * 3 / 2))
        image_height = int(image_height / (image_height / window_size * 3 / 2))
    else:
        image_height = int(image_height / (image_width / window_size))
        image_width = int(image_width / (image_width / window_size))

    canvas = tk.Canvas(window, height=image_height, width=image_width)

    resize_image = image.resize((image_width, image_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(resize_image)
    canvas.create_image(image_width / 2, image_height / 2, image=photo)
    canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    how_to_text_1 = tk.Label(window, text="\'Left\' rotate left - \'Right\' rotate right", font=(font_path, 14))
    how_to_text_2 = tk.Label(window, text="Write the picture description in the grey textbox and press \'Return\', "
                                          "\'Escape\': Don't save picture, load next one", font=(font_path, 14))
    how_to_text_1.pack()
    how_to_text_2.pack()

    command_text_var = tk.StringVar()
    commands_text = tk.Label(window, textvariable=command_text_var, font=(font_path, 14))
    commands_text.pack()

    command_text_var.set("Rotations: None")

    description = tk.Entry(window, bg="grey80", font=(font_path, 18))
    description.bind('<Return>', save_description)
    description.bind('<Left>', turn_left)
    description.bind('<Right>', turn_right)
    description.bind('<Escape>', stop)

    description.pack(expand=True, fill=tk.BOTH)
    description.focus_set()

    window.update_idletasks()
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
        if path[-3:] == "jpg" or path[-3:] == "JPG" or path[-4:] == "jpeg":
            picture_path_list.append(path)
    return picture_path_list


def get_file_paths(path):
    return [os.path.join(path, fn) for fn in next(os.walk(path))[2]]


def main(argv):
    if len(argv) == 4:
        path = argv[0]
        window_size = int(argv[1])
        sensibility = int(argv[2])
        resize = int(argv[3])
        sub_dirs = ["/orig_photos", "/crop_photos", "/desc_photos"]
        if os.path.exists(path) and window_size > 0:
            create_sub_dirs(path, sub_dirs)
            picture_paths = sort_files(get_file_paths(path))
            for path in picture_paths:
                cropped_image_path = crop_picture(path, sensibility, sub_dirs, resize)
                description = picture_window(cropped_image_path, sub_dirs, window_size)
        else:
            print("Your path is not valid or your screen size integer is smaller than 0 or or or ...")
            exit(0)
    else:
        print("You must have exact 3 arguments:"
              "\n1. Path to your picture folder"
              "\n2. Window size for x and y as one"
              "\n3. Sensibility for background"
              "\n4. Value (Pixel) for smaller side of the picture"
              "\nExample: python3 main.py /path/to/your/picture/folder 800 10 1200")


if __name__ == "__main__":
    main(sys.argv[1:])
