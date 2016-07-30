import unittest
import sys
sys.path.insert(0, '../')

from core.RosettaStone import RosettaStone

class MyTest(unittest.TestCase):
    def test_rosetta(self):
        pass
        return
        rosetta = RosettaStone()

        A_file = 'my.caffemodel'
        A_type = 'CaffeImporter'

        B_file = 'your.caffemodel'
        B_type = 'CaffeExporter'
    
        # good example
        rosetta.convert(A_file, B_file, A_type, B_type)
    
        # wrong example
        self.assertRaises(Exception, rosetta.convert, A_file, B_file, B_type, A_type)

    def test_base_importer(self):
        pass
        #from modules.importers.CaffeImporter import CaffeImporter
        #caffe_importer = CaffeImporter()

if __name__ == '__main__':
    unittest.main()
