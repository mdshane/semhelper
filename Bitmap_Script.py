import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from PIL import Image, ImageDraw, ImageOps


def dose(pitch_x, pitch_y, passes, current, dwell_time):
    dose = (dwell_time * passes * current)/(pitch_x * pitch_y)
    # nC/µm^2
    return dose

class SEMBitmapCreator():

    def __init__(self, total_width_pixel: int, total_height_pixel: int, overlap_pixel: int, gap_pixel: int, line_width_pixel: int):
        self.total_width_pixel = total_width_pixel
        self.total_height_pixel = total_height_pixel
        self.overlap_pixel = overlap_pixel
        self.gap_pixel = gap_pixel
        self.line_width_pixel = line_width_pixel




    def create_EBL_meander(self) -> Image:
        image_middle = Image.new(mode='RGB', size = (self.total_width_pixel, self.total_height_pixel))

        draw = ImageDraw.Draw(image_middle)
        # write overlap
        draw.rectangle([0, 0, self.total_width_pixel, self.overlap_pixel], fill='white')
        draw.rectangle([0, self.total_height_pixel - self.overlap_pixel, self.total_width_pixel, self.total_height_pixel], fill='white')

        #write horizontal lines
        y = self.overlap_pixel + self.gap_pixel
        while y < self.total_height_pixel - self.overlap_pixel:
            draw.rectangle([0, y, self.total_width_pixel, y + self.line_width_pixel], fill='white')
            y += self.line_width_pixel + self.gap_pixel

        del draw

        image_left = image_middle.copy()

        # left side
        draw = ImageDraw.Draw(image_left)
        #write connection
        y = self.overlap_pixel + self.gap_pixel
        while y < self.total_height_pixel - self.overlap_pixel:
            draw.rectangle([0, y, self.line_width_pixel, y + self.gap_pixel + self.line_width_pixel], fill='white')
            y += 2 * (self.line_width_pixel + self.gap_pixel)

        del draw

        image_right = image_middle.copy()

        # left side
        draw = ImageDraw.Draw(image_right)
        #write connection
        y = self.overlap_pixel
        while y < self.total_height_pixel - self.overlap_pixel:
            draw.rectangle([self.total_width_pixel - self.line_width_pixel, y, self.total_width_pixel, y + self.gap_pixel + self.line_width_pixel], fill='white')
            y += 2 * (self.line_width_pixel + self.gap_pixel)

        del draw

        return image_left, image_middle, image_right



    def create_EBL_interdigitating_electrodes(h_pixel, b_pixel, pitch, bond_patch_height, w_um, s_um, overlap_offset, filename, file_num):

        def rescale(value):
            return value/pitch

        # Creating the image
        image = Image.new(mode = 'RGB', size = (int(b_pixel), int(h_pixel)), color ='black')
        draw = ImageDraw.Draw(image)

        # Creating the bond patches
        draw.rectangle([rescale(0),rescale(0),
                        b_pixel,rescale(bond_patch_height)], fill='white')
        draw.rectangle([rescale(0),h_pixel - rescale(bond_patch_height),
                        b_pixel,h_pixel], fill='white')

        num_electrodes = (b_pixel-rescale(overlap_offset))/rescale(w_um+s_um)

        for i in range(int(num_electrodes/2+0.5)):
            # upper electrodes
            x_0_upper = rescale(overlap_offset+i*2*(w_um+s_um))
            y_0_upper = rescale(bond_patch_height)
            x_1_upper = x_0_upper + rescale(w_um)
            y_1_upper = y_0_upper + h_pixel-rescale(2*bond_patch_height)-rescale(s_um)
            draw.rectangle([x_0_upper, y_0_upper, x_1_upper, y_1_upper], fill='white')
        
        for i in range(int(num_electrodes/2+0.5)):
            # lower electrodes
            x_0_lower = rescale(overlap_offset+i*2*(w_um+s_um)+(w_um+s_um))
            y_0_lower = rescale(bond_patch_height + s_um)
            x_1_lower = x_0_lower + rescale(w_um)
            y_1_lower = y_0_lower + h_pixel-rescale(bond_patch_height)
            draw.rectangle([x_0_lower, y_0_lower, x_1_lower, y_1_lower], fill='white')

        del draw

        return 
        
    
    #output_filename = filename + '_p' + str(int(pitch*1000)) + '_h' + str(int(h_pixel*pitch)) + '_b' + str(int(b_pixel*pitch)) + '_w' + str(w_um) + '_s' + str(s_um) + '_0' + str(file_num) + '.bmp'
    #image.save(output_filename, "BMP")
    #inverted_image.save('Inverted-' + output_filename, 'BMP')
"""
datasizes = [20, 20, 20, 30, 30, 30, 40, 40, 40] # Mb
pitches = [0.030, 0.060, 0.100, 0.030, 0.060, 0.100, 0.030, 0.060, 0.100] # nm
df = pd.DataFrame({'datasize': datasizes, 'pitch': pitches})
df['pixel'] = df['datasize']*1024*1024/3
df['h_um'] = [240, 540, 1040, 240, 740, 1040, 140, 540, 1040]
df['h_pixel'] = np.floor(df['h_um']/df['pitch'])
df['b_pixel'] = np.floor(df['pixel']/df['h_pixel'])
df['b_um'] = df['b_pixel']*df['pitch']

# Calculating the capacitance
df['w_um'] = 3
df['s_um'] = 3
df['p_um'] = 100
df['num_electrodes'] = [20, None, None, 31, None, None, None, None, None]
df['q_um'] = df['w_um']*df['num_electrodes'] + df['s_um']*(df['num_electrodes']-1)

for i in [1]:
    df['w_um'] = i
    for j in [1,2]:
        df['s_um'] = j
        for i in range(0,len(df)):
            h_pixel = df['h_pixel'][i]
            b_pixel = df['b_pixel'][i]
            pitch = df['pitch'][i] #um
            bond_patch_height = 20 #um
            w_um = df['w_um'][i]
            s_um = df['s_um'][j]
            overlap_offset = 3 #um
            filename = 'Bitmap-Files//IDE_Design'
            file_num = 1
            create_EBL_interdigitating_electrodes(h_pixel, b_pixel, pitch, bond_patch_height, w_um, s_um, overlap_offset, filename, file_num)
"""

class NanometerPixelConverter:
    def __init__(self, pitch_nm: float):
        self._pitch_nm = pitch_nm

    def to_pixel(self, value_nm: float) -> int:
        return int(value_nm / self._pitch_nm)

    def to_nm(self, value_pixel: int) -> float:
        return value_pixel * self._pitch_nm
        

if __name__ == '__main__':
    import os

    width_nm = 24000
    height_nm = 240000
    pitch_nm = 30

    converter = NanometerPixelConverter(pitch_nm = pitch_nm)

    params = {  'total_width_pixel': converter.to_pixel(width_nm), 
                'total_height_pixel': converter.to_pixel(height_nm), 
                'overlap_pixel': converter.to_pixel(10000), 
                'gap_pixel': converter.to_pixel(3000), 
                'line_width_pixel': converter.to_pixel(3000)
            }


    creator = SEMBitmapCreator(**params)
    imageL, imageC, imageR = creator.create_EBL_meander()

    if not os.path.exists(r'.\meander'):
        os.makedirs(r'.\meander')

    imageL.save(r'meander\left_twp_{total_width_pixel}_thp_{total_height_pixel}_ovp_{overlap_pixel}_gp_{gap_pixel}_lwp_{line_width_pixel}.bmp'.format(**params), 'BMP')
    imageC.save(r'meander\center_twp_{total_width_pixel}_thp_{total_height_pixel}_ovp_{overlap_pixel}_gp_{gap_pixel}_lwp_{line_width_pixel}.bmp'.format(**params), 'BMP')
    imageR.save(r'meander\right_twp_{total_width_pixel}_thp_{total_height_pixel}_ovp_{overlap_pixel}_gp_{gap_pixel}_lwp_{line_width_pixel}.bmp'.format(**params), 'BMP')

    plt.figure(figsize=(12,12))
    plt.subplot(131)
    plt.imshow(imageL)
    plt.subplot(132)
    plt.imshow(imageC)
    plt.subplot(133)
    plt.imshow(imageR)
    plt.show()

