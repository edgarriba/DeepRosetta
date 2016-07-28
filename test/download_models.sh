# Downloads models of various formats for test purposes

# Create the directory for downloaded models
if [ ! -d ./test/models ]; then
    mkdir ./test/models
fi

# CAFFE: VGG Face model (http://www.robots.ox.ac.uk/~vgg/software/vgg_face/)
if [ ! -f ./test/models/vgg_face_caffe/VGG_FACE.caffemodel ]; then
    echo "Downloading Caffe model..."
    wget http://www.robots.ox.ac.uk/~vgg/software/vgg_face/src/vgg_face_caffe.tar.gz -O ./test/models/vgg_face_caffe.tar.gz
    tar -xvf ./test/models/vgg_face_caffe.tar.gz -C ./test/models/
    echo "OK"
else
    echo "Caffe model already downloaded..."
fi


# TENSORFLOW: Inception model (http://arxiv.org/abs/1512.00567)
if [ ! -f ./test/models/tensorflow_inception_graph.pb ]; then
    echo "Downloading TensorFlow model..."
    wget https://storage.googleapis.com/download.tensorflow.org/models/inception_dec_2015.zip -O ./test/models/inception_dec_2015.zip

    # Unzip the model (resulting file will be )
    unzip ./test/models/inception_dec_2015.zip -d ./test/models/
    echo "OK"
else
    echo "TensorFlow model already downloaded..."
fi

# MATCONVNET: VGG Face model (http://www.robots.ox.ac.uk/~vgg/software/vgg_face/)
if [ ! -f ./test/models/vgg_face_matconvnet/data/vgg_face.mat ]; then
    echo "Downloading MatConvNet model..."
    wget http://www.robots.ox.ac.uk/~vgg/software/vgg_face/src/vgg_face_matconvnet.tar.gz -O ./test/models/vgg_face_matconvnet.tar.gz
    tar -xvf ./test/models/vgg_face_matconvnet.tar.gz -C ./test/models/
    echo "OK"
else
    echo "MatConvNet model already downloaded..."
fi


# TORCH: VGG Face model (http://www.robots.ox.ac.uk/~vgg/software/vgg_face/)
if [ ! -f ./test/models/vgg_face_torch/VGG_FACE.t7 ]; then
    echo "Downloading Torch model..."
    wget http://www.robots.ox.ac.uk/~vgg/software/vgg_face/src/vgg_face_torch.tar.gz -O ./test/models/vgg_face_torch.tar.gz
    tar -xvf ./test/models/vgg_face_torch.tar.gz -C ./test/models/
    echo "OK"
else
    echo "Torch model already downloaded..."
fi