import os
import unittest
from image_crawler import crawl_images
from image_crawler import make_filename


class MyTestCase(unittest.TestCase):
    input_file = 'testdata/urllist.txt'
    output_directory = 'test_output'

    def setUp(self):
        try:
            os.mkdir(self.output_directory)
        except FileExistsError:
            pass
        os.system('rm -rf {}/*'.format(self.output_directory))

    def tearDown(self):
        os.system('rm -rf {}'.format(self.output_directory))

    def test_load_images(self):
        crawl_images(input_file=self.input_file, output_directory=self.output_directory)
        num_of_images = len(os.listdir(self.output_directory))
        self.assertEqual(
            5,
            num_of_images,
            'Number of received images should be {}, was {}!'.format(5, num_of_images)
        )

    def test_make_filename(self):
        url = 'http://mywebserver.com/images/24174'
        file_extension = 'jpeg'
        filename = make_filename(self.output_directory, file_extension, url)
        filename_solution = '{}/24174.jpeg'.format(self.output_directory)
        self.assertEqual(filename_solution, filename, 'Image file name is wrong! Check extension')

        url = 'http://mywebserver.com/images/271947.png'
        file_extension = 'jpeg'
        filename = make_filename(self.output_directory, file_extension, url)
        filename_solution = '{}/271947.jpeg'.format(self.output_directory)
        self.assertEqual(filename_solution, filename, 'Image file name is wrong! Check extension')

        url = 'http://mywebserver.com/images/992147.png'
        file_extension = 'png'
        filename = make_filename(self.output_directory, file_extension, url)
        filename_solution = '{}/992147.png'.format(self.output_directory)
        self.assertEqual(filename_solution, filename, 'Image file name is wrong!')

        # create files to check if duplicates are avoided properly
        open('{}/24174.jpg'.format(self.output_directory), 'x').close()
        open('{}/24174_(1).jpg'.format(self.output_directory), 'x').close()

        url = 'http://mywebserver.com/images/24174'
        file_extension = 'jpg'
        filename = make_filename(self.output_directory, file_extension, url)
        filename_solution = '{}/24174_(2).jpg'.format(self.output_directory)
        self.assertEqual(filename_solution, filename, 'Image file name is wrong! Check extension')


if __name__ == '__main__':
    unittest.main()
