# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 12:16:22 2021

@author: ferha
"""
import numpy as np 
import imageio
import matplotlib.image as img
import matplotlib.pyplot as plt

class kMeans:
    
    def __init__(self,K,pixels,iteration):
        
        self.K= K
        
        self.pixels = pixels
        
        self.iteration = iteration
    
    def init_centroids(self):
            
        # Reshape methods. 3d pixel array converted to 2d array
        #points = np.reshape(self.pixels, (self.pixels.shape[0] * self.pixels.shape[1], self.pixels.shape[2]))

        # Number of rows
        rows = self.pixels.shape[0]
        
        # Number of columns
        cols = self.pixels.shape[1]                          


        
        # Create empty centroids
        centroids = np.zeros((self.K, cols)) 
        
        # Generate random number sequence related to pixel indexes
        random_pixel_indexes = np.random.permutation(rows)
        
        # Get some random pixel index with its R,G,B values
        centroids = self.pixels[random_pixel_indexes[:self.K]]
        
        return centroids            
    
    def calculate_eucludian_distance(self,x1,x2,y1,y2,z1,z2):
        
        # Apply this sqrt ((x1-x2)^2 + (y1-y2)^2)
        dist = np.square(x1-x2) + np.square(y1-y2) + np.square(z1-z2)
        dist = np.sqrt(dist)
        
        
        return dist
    
    def get_randomized_centroids(self,pixels,cluster_num,img_width, img_height):
        
        centroids = []
        
        for k in range(0,cluster_num):
           
            ranX = np.random.randint(0,img_width)
            
            ranY = np.random.randint(0,img_height)
            
            cent = pixels[ranX, ranY]
            
            centroids.append(cent)
        
        return centroids
    

    
    def get_min(self,pixel, centroids):
        
        # Assign a dummy minimum distance which is as possible as greater number
        min_dist = 9999
        
        min_index = 0
        
        for i in range (0,len(centroids)):
            
            x1 = centroids[i][0]
            x2 = pixel[0]
            
            y1 = centroids[i][1]
            y2 = pixel[1]
            
            z1 = centroids[i][2]
            z2 = pixel[2]
            
            
            dist = self.calculate_eucludian_distance(x1,x2,y1,y2,z1,z2)
            
         
            if dist < min_dist:
                
                # Update new min distance 
                min_dist = dist
                
                # Save index
                min_index = i
    
            
        return min_index

    def update_centroids(self,indexes,pixels):
        
        row = pixels.shape[0]
        col = pixels.shape[1]
        new_centroids = np.zeros((self.K, col)) 
        for i in range(0, self.K):
            
           temp =  np.array(i == indexes,dtype=int)
           count = np.sum(temp)
           temp_mat = np.transpose(np.tile(temp,(col,1)))
           temp_mat= np.multiply(pixels,temp_mat)
           new_centroids[i]= np.true_divide(temp_mat.sum(axis=0),count);
           
        return new_centroids
      
        
        
    def runKmeans(self,centroids,pixels):
    
        counter = 0
        while counter<self.iteration:
            
            min_indexes = []
            for pixel in pixels:
                min_index = self.get_min(pixel,centroids)
                min_indexes=np.append(min_indexes, min_index)
        
            counter = counter + 1    
            
            # Update the cenroids. 
            centroids = self.update_centroids(min_indexes,pixels)
        
        min_indexes = np.array([min_indexes])
        min_indexes= min_indexes.T
        min_indexes= min_indexes.astype(int)
        recovered_pixels = centroids[min_indexes] 
        return recovered_pixels   
            
    