import os
import urllib.parse
import urllib.request
from urllib.error import HTTPError
import random

from urllib.request import Request, urlopen
from PIL import Image
from shutil import copyfileobj


def get_file_name(url: str):
    print(type(url))
    split = urllib.parse.urlsplit(url, "/")
    file_name = f"./images/{split.path.split('/')[-1]}"
    return file_name


def slime_image(url: str):
    file_name = get_file_name(url)
    print(file_name)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(file_name, 'wb') as out_file:
        copyfileobj(response, out_file)
    os.system(f"gm mogrify -auto-orient {file_name}")  # this reorients images based on meta info
    im1 = Image.open(file_name)

    width, height = im1.size
    slime_svg_path = get_random_slime_image()
    #os.system(f"inkscape -z -e ./images/results/slime.png -w {width} -h {height} {slime_svg_path}")
    os.system(f"inkscape -z --export-filename=./images/results/slime.png -w {width} -h {height} {slime_svg_path}")

    if im1.format == "GIF":
        if im1.is_animated:
            result_file = "images/results/results.gif"
            os.system(f"convert {file_name} -coalesce null: ./images/results/slime.png -gravity center -layers "
                      f"composite "
                      f"{result_file}")

    else:
        result_file = "images/results/results.png"
        os.system(f"gm composite ./images/results/slime.png {file_name} {result_file}")
        compressed_file = "images/results/results.webp"
        os.system(f"cwebp -lossless {result_file} -o {compressed_file}") # smaller lossless files
        return compressed_file

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
    for root, dirs, files in os.walk('./images/slimes'):
        for name in files:
            n = n + 1
            if random.uniform(0, n) < 1:
                slime_image_path = os.path.join(root, name)
    return slime_image_path
