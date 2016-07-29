#!/usr/bin/env python
import lasagne
from core.BaseExporter import BaseExporter

class Roseta2Lasagne:
    def __init__(self,useCuDNN=False):
        self.convertDict={
            'InputLayer':lambda d:lasagne.layers.InputLayer([d['dim']['neurons'],d['dim']['channels'],d['dim']['height'],d['dim']['width']]),
            'LinearLayer':lambda d,bot:lasagne.layers.DenseLayer(bot,d['dim']['neurons'],W=d['weights_obj'],b=d['biases_obj'],name=d['name']),
            'ConvolutionLayer':lambda d,bot:lasagne.layers.Conv2DLayer(bot,d['dim']['neurons'],(d['dim']['width'],d['dim']['height']),stride=d['stride'],pad=d['padding'],W=d['weights_obj'],b=d['biases_obj'],name=d['name']),
            'PoolingLayer':lambda d,bot:lasagne.layers.Pool2DLayer(bot,d['kernel_size'],stride=d['stride'],pad=d['padding'],name=d['name']),
            'DropoutLayer':lambda d,bot:lasagne.layers.DropoutLayer(bot,d['dropout_ratio'],name=d['name']),
            'DummyLayer':lambda d,bot:lasagne.layers.NonlinearityLayer(bot,nonlinearity=None,name=d['name']),
            'SoftmaxLayer':lambda d,bot:lasagne.layers.NonlinearityLayer(bot,nonlinearity=lasagne.nonlinearities.softmax,name=d['name']),
            'SigmoidLayer':lambda d,bot:lasagne.layers.NonlinearityLayer(bot,nonlinearity=lasagne.nonlinearities.sigmoid,name=d['name']),
            'TanHLayer':lambda d,bot:lasagne.layers.NonlinearityLayer(bot,nonlinearity=lasagne.nonlinearities.tanh,name=d['name']),
            'ReLULayer':lambda d,bot:lasagne.layers.NonlinearityLayer(bot,nonlinearity=lasagne.nonlinearities.LeakyRectify(d['negative_slope']),name=d['name']),
        }
        if useCuDNN:
            self.convertDict['ConvolutionLayer']=lambda d,bot:lasagne.layers.dnn.Conv2DDNNLayer(bot,d['dim']['neurons'],(d['dim']['width'],d['dim']['height']),stride=d['stride'],pad=d['padding'],W=d['weights_obj'],b=d['biases_obj'],name=d['name']),
            self.convertDict['PoolingLayer']=lambda d,bot:lasagne.layers.dnn.Pool2DDNNLayer(bot,d['kernel_size'],stride=d['stride'],pad=d['padding'],name=d['name']),

    def generateTheanoSharedFromNumpy(self,paramDict):
        theanoDict={}
        for k in paramDict.keys():
            if len(paramDict[k].shape)==1:#if bias
                theanoDict[k]=lasagne.layers.DenseLayer(lasagne.layers.InputLayer([None,1]),paramDict[k].shape[0],b=paramDict[k]).b
            elif len(paramDict[k].shape)==2:#if weights of dense
                theanoDict[k]=lasagne.layers.DenseLayer(lasagne.layers.InputLayer([None,paramDict[k].shape[0]]),paramDict[k].shape[1],W=paramDict[k]).W
            elif len(paramDict[k].shape)==4:#if weights of dense
                theanoDict[k]=lasagne.layers.Conv2DLayer(lasagne.layers.InputLayer([None,paramDict[k].shape[1],10,10]),paramDict[k].shape[0],paramDict[k].shape[2:],W=paramDict[k]).W
            else:
                print '\n\n',k,'\n\n'
                raise Exception('Could not convert weigth mat '+k+' to theano shared object')
        return theanoDict

    def getInputLayers(self,layerDict):
        res=[]
        for k in layerDict.keys():
            if layerDict[k]['bottom']==layerDict[k]['name']:
                res.append(layerDict[k])
        return res

    def __call__(self,d):
        allParams=self.generateTheanoSharedFromNumpy(d['parameters'])
        allLayers=d['layers']
        for k in allLayers.keys():
            allLayers[k]['name']=k
            if 'weights_name' in allLayers[k].keys():
                allLayers[k]['weights_obj']=allParams[allLayers[k]['weights_name']]
            if 'biases_name' in allLayers[k].keys():
                allLayers[k]['biases_obj']=allParams[allLayers[k]['biases_name']]
        inputLayers=self.getInputLayers(allLayers)
        if len(inputLayers)>1:
            raise Exception('For the moment roseta lasagne experter supports only a sigle input layer')
        curLayerName=inputLayers[0]['name']
        nextLayerName=inputLayers[0]['top']
        print 'TYPE', inputLayers[0]['type'],'\n',inputLayers[0]
        curLayer=self.convertDict[inputLayers[0]['type']](inputLayers[0])
        while nextLayerName!=curLayerName:#assuming a single output layer
            curLayerName=nextLayerName
            curLayer=self.convertDict[allLayers[curLayerName]['type']](allLayers[curLayerName],curLayer)
            nextLayerName=allLayers[curLayerName]['top']
        return curLayer


class LasagneExporter(BaseExporter):
    def toObject(self,rosetaDict):
        functor= Roseta2Lasagne(False)
        return functor(rosetaDict)


if __name__=='__main__':
    pass
