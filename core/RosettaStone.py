import os

class RosettaStone(object):
    """ Class imodeling our network representation

    """
    def __init__(self, *args, **kwargs):
        self.importers = self.list_importers()
        self.exporters = self.list_exporters()

    def load_list(self, module):
    	""" Loads a list of files ended with *.py format in a given module
	
    	:param module: string with the relative module name
    	"""
        list_obj = (d for d in os.listdir(module) if d.endswith('.py'))
	return list(list_obj)

    def list_importers(self):
    	""" Loads the list of files inside 'modules/importers'

    	"""
        return self.load_list('modules/importers')

    def list_exporters(self):
    	""" Loads the list of files inside 'modules/exporters'
   
    	"""
        return self.load_list('modules/exporters')
	
    def check_parser_type(self, list_types, parser_type):
	""" Check if a substring is in a strings list.
	
	:param list_types: a strings list
	:param parser_type: the substring to find

	:return: Raises an Exception in case substring is not found
	"""
	if not any(parser_type in s for s in list_types):
	    raise Exception('The parser type is not available: %s' % parser_type)

    def import_module(self, module, klass):
        """ Imports a class given a modules and the class name
    
        Is assumed that the package and class names are the same.

        :param module: string with the module name
        :param klass: string with the class name
    
        :return: the class instance
        """
        mod = __import__(module + '.' + klass, fromlist=[klass])
        return getattr(mod, klass)()

    def convert(self, input_file, output_file, input_format, output_format):
        """ Function that converts from one framework to a another

        :param input_file: path to the model file to be exported
        :param output_file: path to the exported model file
        :param input_format: type of the model to be exported
        :param output_format: type of the exported model

        :return: None
        """
	# check if parser exists
	self.check_parser_type(self.importers, input_format)
	self.check_parser_type(self.exporters, output_format)

	# instantiate importer and exporter
        importer = self.import_module('modules.importers', input_format)
        exporter = self.import_module('modules.exporters', output_format)
        
	# load and save
	# exporter.save(importer.load(input_file), output_file)
