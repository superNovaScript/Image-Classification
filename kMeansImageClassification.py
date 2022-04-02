# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 00:15:30 2021

@author: ferhat bayar
"""

# Importing os module
import os
import imageio
import matplotlib.pyplot as plt
import shelve
import numpy
from PIL import Image
import csv
import pandas
from k_mean_cluster import kMeans

def get_list_directory(path):
    dirList = os.listdir(path)
    
    return dirList
    
def get_image_dir_name(dir_path):
    base_name = os.path.basename(dir_path)

    return base_name

def compress_image(pixels,K,max_iter):
    
    k = kMeans(K,pixels,max_iter)
    
    centroids = k.init_centroids()
    
    recovered_image = k.runKmeans(centroids,pixels)
    
    return recovered_image
    

def populate_futures(image_list, class_name):
    
    # Open a database file to save all pixel data according to class name
    db = shelve.open('lookuptable')
    db[class_name] = []
    
    temp_list = []
    for image in image_list:
        pixels = read_image(image)
        
        # Re-shape 3d to 1d
        future_data = pixels.reshape(-1)   
        
        temp_list.append(class_name)
        temp_list.append(image)
        temp_list.append(future_data)

    db[class_name] = temp_list                
    
    db.close()
    
def read_csv():
    data = pandas.read_csv("data_set.csv")
    x=3

    
    
def populate_futures_2(image_list, class_name,dataset_file_name):
    df = pandas.read_csv(dataset_file_name)
    temp_list = []
    for image in image_list:
        pixels = read_image(image)
        
        temp_list.append(pixels)

    df[class_name] = temp_list
    
    df.to_csv("data_set.csv", index=False)      
            
    
def read_image(file_name):
    
    # Read RGB image as a 3D-matrix
    img = Image.open(file_name)
    
    # Show the image to check it
    #plt.imshow(img)
    
    # One pixel takes 256 different value
    total_pixel = 256
    
    # Scaling r-g-b value into [0-1]
    pixels = numpy.true_divide(img,total_pixel);
    
    # Re-shape 3d to 1d
    pixels = numpy.reshape(pixels, (pixels.shape[0] * pixels.shape[1], pixels.shape[2]))   
    
    
    # Preprosessing--- burda pixel sayısı 4'ye indirilir.
    recovered_image = compress_image(pixels, 4, 10)

    
    return recovered_image
    
def get_file_paths(path):
    imagefiles = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
   
    if imagefiles == []:
        print ("No files were found in the directory, please check and input proper directory.")
    return imagefiles

# Defining main function
def main():
    print("Hey There")

    # Get the path of current working directory
    currentPath = os.getcwd()
    
    
    # List directory
    dirList = get_list_directory(currentPath)
    
    # Check directory list contains data-set folder
    if "dataset" not in dirList:
        assert("Dataset folder doesn't exist")
 
    # Add dataset folder to path
    datasetPath = os.path.join(currentPath, "dataset")
    
    # Print dataset path
    print("Dataset Path: ", datasetPath)
    
    # Get dataset folders
    dataSetFolders = get_list_directory(datasetPath)
    
    # Print dataset folders
    print("Dataset folders: ", dataSetFolders)
    
    image_list = {}
    # Get inside whole folders and read all file         
    for dir_name in dataSetFolders:
        
        # Add dataset folder to path
        image_paths = os.path.join(datasetPath, dir_name)
    
        
        image_list = get_file_paths(image_paths)
        
        print(image_list)
        print("################################\n")
        
        
        dataset_file_name = "data_set.csv"
        
        if True:
            populate_futures_2(image_list, dir_name,dataset_file_name)
        
        read_csv()
        
        
            
    



  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()