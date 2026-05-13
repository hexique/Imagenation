# cmd
from PIL import Image
# from rich import print
from random import shuffle, randint
from colorama import Fore, Back
import time
from math import *
from numpy import arcsin

# base

def load(path):
    img = Image.open(path)
    try:
        pixels = list(img.getdata())
    except:
        pass
    width, height = img.size
    
    pixels_2d = [pixels[i*width:(i+1)*width] for i in range(height)]
    return pixels_2d

def save(pixels_2d, path):
    height = len(pixels_2d)
    width = len(pixels_2d[0])
    flat_pixels = [tuple(pixel) for row in pixels_2d for pixel in row]
    img = Image.new('RGB', (width, height))
    img.putdata(flat_pixels)
    img.save(path)

def rgb_to_hsv(rgb: list) -> list:
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val
    
    if diff == 0:
        h = 0
    elif max_val == r:
        h = (60 * ((g - b) / diff)) % 360
    elif max_val == g:
        h = 60 * ((b - r) / diff) + 120
    else:  # max_val == b
        h = 60 * ((r - g) / diff) + 240

    if max_val == 0:
        s = 0
    else:
        s = (diff / max_val) * 100

    v = max_val * 100
    
    return [round(h, 2), round(s, 2), round(v, 2)]


def hsv_to_rgb(hsv: list) -> list:
    h, s, v = hsv[0], hsv[1] / 100.0, hsv[2] / 100.0
    
    if s == 0:
        rgb_val = int(v * 255)
        return [rgb_val, rgb_val, rgb_val]
    
    h = h % 360
    h_i = int(h / 60) % 6
    f = (h / 60) - h_i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    
    if h_i == 0:
        r, g, b = v, t, p
    elif h_i == 1:
        r, g, b = q, v, p
    elif h_i == 2:
        r, g, b = p, v, t
    elif h_i == 3:
        r, g, b = p, q, v
    elif h_i == 4:
        r, g, b = t, p, v
    else:  # h_i == 5
        r, g, b = v, p, q
    
    return [int(r * 255), int(g * 255), int(b * 255)]

# effects

SCALE = 100
PREVIEW = False

def grayscale(pixels):
    result = []

    for row_i, row in enumerate(pixels):
        result.append([])
        for col_i, pixel in enumerate(row):
            gray = sum(pixel) // 3
            new_pixel = [gray, gray, gray]
            result[row_i].append(new_pixel)
            
        #     if PREVIEW:
        #         if col_i % SCALE == 0 and row_i % SCALE == 0:
        #             print(f'[rgb({gray},{gray},{gray})]██[/]', end='')
        # if PREVIEW:
        #     if row_i % SCALE == 0:
        #         print()

    return result

def mult(pixels):
    result = []

    for row_i, row in enumerate(pixels):
        result.append([])
        for col_i, pixel in enumerate(row):
            gray = pixel[0] * pixel[1] * pixel[2]
            if gray > 255: gray = 255
            new_pixel = [gray, gray, gray]
            result[row_i].append(new_pixel)
            
    return result

def sumpixels(pixels):
    result = []

    for row_i, row in enumerate(pixels):
        result.append([])
        for col_i, pixel in enumerate(row):
            gray = pixel[0] + pixel[1] + pixel[2]
            if gray > 255: gray = 255
            new_pixel = [gray, gray, gray]
            result[row_i].append(new_pixel)
            
    return result

def shuffle_rows(pixels):
    shuffle(pixels)
        
    return pixels

def shuffle_pixels_in_rows(pixels):

    for row_i, row in enumerate(pixels):
        shuffle(row)
        
    return pixels


def shuffle_pixels(pixels):

    WIDTH = len(pixels[0])

    unpacked = []

    for row_i, row in enumerate(pixels):
        for col_i, pixel in enumerate(row):
            unpacked.append(pixel)

    shuffle(unpacked)

    result = [[]]
    for pixel in unpacked:
        result[-1].append(pixel)
        if len(result[-1]) >= WIDTH:
            result.append([])
        
    return result

def sort_pixels(pixels):

    WIDTH = len(pixels[0])

    unpacked = []

    for row_i, row in enumerate(pixels):
        for col_i, pixel in enumerate(row):
            unpacked.append(pixel)

    unpacked = sorted(unpacked, key=lambda x: sum(x), reverse=True) 

    result = [[]]
    for pixel in unpacked:
        result[-1].append(pixel)
        if len(result[-1]) >= WIDTH:
            result.append([])
        
    return result

start = time.time()

def shift(pixels):

    WIDTH = len(pixels[0]) - 256

    unpacked = []

    for row_i, row in enumerate(pixels):
        for col_i, pixel in enumerate(row):
            unpacked.append(pixel)

    result = [[]]
    for pixel in unpacked:
        result[-1].append(pixel)
        if len(result[-1]) >= WIDTH:
            result.append([])

    if result[-1] != WIDTH:
        result = result[:-1]
        
    return result

def brightness(pixels):

    result = []
    COEFFICIENT = 0.9

    for row_i, row in enumerate(pixels):
        result.append([])
        for col_i, pixel in enumerate(row):
            new_pixel = [round(pixel[0] * COEFFICIENT), round(pixel[1] * COEFFICIENT), round(pixel[2] * COEFFICIENT)]
            result[row_i].append(new_pixel)

    return result

def contrast(pixels):

    result = []
    COEFFICIENT = 255

    for row_i, row in enumerate(pixels):
        result.append([])
        for col_i, pixel in enumerate(row):
            new_pixel = [round(round(pixel[i] / COEFFICIENT) * COEFFICIENT) for i in range(3)]
            result[row_i].append(new_pixel)

    return result

def generate_pallette():
    pallette = load('dme pallette 2.png')

    loaded = []
    for row in pallette:
        loaded.append(row)

    unpacked = []

    for row in pallette:
        for pixel in row:
            unpacked.append(list(pixel))

    print(unpacked)

def allowed(pixels):

    # paint
    # ALLOWED = [[0, 0, 0], [255, 255, 255], [127, 127, 127], [195, 195, 195], [185, 122, 87], [237, 28, 36], [255, 174, 201], [255, 201, 14], [255, 242, 0], [239, 228, 176], [34, 177, 76], [181, 230, 29], [0, 162, 232], [153, 217, 234], [63, 72, 204], [112, 146, 190], [163, 73, 164], [200, 191, 231]]
    
    # drawme
    # ALLOWED = [# [255, 255, 255], 
    #           [195, 195, 195], [88, 88, 88], [0, 0, 0], [136, 0, 27], [236, 28, 36], [255, 127, 39], [255, 202, 24], [253, 236, 166], [255, 242, 0], [196, 255, 14], [14, 209, 69], [140, 255, 251], [0, 168, 243], [63, 72, 204], [184, 61, 186], [255, 174, 200], [185, 122, 86]]
    
    # paintnet
    # ALLOWED = [[255, 255, 255], [195, 195, 195], [88, 88, 88], [0, 0, 0], [136, 0, 27], [236, 28, 36], [255, 127, 39], [255, 202, 24], [253, 236, 166], [255, 242, 0], [196, 255, 14], [14, 209, 69], [140, 255, 251], [0, 168, 243], [63, 72, 204], [184, 61, 186], [255, 174, 200], [185, 122, 86]]

    # owop
    # ALLOWED = [[57, 205, 121], [30, 143, 115], [43, 87, 88], [22, 38, 53], [30, 144, 85], [66, 204, 57], [174, 254, 93], [251, 212, 57], [229, 112, 68], [172, 57, 64], [104, 37, 70], [57, 17, 54], [43, 11, 32], [74, 25, 44], [154, 74, 75], [222, 142, 117], [255, 210, 168], [156, 196, 196], [96, 126, 137], [68, 77, 92], [36, 36, 46], [85, 77, 75], [139, 127, 115], [255, 255, 255], [255, 151, 191], [216, 86, 184], [151, 44, 158], [81, 29, 112], [39, 23, 62], [15, 19, 28], [33, 27, 73], [40, 52, 134], [51, 99, 175], [82, 164, 220], [144, 241, 248]][:15]

    # 8
    # ALLOWED = [[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255], [255, 255, 255]]

    # 16
    ALLOWED = [[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255], [255, 255, 255], [128, 0, 0], [0, 128, 0], [0, 0, 128], [128, 128, 0], [0, 128, 128], [128, 0, 128], [128, 128, 128]]

    result = []
    for row_i, row in enumerate(pixels):
        result.append([])

        for col_i, pixel in enumerate(row):
            min = 255 * 3 + 1
            closest = ALLOWED[0]

            for target in ALLOWED:
                score = 0

                for channel in range(3):
                    score += abs(pixel[channel] - target[channel])

                if score < min:
                    min = score
                    closest = target

            new_pixel = closest
            result[row_i].append(new_pixel)

    return result

def noise(pixels):

    COEFFICIENT = 255
    MONO = True

    result = []
    for row_i, row in enumerate(pixels):
        result.append([])

        for col_i, pixel in enumerate(row):
            new_pixel = list(pixel)
            
            if not MONO:
                for channel in range(3):
                    new_pixel[channel] += randint(-COEFFICIENT, COEFFICIENT)
            else:
                shift = randint(-COEFFICIENT, COEFFICIENT)

                for channel in range(3):
                    new_pixel[channel] += shift

            result[row_i].append(new_pixel)

    return result

def divide(pixels):

    RANGE = 20

    result = []
    for row_i, row in enumerate(pixels):
        result.append([])

        for col_i, pixel in enumerate(row):
            new_pixel = list(pixel)
            
            for channel in range(3):
                
                px = pixel[channel]

                for i in range(2, RANGE+1):
                    if px % i == 0:
                        px //= i
                        break



                new_pixel[channel] = px

            result[row_i].append(new_pixel)

    return result

def allowed_channels(pixels):

    ALLOWED = [i for i in range(0, 257, 256//1)]

    # ALLOWED = []

    # for i in range(2, 256):
    #     isPrime = True
    #     for ii in range(2, floor(i ** 0.5) + 2):
    #         if i % ii == 0:
    #             isPrime = False
    #             break
    #     if isPrime and i not in ALLOWED:
    #         ALLOWED.append(i)

    # ALLOWED = [1, 2]

    # while ALLOWED[-1] < 256:
    #     ALLOWED.append(sum(ALLOWED[-3:]))

    # ALLOWED = [i*i for i in range(16)]

    # ALLOWED = list(range(0, 128))

    target = ALLOWED[0]
    print(ALLOWED)

    ELSE_RESET = False

    result = []
    for row_i, row in enumerate(pixels):
        result.append([])

        for col_i, pixel in enumerate(row):
            new_pixel = list(pixel)
            
            for channel in range(3):
                
                px = pixel[channel]

                if ELSE_RESET:
                    if px not in ALLOWED:
                        px = 0
                else:
                    min = 256
                    
                    for allowed in ALLOWED:
                        DIFFERENCE = abs(allowed - px)
                        if DIFFERENCE < min:
                            min = DIFFERENCE
                            target = allowed

                    px = target
                new_pixel[channel] = px

            result[row_i].append(new_pixel)

    return result

def function(pixels):

    result = []
    for row_i, row in enumerate(pixels):
        result.append([])

        for col_i, pixel in enumerate(row):
            new_pixel = list(pixel)
            
            for channel in range(3):

                x = pixel[channel]
                try:
                    new_pixel[channel] = round(
                        # (2.89 * ((x * sin(100*x + 30)) / (100 * x + 30) + (x * sin(100 * x - 30)) + sin(100000 * x ** 10) / 100000 * x ** 9) / sin(sin(2.89 * x))) * 255 # function
                        abs(tan(x))**tan(sin(x*x))
                    )
                except ZeroDivisionError:
                    new_pixel[channel] = 255
                except:
                    new_pixel[channel] = 255

                if new_pixel[channel] > 255:
                    new_pixel[channel] = 255
                elif new_pixel[channel] < 0:
                    new_pixel[channel] = 0
        

            result[row_i].append(new_pixel)

    return result

def replace_hsl(pixels):

    result = []
    for row_i, row in enumerate(pixels):
        result.append([])

        for col_i, pixel in enumerate(row):
            pixel = rgb_to_hsv(list(pixel))
            new_pixel = pixel

            new_pixel[0] = pixel[0] * 361 % 360 # hue (0 - 360)
            new_pixel[1] = pixel[1] * 101 % 100 # saturation (0 - 100)
            new_pixel[2] = pixel[2] * 101 % 100 # value (0 - 100)
            
            result[row_i].append(hsv_to_rgb(list(new_pixel)))

    return result

if __name__ == "__main__":
    start = time.time()

    print(f'{Fore.BLACK}[{time.strftime("%H:%M:%S")}] {Fore.WHITE}loading file...')
    img_list = load('example.png')

    print(f'{Fore.BLACK}[{time.strftime("%H:%M:%S")}] {Fore.WHITE}successfully loaded')
    print(f'{Fore.BLACK}[{time.strftime("%H:%M:%S")}] {Fore.WHITE}applying filters to the file...')

    gray_img = replace_hsl(img_list) # main operation
    PATH =    'hsv--d.png'

    print(f'{Fore.BLACK}[{time.strftime("%H:%M:%S")}] {Fore.WHITE}saving to {PATH}...')
    save(gray_img, PATH)
    print(f'{Fore.GREEN}[{time.strftime("%H:%M:%S")}] done for {round(time.time() - start, 2)}s')
    Image.open(PATH).show()