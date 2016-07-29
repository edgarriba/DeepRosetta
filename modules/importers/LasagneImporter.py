import sys
import cPickle
from core.BaseImporter import BaseImporter
sys.path.insert(0, '../../')



try:
    import lasagne
except:
    pass


class Lasagne2Roseta:
    """ Class modeling a Lasagne importer
    """
    lasagne2CaffeTypes=dict([('DenseLayer','LinearLayer'),
                             ('MaxPool2DLayer','PoolLayer'),
                             ('MaxPool2DDNNLayer','PoolLayer'),
                             ('Pool2DLayer','PoolLayer'),
                             ('Pool2DDNNLayer','PoolLayer'),
                             ('Conv2DLayer','ConvolutionLayer'),
                             ('Conv2DDNNLayer','ConvolutionLayer'),
                             ('InputLayer','InputLayer'),
                             ('NonlinearityLayer','DummyLayer'),
                             ('DropoutLayer','DropoutLayer'),
                             ('rectify','ReLULayer'),
                             ('LeakyRectify','ReLULayer'),
                             ('tanh','TanHLayer'),
                             ('sigmoid','LogsigLayer'),
                             ('softmax','SoftmaxLayer'),
                             ('NonlinearityLayer','DummyLayer')
                             ])
    def paramName(self,x):
        return str(x)+'.'+str(id(x))
    def addLayerNamesIfNotThere(self,outputLayer):
        """This function will make sure all layers have unique layers
        """
        currentLayer=outputLayer
        names=[]
        counter=0
        while 'input_layer' in currentLayer.__dict__.keys():
            if currentLayer.name==None or len(set(names+[currentLayer.name]))!=len((names+[currentLayer.name])):
                currentLayer.name='layer_'+str(counter);
            names.append(currentLayer.name)
            currentLayer=currentLayer.input_layer
            counter+=1
        if currentLayer.name==None or len(set(names+[currentLayer.name]))!=len((names+[currentLayer.name])):
            currentLayer.name='layer_'+str(counter);


    def genParamDict(self,outputLayer):
        self.weightDict=dict([(self.paramName(p),p.get_value()) for p in lasagne.layers.get_all_params(outputLayer)])

    def findParamId(self,paramObj):
        for pId in self.paramDict.keys():
            if self.paramDict[pId]==paramObj:
                return pId
        raise Exception('Object '+str(paramObj)+' not found in parameters')

    def createActivationLayer(self,bottomLayer,topLayer):
        lasagne2CaffeTypes=Lasagne2Roseta.lasagne2CaffeTypes
        #lasagneName=str(type(bottomLayer.nonlinearity))[1:-1].split('.')[-1]
        lasagneName=str(bottomLayer.nonlinearity)[10:].split(' ')[0]
        res= {'type':lasagne2CaffeTypes[lasagneName],'name':bottomLayer.name+'_'+lasagneName}
        if lasagne2CaffeTypes[lasagneName]=='ReLULayer':
            if lasagneName=='LeakyRectify':
                res['negative_slope']=bottomLayer.nonlinearity.leakiness
            else:
                res['negative_slope']=0
        res['bottom']=bottomLayer.name
        if bottomLayer is topLayer:#If this is the output layer
            res['top']=res['name']
        else:
            res['top']=topLayer.name
        return res

    
    def createDummyLayers(self,curLayer,topLayer):
        #used for lasagne.layers.NonlinearityLayer
        layerDict={'top':topLayer.name,'bottom':curLayer.input_layer.name,'name':curLayer.name,'type':'DummyLayer'}
        nonlinearityLayerDict=self.createActivationLayer(curLayer,topLayer)
        layerDict['top']=nonlinearityLayerDict['name']
        return [layerDict,nonlinearityLayerDict]


    def createConvLayers(self,curLayer,topLayer):
        dimSz=curLayer.W.get_value().shape
        dimDict={'neurons':dimSz[0],'channels':dimSz[1],'height':dimSz[2],'width':dimSz[3]}
        layerDict={'top':topLayer.name,'bottom':curLayer.input_layer.name,'type':'ConvolutionLayer','name':curLayer.name,
                   'dim':dimDict,'weights_name':self.findParamId(curLayer.W),'biases_name':self.findParamId(curLayer.b),
                   'stride':list(curLayer.stride),'padding':list(curLayer.pad)
        }
        nonlinearityLayerDict=self.createActivationLayer(curLayer,topLayer)
        layerDict['top']=nonlinearityLayerDict['name']
        return [layerDict,nonlinearityLayerDict]

    def createLinearLayers(self,curLayer,topLayer):
        dimSz=curLayer.W.get_value().shape
        dimDict={'neurons':dimSz[1],'channels':dimSz[0]}
        layerDict={'top':topLayer.name,'bottom':curLayer.input_layer.name,'type':'LinearLayer','name':curLayer.name,
                   'dim':dimDict,'weights_name':self.findParamId(curLayer.W),'biases_name':self.findParamId(curLayer.b),
        }
        nonlinearityLayerDict=self.createActivationLayer(curLayer,topLayer)
        layerDict['top']=nonlinearityLayerDict['name']
        return [layerDict,nonlinearityLayerDict]

    def createPoolingLayers(self,curLayer,topLayer):
        lasagneName=str(type(curLayer))[8:-2].split('.')[-1]
        layerDict={'top':topLayer.name,'bottom':curLayer.input_layer.name,'type':'PoolingLayer','name':curLayer.name,
                   'stride':list(curLayer.stride),'padding':list(curLayer.pad),'kernel_size':list(curLayer.pool_size)}
        if lasagneName in ['MaxPool2DLayer' ,'MaxPool2DDNNLayer']or (lasagneName in ['Pool2DLayer','Pool2DDNNLayer' ]and curLayer.mode=='max'):
            layerDict['pool']='max'
        else:
            raise NotImplementedError
        if curLayer is topLayer:#If this is the output layer
            layerDict['top']=layerDict['name']
        else:
            layerDict['top']=topLayer.name
        return [layerDict]
        #Assuming there is never a Relu layer after pooling
        #nonlinearityLayerDict=self.createActivationLayer(curLayer,topLayer)
        #layerDict['top']=nonlinearityLayerDict['name']
        #return [layerDict,nonlinearityLayerDict]

    def createDropoutLayers(self,curLayer,topLayer):
        layerDict={'top':topLayer.name,'bottom':curLayer.input_layer.name,'name':curLayer.name,'type':'DropoutLayer','dropout_ratio':curLayer.p}
        if curLayer is topLayer:#If this is the output layer
            layerDict['top']=layerDict['name']
        else:
            layerDict['top']=topLayer.name
        return [layerDict]

    def createInputLayers(self,curLayer,topLayer):
        dimSz=curLayer.shape
        if len(dimSz)==2:
            dimDict={'neurons':dimSz[0],'channels':dimSz[1],'height':1,'width':1}
        elif len(dimSz)==4:
            dimDict={'neurons':dimSz[0],'channels':dimSz[1],'height':dimSz[2],'width':dimSz[3]}
        else:
            raise Exception('Input Layers should either have 2 or 4 dimensions')
        layerDict={'top':topLayer.name,'bottom':curLayer.name,'name':curLayer.name,'type':'InputLayer','dim':dimDict}
        if curLayer is topLayer:#If this is the output layer
            layerDict['top']=layerDict['name']
        else:
            layerDict['top']=topLayer.name
        return [layerDict]

    def createLayers(self,curLayer,topLayer):
        """returns a list with dictionaries , one for each layer created"""
        lName=str(type(curLayer))[8:-2].split('.')[-1];
        if lName=='DenseLayer':
            return self.createLinearLayers(curLayer,topLayer)
        elif lName in ['MaxPool2DLayer','Pool2DLayer','MaxPool2DDNNLayer','Pool2DDNNLayer'] :
            return self.createPoolingLayers(curLayer,topLayer)
        elif lName in ['Conv2DLayer','Conv2DDNNLayer']:
            return self.createConvLayers(curLayer,topLayer)
        elif lName=='InputLayer':
            return self.createInputLayers(curLayer,topLayer)
        elif lName=='DropoutLayer':
            return self.createDropoutLayers(curLayer,topLayer)
        elif lName=='NonlinearityLayer':
            return self.createDummyLayers(curLayer,topLayer)
        else:
            raise Exception('Inrecognised layer type '+lName)

    def __eval__(self, lasagneOutputLayer):
        self.addLayerNamesIfNotThere(lasagneOutputLayer)
        self.paramDict=dict([(self.paramName(p),p) for p in lasagne.layers.get_all_params(lasagneOutputLayer)])
        curLayer=lasagneOutputLayer
        topLayer=lasagneOutputLayer
        allLayers=[]
        while str(type(curLayer))[8:-2].split('.')[-1]!='InputLayer':
            allLayers+=self.createLayers(curLayer,topLayer)
            topLayer=curLayer
            curLayer=curLayer.input_layer
        allLayers+=self.createLayers(curLayer,topLayer)
        layerDict = dict([(l['name'],l) for l in allLayers])
        npParamDict={}
        for k in self.paramDict.keys():
            npParamDict[k]=self.paramDict[k].get_value()
        res={'parameters':npParamDict,'layers':layerDict}
        del self.paramDict #no longer needed
        return res


class LasagneImporter(BaseImporter):
    def loadFromObject(self,lasagneOutputLayer):
        functor=Lasagne2Roseta()
        return functor(lasagneOutputLayer)


if __name__=='__main__':
    il=lasagne.layers.InputLayer((None,1,28,28),name='input')
    c1=lasagne.layers.Conv2DLayer(il,32,(5,5),pad=(2,2),name='c1')
    p1=lasagne.layers.Pool2DLayer(c1,(2,2),stride=(2,2),name='p1')
    c2=lasagne.layers.Conv2DLayer(p1,64,(5,5),pad=(2,2),name='c2')
    p2=lasagne.layers.Pool2DLayer(c2,(2,2),stride=(2,2),name='p2')
    fc1=lasagne.layers.DenseLayer(p2,256,name='fc1')
    do1=lasagne.layers.DropoutLayer(fc1,0.5,name='do1')
    fc2=lasagne.layers.DenseLayer(do1,256,name='fc2')
    do2=lasagne.layers.DropoutLayer(fc2,0.5,name='do2')
    fc3=lasagne.layers.DenseLayer(do2,10,nonlinearity=lasagne.nonlinearities.softmax,name='fc3')
    functor=Lasagne2Roseta()
    cPickle.dump(functor(fc3),open('/tmp/lasagne_untrained_network.cPickle','w'))
