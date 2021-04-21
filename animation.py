from PIL import Image
import os
import sys

def gen_frame(im):
    '''
    adapted from https://stackoverflow.com/questions/46850318/transparent-background-in-gif-using-python-imageio
    '''
    alpha = im.getchannel('A')
    # Convert the image into P mode but only use 255 colors in the palette out of 256
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
    # Set all pixel values below 128 to 255 , and the rest to 0
    mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
    # Paste the color of index 255 and use alpha as a mask
    im.paste(255, mask)
    # The transparency index is 255
    im.info['transparency'] = 255
    return im

def main():
    try:
        duration = int(sys.argv[1])
    except IndexError:
        duration = 400

    frames = [Image.open("frames/" + filename) for filename in os.listdir("frames/")]
    frames = [gen_frame(frame) for frame in frames]
    frames[0].save('anim.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True, duration=duration,
                   loop=0);

if __name__ == "__main__":
    main()
