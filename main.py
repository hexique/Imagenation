# main

import tkinter as tk
import json
import imagenation
import time
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from colorama import Fore

TITLE = 'Imagenation'
VER = 'a1.0.1'
WINDOW_TITLE = f'{TITLE} {VER}'

path = ''

def load():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def reset():
    data = {'first-launch': time.time(), 'last-launch': time.time(), 'audit': {}}
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

def pack_image(name, w, h):
    canvas = tk.Canvas(
        root,
        width=w,
        height=h
    )

    img = Image.open(f'img/{name}')
    photo = ImageTk.PhotoImage(img)

    canvas.create_image(
        10,
        10,
        image=photo,
        anchor='nw'
    )

    canvas.image = photo

    canvas.pack()

def place_image(path, w, h, **kwargs):
    canvas = tk.Canvas(
        root,
        width=w,
        height=h
    )

    img = Image.open(path)
    photo = ImageTk.PhotoImage(img)

    canvas.create_image(
        10,
        10,
        image=photo,
        anchor='nw'
    )
    
    canvas.image = photo

    canvas.place(kwargs)

def display_resized_image(image_path):
    img = Image.open(image_path)
    res = img.resize((320, 180))
    RESIZED_PATH = 'img\cache\\resized.png'
    res.save(RESIZED_PATH)

    place_image(RESIZED_PATH, 320, 180, x=200, y=100)

def open_image():
    global path

    image_path = filedialog.askopenfilename(
        filetypes=[("JPEG file", "*.jpg"), ("PNG file", "*.png"), ("GIF file", "*.gif")]
    )

    display_resized_image(image_path)

    path = image_path

def apply_filter(image_path):
    start = time.time()

    img = imagenation.load(image_path)

    print(f'{Fore.BLACK}[{time.strftime("%H:%M:%S")}] {Fore.WHITE}successfully loaded')
    print(f'{Fore.BLACK}[{time.strftime("%H:%M:%S")}] {Fore.WHITE}applying filters to the file...')

    gray_img = imagenation.grayscale(img) # main operation
    PATH =    'img\cache\\result.png'

    print(f'{Fore.BLACK}[{time.strftime("%H:%M:%S")}] {Fore.WHITE}saving to {PATH}...')
    imagenation.save(gray_img, 'img\cache\\result.png')
    print(f'{Fore.GREEN}[{time.strftime("%H:%M:%S")}] done for {round(time.time() - start, 2)}s')

    display_resized_image(PATH)




try:
    load()
except FileNotFoundError:
    print(f'{Fore.RED}data file not found, reset to default')
    messagebox.showinfo(WINDOW_TITLE, '''Welcome to the Imagenation program. This program is created for photo editing and creating custom filters. It is currently in the alpha stage and has limited functionality.

For more information on updates:
https://github.com/hexique/Imagenation''')
    reset()
except Exception as e:
    messagebox.showerror(WINDOW_TITLE, f'Error occurred while reading data file:\n{e}')
    reset()

root = tk.Tk()
root.geometry('600x600')
root.title(WINDOW_TITLE)
root.resizable(False, False)
root.iconbitmap('icon.ico')

filters = ['', 'Grayscale']
filter_variable = tk.StringVar(value = '')

pack_image(f'title-{VER[0]}.png', 500, 100)

ttk.Button(root, text='Open image', command=open_image).place(x=10, y=100)
ttk.Combobox(root, values=filters, textvariable=filter_variable).place(x=10, y=130)
ttk.Button(root, text='Apply', command=lambda : apply_filter(path)).place(x=10, y=160)

root.mainloop()