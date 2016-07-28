# DeepRosetta
An universal deep learning models conversor:

The general idea of this project is to convert any deep learning framework model to an other.
Each deep learning framework has its ows structure representation defined by its layers, parameters and syntax. Thsi structure representation makes difficult to swap from one framework to another. This project tries to solve this problem in a straightforward manner, making it simple for the non-experienced users. This project fills this gap using an inner representation which be the bridge between all deep learning frameworks. 

Input:
There are three kinds of inputs. First the model to be converted, second the name of one of the predifined name models of the file predefined.txt
The user should provide the model to be converted or the name of one of the models predefined in the Model Zoo. As a first step the user is the responsible to convert the image at the correct colorspace of each network.


The user needs only to define the structure representation of the framework models to be converted. The Most of the general structure of the common deep learning frameworks are already provided by this project. But this project is extensable to any other structure framework that is not provided here. So, this inner structure representation is easy to extend and adapt to new layers of  

An exmple : 

Imagine we have a starting Caffe model and we want to translate it to Torch model. 



The structure representation of each model is different.

As a first step, we write an YAML file for each framework model that saves its different layers and parameters  


Secondly, we assign an encoder for each framework model language. the roal of this encoder is to generate a commun representation.

The third step can be done in two different ways. First  method is storing the commun representation is an hdf5 file. This file stores all the needed parameters to rebuild the deep neural network of any other framework. The second method is having a link manager that gives access to the model Zoo of each framework. This link can download the model from the host web page and convert this model without storing on disk.

Fourthly, a decoding step is performed that transformers the inner data representation (hdf5) to the desired framework language model.




So we write the The inner layers and parameters of each one of its layers are 

