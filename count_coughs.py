# detect cough, see notebooks for segment cough
import os
import sys
#sys.path.append('./src')
#from src.DSP import classify_cough
from scipy.io import wavfile
import pickle
from detect_segment_cough import *
#import isolate_cough_speech_webrtc
import py_webrtcvad
from py_webrtcvad import example as webrtcv_cut_wav
from detect_segment_cough import detect_cough
import glob
import re

#from which directory get cut out samples
directory_path = './'
chunk_files = []
cough_chunks = {}
detection_threshold_level = 0.43

def get_chunk_files(directory):
    # Use a glob pattern to match files starting with 'chunk-' followed by any digits and ending with '.wav'
    pattern = f"{directory}/chunk-*.wav"
    files = glob.glob(pattern)

    # Use regular expression to filter out files that strictly follow 'chunk-{number}.wav'
    chunk_files = [file for file in files if re.match(r"chunk-\d+\.wav", file.split('/')[-1])]

    return chunk_files


def delete_speach_count_coughs(chunk_files):
    for chunk in chunk_files:
        chunk_prob = detect_cough.main(chunk)
        if chunk_prob>detection_threshold_level:
            print(chunk,chunk_prob,"cough")
            cough_chunks[chunk] = chunk_prob
        else:
            print(f"no cough wywalamy plik{chunk} prawdopodobienstwo: {chunk_prob}")

            #usuwanie pliku
            # os.remove(chunk)


def count_coughs(file,strictness):
    # audio = sys.argv[1:]
    # cut wave fragments to cough and speach fragments
    parameters = [strictness,file]
    webrtcv_cut_wav.main(parameters)
    chunk_files = get_chunk_files(directory_path)
    delete_speach_count_coughs(chunk_files)
    coughs_counted = len(cough_chunks)
    return cough_chunks
    # print(f"\033[94mProbabilities of the cough in \033[91m{coughs_counted}\033[94m chunks:\033[0m")
    # print(f"\033[94m{cough_chunks}\033[0m")


if __name__ == '__main__':
    audio = sys.argv[1:]
    #cut wave fragments to cough and speach fragments
    webrtcv_cut_wav.main(sys.argv[1:])
    chunk_files = get_chunk_files(directory_path)
    delete_speach_count_coughs(chunk_files)
    coughs_counted = len(cough_chunks)
    print(f"\033[94mProbabilities of the cough in \033[91m{coughs_counted}\033[94m chunks:\033[0m")
    print(f"\033[94m{cough_chunks}\033[0m")



# prob = detect_cough.main('./chunk-00.wav')
# print(prob)
