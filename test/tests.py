import unittest
import sys
sys.path.insert(0, '../')

from core.RosettaStone import RosettaStone
from modules.importers.DummyCaffeImporter import DummyCaffeImporter

class MyTest(unittest.TestCase):
    def test_rosetta(self):
        rosetta = RosettaStone()

	A_file = 'my.caffemodel'
	A_type = 'DummyCaffeImporter'

	B_file = 'your.caffemodel'
	B_type = 'DummyCaffeExporter'
	
	# good example
        rosetta.convert(A_file, B_file, A_type, B_type)
	
	# wrong example
	self.assertRaises(Exception, rosetta.convert, A_file, B_file, B_type, A_type)

    def test_base_importer(self):
        caffe_importer = DummyCaffeImporter()

if __name__ == '__main__':
    unittest.main()
