![Alt text](docs/img/Head-logo_V1.png?raw=true "Deep Rosetta logo")

[![Join the chat at https://gitter.im/edgarriba/DeepRosetta](https://badges.gitter.im/edgarriba/DeepRosetta.svg)](https://gitter.im/edgarriba/DeepRosetta?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/edgarriba/DeepRosetta.svg?branch=master)](https://travis-ci.org/edgarriba/DeepRosetta)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)  

An universal deep learning models conversor :shipit:

The general idea of this project is to convert any deep learning framework model to another.
Each deep learning framework has its own structure representation defined by its layers, parameters and syntax. This structure representation makes difficult to swap from one framework to another. The project tries to solve this problem in a straightforward manner, making it simple for the non-experienced users. The project fills this gap using an inner representation which is the bridge between all deep learning frameworks.

General Usage
-------------
You can convert from one framework to another

    import DeepRosetta as dr

    if __name__ == '__main__':
        rosetta = dr.RosettaStone()
        rosetta.convert('my.caffemodel', 'your.caffemodel', 'DummyCaffeImporter', 'DummyCaffeExporter')

        print 'All went OK!'
  
Supported formats
-----------------
- Importers
  - [x] CaffeImporter
  - [x] MatConvnetImporter
  - [x] LasagneImporter
  - [ ] TorchImporter
  - [x] TensorflowImporter
  - [ ] ChainerImporter
  - [ ] TinyCNNImporter

- Exporters
  - [ ] CaffeExporter
  - [ ] MatConvnetExporter
  - [x] LasagneExporter
  - [ ] TorcExporter
  - [ ] TensorflowExporter
  - [ ] ChainerExporter
  - [ ] TinyCNNExporter

Contributing
------------
Developers are needed! Check our Contribution Documents.

Licence
-------
the BSD 3-Clause Licence
