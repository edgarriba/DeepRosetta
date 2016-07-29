from abc import ABCMeta, abstractmethod, abstractproperty

class BaseImporter:
    """ Abstract class modeling a base importer

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def load(self, file_path):
        """ Loads a given model file.
            It will call the subroutine to load an specific format

        :param file_path: path to the model file
        """
        return NotImplementedError

    @abstractmethod
    def loadFromObject(self, frameworkObj):
        """ Converts a network object of a framework to a dictionary 
            in the roseta representation. This method should only be 
            implemeted for frameworks that operate in python
            
            :param frameworkObj: a python object containing a trained network
        """
        return NotImplementedError