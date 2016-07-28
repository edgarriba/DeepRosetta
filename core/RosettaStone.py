from importlib import import_module
import os

class RosettaStone(object):
    """ Class imodeling our network representation

    """
    def __init__(self, *args, **kwargs):
        self.importers = self.list_importers()
        self.exporters = self.list_exporters()

    def list_importers(self):
        importers = []
        for d in os.listdir('../modules/importers'):
            if 'Importer' in d:
                importers.append(d)
        return importers

    def list_exporters(self):
        exporters = []
        for d in os.listdir('../modules/exporters'):
            if 'Exporter' in d:
                exporters.append(d)
        return exporters

    def convert(self, input, output, input_format='', output_format=''):
        assert(input_format in self.importers)
        assert(output_format in self.exporters)
        importer = import_module("modules.importers.%s" %input_format).Importer()
        exporter = import_module("modules.exporters.%s" %output_format).Importer()
        exporter.save(importer.load(input), output)



