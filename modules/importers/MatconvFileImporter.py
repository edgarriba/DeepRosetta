import os
from core.BaseImporter import BaseImporter
from scipy.io import loadmat
import yaml

class Importer(BaseImporter):
    def __init__(self):
        with open('./modules/config/Matconv/equivalences.yaml', 'r') as infile:
            self.equivalences = yaml.load(infile)
        self.bottom = None

    def find_layer_by_type(self, dict_, type_):
        for key in dict_:
            if dict_[key]['type'] == type_:
                return key

    def load(self, file_path):
        output = {}
        output['layers'] = {}
        output['parameters'] = {}
        model = loadmat(file_path)['layers'][0]
        for index, layer in enumerate(model):
            layer_type = layer['type'][0][0][0]
            name = layer['name'][0][0][0]
            if layer_type == 'conv' and 'fc' in name:
                layer_type = 'fc'
            converted_type = self.find_layer_by_type(self.equivalences['layers'], layer_type)
            eq_fields = self.equivalences['layers'][converted_type]

            output['layers'][name] = {}
            layer_obj = output['layers'][name]
            for field in eq_fields:
                if layer_type == 'conv' or layer_type == 'fc':
                    if field == 'weights_name':
                        weights = layer[eq_fields[field]].item()[0][0].copy()
                        weights = weights.transpose(3,2,0,1)
                        output['parameters'][name + '_w'] = weights
                        layer_obj['weights_name'] = name + '_w'
                        layer_obj['dim'] = weights.shape
                    elif field == 'biases_name':
                        try:
                            biases = layer[eq_fields[field]].item()[0][1].copy()
                            output['parameters'][name + '_b'] = biases
                            layer_obj['biases_name'] = name + '_b'
                        except:
                            pass
                elif layer_type == 'lrn':
                    if field == 'local_size':
                        layer_obj['local_size'] = layer['param'][0][0][0][0]
                    elif field == 'kappa':
                        layer_obj['kappa'] = layer['param'][0][0][0][1]
                    elif field == 'alpha':
                        layer_obj['alpha'] = layer['param'][0][0][0][0]*layer['param'][0][0][0][1]
                    elif field == 'beta':
                        layer_obj['beta'] = layer['param'][0][0][0][3]
                if field == 'bottom':
                    layer_obj['bottom'] = self.bottom
                    self.bottom = name
                elif field == 'top':
                    if index + 1 < len(model):
                        layer_obj['top'] = model[index + 1]['name'][0][0][0]
                    else:
                        layer_obj['top'] = None
                else:
                    if eq_fields[field] in layer.dtype.names:
                        layer_obj[field] = layer[eq_fields[field]][0][0][0]
                    else:
                        layer_obj[field] = eq_fields[field]
        return output

if __name__=='__main__':
    importer = Importer()
    output = importer.load('/Users/prlz77/Downloads/imagenet-vgg-f.mat')
    pass