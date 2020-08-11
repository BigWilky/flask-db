import nn_process
import time
import os
import sys

extract_feature = nn_process.create('extract_feature')
generate_poem = nn_process.create('generate_poem')




def get_poem(image_file):
    img_feature = extract_feature(image_file)
    poem_output='\n'+generate_poem(img_feature)[0].replace('\n', '\n') 
    return poem_output
