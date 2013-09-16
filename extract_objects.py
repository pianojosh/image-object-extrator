#!/usr/bin/env python

import random

def extract_objects(image, trigger_pixel_fn, object_pixel_fn):
    objects = []
    pixels_to_scan = set()
    for x_loc in range(len(image)):
        for y_loc in range(len(image[x_loc])):
            pixels_to_scan.add((x_loc, y_loc))
    while pixels_to_scan:
        #print "There are %d pixels remaining to scan" % (len(pixels_to_scan))
        pixel_to_search = pixels_to_scan.pop()
        x_loc = pixel_to_search[0]
        y_loc = pixel_to_search[1]
        if trigger_pixel_fn(image[x_loc][y_loc]):
            maybe_object = find_object(image, x_loc, y_loc, object_pixel_fn)
            if maybe_object:
                objects.append(maybe_object)
                for bad_pixel in maybe_object['bad_pixels']:
                    pixels_to_scan.discard((bad_pixel[0], bad_pixel[1]))
    return objects


def find_object(image, start_x_loc, start_y_loc, bad_pixel_fn):
    bad_pixels = search_object(image, start_x_loc, start_y_loc, bad_pixel_fn)
    if (bad_pixels):
        object_min_x = start_x_loc
        object_min_y = start_y_loc
        object_max_x = start_x_loc
        object_max_y = start_y_loc
        for pixel in bad_pixels:
            if pixel[0] < object_min_x:
                object_min_x = pixel[0]
            if pixel[0] > object_max_x:
                object_max_x = pixel[0]
            if pixel[1] < object_min_y:
                object_min_y = pixel[1]
            if pixel[1] > object_max_y:
                object_max_y = pixel[1]
        return {
            'min_x': object_min_x,
            'min_y': object_min_y,
            'max_x': object_max_x,
            'max_y': object_max_y,
            'bad_pixels': bad_pixels,
        }


def search_object(image, start_x_loc, start_y_loc, bad_pixel_fn):
    pixels_to_search = set()
    searched_pixels = set()
    bad_pixels = set()
    pixels_to_search.add((start_x_loc, start_y_loc))
    
    while pixels_to_search:
        #print 'Looking for an object, there are %d pixels left to search, and we have already searched %d pixels, and have found %d bad pixels' % (len(pixels_to_search), len(searched_pixels), len(bad_pixels))
        pixel_to_search = pixels_to_search.pop()
        x_loc = pixel_to_search[0]
        y_loc = pixel_to_search[1]
        searched_pixels.add((x_loc, y_loc))
        if bad_pixel_fn(image[x_loc][y_loc]):
            bad_pixels.add((x_loc, y_loc))
            for search_x_offset in range(-2, 3):
                search_x_loc = x_loc + search_x_offset
                if search_x_loc >= 0 and search_x_loc < len(image):
                    for search_y_offset in range(-2, 3):
                        search_y_loc = y_loc + search_y_offset
                        if search_y_loc >= 0 and search_y_loc < len(image[search_x_loc]):
                            if (search_x_loc, search_y_loc) not in searched_pixels:
                                pixels_to_search.add((search_x_loc, search_y_loc))
    return bad_pixels
    
    
def main():

    def is_trigger_pixel(value):
        if value >= 7:
            return True

    def is_object_pixel(value):
        if value >= 3:
            return True

    
    image = []
    '''
    for x in range(2048):
        row = []
        for y in range(4096):
            row.append(random.randint(0, 9))
        #print ''.join(map(str, row))
        image.append(row)
    '''
    image = [
        [0,2,1,0,1,2,4,6,6,4],
        [3,4,1,0,1,2,5,4,5,2],
        [0,9,2,0,1,0,6,7,2,5],
        [0,3,1,1,1,2,2,3,0,1],
        [0,0,2,1,1,2,1,1,2,2],
    ]
    print "\n".join([''.join(map(str, row)) for row in image])
    
    found_objects = extract_objects(image, is_trigger_pixel, is_object_pixel)
    for found_object in found_objects:
        print "found an object from (%d, %d) to (%d, %d)" % (
            found_object['min_x'],
            found_object['min_y'],
            found_object['max_x'],
            found_object['max_y']
        )


if __name__ == '__main__':
    main()
    



