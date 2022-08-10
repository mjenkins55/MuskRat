#When input image is selected, run it through models and make predictions 
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from tensorflow import keras 
import numpy as np
from video_reader import VideoReader

IMG_SIZE = 128
CATEGORIES = ['real', 'fake']

model1 = keras.models.load_model('double_trained_model.h5')
model2 = keras.models.load_model('model_00_20.h5')
model3 = keras.models.load_model('model_20_40.h5')
model4 = keras.models.load_model('model_40_60.h5')
model5 = keras.models.load_model('model_q2_q4.h5')

MODELS = [model1, model2, model3, model4, model5]

#Function ingests a Lists, returns the most frequent value in list
def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num

def get_list_of_predictions(img_path):
    #parameter is path to input file on local machine 
    #convert image to grayscale 
    if img_path.split('/')[-1].split('.')[-1] == 'mp4':
        vid_reader = VideoReader(verbose = False)
        img_array = vid_reader.read_frames(img_path,num_frames=1)[0][0]
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    else:
        img_array = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    #plt.imshow(img_array, cmap="gray")
    #plt.show()

    #resize image to fit model input layer
    img_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    img_array = img_array.reshape(-1, 128, 128, 1)

    #i = 0
    temp_list = []
    #make a prediction with each model
    for mod in MODELS:
        predictions = mod.predict(img_array)
        temp_list.append(int(predictions[0][0]))
        #print("Predicted Class Model " + str(i) + ": " + CATEGORIES[int(predictions[0][0])])
        #i = i + 1
    pred = prediction_array(img_array)
    #print("here")
    #print(pred)
    return pred

def prediction_array(img):
    pred = []

    for mod in MODELS:
        predictions = mod.predict(img)
        pred.append(int(predictions[0][0]))
    #append the most frequent result on total_pred list so that we return 1 list
    pred.append(most_frequent(pred))
    #print(pred)
    return pred
    
    
