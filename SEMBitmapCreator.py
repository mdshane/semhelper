from PIL import Image, ImageDraw, ImageOps


class SEMBitmapCreator():

    def __init__(self, total_width_pixel: int, total_height_pixel: int, bondpatch_overlap_pixel: int, gap_pixel: int, line_width_pixel: int):
        self.total_width_pixel = total_width_pixel
        self.total_height_pixel = total_height_pixel
        self.bondpatch_overlap_pixel = bondpatch_overlap_pixel
        self.gap_pixel = gap_pixel
        self.line_width_pixel = line_width_pixel
        

    def create_EBL_meander(self) -> Image:
        image_middle = Image.new(mode='RGB', size = (self.total_width_pixel, self.total_height_pixel))

        draw = ImageDraw.Draw(image_middle)
        # write overlap to bondpatch
        draw.rectangle([0, 0, self.total_width_pixel, self.bondpatch_overlap_pixel], fill='white')
        draw.rectangle([0, self.total_height_pixel - self.bondpatch_overlap_pixel, self.total_width_pixel, self.total_height_pixel], fill='white')

        #write horizontal lines
        y = self.bondpatch_overlap_pixel + self.gap_pixel
        while y < self.total_height_pixel - self.bondpatch_overlap_pixel:
            draw.rectangle([0, y, self.total_width_pixel, y + self.line_width_pixel], fill='white')
            y += self.line_width_pixel + self.gap_pixel

        del draw

        image_left = image_middle.copy()

        # left side
        draw = ImageDraw.Draw(image_left)
        #write connection
        y = self.bondpatch_overlap_pixel + self.gap_pixel
        while y < self.total_height_pixel - self.bondpatch_overlap_pixel:
            draw.rectangle([0, y, self.line_width_pixel, y + self.gap_pixel + self.line_width_pixel], fill='white')
            y += 2 * (self.line_width_pixel + self.gap_pixel)

        del draw

        image_right = image_middle.copy()

        # left side
        draw = ImageDraw.Draw(image_right)
        #write connection
        y = self.bondpatch_overlap_pixel
        while y < self.total_height_pixel - self.bondpatch_overlap_pixel:
            draw.rectangle([self.total_width_pixel - self.line_width_pixel, y, self.total_width_pixel, y + self.gap_pixel + self.line_width_pixel], fill='white')
            y += 2 * (self.line_width_pixel + self.gap_pixel)

        del draw

        return image_left, image_middle, image_right



    def create_EBL_ide(self):


        num_electrodes = int(self.total_width_pixel/(self.line_width_pixel + self.gap_pixel))
        if num_electrodes % 2 != 0:
            num_electrodes -= 1

        total_width_pixel_ide = int((self.gap_pixel + self.line_width_pixel) * num_electrodes)
        
        if total_width_pixel_ide == 0:
            raise Exception("Error: Can't fit one pair of electrodes with desired dimensions in picture size.")

        # Create the image
        image = Image.new(mode = 'RGB', size = (total_width_pixel_ide, self.total_height_pixel), color ='black')
        draw = ImageDraw.Draw(image)

        # Write overlap to bondpatch
        draw.rectangle([0, 0, total_width_pixel_ide, self.bondpatch_overlap_pixel], fill='white')
        draw.rectangle([0, self.total_height_pixel - self.bondpatch_overlap_pixel, total_width_pixel_ide, self.total_height_pixel], fill='white')


        for i in range(int(num_electrodes/2)+1):
            # upper electrodes
            x_0_upper = i * 2 * (self.line_width_pixel + self.gap_pixel)
            y_0_upper = self.bondpatch_overlap_pixel
            x_1_upper = x_0_upper  + self.line_width_pixel
            y_1_upper = y_0_upper + self.total_height_pixel - 2 * self.bondpatch_overlap_pixel - self.gap_pixel
            draw.rectangle([x_0_upper, y_0_upper, x_1_upper, y_1_upper], fill='white')
        
        for j in range(0,int(num_electrodes/2)+1):
            # lower electrodes
            x_0_lower = (j * 2 + 1) * (self.line_width_pixel +  self.gap_pixel)
            y_0_lower = self.bondpatch_overlap_pixel + self.gap_pixel
            x_1_lower = x_0_lower + self.line_width_pixel
            y_1_lower = y_0_lower + self.total_height_pixel - self.bondpatch_overlap_pixel
            draw.rectangle([x_0_lower, y_0_lower, x_1_lower, y_1_lower], fill='white')
        del draw

        # add one electrode for last bitmap

        image_last = Image.new(mode = 'RGB', size = (total_width_pixel_ide + self.line_width_pixel, self.total_height_pixel), color ='black')
        image_last.paste(image)
        draw = ImageDraw.Draw(image_last)

        
        # Write overlap to bondpatch
        draw.rectangle([0, 0, total_width_pixel_ide + self.line_width_pixel, self.bondpatch_overlap_pixel], fill='white')
        draw.rectangle([0, self.total_height_pixel - self.bondpatch_overlap_pixel, total_width_pixel_ide + self.line_width_pixel, self.total_height_pixel], fill='white')

        # last electrode
        x_0_upper = total_width_pixel_ide
        y_0_upper = self.bondpatch_overlap_pixel
        x_1_upper = x_0_upper  + self.line_width_pixel
        y_1_upper = y_0_upper + self.total_height_pixel - 2 * self.bondpatch_overlap_pixel - self.gap_pixel
        draw.rectangle([x_0_upper, y_0_upper, x_1_upper, y_1_upper], fill='white')

        del draw
    
        print("DEBUG: With a desired width of {0} pixel, {1} electrode pairs can "
            "be fitted into the picture. The resulting picture size is now {2} "
            "pixel.\n".format(self.total_width_pixel, num_electrodes, total_width_pixel_ide)
            )

        return image, image_last, total_width_pixel_ide


if __name__ == '__main__':
    import os

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


'''
'''