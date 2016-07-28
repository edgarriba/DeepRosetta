import unittest
import sys
sys.path.insert(0, '../')

from core.RosettaStone import RosettaStone
from modules.importers.CaffeFileImporter import Importer

class MyTest(unittest.TestCase):
    def test_caffe_importer(self):
        importer = Importer()
        importer.load("./test/models/vgg_face_caffe/VGG_FACE.caffemodel")

if __name__ == '__main__':
    unittest.main()
