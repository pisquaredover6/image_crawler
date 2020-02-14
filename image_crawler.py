#!/usr/bin/env python3

import logging
import requests
import sys

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger('')


with open(sys.argv[1], 'r') as input_list:
    output_directory = sys.argv[2]
    # read plaintext file line by line
    for line in input_list:
        url = line.rstrip('\n')
        try:
            image_request = requests.get(url)
        except Exception as e:
            logger.error('Error at image {} - ignoring. {}'.format(url, e))
            continue

        if image_request.status_code == 200:
            filename = '{}/{}'.format(output_directory, url.rsplit('/', 1)[1])
            with open(filename, 'wb') as image_file:
                image_file.write(image_request.content)
