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
        for d in os.listidr('importers'):
            if 'Importer' in d:
                importers.append(d)
        return importers

    def list_exporters(self):
        exporters = []
        for d in os.listidr('exporters'):
            if 'Exporter' in d:
                exporters.append(d)
        return exporters

    def convert(self, input, output, input_format='', output_format=''):
        assert(input_format in self.importers)
        assert(output_format in self.exporters)
        Importer = import_module(os.path.join('io','importers',input_format))
        Exporter = import_module(os.path.join('io', 'exporters', export_format))
        Exporter.save(Importer.load(input), output)



