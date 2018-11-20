from PIL import Image, ImageDraw, ImageFont
from PIL.TiffTags import TAGS
from io import StringIO
from configparser import ConfigParser
import numpy as np
import glob

class EngineerNumber:
    def __init__(self, number):
        self._number = number

    @property
    def value(self):
        return self._number

    @property
    def engineer_power(self):
        return (np.log10(self._number) // 3) * 3

    @property
    def prefix(self):
        assert -24 <= self.engineer_power <= 24, 'power out of range'
        prefixes = 'yzafpnµm kMGTPEZY'
        return prefixes[int((self.engineer_power + 24) // 3)]

    @property
    def reduced_value(self):
        return round(self._number / 10**self.engineer_power, 0)

    def __str__(self):
        return '{:5.1f} {}'.format(self.reduced_value, self.prefix)


class ScaleNumber(EngineerNumber):
    def __init__(self, number):
        self._real_number = number
        self._number = self.scale_bar_length()

    def scale_bar_length(self):
        l = np.log10(self._real_number)
        m = np.floor(l)
        b = 10**(l - m)

        if b < 2:
            return 10**m
        elif b < 5:
            return 2 * 10**m
        else:
            return 5 * 10**m

    @property
    def real_value(self):
        return self._real_number




class ScaleBar():

    def __init__(self, filename, text_font = "cambria.ttc"):


        self.img = Image.open(filename)
        self.original = Image.open(filename)
        self.x_size, self.y_size = self.image_size
        self.text_font = text_font


    
    @ property
    def config_data(self):
        config_data = self.original.tag[34682][0]
        parser = ConfigParser()
        file_handle = StringIO(config_data)

        parser.readfp(file_handle)
        return parser

    @property
    def pixel_width(self):
        pixel_width = float(self.config_data['Scan']['PixelWidth'])
        return pixel_width

        
    @property
    def data_bar_height(self):
        data_bar_height = float(self.config_data['PrivateFei']['DatabarHeight'])
        return data_bar_height


    @property
    def image_size(self):
        x_size, y_size = self.img.size
        return x_size, y_size


    def get_scale(self):

        desired_length = (self.x_size/3)*self.pixel_width

        s = ScaleNumber(desired_length)
        scale_bar_length = float(s.scale_bar_length())
        scale_bar_reduced = float(s.reduced_value)
        unit = s.prefix

        return (scale_bar_length, scale_bar_reduced, unit)

    def crop_data_bar(self):
        self.img = self.img.crop((0, 0, self.x_size, self.y_size - self.data_bar_height)).copy()
        self.x_size, self.y_size = self.image_size
        return self.img

    def save_image(self, output_filename):
        self.img.save(output_filename)

    def close_image(self):
        self.img.close()

    def insert_scalebar(self, position = 'bottomright'):

        (scale_bar_length, scale_bar_reduced, unit) = self.get_scale()
        scale_bar_box = self.draw_scalebar(scale_bar_length, scale_bar_reduced, unit)
        box_size_x = int(scale_bar_box.size[0])
        box_size_y = int(scale_bar_box.size[1])

        if position == 'topleft':
            self.img.paste(scale_bar_box, (0,0,box_size_x, box_size_y))
        elif position == 'topright':
            self.img.paste(scale_bar_box, (self.x_size - box_size_x, 0, self.x_size, box_size_y))
        elif position == 'bottomleft':
            self.img.paste(scale_bar_box, (0, self.y_size - box_size_y, box_size_x, self.y_size))
        elif position == 'bottomright':
            self.img.paste(scale_bar_box, (self.x_size - box_size_x, self.y_size - box_size_y, self.x_size, self.y_size))
        else:
            print('Position specifier not in use. Chose between topleft, topright, bottomleft or bottomright. Scalebar not inserted.')

    def draw_scalebar(self, scale_bar_length, scale_bar_reduced, unit):

        scale_bar_pixel = scale_bar_length/self.pixel_width
        font = ImageFont.truetype(self.text_font, 50)
        dummy_draw = ImageDraw.Draw(self.img)
        text_x, text_y = dummy_draw.textsize(text='{0:.0f} {1}m'.format(scale_bar_reduced, unit), font=font)

        if scale_bar_pixel > text_x:
            box_size_x = scale_bar_pixel + 10
        else:
            box_size_x = text_x + 10

        box_size_y = 1.4 * text_y

        scale_bar_box = Image.new(mode="RGB", size=(int(box_size_x), int(box_size_y)))
        draw_box = ImageDraw.Draw(scale_bar_box)
        draw_line = ImageDraw.Draw(scale_bar_box)
        draw_text = ImageDraw.Draw(scale_bar_box)

        draw_box.rectangle(xy=[(10, 0),(box_size_x, box_size_y)],
                           fill='black')

        draw_line.line(xy=[(box_size_x - scale_bar_pixel-5, 0.2 * text_y),
                           (box_size_x - 5, 0.2 * text_y)], 
                       width= 10,
                       fill='white')

        draw_text.text(xy= (box_size_x - (scale_bar_pixel - text_x)/2 - text_x, box_size_y - 1.1 * text_y), 
                    text='{0:.0f} {1}m'.format(scale_bar_reduced, unit), 
                    font=font)
        
        return scale_bar_box



if __name__ == '__main__':
  
    filename = input()
    scale_bar_dummy = ScaleBar(filename)
    scale_bar_dummy.crop_data_bar()
    scale_bar_dummy.insert_scalebar(position='topleft')
    output_filename = filename.replace('.tif', '.png')
    scale_bar_dummy.save_image(output_filename)

    scale_bar_dummy.close_image()
