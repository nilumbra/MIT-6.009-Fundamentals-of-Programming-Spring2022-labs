#!/usr/bin/env python3

import math

from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!

def get_width(image):
    return image['width']

def get_height(image):
    return image['height']

def get_pixel(image, x, y):
    width = image['width']
    # assert 0 <= (y * width + (x + 1)) - 1 < len(image['pixels'])
    return image['pixels'][(y * width + (x + 1)) - 1]

def isBounded(image, x, y):
    """
    Check if (x, y) is a valid pixel index for <image>
    rtype: bool
    """
    return True if 0 <= x < get_width(image) and 0 <= y < get_height(image) else False  

def snap_periphery_to_edge(image, x, y):
    w, h = get_width(image), get_height(image)
    if x < 0:
        x = 0
    elif x >= w:
        x = w - 1
    
    if y < 0:
        y = 0
    elif y >= h:
        y = h - 1

    return (x, y)


def get_pixel_augmented(image, x, y, t="zero"):
    if t == "zero":
        return get_pixel(image, x, y) if isBounded(image, x, y) else 0
    elif t == "wrap":
        if isBounded(image, x, y):
            return get_pixel(image, x, y) 
        else:
            return get_pixel(image, x % get_width(image), y % get_height(image))
    elif t == "extend":
        if isBounded(image, x, y):
            return get_pixel(image, x, y) 
        else:
            coor = snap_periphery_to_edge(image, x, y)
            return get_pixel(image, *coor) 
    else:
        raise Exception("Unknown wraping type")

def set_pixel(image, x, y, c):
    width = image['width']
    # assert 0 <= (y * width + (x + 1)) - 1 < len(image['pixels'])
    # print(len(image['pixels']),  (y * width + (x + 1)) - 1)
    image['pixels'][(y * width + (x + 1)) - 1] = c


def apply_per_pixel(image, func):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0 for i in range(image['width']) for j in range(image['height'])],
    }
    for x in range(image['width']):
        for y in range(image['height']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)


# HELPER FUNCTIONS

def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings 'zero', 'extend', or 'wrap',
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of 'zero', 'extend', or 'wrap', return
    None.

    Otherwise, the output of this function should have the same form as a 6.009
    image (a dictionary with 'height', 'width', and 'pixels' keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    average_kernel = {
        'scale': 3,
        'data': { 1:0.2, 3:0.2, 4:0.2, 5:0.2, 7:0.2 }
    }
    """
    def calc_kernel_to_pixel(x, y, kernal, bh):
        scale = kernal['scale']
        mid = scale // 2
        lc = 0
        for i in range(scale):
            for j in range(scale):
                if (j * scale + i) in kernal['data']:
                    lc += get_pixel_augmented(image, x - mid + i, y - mid + j, bh) * kernal['data'][(j * scale + i)]
        return lc 

    if boundary_behavior not in {'zero', 'extend', 'wrap'}: return None

    result = {
        'width': get_width(image),
        'height': get_height(image),
        'pixels': [0 for i in range(image['width']) for j in range(image['height'])],
    }

    for i in range(result['width']):
        for j in range(result['height']):
            set_pixel(result, i, j, calc_kernel_to_pixel(i, j, kernel, boundary_behavior))

    return result

# TEST PASSED
def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    image['pixels'] = list(map(lambda p: round(min(max(0, p), 255)), image['pixels']))


def blur_kernel(n):
    if n % 2 == 0: 
        raise Exception("Kernal scale must be a odd number!!")
    val = 1 / (n * n)
    return {
        'scale': n,
        'data': {idx: val for idx in range(n * n)}
    }

# FILTERS

def blurred(image, n, boundary_behavior="extend"):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    kernel = blur_kernel(n)

    # then compute the correlation of the input image with that kernel using
    # the 'extend' behavior for out-of-bounds pixels
    result = correlate(image, kernel, boundary_behavior)

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    round_and_clip_image(result)
    return result

def sharpened(image, n):
    """
    Return a new image representing the result of applying an unsharp mask to 
    the givin input image

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """

    # First, create a n-by-n unsharp mask
    unsharp = blur_kernel(n)
    unsharp['data'] = {k: -v for (k, v) in unsharp['data'].items()}
    unsharp['data'][(n * n) // 2] = 2 - 1 / (n * n)

    # compute the correlation of the input image with the unsharp mask
    # (using the 'extend' behavior for out-of-bounds pixels)
    result = correlate(image, unsharp, "extend")

    # and, finally, make sure that the output is a valid image 
    round_and_clip_image(result)
    return result

def edges(image):
    Kx = {
        'scale': 3,
        'data': {0:-1, 2:1, 3:-2, 5:2, 6:-1, 8:1}
    }

    Ky = {
        'scale': 3,
        'data': {0:-1, 1:-2, 2:-1, 6:1, 7:2, 8:1}
    }

    Ox = correlate(image, Kx, "extend")
    Oy = correlate(image, Ky, "extend")

    result = {
        'width': Ox['width'],
        'height': Ox['height'],
        'pixels': [round(math.sqrt(Ox['pixels'][idx] ** 2 + Oy['pixels'][idx] ** 2)) 
                    for idx in range(Ox['width'] * Ox['height'])]
    }

    round_and_clip_image(result)
    return result

# COLOR FILTERS
def color_to_grey_scale_channels(image):
    """
    Takes a colored image as input and returns a list consisting three gray scale image,
    each corresponding to the RGB channel of the original colored image.
    """
    return [{
        'width': image['width'],
        'height': image['height'],
        'pixels': [px[c] for px in image['pixels']]
     } for c in range(3)]

def grey_scale_channels_to_color(channels):
    w, h = channels[0]['width'], channels[0]['height']
    return {
        'width': channels[0]['width'],
        'height': channels[0]['height'],
        'pixels': [(channels[0]['pixels'][idx], channels[1]['pixels'][idx], channels[2]['pixels'][idx]) for idx in range(w * h)]
    }


def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def color_filter(image):
        """
        Takes a colored image and produces the filtered color image. 
        (instead of mutating the input image, a new image structure will be created and returned)
        """

        # apply filter to each channel
        filterd_grays = [filt(ch) for ch in color_to_grey_scale_channels(image)]

        # combine channels back to a color image
        result = grey_scale_channels_to_color(filterd_grays)
        return result

    return color_filter


def make_blur_filter(n):
    """
    Make a blur filter with n-by-n kernel. Return a function which takes an image as input
    and returns the image blurred by the n-by-n kernel
    """
    def blur_filter(image):
        return blurred(image, n)

    return blur_filter


def make_sharpen_filter(n):
    def sharpen_filter(image):
        return sharpened(image, n)

    return sharpen_filter


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def c(image):
        result = image
        for f in filters:
            result = f(result)
        return result

    return c

def contrast_filter(image, contrast):
    """
    Works on both color and greyscale images. The effect is controlled by <contrast>.
    Instead of affecting the input image, a new image instance with contrast adjusted
    will be created and returned
    """
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': None
    }

    


    f = (259 * (contrast + 255)) / (255 * (259 - contrast))
    truncate = lambda p: max(0, min(p, 255))
    constrast_formula = lambda p: round(f * (p - 128) + 128)
    if(type(image['pixels'][0]) is tuple):
        result['pixels'] = [tuple(map(truncate,
                                    map(constrast_formula,px)
                                    )
                                ) for px in image['pixels']]
    else:
        result['pixels'] = [truncate(constrast_formula(px)) for px in image['pixels']]

    return result


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_greyscale_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    def test_inverted():
        out_filename = "inverted_bluegill.png"
        im = load_greyscale_image("./test_images/bluegill.png")
        inverted_im = inverted(im)
        save_greyscale_image(inverted_im, out_filename)

    translate_2_kernel = {
        'scale': 5,
        'data': {10: 1},
    }

    translate_13_kernel = {
        'scale': 13,
        'data': {26: 1},
    }

    average_3_kernel = {
        'scale': 3,
        'data': { 1:0.2, 3:0.2, 4:0.2, 5:0.2, 7:0.2 },
    }

    def test_correlation(kernel, filename, boundary_behavior):
        im = load_greyscale_image("./test_images/" + filename + ".png")

        result = correlate(im, kernel, boundary_behavior)
        round_and_clip_image(result)
        save_greyscale_image(result, filename + boundary_behavior + ".png")

    # test_correlation(translate_13_kernel, "pigbird", "zero")
    # test_correlation(translate_13_kernel, "pigbird", "wrap")

    def peek_centered_pixel():
        im = load_greyscale_image("./test_images/centered_pixel.png")
        print(im)

    # peek_centered_pixel()

    def blur_cat_13():
        im = load_greyscale_image("./test_images/cat.png")
        cat_blurred_extend = blurred(im, 13, "extend")
        cat_blurred_zero = blurred(im, 13, "zero")
        cat_blurred_wrap = blurred(im, 13, "wrap")

        save_greyscale_image(cat_blurred_extend, "cat_blurred_extend.png")
        save_greyscale_image(cat_blurred_zero, "cat_blurred_zero.png")
        save_greyscale_image(cat_blurred_wrap, "cat_blurred_wrap.png")

    # blur_cat_13()
    def unsharp_python_11():
        im = load_greyscale_image("./test_images/python.png")
        python_sharpend = sharpened(im, 11)
        
        save_greyscale_image(python_sharpend, "python_sharpend.png")

    # unsharp_python_11()
    def edge_construct():
        im = load_greyscale_image("./test_images/construct.png")
        construct_edge = edges(im)
        
        save_greyscale_image(construct_edge, "construct_edge.png")

    # edge_construct()  

    def invert_color_cat():
        im = load_color_image("./test_images/cat.png")
        invert_filter = color_filter_from_greyscale_filter(inverted)
        inverted_cat = invert_filter(im)
        
        save_color_image(inverted_cat, "inverted_cat.png")

    # invert_color_cat()

    def blurred_python_color_9():
        im = load_color_image("./test_images/python.png")
        python_blurred_color_9 = color_filter_from_greyscale_filter(make_blur_filter(9))(im)

        save_color_image(python_blurred_color_9, "python_blurred_color_9.png")

    # blurred_python_color_9()

    def sharpened_sparrow_7():
        im = load_color_image("./test_images/sparrowchick.png")
        sparrow_sharpened_color_7 = color_filter_from_greyscale_filter(make_sharpen_filter(7))(im)

        save_color_image(sparrow_sharpened_color_7, "sparrow_sharpened_color_7.png")
    # sharpened_sparrow_7()

    def filters_cascade_frog():
        im = load_color_image("./test_images/frog.png")
        filter1 = color_filter_from_greyscale_filter(edges)
        filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
        filt = filter_cascade([filter1, filter1, filter2, filter1])

        save_color_image(filt(im), "filters_cascade_frog.png")

    # filters_cascade_frog()

    def mushroom_constrast_plus_40():
        im = load_color_image("./test_images/mushroom.png")
        save_color_image(contrast_filter(im, 40), "mushroom_constrast_plus_40.png")

    mushroom_constrast_plus_40()