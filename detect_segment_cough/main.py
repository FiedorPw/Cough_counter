# detect cough, see notebooks for segment cough
import sys
sys.path.append('./src')
from src.feature_class import features
from src.DSP import classify_cough
from scipy.io import wavfile
import pickle

def detect_coughing(file):
    input_file = file
    model = pickle.load(open('./models/cough_classifier', 'rb'))
    scaler = pickle.load(open('./models/cough_classification_scaler', 'rb'))

    fs, x = wavfile.read(file)
    prob = classify_cough(x, fs, model, scaler)
    print(f"{input_file} has probability of cough: {prob}")


cough = "chunk-kaszel.wav"
tekst = 'chunk-tekst.wav'
detect_coughing(cough)
detect_coughing(tekst)
