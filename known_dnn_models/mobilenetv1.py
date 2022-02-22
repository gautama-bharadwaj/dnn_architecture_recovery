#!/usr/bin/env python
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.mobilenet import preprocess_input
from keras.applications.mobilenet import decode_predictions
from keras.applications.mobilenet import MobileNet

# iteration count
_iter = 1


"""
    Main
"""
def run_model():
    # load the model
    model = MobileNet(alpha=1.0)
    # load an image from file
    image = load_img('known_dnn_models/mug.jpg', target_size=(224, 224))
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)

    # predict the probability across all output classes
    for i in range(_iter):
        # input('{} iteration, press any key to perform...'.format(str(i)))
        yhat = model.predict(image)

    # return if not iter
    if not _iter: exit() 
    # convert the probabilities to class labels
    label = decode_predictions(yhat)
    # retrieve the most likely result, e.g. highest probability
    label = label[0][0]
    # print the classification
    print('%s (%.2f%%)' % (label[1], label[2]*100))
    # done.

