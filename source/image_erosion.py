from PIL import Image
import numpy as np
import argparse

def binarize_image(im):
    return (im > np.mean(im)) * 1

def get_structuring_element():
    struct_elm = np.ones((11, 11))
    return struct_elm

def has_background(region, struct_elm):
    for i in range(region.shape[0]):
        for j in range(region.shape[1]):
            if ((struct_elm[i, j] == 1) and (region[i, j]) == 0):
                return True
    return False

def erode(bin_im, struct_elm):
    se_height, se_width = struct_elm.shape
    vert_range, horz_range = bin_im.shape[0]-se_height, bin_im.shape[1]-se_width
    eroded_im = np.zeros(bin_im.shape)
    for i in range(vert_range):
        for j in range(horz_range):
            region = bin_im[i:(i+se_height), j:(j+se_width)]
            center_x, center_y = (i+(se_height//2)), (j+(se_width//2))
            if (region[(se_height//2), (se_width//2)] == 1):
                if (not has_background(region, struct_elm)):
                        eroded_im[center_x, center_y] = 1
    return eroded_im

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('im_path', type=str)
    args = parser.parse_args()
    return args.im_path

def main():
    im_path = parse_arguments()
    im = np.array(Image.open(im_path).convert('L'))
    bin_im = binarize_image(im)

    struct_elm = get_structuring_element()
    print(bin_im.sum())

    eroded_im = erode(bin_im, struct_elm)
    print(eroded_im.sum())

    Image.fromarray(im).show()
    Image.fromarray(eroded_im * 255).show()

if __name__ == '__main__':
    main()

