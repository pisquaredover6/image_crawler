import os
import unittest
from image_crawler import crawl_images


class MyTestCase(unittest.TestCase):
    input_file = 'testdata/urllist.txt'
    output_directory = 'test_output'

    def test_load_images(self):
        crawl_images(input_file=self.input_file, output_directory=self.output_directory)
        num_of_images = len(os.listdir(self.output_directory))
        self.assertEqual(
            28,
            num_of_images,
            'Number of received images should be {}, was {}!'.format(28, num_of_images)
        )


if __name__ == '__main__':
    unittest.main()
