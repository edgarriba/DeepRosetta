import sys
sys.path.insert(0, '../../')

from core.BaseImporter import BaseImporter
from modules.config.caffe import caffe_pb2 as caffe_pb2
from modules.config.caffe.layers import *
import numpy as np

def blobproto_to_array(blob):
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

class Importer(BaseImporter):
    """ Class modeling a Caffe importer

    """
    def __init__(self):
        pass

    def load(self, file_path):
        print 'Loading Caffe model: %s' % file_path

        # open and load caffe model into data
        data=caffe_pb2.NetParameter()
        caffe_data = open(file_path, 'rb')
        data.ParseFromString(caffe_data.read())

        #read layers
        data_layers_list = data.layers

        for layer in data_layers_list:
            layer_type = layer.type if type(layer.type) != int else layers_type[layer.type]
            print('Layer %s (%s)' % (layer_type, layer.name))

            if layer_type in ['conv', 'Convolution']:
                print('\tkernel_size: %s' % layer.convolution_param.kernel_size)
                print('\tnum_output: %s' % layer.convolution_param.num_output)
                print('\tstride: %s' % layer.convolution_param.stride)
                print('\tpad: %s' % layer.convolution_param.pad)
                print('\tweights: %i,%i,%i,%i' % blobproto_to_array(layer.blobs[0]).shape)
                print('\tbiases: %i,%i,%i,%i' % blobproto_to_array(layer.blobs[1]).shape)
                print('')
            elif layer_type in ['relu', 'ReLU']:
                print('')
            elif layer_type in ['lrn', 'LRN']:
                print('\tlocal_size: %s' % layer.lrn_param.local_size)
                print('\talpha: %s' % layer.lrn_param.alpha)
                print('\tbeta: %s' % layer.lrn_param.beta)
                print('\tk: %s' % layer.lrn_param.k)
                regions = ['across_channels', 'within_channel']
                print('\tnorm_region: %s' % regions[layer.lrn_param.norm_region])
            elif layer_type in ['pool', 'Pooling']:
                print('\tpool: %s' % pool_methods[layer.pooling_param.pool])
                print('\tstride: %s' % layer.pooling_param.stride)
                print('\tpad: %s' % layer.pooling_param.pad)
                print('\tkernel_size: %s' % layer.pooling_param.kernel_size)
                print('')
            elif layer_type in ['inner_product', 'InnerProduct']:
                print('\tweights: %i,%i,%i,%i' % blobproto_to_array(layer.blobs[0]).shape)
                print('\tbiases: %i,%i,%i,%i' % blobproto_to_array(layer.blobs[1]).shape)
                print('')
            elif layer_type in ['dropout', 'DROPOUT']:
                print('\tdropout_ratio: %s' % layer.dropout_param.dropout_ratio)
                print('')
            elif layer_type in ['softmax_loss', 'SOFTMAX']:
                print('\taxis: %s' % layer.softmax_param.axis)
                print('')

        return {}