

#!/usr/bin/env python

IMAGE = [
    [1,1,1,0,0,1,1,1,1,0,0,1],
    [0,1,1,1,0,0,1,1,0,0,1,0],
    [1,1,1,0,1,1,1,1,1,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,1,1,1,1,1,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,1,1,1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,0,1,1,1,1,1],
]


def extract_objects(image, bad_pixel_fn):
    objects = []
    for x_loc in range(len(image)):
        for y_loc in range(len(image[x_loc])):
            pixel_in_found_object = False
            for obj in objects:
                if (
                        x_loc >= obj['min_x'] and
                        x_loc <= obj['max_x'] and
                        y_loc >= obj['min_y'] and
                        y_loc <= obj['max_y']
                ):
                    pixel_in_found_object = True
            if not pixel_in_found_object:
                maybe_object = find_object(image, x_loc, y_loc, bad_pixel_fn)
                if maybe_object:
                    objects.append(maybe_object)
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

    found_objects = extract_objects(IMAGE, is_bad_pixel)
    for found_object in found_objects:
        print "found an object from (%d, %d) to (%d, %d)" % (
            found_object['min_x'],
            found_object['min_y'],
            found_object['max_x'],
            found_object['max_y']
        )


if __name__ == '__main__':
    main()
    


