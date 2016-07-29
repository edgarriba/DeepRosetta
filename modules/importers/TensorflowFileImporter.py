import os
from core.BaseImporter import BaseImporter
import yaml
import numpy as np
from math import ceil

try:
  import tensorflow as tf
  from tensorflow.python.client import graph_util
  from tensorflow.python.framework import tensor_shape
  from tensorflow.python.platform import gfile
except:
    pass


class Importer(BaseImporter):
    """ Class modeling a Tensorflow importer
    """
    def __init__(self):
        with open('./modules/config/Tensorflow/equivalences.yaml', 'r') as infile:
            self.equivalences = yaml.load(infile)
        with open('./core/config.yaml', 'r') as infile:
            self.layer_definitions = yaml.load(infile)
        self.known_ops = [self.equivalences['layers'][key]['type'] for key in self.equivalences['layers']]
        self.known_ops.append('AvgPool')  # TODO: how we handle several equivalencies in one layer type?
        self.util_ops = []
        self.util_ops.append('Const')    # Const ops contain the weights as Tensors
        self.util_ops.append('Identity') # Trivial utility op for reading Const tensors
        self.util_ops.append('BiasAdd')  # BiasAdd op is usually part of a conv or fc layer
        self.util_ops.append('Add')      # Add op is usually part of a conv or fc layer
        self.mapsizes = [] # Needed to calculate paddings 

    def find_const_input(self, node, graph_def):
        """Helper function that finds a 'Const' input of a given node in the tf Graph definition.
           'Const' nodes have the numerical data for the weights stored in its attributes.
        """
        const_input_nodes = [n_ for n_ in graph_def.node if ((n_.op == 'Const' or n_.op == 'Identity') 
                                                        and any(n_.name == s for s in node.input))]
        assert(len(const_input_nodes)==1), 'Unexpected graph definition!'

        # If there is no 'Const' node then we have an 'Identity' node reading from a 'Const'
        if (const_input_nodes[0].op == 'Identity'): 
          const_input_nodes = [n_ for n_ in graph_def.node if (n_.op == 'Const' 
                                    and any(n_.name == s for s in const_input_nodes[0].input))]
          assert(len(const_input_nodes)==1), 'Unexpected graph definition!'

        return const_input_nodes[0]

    def find_bottom_layer_name(self, node, graph_def):
        """ Finds the bottom layer (ignoring unsuported layers and utility nodes)
        """
        valid_inputs = []
        while len(valid_inputs) == 0 and node != None: 
          inputs = [n_ for n_ in graph_def.node if any(n_.name == s for s in node.input)]
          if len(inputs) == 0:
            return ''
          valid_inputs  = [n_ for n_ in inputs if any(n_.op == s for s in self.known_ops)]
          assert(len(valid_inputs)<=1),'This Importer does not allow more than one bottom layer'
          if len(valid_inputs) == 1:
            return str(valid_inputs[0].name)
          else:
            node = inputs[0] # TODO it may be the case we have two unsuported layers
            if (node.op == 'Identity' or node.op == 'Const'):
              if len(inputs)>1: node = inputs[1]
              else: node = None
        return ''

    def find_top_layer_name(self, node, graph_def):
        """ Finds the top layer (ignoring unsuported layers and utility nodes)
        """
        valid_outputs = []
        while len(valid_outputs) == 0 and node != None: 
          outputs = [n_ for n_ in graph_def.node if any(node.name == s for s in n_.input)]
          if len(outputs) == 0:
            return ''
          valid_outputs  = [n_ for n_ in outputs if any(n_.op == s for s in self.known_ops)]
          assert(len(valid_outputs)<=1),'This Importer does not allow more than one top layer'
          if len(valid_outputs) == 1:
            return str(valid_outputs[0].name)
          else:
            node = outputs[0] # TODO it may be the case we have two unsuported layers
        return ''
        
    def find_layer_by_type(self, dict_, type_):
        """ Finds the equvalet Rosseta layer type for a given TF layer type_
        """
        for key in dict_:
            if dict_[key]['type'] == type_:
                return key

    def load(self, file_path):
        """ Loads a Tensorflow graph from protobuf file and converts to Rosseta dict format
        """
        output = {}
        output['layers'] = {}
        output['parameters'] = {}

        print 'Loading Tensorflow model: %s' % file_path
        with gfile.FastGFile(file_path, 'rb') as f:
        
          graph_def = tf.GraphDef()
        
          filename, extension = os.path.splitext(file_path)
          if extension == '.pb':
            graph_def.ParseFromString(f.read())
          else:
            text_format.Merge(f.read(), graph_def)
        
        
          for node in graph_def.node: # each node has .op .name .input .attr
                                      # attr is dict with key value pairs
        
            if any(node.op == s for s in self.known_ops):
              name = node.name
              layer_type = node.op
              converted_type = self.find_layer_by_type(self.equivalences['layers'], layer_type)
              if (layer_type == 'AvgPool'): converted_type = 'PoolingLayer' #TODO fix this!
              output['layers'][name] = {}
              layer_obj = output['layers'][name]
              layer_obj_fields = self.layer_definitions['layers'][converted_type]
              layer_obj['type'] = layer_obj_fields['type']
              if (layer_obj['type'] != 'InputLayer'):
                layer_obj['bottom'] = self.find_bottom_layer_name(node, graph_def)
              layer_obj['top'] = self.find_top_layer_name(node, graph_def)
              #print('Layer op: ' +node.op+' name: '+node.name) 
              #print([at for at in node.attr.keys()])
              inputs = [n_ for n_ in graph_def.node if  any(n_.name == s for s in node.input)]
              outputs = [n_ for n_ in graph_def.node if any(node.name == s for s in n_.input)]
            elif any(node.op == s for s in self.util_ops):
              continue
            else:
              # TODO Reshape nodes seem critical in tf since they specify the way the feature map cuboids are mapped into 2D matrices to feed them to the fully connected layers. Not trivial at all, but seems that the standard is to do it same way as other frameworks do it by default.
              print(' >> Warning: Tensorflow importer to Rossetta does not support "'+node.op+'" Nodes. This node will be ignored!')
              continue
        
            if node.op == 'Placeholder':
              shape = [int(node.attr['shape'].shape.dim.__getitem__(i).size) for i in range(4)]
              layer_obj['dim'] = [shape[3],shape[1],shape[2]]
              self.mapsizes.append((shape[1],shape[2]))

            if node.op == 'Conv2D' or node.op == 'MatMul':
              # we expect here (at least) two input nodes (one bottom layer and one tensor with the weights)
              # and one output node 
              assert(len(inputs)>=2 and len(outputs)>=1), 'Unexpected graph definition!'
        
              # Find 'Const' input and read the tensor with weights
              conv_const_input_node = self.find_const_input(node,graph_def) 
              t_weights = tf.contrib.util.make_ndarray(conv_const_input_node.attr['value'].tensor)
              # filter weights for the Conv2D operation are stored on the second input, and are expected to be in the order [filter_height, filter_width, input_depth, output_depth] (https://www.tensorflow.org/versions/r0.9/how_tos/tool_developers/index.html#weight-formats)
              if node.op == 'Conv2D': t_weights = t_weights.transpose(3,2,0,1)
              output['parameters'][conv_const_input_node.name] = t_weights
              layer_obj['weights_name'] = conv_const_input_node.name
              layer_obj['dim'] = t_weights.shape
        
              # Try to find a 'BiasAdd' in the output nodes and read the tensor with biases (if there are)
              conv_biasAdd_output_nodes = [n_ for n_ in outputs if (n_.op == 'BiasAdd' or n_.op == 'Add')]
              assert(len(conv_biasAdd_output_nodes)<=1), 'Unexpected graph definition!'
              biases_name = 'none'
              if len(conv_biasAdd_output_nodes)==1:
                biasAdd_const_input_node = self.find_const_input(conv_biasAdd_output_nodes[0],graph_def) 
                t_bias = tf.contrib.util.make_ndarray(biasAdd_const_input_node.attr['value'].tensor)
                biases_name = biasAdd_const_input_node.name
              else: # No bias
                t_bias = np.zeros(shape=(t_weights.shape[0],))
              output['parameters'][biases_name] = t_bias
              layer_obj['biases_name'] = biases_name
              # print(node.attr['data_format']) # TODO warning: the default is "NHWC" format with shape [batch, in_height, in_width, in_channels]. but others exist
        
            if node.op == 'MaxPool' or node.op == 'AvgPool':
              # we expect here (at least) one input node and one output node
              assert(len(inputs)>=1 and len(outputs)>=1), 'Unexpected graph definition!'
               
              ksize = [int(i) for i in node.attr['ksize'].list.i]
              layer_obj['kernel_size'] = [ksize[1],ksize[2]]
              layer_obj['pool'] = node.op
                            
            if node.op == 'MaxPool' or node.op == 'AvgPool' or node.op == 'Conv2D':

              layer_obj['stride'] = [int(i) for i in node.attr['strides'].list.i]

              # In tensorflow there are two padding scheme chosen as `'SAME'` or `'VALID'`
              # (https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/ops/nn.py)
              if node.attr[u'padding'].s == u'VALID':
              # For the `'VALID'` the padding values are always zero 
                layer_obj['padding'] = [0,0]
              elif node.attr[u'padding'].s == u'SAME':
              # For the `'SAME'` padding, they are computed as a function of the input height and width
                assert(len(self.mapsizes)>0),'Unexpected graph definition! Node '+node.op+' use SAME as padding strategy but not possible to calculate padding without a Palceholder node'
                last_size = self.mapsizes[len(self.mapsizes)-1]
                in_height = last_size[0]
                in_width  = last_size[1]
                filter_height = layer_obj['dim'][2] if node.op == 'Conv2D' else layer_obj['kernel_size'][0]
                filter_width = layer_obj['dim'][3] if node.op == 'Conv2D' else layer_obj['kernel_size'][1]
                out_height = ceil(float(in_height) / float(layer_obj['stride'][1]))
                out_width = ceil(float(in_width) / float(layer_obj['stride'][2]))
                pad_along_height = ((out_height - 1) * layer_obj['stride'][1] + filter_height - in_height)
                pad_along_width = ((out_width - 1) * layer_obj['stride'][2] + filter_width - in_width)
                layer_obj['padding'] = [pad_along_height,pad_along_width]
                self.mapsizes.append((out_height,out_width))
 
            if node.op == 'Relu':
              # we expect here (at least) one input node and one output node 
              assert(len(inputs)>=1 and len(outputs)>=1), 'Unexpected graph definition!'
              layer_obj['negative_slope'] = None
        
            if node.op == 'Softmax':
              # we expect here one input node and no output node 
              assert(len(inputs)==1 and len(outputs)==0), 'Unexpected graph definition!'
              layer_obj['axis'] = None

            # Check if we have all required fields
            #print('       -  layer_obj: '+str(layer_obj))
            assert(sorted(layer_obj_fields.keys()) == sorted(layer_obj.keys())), 'Layer definition is not complete!'
        print('Done!')
        return output

    def loadFromObject(self, frameworkObj):
        return NotImplementedError

if __name__=='__main__':
    importer = Importer()
    out_model = importer.load('/home/lluis/tensorflow_in_out/mnist/mnist_conv.pb')
    pass
