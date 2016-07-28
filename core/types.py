from abc import ABCMeta, abstractmethod, abstractproperty

class RosettaStone(object):
    """ Class imodeling our network representation

    """
    layer_type = 'empty'

    def __init__(self, *args, **kwargs):
        pass

class BaseImporter:
    """ Abstract class modeling a base importer
    
    """
    __metaclass__ = ABCMeta

    rosetta = RosettaStone() 

    @abstractmethod
    def load(self, file_path):
        """ Loads a given model file.
            It will call the subroutine to load an specific format
        
        :param file_path: path to the model file
        """
        pass

class CaffeImporter(BaseImporter):
    """ Class modeling a Caffe importer

    """
    def __init__(self):
        pass

    def load(self, file_path):
        print 'Loading Caffe model: %s' % file_path
        return True

