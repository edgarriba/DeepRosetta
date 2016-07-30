from core.BaseImporter import BaseImporter
from modules.config.caffe import caffe_pb2 as caffe_pb2
from modules.config.caffe.layers import *
from modules.config.caffe.equivalences import *
import numpy as np

class CaffeImporter(BaseImporter):
    """ Class modeling a Caffe importer

    """
    def __init__(self):
        self.equivalences = equivalences
        self.layers_type = layers_type
        self.pool_methods = pool_methods
        self.regions = ['across_channels', 'within_channel']

    def blobproto_to_array(self, blob):
        """Convert a Caffe Blob to a numpy array.

        It also reverses the order of all dimensions to [width, height,
        channels, instance].
        """
        dims = []
        if hasattr(blob, 'shape'):
            dims = list(blob.shape.dim)
        if not dims:
            dims = [blob.num, blob.channels, blob.height, blob.width]
        return np.array(blob.data,dtype='float32').reshape(dims)

    def find_layer_by_type(self, dict_, type_):
        for key in dict_:
            if dict_[key]['type'] == type_:
                return key

    def get_data_from_caffemodel(self, file_path):
        print 'Loading Caffe model: %s' % file_path
        data=caffe_pb2.NetParameter()
        caffe_data = open(file_path, 'rb')
        data.ParseFromString(caffe_data.read())
        return data


    def load(self, file_path):
        # open and load caffe model into data
        data = self.get_data_from_caffemodel()

        #read layers
        data_layers_list = data.layers

        output = {}
        output['layers'] = {}
        output['parameters'] = {}

        for layer in data_layers_list:
            layer_type = layer.type if type(layer.type) != int else Importer.layers_type[layer.type]
            name = layer.name
            print('Layer %s (%s)' % (layer_type, name))
            
            if layer_type == 'data':
                continue
            
            converted_type = Importer.find_layer_by_type(Importer.equivalences['layers'], layer_type)
            eq_fields = Importer.equivalences['layers'][converted_type]
            
            output['layers'][name] = {}
            layer_obj = output['layers'][name]
            if layer_type in ['conv', 'Convolution']:
                for field in eq_fields:
                    if field == 'weights_name':
                        weights = Importer.blobproto_to_array(layer.blobs[0]).copy()
                        output['parameters'][name + '_w'] = weights
                        layer_obj['weights_name'] = name + '_w'
                        layer_obj['dim'] = weights.shape
                    elif field == 'biases_name':
                        biases = Importer.blobproto_to_array(layer.blobs[1]).copy()
                        output['parameters'][name + '_b'] = biases
                        layer_obj['biases_name'] = name + '_b'
                    elif field == 'dim':
                        pass
                    elif field == 'type':
                        pass
                    else:
                        prop = eq_fields[field] if eq_fields[field] else field
                        try:
                            layer_obj[field] = getattr(layer.convolution_param, prop)
                        except AttributeError:
                            # for bottom and top
                            layer_obj[field] = getattr(layer, prop)
                            
            elif layer_type in ['relu', 'ReLU']:
                for field in eq_fields:
                    if field == 'type':
                        pass
                    else:
                        prop = eq_fields[field] if eq_fields[field] else field
                        try:
                            layer_obj[field] = getattr(layer.relu_param, prop)
                        except AttributeError:
                            # for bottom and top
                            layer_obj[field] = getattr(layer, prop)
                            
            elif layer_type in ['lrn', 'LRN']:
                for field in eq_fields:
                    if field == 'type':
                        pass
                    elif field == 'norm_region':
                        layer_obj[field] = Importer.regions[getattr(layer.lrn_param, field)]
                    else:
                        prop = eq_fields[field] if eq_fields[field] else field
                        try:
                            layer_obj[field] = getattr(layer.lrn_param, prop)
                        except AttributeError:
                            # for bottom and top
                            layer_obj[field] = getattr(layer, prop)
            
            elif layer_type in ['pool', 'Pooling']:
                for field in eq_fields:
                    if field == 'type':
                        pass
                    elif field == 'pool':
                        layer_obj[field] = Importer.pool_methods[getattr(layer.pooling_param, field)]
                    else:
                        prop = eq_fields[field] if eq_fields[field] else field
                        try:
                            layer_obj[field] = getattr(layer.pooling_param, prop)
                        except AttributeError:
                            # for bottom and top
                            layer_obj[field] = getattr(layer, prop)
                
            elif layer_type in ['inner_product', 'InnerProduct']:
                for field in eq_fields:
                    if field == 'weights_name':
                        weights = Importer.blobproto_to_array(layer.blobs[0]).copy()
                        output['parameters'][name + '_w'] = weights
                        layer_obj['weights_name'] = name + '_w'
                        layer_obj['dim'] = weights.shape
                    elif field == 'biases_name':
                        biases = Importer.blobproto_to_array(layer.blobs[1]).copy()
                        output['parameters'][name + '_b'] = biases
                        layer_obj['biases_name'] = name + '_b'
                    elif field == 'dim':
                        pass
                    elif field == 'type':
                        pass
                    else:
                        prop = eq_fields[field] if eq_fields[field] else field
                        try:
                            layer_obj[field] = getattr(layer.inner_product_param, prop)
                        except AttributeError:
                            # for bottom and top
                            layer_obj[field] = getattr(layer, prop)
                
            elif layer_type in ['dropout', 'Dropout']:
                for field in eq_fields:
                    if field == 'type':
                        pass
                    else:
                        prop = eq_fields[field] if eq_fields[field] else field
                        try:
                            layer_obj[field] = getattr(layer.dropout_param, prop)
                        except AttributeError:
                            # for bottom and top
                            layer_obj[field] = getattr(layer, prop)
                            
            elif layer_type in ['softmax_loss', 'SoftmaxLoss']:
                for field in eq_fields:
                    if field == 'type':
                        pass
                    else:
                        prop = eq_fields[field] if eq_fields[field] else field
                        try:
                            layer_obj[field] = getattr(layer.softmax_param, prop)
                        except AttributeError:
                            # for bottom and top
                            layer_obj[field] = getattr(layer, prop)

        return {}

    def loadFromObject(self, frameworkObj):
        return NotImplementedError

if __name__ == '__main__':
    importer = CaffeImporter()
    file_path = '/home/guillem/git/caffe/models/bvlc_alexnet/bvlc_alexnet.caffemodel'
    output = importer.load(file_path)