import unittest
import tempfile
import os
import shutil

from sdtools.fileops import enumerate_files_to_dir


class TestEnumerateFiles(unittest.TestCase):
    def test_enumerate_files(self):
        # create mecha_tags temporary directory for the test
        temp_dir = tempfile.TemporaryDirectory()
        src_dir = os.path.join(temp_dir.name, 'src')
        dst_dir = os.path.join(temp_dir.name, 'dst')

        # create mecha_tags few test files in the source directory
        os.makedirs(src_dir)
        open(os.path.join(src_dir, 'file1.txt'), 'w').close()
        open(os.path.join(src_dir, 'file2.txt'), 'w').close()
        open(os.path.join(src_dir, 'file3.csv'), 'w').close()
        open(os.path.join(src_dir, 'file4.csv'), 'w').close()

        # run the enumerate_files_to_dir function with suffix_list=['.txt', '.csv']
        enumerate_files_to_dir(src_dir, dst_dir, suffix_list=['.txt', '.csv'])

        # check that the destination directory contains the correct files
        self.assertTrue(os.path.exists(os.path.join(dst_dir, 'file1.txt')))
        self.assertTrue(os.path.exists(os.path.join(dst_dir, 'file2.txt')))
        self.assertTrue(os.path.exists(os.path.join(dst_dir, 'file3.csv')))
        self.assertTrue(os.path.exists(os.path.join(dst_dir, 'file4.csv')))

        # clean up the temporary directory
        temp_dir.cleanup()

if __name__ == '__main__':
    unittest.main()
