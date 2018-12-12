import os
import matplotlib.pyplot as plt

from SEMBitmapCreator import SEMBitmapCreator
from NanometerPixelConverter import NanometerPixelConverter


width_nm = 24000
height_nm = 240000
pitch_nm = 30

converter = NanometerPixelConverter(pitch_nm = pitch_nm)

params = {  'total_width_pixel': converter.to_pixel(width_nm), 
            'total_height_pixel': converter.to_pixel(height_nm), 
            'bondpatch_overlap_pixel': converter.to_pixel(10000), 
            'gap_pixel': converter.to_pixel(3000), 
            'line_width_pixel': converter.to_pixel(3000)
        }


creator = SEMBitmapCreator(**params)
imageL, imageC, imageR = creator.create_EBL_meander()

if not os.path.exists(r'.\meander'):
    os.makedirs(r'.\meander')

imageL.save(r'meander\left_twp_{total_width_pixel}_thp_{total_height_pixel}_ovp_{bondpatch_overlap_pixel}_gp_{gap_pixel}_lwp_{line_width_pixel}.bmp'.format(**params), 'BMP')
imageC.save(r'meander\center_twp_{total_width_pixel}_thp_{total_height_pixel}_ovp_{bondpatch_overlap_pixel}_gp_{gap_pixel}_lwp_{line_width_pixel}.bmp'.format(**params), 'BMP')
imageR.save(r'meander\right_twp_{total_width_pixel}_thp_{total_height_pixel}_ovp_{bondpatch_overlap_pixel}_gp_{gap_pixel}_lwp_{line_width_pixel}.bmp'.format(**params), 'BMP')

plt.figure(figsize=(12,12))
plt.subplot(131)
plt.imshow(imageL)
plt.subplot(132)
plt.imshow(imageC)
plt.subplot(133)
plt.imshow(imageR)
plt.show()