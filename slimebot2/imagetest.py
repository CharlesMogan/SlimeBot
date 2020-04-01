import os
import urllib.parse
import urllib.request
from urllib.error import HTTPError
import random

from urllib.request import Request, urlopen
import shutil
#  rsbgv????
import cairosvg
import svglib
import cairo
from PIL import Image, ImageDraw, ImageFilter
from shutil import copyfileobj
from cairosvg import svg2png


def get_file_name(url: str):
    print(type(url))
    split = urllib.parse.urlsplit(url, "/")
    file_name = f"./images/{split.path.split('/')[-1]}"
    return file_name


# def get_unborked_url(url: str):
#     split = urllib.parse.urlsplit(url, "/")
#     return f"{split.netloc}{split.path}"


def slime_image(url: str):
    file_name = get_file_name(url)
    print(file_name)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(file_name, 'wb') as out_file:
        copyfileobj(response, out_file)
    os.system(f"gm mogrify -auto-orient {file_name}")
    im1 = Image.open(file_name)

    width, height = im1.size
    slime_svg_path = get_random_slime_image()
    os.system(f"inkscape -z -e ./images/result/slime.png -w {width} -h {height} {slime_svg_path}")
    if im1.format == "GIF":
        if im1.is_animated:
            result_file = "./images/result/result.gif"
            os.system(f"convert {file_name} -coalesce null: ./images/result/slime.png -gravity center -layers "
                      f"composite "
                      f"{result_file}")

    else:
        result_file = "./images/result/result.png"
        os.system(f"gm composite ./images/result/slime.png {file_name} {result_file}")
    os.remove(file_name)
    return result_file


def valid_image_url(url: str):
    try:
        print(f"{url}")
        split = urllib.parse.urlsplit(url, "/")
        if split.scheme != "https" and split.scheme != "http":
            return
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        meta_info = urlopen(req).info()
    except ValueError:  # for when it isn't a url at all
        print(f"{e}")
        return False
    except HTTPError as e:  # mostly concerned about 403 forbiden errors
        print(f"{e}")
        return False
    accepted_formats = ("image/png", "image/jpeg", "image/gif", "image/webp")
    if meta_info["content-type"] in accepted_formats:
        return True
    return False


def get_random_slime_image():  # https://stackoverflow.com/questions/701402/best-way-to-choose-a-random-file-from-a-directory
    n = 0
    random.seed();
    for root, dirs, files in os.walk('./images/src'):
        for name in files:
            n = n + 1
            if random.uniform(0, n) < 1:
                slime_image_path = os.path.join(root, name)
    return slime_image_path

# im2 = Image.open('./images/slime1.png')
# im = Image.alpha_composite(im1, im2)
# im.save("./images/result", "png")


# slime_image = Image.open("./images/slime1.svg")
# cairosvg.svg2png(
#     file_obj=open("./images/slime1.svg", "rb"), scale=1,
#     write_to="./images/slime1.png")
