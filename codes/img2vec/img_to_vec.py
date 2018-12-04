import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable
from model_vgg19bn_attention import vgg19_bn_attention


class Img2Vec():

    def __init__(self, cuda=False, model='resnet-18', layer='default', layer_output_size=512):
    # def __init__(self, cuda=False, model='alexnet', layer=3, layer_output_size=4096):
        """ Img2Vec
        :param cuda: If set to True, will run forward pass on GPU
        :param model: String name of requested model
        :param layer: String or Int depending on model.  See more docs: https://github.com/christiansafka/img2vec.git
        :param layer_output_size: Int depicting the output size of the requested layer
        """
        self.device = torch.device("cuda" if cuda else "cpu")
        self.layer_output_size = layer_output_size
        self.model, self.extraction_layer = self._get_model_and_layer(model, layer)

        self.model = self.model.to(self.device)

        self.model.eval()

        self.scaler = transforms.Scale((224, 224))
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                              std=[0.229, 0.224, 0.225])
        self.to_tensor = transforms.ToTensor()

    def get_vec(self, img, tensor=True):
        """ Get vector embedding from PIL image
        :param img: PIL Image
        :param tensor: If True, get_vec will return a FloatTensor instead of Numpy array
        :returns: Numpy ndarray
        """
        # 2. Create a PyTorch Variable with the transformed image
        image = self.normalize(self.to_tensor(self.scaler(img))).unsqueeze(0).to(self.device)
        # image = Variable(self.normalize(self.to_tensor(self.scaler(img))).unsqueeze(0))

        # 3. Create a vector of zeros that will hold our feature vector
        #    The 'avgpool' layer has an output size of 512
        my_embedding = torch.zeros(1, self.layer_output_size)

        # If it's resnet-18, use this line
        # my_embedding = torch.zeros(1, self.layer_output_size, 1, 1)

        # 4. Define a function that will copy the output of a layer
        def copy_data(m, i, o):
            my_embedding.copy_(o.data)


        # 5. Attach that function to our selected layer
        h = self.extraction_layer.register_forward_hook(copy_data)
        # 6. Run the model on our transformed image
        h_x = self.model(image)
        # 7. Detach our copy function from the layer
        h.remove()

        # 8. Return the feature vector
        if tensor:
            return my_embedding
        else:
            return my_embedding.numpy()[0, :]
            # If it's resnet-18, use this line
            # return my_embedding.numpy()[0, :, 0, 0]


    def _get_model_and_layer(self, model_name, layer):
        """ Internal method for getting layer from model
        :param model_name: model name such as 'resnet-18'
        :param layer: layer as a string for resnet-18 or int for alexnet
        :returns: pytorch model, selected layer
        """
        if model_name == 'resnet-18':
            model = models.resnet18(pretrained=True)
            if layer == 'default':
                layer = model._modules.get('avgpool')
                self.layer_output_size = 512
            else:
                layer = model._modules.get(layer)

            return model, layer

        elif model_name == 'alexnet':
            model = models.alexnet(pretrained=True)
            if layer == 'default':
                layer = model.classifier[-2]
                self.layer_output_size = 4096
            else:
                # # 1 Freeze training for all layers
                # for param in model.features.parameters():
                #     param.require_grad = False
                
                # # Newly created modules have require_grad=True by default
                # num_features = model.classifier[6].in_features
                # features = list(model.classifier.children())[:-1]  # Remove last layer
                # features.extend([nn.Linear(num_features, 4096)])  # Add our layer with 4 outputs
                # model.classifier = nn.Sequential(*features)  # Replace the model classifier
                # print(model)

                # # 2remove last fully-connected layer
                # new_classifier = nn.Sequential(*list(model.classifier.children())[:-1])
                # model.classifier = new_classifier

                # # 3# remove last fully-connected layer
                # new_classifier = nn.Sequential(*list(model.classifier.children())[:-1])
                # model.classifier = new_classifier

                # #4
                
                # model = models.vgg19(pretrained=True)
                # # Number of filters in the bottleneck layer
                # num_ftrs = model.classifier[6].in_features
                # # convert all the layers to list and remove the last one
                # features = list(model.classifier.children())[:-1]
                # ## Add the last layer based on the num of classes in our dataset
                # features.extend([nn.Linear(num_ftrs, 4)])
                # ## convert it into container and add it to our model class.
                # model.classifier = nn.Sequential(*features)


                layer = model.classifier[-layer]
                # self.layer_output_size = 4096

            return model, layer

        elif model_name == 'vgg19_bn':
            model = models.vgg19_bn(pretrained=True)
            layer = model.classifier[-layer]
            print('vgg19_bn')

            return model, layer

        elif model_name == 'vgg19_bn_attention':
            model = vgg19_bn_attention()
            layer = model.classifier[-layer]
            print('vgg19_bn_attention')

            return model, layer

        # elif model_name == 'inception_v3':
        #     model = models.inception_v3()
        #     layer = model._modules.get('avg_pool2d')
        #     # layer = model.classifier[-layer]
        #     print('inception_v3')
        #
        #     return model, layer
        #
        # elif model_name == 'squeezenet1_1':
        #     model = models.inception_v3()
        #     # layer = model.classifier[-layer]
        #     print('squeezenet1_1')
        #
        #     return model, layer


        else:
            raise KeyError('Model %s was not found' % model_name)
