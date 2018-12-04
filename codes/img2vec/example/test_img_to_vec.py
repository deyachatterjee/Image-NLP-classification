import sys
import os
sys.path.append("..")  # Adds higher directory to python modules path.
from img_to_vec import Img2Vec
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from model_vgg19bn_attention import vgg19_bn_attention


input_path = '../../../data/19Breast'
# input_path = '../../../data/test_images'

# chose a model
# model='resnet-18'
# img2vec = Img2Vec()

# model = 'alexnet'
# model = 'vgg19_bn'
model = 'vgg19_bn_attention'
model_zoo = ['resnet-18', 'alexnet', 'vgg19_bn', 'vgg_19bn_attention', 'squeezenet1_1', 'inception_v3', 'Densenet121']
img2vec = Img2Vec(cuda=False, model = model, layer = 2, layer_output_size = 4096)

# For each test image, we store the filename and vector as key, value in a dictionary
pics = {}
for file in os.listdir(input_path):
    filename = os.fsdecode(file)
    img = Image.open(os.path.join(input_path, filename))
    vec = img2vec.get_vec(img)
    pics[filename] = vec

# output: top 10 most similar images for a specific image, and calculate all of the image in folder
log_file = open('./%s.txt'%model, 'w')
for pic_name in os.listdir(input_path):
    log_file.write('%s top 10 similar images:\n'%pic_name)
# pic_name = ""
# while pic_name != "exit":
#     pic_name = str(input("Which filename would you like similarities for?\n"))
    try:
        sims = {}
        for key in list(pics.keys()):
            if key == pic_name:
                continue

            sims[key] = cosine_similarity(pics[pic_name].reshape((1, -1)), pics[key].reshape((1, -1)))[0][0]

        d_view = [(v, k) for k, v in sims.items()]
        d_view.sort(reverse=True)
        # show top 10
        for v, k in d_view[:10]:
            log_file.write('%s %s\n'%(str(v), str(k)))
            # print(v, k)

    except KeyError as e:
        print('Could not find filename %s' % e)

    except Exception as e:
        print(e)

log_file.close()