# main

import tkinter as tk
import json
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from time import time
from colorama import Fore
from functions import *

TITLE = 'Imagenation'
VER = 'a1.0'
WINDOW_TITLE = f'{TITLE} {VER}'

def load():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def reset():
    data = {'first-launch': time(), 'last-launch': time(), 'audit': {}}
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

def open_image():

    image_path = filedialog.askopenfilename(
        filetypes=[("JPEG file", "*.jpg"), ("PNG file", "*.png"), ("GIF file", "*.gif")]
    )

    place_image(image_path, 320, 180, x=200, y=100)

try:
    load()
except FileNotFoundError:
    print(f'{Fore.RED}data file not found, reset to default')
    messagebox.showinfo(WINDOW_TITLE, '''Welcome to the Imagenation program. This program is created for photo editing and creating custom filters. It is currently in the alpha stage and has limited functionality.

For more information on updates:
https://github.com/hexique/Imagenation''')
    reset()
except Exception as e:
    messagebox.showerror(WINDOW_TITLE, f'Error occured while reading data file:\n{e}')
    reset()

root = tk.Tk()
root.geometry('600x600')
root.title(WINDOW_TITLE)
root.resizable(False, False)
root.iconbitmap('icon.ico')

filters = ['in development...']
filter_variable = tk.StringVar(value = '')

pack_image('title.png', 500, 100)

ttk.Button(root, text='Open image', command=open_image).place(x=10, y=100)
ttk.Combobox(root, values=filters, textvariable=filter_variable).place(x=10, y=130)

root.mainloop()