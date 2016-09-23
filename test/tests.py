import unittest

import DeepRosetta as dr

class MyTest(unittest.TestCase):
    def test_rosetta(self):
        rosetta = dr.RosettaStone()

        A_file = 'my.caffemodel'
        A_type = 'DummyCaffeImporter'

        B_file = 'your.caffemodel'
        B_type = 'DummyCaffeExporter'
    
        # good example
        rosetta.convert(A_file, B_file, A_type, B_type)
    
        # wrong example
        self.assertRaises(Exception, rosetta.convert, A_file, B_file, B_type, A_type)


if __name__ == '__main__':
    unittest.main()
