import sys
import cairosvg
import cv2
import numpy as np

from pixel_denoise import kMeansImage
from step_filter import step_filter

#INPUT IMAGE SHOULD BE SQUARE
#PREFERABLY SIMPLE
#INCREASE POSSIBLE COLORS IF NECESSARY

def main():
    input = sys.argv[1]
    pngs = []
    possible_colors = 5
    output_size = 64

 
    scale = 1
    parts = input.split('/')
    filename = parts[len(parts) - 1]
    filename = filename.split('.')[0]
    out = 'temp/' + filename + '.png';
    pngs.append(out)

    cairosvg.svg2png(url=input, write_to=out, scale=scale)

    print(pngs)

    png = cv2.imread(pngs[0],cv2.IMREAD_UNCHANGED)

    height, width = png.shape[:2]
    new_w, new_h = (output_size,int((height / width) * output_size))

    downscaled = cv2.resize(png, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    downscaled_filtered = step_filter(downscaled);
    #The custom filter might be enough we'll see.
    #denoised_pixels = kMeansImage(downscaled_filtered, possible_colors)
    pixel_image = cv2.resize(downscaled_filtered, (width, height), interpolation=cv2.INTER_NEAREST)


    cv2.imwrite("pixel_art.png",pixel_image)
    cv2.imwrite("downscaled.png",downscaled)
    cv2.imwrite("downscaled_filtered.png",downscaled_filtered)

if __name__ == "__main__":
    main()