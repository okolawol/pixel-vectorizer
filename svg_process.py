import sys
import cairosvg
import cv2
import numpy as np
import os

from pixel_denoise import kMeansImage
from step_filter import step_filter

#INPUT IMAGE SHOULD BE SQUARE
#PREFERABLY SIMPLE
#INCREASE POSSIBLE COLORS IF NECESSARY

def main():
    input = sys.argv[1]
    pngs = []
    try:
        possible_colors = int(sys.argv[2])
        output_size = int(sys.argv[3])
    except IndexError:
        possible_colors = 5
        output_size = 64

    scale = 1
    parts = os.path.split(input)
    filename = parts[len(parts) - 1]
    filename = filename.split('.')[0]
    if not os.path.exists("temp/"):
        os.makedirs("temp/")
    out = os.path.join('temp/', filename + '.png');
    pngs.append(out)

    cairosvg.svg2png(url=input, write_to=out, scale=scale)

    # print(pngs)

    png = cv2.imread(pngs[0],cv2.IMREAD_UNCHANGED)

    height, width = png.shape[:2]
    new_w, new_h = (output_size,int((height / width) * output_size))

    downscaled = cv2.resize(png, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    downscaled_filtered = step_filter(downscaled);
    #The custom filter might be enough we'll see.
    #denoised_pixels = kMeansImage(downscaled_filtered, possible_colors)
    pixel_image = cv2.resize(downscaled_filtered, (width, height), interpolation=cv2.INTER_NEAREST)

    directory = "frames/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    max = -1
    for filename in os.listdir(directory):
        num = int("".join(filter(lambda x: x.isdigit(), filename)))
        if num > max:
            max = num

    os.chdir(directory)
    cv2.imwrite(str(max + 1) + ".png", pixel_image)
    os.chdir("..")

    # cv2.imwrite("outputs/pixel_art.png",pixel_image)
    # cv2.imwrite("outputs/downscaled.png",downscaled)
    # cv2.imwrite("outputs/downscaled_filtered.png",downscaled_filtered)

if __name__ == "__main__":
    main()
