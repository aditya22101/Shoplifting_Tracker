import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TF warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


import cv2
import numpy as np
import warnings

# Suppress NumPy, OpenCV, and other library warnings
warnings.filterwarnings("ignore")


import streamlit as st

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("shoplifting_model.h5")

model = load_model()

def output(image):
    inp=cv2.resize(image,(224,224))
    inp=inp.reshape(1,224,224,3)
    # out=np.argmax(model.predict(inp)[0])
    prob = model.predict(inp) 
    print(prob)
    prob=prob[0][0]
    out=int(prob>0.5)
    return out
