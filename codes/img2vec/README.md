# Image 2 Vec with PyTorch
 Use pre-trained models (or do not pre-trained) in PyTorch to extract vector embeddings from any image and calculate their similarity.

## Available models
['resnet-18', 'alexnet', 'vgg19_bn', 'vgg_19bn_attention', 'squeezenet1_1', 'inception_v3', 'Densenet121']

## Installation

Tested on Python 3.6

Pytorch: http://pytorch.org/

Pillow:  ```pip install Pillow```

Sklearn ```pip install scikit-learn```

## Running the example
```
git clone https://github.com/weimin17/pdfminer-textmining-word2vec-img2vec.git

cd codes/img2vec/example

python test_img_to_vec.py

```


## Using img2vec as a library
```
from img_to_vec import Img2Vec
from PIL import Image

# Initialize Img2Vec with GPU
img2vec = Img2Vec(cuda=True)

# Read in an image
img = Image.open('test.jpg')
# Get a vector from img2vec
vec = img2vec.get_vec(img)
```
#### Expected output
```
cat.jpg
0.72832 cat2.jpg
0.641478 catdog.jpg
0.575845 face.jpg
0.516689 face2.jpg

face2.jpg
0.668525 face.jpg
0.516689 cat.jpg
0.50084 cat2.jpg
0.484863 catdog.jpg

```

Try adding your own photos!


#### Img2Vec Params
**cuda** = (True, False) ; # Run on GPU?  default: False
**model** = ('resnet-18', 'alexnet')   # Which model to use?   default: 'resnet-18'
**layer** = 'layer_name' or int   # For advanced users, which layer of the model to extract the output from.  default: 'avgpool' 
**layer_output_size** = int   # Size of the output of your selected layer

### [Resnet-18](http://pytorch-zh.readthedocs.io/en/latest/_modules/torchvision/models/resnet.html)
Defaults: (layer = 'avgpool', layer_output_size = 512)<br>
Layer parameter must be an string representing the name of a  layer below
```python
conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
bn1 = nn.BatchNorm2d(64)
relu = nn.ReLU(inplace=True)
maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
layer1 = self._make_layer(block, 64, layers[0])
layer2 = self._make_layer(block, 128, layers[1], stride=2)
layer3 = self._make_layer(block, 256, layers[2], stride=2)
layer4 = self._make_layer(block, 512, layers[3], stride=2)
avgpool = nn.AvgPool2d(7)
fc = nn.Linear(512 * block.expansion, num_classes)
```
### [Alexnet](http://pytorch-zh.readthedocs.io/en/latest/_modules/torchvision/models/alexnet.html)
Defaults: (layer = 2, layer_output_size = 4096)
Layer parameter must be an integer representing one of the layers below
```python
alexnet.classifier = nn.Sequential(
            7. nn.Dropout(),                  < - output_size = 9216
            6. nn.Linear(256 * 6 * 6, 4096),  < - output_size = 4096
            5. nn.ReLU(inplace=True),         < - output_size = 4096
            4. nn.Dropout(),		      < - output_size = 4096
            3. nn.Linear(4096, 4096),	      < - output_size = 4096
            2. nn.ReLU(inplace=True),         < - output_size = 4096
            1. nn.Linear(4096, num_classes),  < - output_size = 4096
        )
```
###other models
You could also add other models like vgg, vgg19_attention, as long as you changes the following:

* Add model.py file in folder `img2vec`, like `model_vgg19bn_attention.py`.
* Change `model_zoo = ['resnet-18', 'alexnet', 'vgg19_bn', 'vgg_19bn_attention', 'squeezenet1_1', 'inception_v3', 'Densenet121']` in `test_img_to_vec.py`.
* Revise `_get_model_and_layer` in `img_to_vec.py`.
* In `get_vec` from `img_to_vec.py`, you need also change two lines: 
Alexnet/vgg: `my_embedding = torch.zeros(1, self.layer_output_size)` and `return my_embedding.numpy()[0, :]`
Resnet-18: `my_embedding = torch.zeros(1, self.layer_output_size,1, 1)` and `return my_embedding.numpy()[0, :, 0, 0]`

### return selected layer(last layer)

```
# 1 Freeze training for all layers
for param in model.features.parameters():
    param.require_grad = False

# Newly created modules have require_grad=True by default
num_features = model.classifier[6].in_features
features = list(model.classifier.children())[:-1]  # Remove last layer
features.extend([nn.Linear(num_features, 4096)])  # Add our layer with 4 outputs
model.classifier = nn.Sequential(*features)  # Replace the model classifier
print(model)
# 2remove last fully-connected layer
new_classifier = nn.Sequential(*list(model.classifier.children())[:-1])
model.classifier = new_classifier
# 3# remove last fully-connected layer
new_classifier = nn.Sequential(*list(model.classifier.children())[:-1])
model.classifier = new_classifier
#4
# 
model = models.vgg19(pretrained=True)
# Number of filters in the bottleneck layer
num_ftrs = model.classifier[6].in_features
# convert all the layers to list and remove the last one
features = list(model.classifier.children())[:-1]
## Add the last layer based on the num of classes in our dataset
features.extend([nn.Linear(num_ftrs, 4)])
## convert it into container and add it to our model class.
model.classifier = nn.Sequential(*features)
```

This work is inspired by [Extract a feature vector for any image with PyTorch](https://becominghuman.ai/extract-a-feature-vector-for-any-image-with-pytorch-9717561d1d4c).
