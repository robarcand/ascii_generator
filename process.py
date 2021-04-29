import glob
import os
import shutil
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont


class Digitizer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.img = Image.open(filepath).convert('RGBA')
    
    def make_upside_down(self):
        self.img = self.img.rotate(180)
    
    def make_thumbnail_size(self):
        size = (200, 200)
        self.img.thumbnail(size)

    def make_grayscale(self):
        self.img = ImageOps.grayscale(self.img)
        self.img = self.img.convert('RGBA')

    def adjust_contrast(self, amount):
        enhancer = ImageEnhance.Contrast(self.img)
        self.img = enhancer.enhance(amount)

    def make_square(self, size=200):
        (w, h) = self.img.size

        if w > h:
            print('This is a landscape image')
            x = (w - h) * 0.5
            y = 0
            box = (x, y, h + x, h + y)
        else:
            print('This is a portrait image')
            x = 0
            y = (h - w) * 0.5
            box = (x, y, x + w, y + w)

        self.img = self.img.resize((size, size), box=box)
    
    def add_watermark(self):
        fnt = ImageFont.truetype("ibm-plex-mono.ttf", 24)
        drawer = ImageDraw.Draw(self.img)

        drawer.multiline_text((32, 32), 'my watermark', font=fnt, fill=(255, 0, 0, 100))

    def convert_to_ascii(self):
        font_size = 10
        letters = [' ', '.', 'i', 'u', 'r', 'e', 'p', 'S', 'H', 'W']

        (w, h) = self.img.size

        new_width = int(w / font_size)
        new_height = int(h / font_size)

        sample_size = (new_width, new_height)
        final_size = (new_width * font_size, new_height * font_size)

        self.make_grayscale()
        self.adjust_contrast(3.0)
        self.img = self.img.resize(sample_size)

        ascii_img = Image.new('RGBA', final_size, color="#000000")

        fnt = ImageFont.truetype("ibm-plex-mono.ttf", font_size)
        drawer = ImageDraw.Draw(ascii_img)

        for x in range(new_width):
            for y in range(new_height):

                (r, g, b, a) = self.img.getpixel((x, y))

                brightness = r / 256
                letter_num = int(len(letters) * brightness)

                letter = letters[letter_num]

                position = (x * font_size, y * font_size)
                drawer.text(position, letter, font=fnt, fill=(255, 255, 255, 255))

        self.img = ascii_img
    
    def save(self, output_filepath):
        print("This has saved!")

        if self.filepath.endswith('.jpg'):
            self.img = self.img.convert('RGB')

        self.img.save(output_filepath)

if __name__ == '__main__':
    inputs = glob.glob('inputs/*')

    os.makedirs('outputs', exist_ok=True)

    for filepath in inputs:
        output = filepath.replace('inputs', 'outputs')
        image = Digitizer(filepath)
        # image.make_upside_down()
        # image.make_thumbnail_size()
        # image.make_grayscale()
        # image.adjust_contrast(3.0)
        # image.make_square()
        # image.add_watermark()
        image.convert_to_ascii()
        image.save(output)