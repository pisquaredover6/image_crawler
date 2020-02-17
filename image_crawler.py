#!/usr/bin/env python3

"""fetch images from a plaintext file list and store them on harddrive"""

import imghdr
import logging
import requests
import sys
from os import path

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger('image_crawler')


def make_filename(output_directory, file_extension, url):
    """
    Create filename for image by using last part of url (after last '/').
    Make sure file ends with proper file extension.
    Check if filename already exists in folder.
    If yes, append counter and count up until filename is available
    (e.g. output_dir/image.jpg, output_dir/image_(1).jpg, output_dir/image_(2).jpg)
    :param output_directory: path to output directory
    :param file_extension: image file extension (e.g. jpeg, png)
    :param url: url to image
    :return: filename (e.g. output_dir/image.jpg )
    """
    filename = '{}/{}'.format(output_directory, url.rsplit('/', 1)[1])
    try:
        image_name, extension = filename.rsplit('.')
    except ValueError:
        image_name = filename
    filename = '{}.{}'.format(image_name, file_extension)
    filename_counter = 1
    # if filename is already taken, attach a number (counting up) until we find a free name
    while path.exists(filename):
        filename = '{}_({}).{}'.format(image_name, filename_counter, file_extension)
        filename_counter += 1
    return filename


def crawl_images(input_file, output_directory='output'):
    """
    read a plaintext file, fetch the image and store it on disk
    In case of error, the image url is ignored and the script continues
    :param input_file: plaintext file containing one image url per line
    :param output_directory: target directory to save the collected images
    :return: nothing
    """
    line_counter = 0
    saved_images_counter = 0
    with open(input_file, 'r') as input_list:
        # read plaintext file line by line
        for line in input_list:
            url = line.rstrip('\n')
            try:
                image_request = requests.get(url)
            except Exception as e:
                logger.error('Error at image {} - ignoring. {}'.format(url, e))
                line_counter += 1
                continue

            if image_request.status_code == 200:
                # find out type of image (png, jpg...)
                file_extension = imghdr.what("dummy", h=image_request.content)
                if not file_extension:
                    logger.error('Not an image file - ignoring: {}'.format(url))
                else:
                    filename = make_filename(output_directory, file_extension, url)
                    with open(filename, 'wb') as image_file:
                        image_file.write(image_request.content)
                    saved_images_counter += 1
            else:
                logger.error('Error retrieving image {}: Error {}'.format(url, image_request.status_code))
            line_counter += 1
        logger.info('Processed {} lines, saved {} images'.format(line_counter, saved_images_counter,))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        crawl_images(input_file=sys.argv[1])
    elif len(sys.argv) == 3:
        crawl_images(input_file=sys.argv[1], output_directory=sys.argv[2])