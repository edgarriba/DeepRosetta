![Alt text](docs/Head-logo_V1.png?raw=true "Deep Rosetta logo")

[![Join the chat at https://gitter.im/edgarriba/DeepRosetta](https://badges.gitter.im/edgarriba/DeepRosetta.svg)](https://gitter.im/edgarriba/DeepRosetta?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/edgarriba/DeepRosetta.svg?branch=master)](https://travis-ci.org/edgarriba/DeepRosetta)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)  

An universal deep learning models conversor :shipit:



The general idea of this project is to convert any deep learning framework model to an other.
Each deep learning framework has its ows structure representation defined by its layers, parameters and syntax. Thsi structure representation makes difficult to swap from one framework to another. This project tries to solve this problem in a straightforward manner, making it simple for the non-experienced users. This project fills this gap using an inner representation which be the bridge between all deep learning frameworks. 

- Input:
The system requires two inputs: (1)the model and (2)the framework language name of the result model. (1)The model can be specified in three ways: first the file model to be converted depending on the framework, second the name of one of the predifined models, thirdly a link which will be downloaded aumotatically. (2) The name could be such as 'Torch', 'Caffe', etc. 

- Output: 
The converted model in the desired framework type. The output can be for example a '.caffemodel' or '.t7' file.

- The architecture of this project:
  1. YAML layer:
    1.  YAML inner representation: this file contains all the common names and parameters.
    2. YAML map file: This layer contains a dictionary to map from each one of the components and paramteres, of a specific framework, to the inner representation of this project (which is YAML inner representation). 
  2. Core layer:
    1.  Importer: we have one encoder associated to each framework model language. 
    2. Roseta Stone: It can be done in two different ways. First  method is storing the common representation is an hdf5 file at disk. This file stores all the needed parameters to rebuild the deep neural network of any other framework. The second method is not storing at disk and do all the operations in memory. 
    3. Exporter: transforms the inner data representation (hdf5) to the desired framework language model.
    
- Folder structure:
  1. core: Roseta Stone, Abstract classes of importers and exporters.
  2. io: 
    * Config: YAML files
    * Exporters: encoder of each model
    * Importers: decoder of each model
  3. test: test files

- General Schema:
![Alt text](docs/RosettaStone.png?raw=true "Deep Rosetta architecture")
