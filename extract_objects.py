

#!/usr/bin/env python

import random

def extract_objects(image, bad_pixel_fn):
    objects = []
    pixels_to_search = set()
    for x_loc in range(len(image)):
        for y_loc in range(len(image[x_loc])):
            pixels_to_search.add((x_loc, y_loc))
    while pixels_to_search:
        pixel_to_search = pixels_to_search.pop()
        x_loc = pixel_to_search[0]
        y_loc = pixel_to_search[1]
        if bad_pixel_fn(image[x_loc][y_loc]):
            maybe_object = find_object(image, x_loc, y_loc, bad_pixel_fn)
            if maybe_object:
                objects.append(maybe_object)
                for remove_x in range(maybe_object['min_x'], maybe_object['max_x'] + 1):
                    for remove_y in range(maybe_object['min_y'], maybe_object['max_y'] + 1):
                        pixels_to_search.discard((remove_x, remove_y))
    return objects


def find_object(image, start_x_loc, start_y_loc, bad_pixel_fn):
    searched_pixels = set()
    bad_pixels = set()
    found_objects = []
    search_object(image, searched_pixels, bad_pixels, start_x_loc, start_y_loc, bad_pixel_fn)
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
            'max_y': object_max_y
        }


def search_object(image, searched_pixels, bad_pixels, x_loc, y_loc, bad_pixel_fn):
    if (x_loc, y_loc) in searched_pixels:
        return
    searched_pixels.add((x_loc, y_loc))
    if bad_pixel_fn(image[x_loc][y_loc]):
        bad_pixels.add((x_loc, y_loc))
        for search_x_offset in range(-2, 3):
            search_x_loc = x_loc + search_x_offset
            if search_x_loc >= 0 and search_x_loc < len(image):
                for search_y_offset in range(-2, 3):
                    search_y_loc = y_loc + search_y_offset
                    if search_y_loc >= 0 and search_y_loc < len(image[search_x_loc]):
                        search_object(image,
                                      searched_pixels,
                                      bad_pixels,
                                      search_x_loc,
                                      search_y_loc,
                                      bad_pixel_fn)
    
    
def main():

    def is_bad_pixel(value):
        if value <= 0:
            return True

    
    image = []
    for x in range(2048):
        row = []
        for y in range(4096):
            if random.random() < .001:
                row.append(0)
            else:
                row.append(1)
        #print ''.join(map(str, row))
        image.append(row)
    
    
    found_objects = extract_objects(image, is_bad_pixel)
    for found_object in found_objects:
        print "found an object from (%d, %d) to (%d, %d)" % (
            found_object['min_x'],
            found_object['min_y'],
            found_object['max_x'],
            found_object['max_y']
        )


if __name__ == '__main__':
    main()
    



