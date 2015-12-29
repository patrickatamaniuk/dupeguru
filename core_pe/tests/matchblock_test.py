# Created By: Patrick Atamaniuk
# Created On: 2015/12/29
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html
# The commented out tests are tests for function that have been converted to pure C for speed

import logging, sys
from pytest import raises, skip
from hscommon.testutil import eq_
from core.engine import Match
from ..matchblock import getmatches
import hashlib

try:
    from ..block import *
except ImportError:
    skip("Can't import the block module, probably hasn't been compiled.")

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

#def getblock(image):
#    """Returns a 3 sized tuple containing the mean color of 'image'.
#
#    image: a PIL image or crop.
#    """
#    if image.size[0]:
#        pixel_count = image.size[0] * image.size[1]
#        red = green = blue = 0
#        for r,g,b in image.getdata():
#            red += r
#            green += g
#            blue += b
#        return (red // pixel_count, green // pixel_count, blue // pixel_count)
#    else:
#        return (0,0,0)
#
#def getblocks2(image,block_count_per_side):
#    """Returns a list of blocks (3 sized tuples).
#
#    image: A PIL image to base the blocks on.
#    block_count_per_side: This integer determine the number of blocks the function will return.
#    If it is 10, for example, 100 blocks will be returns (10 width, 10 height). The blocks will not
#    necessarely cover square areas. The area covered by each block will be proportional to the image
#    itself.
#    """
#    if not image.size[0]:
#        return []
#    width,height = image.size
#    block_width = max(width // block_count_per_side,1)
#    block_height = max(height // block_count_per_side,1)
#    result = []
#    for ih in range(block_count_per_side):
#        top = min(ih * block_height, height - block_height)
#        bottom = top + block_height
#        for iw in range(block_count_per_side):
#            left = min(iw * block_width, width - block_width)
#            right = left + block_width
#            box = (left,top,right,bottom)
#            crop = image.crop(box)
#            result.append(getblock(crop))
#    return result

class FakeImage(object):
    is_ref = False

    def __init__(self, size, data, path):
        self.size = size
        self.data = data
        self.path = path
        m = hashlib.md5()
        m.update(repr(self.data).encode('utf-8'))
        self.md5 = m.digest()

    def __repr__(self):
        return "FakeImage(%s, %s, %s)" % (repr(self.size), repr(self.data), repr(self.path))

    def get_blocks(self, block_count_per_side):
        return getblocks2(self, block_count_per_side)

    @property
    def dimensions(self):
        return self.size

    def getdata(self):
        return self.data

    def crop(self, box):
        pixels = []
        for i in range(box[1], box[3]):
            for j in range(box[0], box[2]):
                pixel = self.data[i * self.size[0] + j]
                pixels.append(pixel)
        return FakeImage((box[2] - box[0], box[3] - box[1]), pixels, self.path)

BLACK = (0,0,0)
RED = (0xff,0,0)
GREEN = (0,0xff,0)
BLUE = (0,0,0xff)
def empty():
    return FakeImage((0,0), [], '/empty.jpg')

def single_pixel(): #one red pixel
    return FakeImage((1, 1), [(0xff,0,0)], '/single.jpg')

def four_pixels(path=None, data=None):
    pixels = data or [RED,(0,0x80,0xff),(0x80,0,0),(0,0x40,0x80)]
    return FakeImage((2, 2), pixels, path or '/four.jpg')

class TestMatchblock:
    """tests for
    getmatches(pictures, cache_path, threshold=75, match_scaled=False, j=job.nulljob, scanbase=None):
    """
    def test_simple(self, tmpdir):
        cache_path = str(tmpdir.join('foo.db'))
        pictures = []
        result = getmatches(pictures, cache_path)
        logging.debug('Result: %s' % repr(result))
        eq_(result, [])

    def test_nomatch(self, tmpdir):
        cache_path = str(tmpdir.join('foo.db'))
        pictures = [single_pixel(), four_pixels()]
        result = getmatches(pictures, cache_path)
        logging.debug('Result: %s' % repr(result))
        eq_(result, [])

    def test_match(self, tmpdir):
        cache_path = str(tmpdir.join('foo.db'))
        pictures = [four_pixels(), four_pixels('/four copy.jpg')]
        result = getmatches(pictures, cache_path)
        logging.debug('Result: %s' % repr(result))
        assert result != []
        eq_(result, [Match(pictures[0], pictures[1], 100)])

class TestIncrementalMatch:
    def test_incremental(self, tmpdir):
        cache_path = str(tmpdir.join('foo.db'))
        pictures = [four_pixels(), four_pixels('/four copy.jpg'), four_pixels('/blue.jpg', [BLUE]*4)]
        result = getmatches(pictures, cache_path)
        logging.debug('Result: %s' % repr(result))
        eq_(len(result), 1)

        scanbase = [p.path for p in pictures]
        pictures.append(four_pixels('/blue copy.jpg', [BLUE]*4))
        result = getmatches(pictures, cache_path, scanbase=scanbase)
        logging.debug('Result: %s' % repr(result))
        eq_(len(result), 1) # one new result

        result = getmatches(pictures, cache_path)
        logging.debug('Result: %s' % repr(result))
        eq_(len(result), 2) # all results when rescanning without scanbase
