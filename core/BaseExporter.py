from abc import ABCMeta, abstractmethod, abstractproperty
import os

class BaseExporter:
    """ Abstract class modeling a base importer

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def save(self, file_path):
        """ Loads a given model file.
            It will call the subroutine to load an specific format

        :param file_path: path to the model file
        """
        raise NotImplementedError

    @abstractmethod
    def toObject(self, rosetaDict):
        """Generates a python object with a trained network from a
           dictionary in the rosetaFormat.

        :param rosetaDict: the roseta dictionary
        """
        raise NotImplementedError
