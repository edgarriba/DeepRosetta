import unittest
import sys
sys.path.insert(0, '../')

from core.RosettaStone import RosettaStone
from modules.importers.CaffeFileImporter import Importer

class MyTest(unittest.TestCase):
    def test_rosetta(self):
        rosetta = RosettaStone()

    def test_base_importer(self):
       caffe_importer = Importer() 

if __name__ == '__main__':
    unittest.main()
