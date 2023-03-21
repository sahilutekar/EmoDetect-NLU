# -*- coding: utf-8 -*-
"""Ffinal_EmotionsRecognition1_with_pred.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VTzegJlxtiF7kIg8vaL5QkmPIyoRThv-

#Analysis
"""

from google.colab import drive 
drive.mount('/content/drive')

!pip install librosa

import librosa
from librosa import display

data, sampling_rate = librosa.load('/content/drive/MyDrive/Mini Project II/emodetect/features/Actor_01/03-01-01-01-01-01-01.wav')



# % pylab inline
import os
import pandas as pd
import glob 

plt.figure(figsize=(12, 4))
librosa.display.waveplot(data, sr=sampling_rate)

"""# Load all files

Create our numpy array extracting Mel-frequency cepstral coefficients (MFCCs), while the classes to predict will be extracted from the name of the file 
"""

from google.colab import drive
drive.mount('/content/drive')

import time

path = '/content/drive/MyDrive/Mini Project II/emodetect/'
lst = []

start_time = time.time()

for subdir, dirs, files in os.walk(path):
  for file in files:
      try:
        #Load librosa array, obtain mfcss, store the file and the mcss information in a new array
        X, sample_rate = librosa.load(os.path.join(subdir,file), res_type='kaiser_fast')
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0) 
        # Convert the labels (from 1 to 8) to a series from 0 to 7
        # This is because our predictor needs to start from 0 otherwise it will try to predict 0 also.
        file = int(file[7:8]) - 1 
        arr = mfccs, file
        lst.append(arr)
      # If the file is not valid, skip it
      except ValueError:
        continue

print("--- Data loaded. Loading time: %s seconds ---" % (time.time() - start_time))

# Creating X and y: zip makes a list of all the first elements, and a list of all the second elements.
X, y = zip(*lst)

import numpy as np
X = np.asarray(X)
y = np.asarray(y)


X.shape, y.shape

# Saving joblib files to not load them again with the loop above

import joblib

X_name = 'X.joblib'
y_name = 'y.joblib'
save_dir = '/content/drive/My Drive/emodetectgit/Ravdess/jobfiles' 

savedX = joblib.dump(X, os.path.join(save_dir, X_name))
savedy = joblib.dump(y, os.path.join(save_dir, y_name))

# Loading saved models

X = joblib.load('/content/drive/My Drive/emodetectgit/Ravdess/jobfiles/X.joblib')
y = joblib.load('/content/drive/My Drive/emodetectgit/Ravdess/jobfiles/y.joblib')

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
X_train.shape, X_test.shape

"""# Neural network"""

x_traincnn = np.expand_dims(X_train, axis=2)
x_testcnn = np.expand_dims(X_test, axis=2)

x_traincnn.shape, x_testcnn.shape

import keras
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
#from keras.utils import to_categorical
from tensorflow.keras.utils import to_categorical
from keras.layers import Input, Flatten, Dropout, Activation
from keras.layers import Conv1D, MaxPooling1D
from keras.models import Model
from keras.callbacks import ModelCheckpoint

model = Sequential()

model.add(Conv1D(128, 5,padding='same',
                 input_shape=(40,1)))
model.add(Activation('relu'))
model.add(Dropout(0.1))
model.add(MaxPooling1D(pool_size=(8)))
model.add(Conv1D(128, 5,padding='same',))
model.add(Activation('relu'))
model.add(Dropout(0.1))
model.add(Flatten())
model.add(Dense(8))
model.add(Activation('softmax'))

!pip install pickle-mixin

model.summary()

"""Compile and fit our model"""

opt = tf.keras.optimizers.RMSprop(learning_rate=0.00005, epsilon=None, decay=0.0)

model.compile(loss='sparse_categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

cnnhistory=model.fit(x_traincnn, y_train, batch_size=16, epochs=1000, validation_data=(x_testcnn, y_test))

import pickle
pickle.dump(model, open('model.pkl','wb'))

import dill
import weakref
dill.dump(weakref, open('model.pkl', 'wb'))

"""Plot the loss:"""

plt.plot(cnnhistory.history['loss'])
plt.plot(cnnhistory.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

"""

Plot the accuracy:"""

plt.plot(cnnhistory.history['accuracy'])
plt.plot(cnnhistory.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

"""Predictions"""

predictions = np.argmax(model.predict(x_testcnn), axis=-1)

predictions

y_test

new_Ytest = y_test.astype(int)

new_Ytest

"""Classification report:"""

from sklearn.metrics import classification_report
report = classification_report(new_Ytest, predictions)
print(report)

# 0 = neutral, 1 = calm, 2 = happy, 3 = sad, 4 = angry, 5 = fearful, 6 = disgust, 7 = surprised

"""Confusion matrix: it will show the misclassified samples"""

from sklearn.metrics import confusion_matrix
matrix = confusion_matrix(new_Ytest, predictions)
print (matrix)

# 0 = neutral, 1 = calm, 2 = happy, 3 = sad, 4 = angry, 5 = fearful, 6 = disgust, 7 = surprised

"""# Save the model"""

model_name = 'Emotion_Voice_Detection_Model1.h5'
save_dir = '/content/drive/My Drive/emodetectgit/Ravdess/ravdess_model' 
# Save model and weights
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
model_path = os.path.join(save_dir, model_name)
model.save(model_path)
print('Saved trained model at %s ' % model_path)

"""# Reloading the model to test it"""

loaded_model = keras.models.load_model('/content/drive/My Drive/emodetectgit/Ravdess/ravdess_model/Emotion_Voice_Detection_Model1.h5')
loaded_model.summary()

"""# Checking the accuracy of the loaded model


"""

loss, accuracy = loaded_model.evaluate(x_testcnn, y_test)
print("Restored model, accuracy: {:5.2f}%".format(100*accuracy))



"""#Live Predictions"""

import keras
import librosa
import numpy as np
import sys
import pathlib

working_dir_path = pathlib.Path().absolute()

EXAMPLES_PATH = str(working_dir_path) + '/drive/My Drive/emodetectgit/examples/'
MODEL_DIR_PATH = str(working_dir_path) + '/drive/My Drive/emodetectgit/Ravdess/ravdess_model/'


class LivePredictions:
    
    #Main class of the application.
    

    def __init__(self, file):
        
        #Init method is used to initialize the main parameters.
        
        self.file = file
        self.path = MODEL_DIR_PATH + 'Emotion_Voice_Detection_Model1.h5'
        self.loaded_model = keras.models.load_model(self.path)

    def make_predictions(self):
        
        #Method to process the files and create your features.
        
        data, sampling_rate = librosa.load(self.file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=1)
        x = np.expand_dims(x, axis=0)
        predictions = np.argmax(self.loaded_model.predict(x), axis=-1)
        print( "Prediction is", " ", self.convert_class_to_emotion(predictions))

    @staticmethod
    def convert_class_to_emotion(pred):
        
        #Method to convert the predictions (int) into human readable strings.
        
        
        label_conversion = {'0': 'neutral',
                            '1': 'calm',
                            '2': 'happy',
                            '3': 'sad',
                            '4': 'angry',
                            '5': 'fearful',
                            '6': 'disgust',
                            '7': 'surprised'}

        for key, value in label_conversion.items():
            if int(key) == pred:
                label = value
        return label


if __name__ == '__main__':
    #RAVDESS
    live_prediction = LivePredictions(file=EXAMPLES_PATH + '03-01-01-01-01-02-05.wav')
    live_prediction.make_predictions()
    live_prediction = LivePredictions(file=EXAMPLES_PATH + '10-16-07-29-82-30-63.wav')
    live_prediction.make_predictions()

    #TESS
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'OAF_back_angry.wav')
    live_prediction.make_predictions()
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'OAF_back_ps.wav')
    live_prediction.make_predictions()
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'OA_bite_neutral.wav')
    live_prediction.make_predictions()
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'YAF_back_happy.wav')
    live_prediction.make_predictions()

    #Savee
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'savee_a01.wav')
    live_prediction.make_predictions()
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'savee_a06.wav')
    live_prediction.make_predictions()
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'savee_a09.wav')
    live_prediction.make_predictions()
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'savee_a15.wav')
    live_prediction.make_predictions()
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'recording0.wav')
    live_prediction.make_predictions()
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'Ses02F_impro02_F002.wav')
    live_prediction.make_predictions()
    live_prediction = LivePredictions(file=EXAMPLES_PATH + 'Ses01F_impro01.wav')
