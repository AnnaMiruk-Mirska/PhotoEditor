import ttkbootstrap as ttk
from tkinter import filedialog
from PIL import Image, ImageTk


root = ttk.Window(themename="cosmo")
root.title("Image Editor")
root.geometry("800x700")
root.resizable(1, 1)

Width = 750
Height = 560



top_frame = ttk.Frame(root, width=600, height=200)
top_frame.pack(side="top", fill="x")

canvas = ttk.Canvas(root, width=Width, height=Height)
canvas.pack()


filter_label = ttk.Label(top_frame, text="Select Filter:", background="white")
filter_label.pack(padx=0, pady=2, side = "left")


image_filters = ["1", "2"]


filter_combobox = ttk.Combobox(top_frame, values=image_filters, width=15)
filter_combobox.pack(padx=10, pady=5, side = "left")


open_image_icon = ttk.PhotoImage(file ='icon.png').subsample(12, 12)


def open_image():
    global file_path
    file_path = filedialog.askopenfilename(title="Open Image File",
                                           filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if file_path:
        global image, photo_image
        image = Image.open(file_path)
        new_width = int((Width / 2))
        image = image.resize((new_width, Height), Image.LANCZOS)

        image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=image)


image_button = ttk.Button(top_frame, image=open_image_icon, bootstyle="light", command=open_image)
image_button.pack(pady=5, side = "left")




root.mainloop()

