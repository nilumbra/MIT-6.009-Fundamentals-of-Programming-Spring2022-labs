#!/usr/bin/env python3

import os
import pickle
import hashlib

import lab
import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


def object_hash(x):
    return hashlib.sha512(pickle.dumps(x)).hexdigest()


def compare_greyscale_images(im1, im2):
    assert set(im1.keys()) == {'height', 'width', 'pixels'}, 'Incorrect keys in dictionary'
    assert im1['height'] == im2['height'], 'Heights must match'
    assert im1['width'] == im2['width'], 'Widths must match'
    assert len(im1['pixels']) == im1['height']*im1['width'], 'Incorrect number of pixels'
    pix_incorrect = (None, None)
    for ix, (i, j) in enumerate(zip(im1['pixels'], im2['pixels'])):
        assert i == j, 'Incorrect value at location %s (differs from expected by %s)' % (ix, abs(i-j))


def compare_color_images(im1, im2):
    assert set(im1.keys()) == {'height', 'width', 'pixels'}, 'Incorrect keys in dictionary'
    assert im1['height'] == im2['height'], 'Heights must match'
    assert im1['width'] == im2['width'], 'Widths must match'
    assert len(im1['pixels']) == im1['height']*im1['width'], 'Incorrect number of pixels'
    assert all(isinstance(i, tuple) and len(i)==3 for i in im1['pixels']), 'Pixels must all be 3-tuples'
    assert all(0<=subi<=255 for i in im1['pixels'] for subi in i), 'Pixels values must all be in the range from [0, 255]'
    pix_incorrect = (None, None)
    for ix, (i, j) in enumerate(zip(im1['pixels'], im2['pixels'])):
        if i != j:
            assert False, 'Incorrect value at location %s (differs from expected by %s)' % (ix, tuple(abs(i[t]-j[t]) for t in {0,1,2}))


def test_load():
    result = lab.load_greyscale_image(os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png'))
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }
    compare_greyscale_images(result, expected)


def test_inverted_1():
    im = lab.load_greyscale_image(os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png'))
    result = lab.inverted(im)
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    }
    compare_greyscale_images(result, expected)


def test_inverted_2():
    assert False


@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_inverted_images(fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % fname)
    im = lab.load_greyscale_image(inpfile)
    oim = object_hash(im)
    result = lab.inverted(im)
    expected = lab.load_greyscale_image(expfile)
    assert object_hash(im) == oim, 'Be careful not to modify the original image!'
    compare_greyscale_images(result, expected)


@pytest.mark.parametrize("kernsize", [1, 3, 7])
@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_blurred_images(kernsize, fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_blur_%02d.png' % (fname, kernsize))
    input_img = lab.load_greyscale_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.blurred(input_img, kernsize)
    expected = lab.load_greyscale_image(expfile)
    assert object_hash(input_img) == input_hash, "Be careful not to modify the original image!"
    compare_greyscale_images(result, expected)


def test_blurred_black_image():
    # REPLACE THIS with your own test case
    assert False


def test_blurred_centered_pixel():
    # REPLACE THIS with your own test case
    assert False


@pytest.mark.parametrize("kernsize", [1, 3, 9])
@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_sharpened_images(kernsize, fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_sharp_%02d.png' % (fname, kernsize))
    input_img = lab.load_greyscale_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.sharpened(input_img, kernsize)
    expected = lab.load_greyscale_image(expfile)
    assert object_hash(input_img) == input_hash, "Be careful not to modify the original image!"
    compare_greyscale_images(result, expected)


@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_edges_images(fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % fname)
    input_img = lab.load_greyscale_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.edges(input_img)
    expected = lab.load_greyscale_image(expfile)
    assert object_hash(input_img) == input_hash, "Be careful not to modify the original image!"
    compare_greyscale_images(result, expected)


def test_edges_centered_pixel():
    # REPLACE THIS with your own test case
    assert False


def test_load_color():
    result = lab.load_color_image('test_images/centered_pixel_color.png')
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [(244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (253, 253, 149), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198)]
    }
    compare_color_images(result, expected)


def test_color_filter_inverted():
    im = lab.load_color_image('test_images/centered_pixel_color.png')
    color_inverted = lab.color_filter_from_greyscale_filter(lab.inverted)
    assert callable(color_inverted), 'color_filter_from_greyscale_filter should return a function.'
    result = color_inverted(im)
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [(11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),  (2, 2, 106), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57)]
    }
    compare_color_images(result, expected)


def test_color_filter_edges():
    im = lab.load_color_image('test_images/centered_pixel_color.png')
    color_edges = lab.color_filter_from_greyscale_filter(lab.edges)
    assert callable(color_edges), 'color_filter_from_greyscale_filter should return a function.'
    result = color_edges(im)
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (13, 113, 69), (18, 160, 98), (13, 113, 69), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (18, 160, 98), (0, 0, 0), (18, 160, 98), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (13, 113, 69), (18, 160, 98), (13, 113, 69), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
    }
    compare_color_images(result, expected)


@pytest.mark.parametrize("fname", ['frog', 'tree'])
@pytest.mark.parametrize("filter_info", [(getattr(lab, 'edges', None), 'edges'), (getattr(lab, 'inverted', None), 'inverted')])
def test_color_filter_images(fname, filter_info):
    filt, filt_name = filter_info
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', f'{fname}.png')
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_{filt_name}.png')
    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    color_filter = lab.color_filter_from_greyscale_filter(filt)
    assert callable(color_filter), 'color_filter_from_greyscale_filter should return a function.'
    result = color_filter(im)
    expected = lab.load_color_image(expfile)
    assert object_hash(im) == oim, 'Be careful not to modify the original image!'
    compare_color_images(result, expected)


def test_color_blur_small():
    blur_filter = lab.make_blur_filter(3)
    assert callable(blur_filter), 'make_blur_filter should return a function.'
    color_blur = lab.color_filter_from_greyscale_filter(blur_filter)
    im = lab.load_color_image('test_images/centered_pixel_color.png')
    result = color_blur(im)
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [(244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (245, 182, 193), (245, 182, 193), (245, 182, 193), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (245, 182, 193), (245, 182, 193), (245, 182, 193), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (245, 182, 193), (245, 182, 193), (245, 182, 193), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198)]
    }
    compare_color_images(result, expected)


@pytest.mark.parametrize("ker_size", [3, 5])
@pytest.mark.parametrize("fname", ['cat', 'mushroom'])
def test_color_blur_filter_images(fname, ker_size):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', f'{fname}.png')
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_blurred{ker_size}.png')
    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    blur_filter = lab.make_blur_filter(ker_size)
    assert callable(blur_filter), 'make_blur_filter should return a function.'
    color_blur = lab.color_filter_from_greyscale_filter(blur_filter)
    result = color_blur(im)
    expected = lab.load_color_image(expfile)
    assert object_hash(im) == oim, 'Be careful not to modify the original image!'
    compare_color_images(result, expected)


@pytest.mark.parametrize("ker_size", [3, 5])
@pytest.mark.parametrize("fname", ['construct', 'bluegill'])
def test_color_sharpen_filter_images(fname, ker_size):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', f'{fname}.png')
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_sharpened{ker_size}.png')
    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    sharpen_filter = lab.make_sharpen_filter(ker_size)
    assert callable(sharpen_filter), 'make_sharpen_filter should return a function.'
    color_sharpen = lab.color_filter_from_greyscale_filter(sharpen_filter)
    result = color_sharpen(im)
    expected = lab.load_color_image(expfile)
    assert object_hash(im) == oim, 'Be careful not to modify the original image!'
    compare_color_images(result, expected)


def test_small_cascade():
    color_edges = lab.color_filter_from_greyscale_filter(lab.edges)
    color_inverted = lab.color_filter_from_greyscale_filter(lab.inverted)
    color_blur_5 = lab.color_filter_from_greyscale_filter(lab.make_blur_filter(5))

    im = lab.load_color_image('test_images/centered_pixel_color.png')
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (254, 250, 252), (254, 244, 248), (253, 240, 246), (253, 240, 246), (253, 240, 246), (254, 244, 248), (254, 250, 252), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (254, 244, 248), (253, 238, 244), (252, 227, 238), (252, 227, 238), (252, 227, 238), (253, 238, 244), (254, 244, 248), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (253, 240, 246), (252, 227, 238), (250, 211, 228), (250, 211, 228), (250, 211, 228), (252, 227, 238), (253, 240, 246), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (253, 240, 246), (252, 227, 238), (250, 211, 228), (250, 211, 228), (250, 211, 228), (252, 227, 238), (253, 240, 246), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (253, 240, 246), (252, 227, 238), (250, 211, 228), (250, 211, 228), (250, 211, 228), (252, 227, 238), (253, 240, 246), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (254, 244, 248), (253, 238, 244), (252, 227, 238), (252, 227, 238), (252, 227, 238), (253, 238, 244), (254, 244, 248), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (254, 250, 252), (254, 244, 248), (253, 240, 246), (253, 240, 246), (253, 240, 246), (254, 244, 248), (254, 250, 252), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)]
    }
    f_cascade = lab.filter_cascade([color_edges, color_inverted, color_blur_5])
    assert callable(f_cascade), 'filter_cascade should return a function.'
    result = f_cascade(im)
    compare_color_images(result, expected)


@pytest.mark.parametrize("cascade", [0, 1, 2])
@pytest.mark.parametrize("image", ['tree', 'stronger'])
def test_cascades(cascade, image):
    color_edges = lab.color_filter_from_greyscale_filter(lab.edges)
    color_inverted = lab.color_filter_from_greyscale_filter(lab.inverted)
    cascade0 = [color_edges,
                lab.color_filter_from_greyscale_filter(lab.make_sharpen_filter(3))]
    cascade1 = [lab.color_filter_from_greyscale_filter(lab.make_blur_filter(5)),
                color_edges,
                lab.color_filter_from_greyscale_filter(lab.make_sharpen_filter(3)),
                lambda im: {k: ([(i[1], i[0], i[2]) for i in v] if isinstance(v, list) else v) for k, v in im.items()}]
    cascade2 = [color_edges]*5 + [color_inverted]

    cascades = [cascade0, cascade1, cascade2]

    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', f'{image}.png')
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', f'{image}_cascade{cascade}.png')
    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    f_cascade = lab.filter_cascade(cascades[cascade])
    assert callable(f_cascade), 'filter_cascade should return a function.'
    result = f_cascade(im)
    expected = lab.load_color_image(expfile)
    assert object_hash(im) == oim, 'Be careful not to modify the original image!'
    compare_color_images(result, expected)


if __name__ == '__main__':
    import os
    import sys
    import json
    import pickle
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--gather", action='store_true')
    parser.add_argument("--server", action='store_true')
    parser.add_argument("--initial", action='store_true')
    parser.add_argument("args", nargs="*")

    parsed = parser.parse_args()

    class TestData:
        def __init__(self, gather=False):
            self.alltests = None
            self.results = {'passed': []}
            self.gather = gather

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != 'call':
                return
            self.results.setdefault(report.outcome, []).append(report.head_line)

        def pytest_collection_finish(self, session):
            if self.gather:
                self.alltests = [i.name for i in session.items]


    pytest_args = ['-v', __file__]

    if parsed.server:
        pytest_args.insert(0, '--color=yes')

    if parsed.gather:
        pytest_args.insert(0, '--collect-only')

    testinfo = TestData(parsed.gather)
    res = pytest.main(
        ['-k', ' or '.join(parsed.args), *pytest_args],
        **{'plugins': [testinfo]}
    )

    if parsed.server:
        _dir = os.path.dirname(__file__)
        if parsed.gather:
            with open(os.path.join(_dir, 'alltests.json'), 'w' if parsed.initial else 'a') as f:
                f.write(json.dumps(testinfo.alltests))
                f.write('\n')
        else:
            with open(os.path.join(_dir, 'results.json'), 'w' if parsed.initial else 'a') as f:
                f.write(json.dumps(testinfo.results))
                f.write('\n')
