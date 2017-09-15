from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image   
from keras.models import load_model               
from tqdm import tqdm
import numpy as np
import cv2 
from extract_bottleneck_features import *
from glob import glob
import sys
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_alt.xml')
ResNet50_model = ResNet50(weights='imagenet')
model_path = '../saved_models/best_xception_model.h5'
Xception_model = load_model(model_path)
dog_names = [item[20:-1] for item in sorted(glob("../dogImages/train/*/"))]

def Xception_predict_breed(img_path):
    bottleneck_feature = extract_Xception(path_to_tensor(img_path))
    predicted_vector = Xception_model.predict(bottleneck_feature)
    return dog_names[np.argmax(predicted_vector)]


def path_to_tensor(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    return np.expand_dims(x, axis=0)


def ResNet50_predict_labels(img_path):
    img = preprocess_input(path_to_tensor(img_path))
    return np.argmax(ResNet50_model.predict(img))


def face_detector(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces) > 0


def dog_detector(img_path):
    prediction = ResNet50_predict_labels(img_path)
    return ((prediction <= 268) & (prediction >= 151))


def predict_breed(path):
    is_human = face_detector(path) 
    is_dog = dog_detector(path)
    speciment = message = dog_breed = ''

    if is_dog:
        dog_breed = Xception_predict_breed(path).replace('_', ' ').title().split('.')[1]
        speciment = 'dog'
        
    if not is_dog and is_human == True:
        dog_breed = Xception_predict_breed(path).replace('_', ' ').title().split('.')[1]
        speciment = 'human'
        
    if not is_dog and not is_human:
        message = 'Error! no dog or human found in image.'
    print ('"speciment": "{}",  "message": "{}", "dog_breed": "{}"'.format(speciment, message, dog_breed))



if __name__ == "__main__":
    predict_breed(sys.argv[1])



