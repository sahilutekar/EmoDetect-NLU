# EmoDetect/NLU
"EmoDetect: Automatic Emotion Recognition using Neural Networks and MFCCs"

Emotion Recognition using Deep Learning

Overview

The project aims to develop a deep learning model that can recognize emotions from voice samples. The model is trained using Mel-frequency cepstral coefficients (MFCCs) extracted from voice samples of the RAVDESS dataset. The dataset consists of 7356 files, each file contains emotional speech from actors. The emotional states include calm, happy, sad, angry, fearful, surprise, and disgust.

The project uses the Keras deep learning library and trains a Convolutional Neural Network (CNN) model. The model takes the MFCCs as input and produces the probability distribution of the emotional states as output. The trained model is saved to a pickle file.
Requirements

    Python 3
    Jupyter Notebook
    Libraries:
        numpy
        pandas
        librosa
        matplotlib
        sklearn
        keras
        tensorflow
        pickle-mixin
        dill

How to run the project

    Clone the repository to your local machine.
    Open Jupyter Notebook and navigate to the cloned repository directory.
    Open the file "Ffinal_EmotionsRecognition1_with_pred.ipynb".
    Run the code cells in the notebook from top to bottom.
    After training, the trained model is saved to a pickle file named "model.pkl".

