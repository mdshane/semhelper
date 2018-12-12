import os
import matplotlib.pyplot as plt

from SEMBitmapCreator import SEMBitmapCreator
from NanometerPixelConverter import NanometerPixelConverter

width_nm = 24000
height_nm = 240000
pitch_nm = 30
gap_nm = 3000
line_width_nm = 3000

converter = NanometerPixelConverter(pitch_nm = pitch_nm)

params = {  'total_width_pixel': converter.to_pixel(width_nm), 
            'total_height_pixel': converter.to_pixel(height_nm), 
            'bondpatch_overlap_pixel': converter.to_pixel(10000), 
            'gap_pixel': converter.to_pixel(gap_nm), 
            'line_width_pixel': converter.to_pixel(line_width_nm)
        }


creator = SEMBitmapCreator(**params)
image_main, image_last, total_width_pixel_ide = creator.create_EBL_ide()

print("Image width:\n"
    "First n images: {} nm.\n"
    "Final image: {} nm".format(converter.to_nm(total_width_pixel_ide), converter.to_nm(total_width_pixel_ide) + line_width_nm))

if not os.path.exists(r'.\ide'):
    os.makedirs(r'.\ide')

image_main.save(r'ide\main_twp_{total_width_pixel}_thp_{total_height_pixel}_ovp_{bondpatch_overlap_pixel}_gp_{gap_pixel}_lwp_{line_width_pixel}.bmp'.format(**params), 'BMP')
image_last.save(r'ide\last_twp_{total_width_pixel}_thp_{total_height_pixel}_ovp_{bondpatch_overlap_pixel}_gp_{gap_pixel}_lwp_{line_width_pixel}.bmp'.format(**params), 'BMP')

plt.figure(figsize=(12,12))
plt.subplot(121)
plt.imshow(image_main)
plt.subplot(122)
plt.imshow(image_last)
plt.show()

