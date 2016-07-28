import unittest
import sys
sys.path.insert(0, '../')

from core.RosettaStone import RosettaStone
from modules.importers.CaffeFileImporter import Importer

class MyTest(unittest.TestCase):
    def test_rosetta(self):
        rosetta = RosettaStone()
        #self.assertEqual(rosetta.layer_type, 'empty')

        rosetta.layer_type = 'random_type'
        #self.assertEqual(rosetta.layer_type, 'random_type')

    def test_base_importer(self):
       caffe_importer = Importer() 

       #self.assertEqual(caffe_importer.rosetta.layer_type, 'empty')
       #self.assertEqual(caffe_importer.load('empty_path'), True)

if __name__ == '__main__':
    unittest.main()
