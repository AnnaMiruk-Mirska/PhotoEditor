import ttkbootstrap as ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageGrab
from tkinter import colorchooser
from tkinter.messagebox import askyesno


root = ttk.Window(themename="cosmo")
root.title("PhotoEditor")
root.geometry("600x620")
root.resizable(1, 1)

Width = 750
Height = 650
rotation_angle =0
pen_size = 2
pen_color = "blue"



top_frame = ttk.Frame(root, width=600, height=20)
top_frame.pack(side="top", fill="x")

right_frame = ttk.Frame(root, width=20, height=700)
right_frame.pack(side="right", fill="y")


canvas = ttk.Canvas(root, width=Width, height=Height)
canvas.pack()

image_filters = ["None","Black and white", "Colorful", "Brightness"]
filter_combobox = ttk.Combobox(top_frame, values=image_filters, width=15)
filter_combobox.pack(padx=10, pady=5, side = "right")
filter_label = ttk.Label(top_frame, text="Select Filter:", background="white")
filter_label.pack(padx=10, pady=2, side = "right")




open_image_icon = ttk.PhotoImage(file ='add_image_icon.png').subsample(8, 8)


def open_image():
    global file_path
    file_path = filedialog.askopenfilename(title="Open Image File",
                                           filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if file_path:
        global image, photo_image
        image = Image.open(file_path)
        # new_width = int((Width / 2))
        # image = image.resize((new_width, Height), Image.LANCZOS)

        image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=image)


open_image_button = ttk.Button(top_frame, image=open_image_icon, bootstyle="light", command=open_image)
open_image_button.pack(pady=5, side ="left")

rotate_icon = ttk.PhotoImage(file = 'rotate_icon.png').subsample(8, 8)
def rotate():
    global image, photo_image, rotation_angle
    image = Image.open(file_path)
    rotated_image = image.rotate(rotation_angle + 90)
    rotation_angle += 90
    if rotation_angle % 360 == 0:
        rotation_angle = 0
        image = Image.open(file_path)
        rotated_image = image
    photo_image = ImageTk.PhotoImage(rotated_image)
    canvas.create_image(0, 0, anchor="nw", image=photo_image)


rotate_button = ttk.Button(right_frame, image=rotate_icon, bootstyle="light", command=rotate)
rotate_button.pack(pady=5)

def add_filter(filter):
    global image, photo_image
    image = Image.open(file_path).rotate(rotation_angle)
    if filter == "None":
        image = image
    elif filter == "Black and white":
        image = ImageOps.grayscale(image)
    elif filter == "Colorful":
        image = ImageEnhance.Contrast(image).enhance(1.7)
    elif filter == "Brightness":
        image = ImageEnhance.Brightness(image).enhance(1.7)
    photo_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=photo_image)

filter_combobox.bind("<<ComboboxSelected>>", lambda event: add_filter(filter_combobox.get()))


def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]


drawing_icon = ttk.PhotoImage(file ='drawing_icon.png').subsample(8, 8)
drawing_button = ttk.Button(right_frame, image=drawing_icon, bootstyle="light", command=change_color)
drawing_button.pack(pady=5)

def draw(event):
    global file_path
    if file_path:
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)
        canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="", width=pen_size, tags="oval")

canvas.bind("<B1-Motion>", draw)



def erase_lines():
    global file_path
    if file_path:
        canvas.delete("oval")

erase_icon = ttk.PhotoImage(file = 'erase_icon.png').subsample(8, 8)
erase_button = ttk.Button(right_frame, image=erase_icon, bootstyle="light", command = erase_lines)
erase_button.pack(pady=5)

def save_image():
    global file_path, rotation_angle
    if file_path:
        image = ImageGrab.grab(bbox=(canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(), canvas.winfo_rooty() + canvas.winfo_height()))
        # if rotation_angle % 360 != 0:
            #image = image.rotate(rotation_angle)
        filter = filter_combobox.get()
        if filter == "None":
            image = image
        elif filter == "Black and white":
            image = ImageOps.grayscale(image)
        elif filter == "Colorful":
            image = ImageEnhance.Contrast(image).enhance(1.7)
        elif filter == "Brightness":
            image = ImageEnhance.Brightness(image).enhance(1.7)
        file_path = file_path.split(".")[0] + "_new.jpg"
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        image.save(file_path)


save_icon = ttk.PhotoImage(file = 'save_icon.png').subsample(8,8)
save_button = ttk.Button(right_frame, image=save_icon, bootstyle="light", command=save_image)
save_button.pack(pady=5)

root.mainloop()

