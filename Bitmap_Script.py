import matplotlib.pyplot as plt
import numpy as np
import scipy.special as sp
import pandas as pd
import glob

def dose(pitch_x, pitch_y, passes, current, dwell_time):
    dose = (dwell_time * passes * current)/(pitch_x * pitch_y)
    # nC/µm^2
    return dose

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
    
    
    output_filename = filename + '_p' + str(int(pitch*1000)) + '_h' + str(int(h_pixel*pitch)) + '_b' + str(int(b_pixel*pitch)) + '_w' + str(w_um) + '_s' + str(s_um) + '_0' + str(file_num) + '.bmp'
    image.save(output_filename, "BMP")

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
eps_r = eps_r_StTiO3
df['capacitance'] = capacitance(df['p_um']*1E-6, df['w_um']*1E-6, df['s_um']*1E-6, df['q_um']*1E-6, eps_r, n)
df




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