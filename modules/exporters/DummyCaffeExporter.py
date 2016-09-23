from core.BaseExporter import BaseExporter

class DummyCaffeExporter(BaseExporter):
    """ Class modeling a Caffe exporter 

    """
    def __init__(self):
        pass

    def save(self, file_path):
        print 'Saving Caffe model: %s' % file_path
        return {}
    
    def toObject(self, rosetaDict):
        raise NotImplementedError
