import DeepRosetta as dr

if __name__ == '__main__':
    rosetta = dr.RosettaStone()
    rosetta.convert('my.caffemodel', 'your.caffemodel', 'DummyCaffeImporter', 'DummyCaffeExporter')

    print 'All went OK!'
