#import packages we will need
from typing import Mapping
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

#---initial condition ---
theta_init=np.pi/3
theta_d_init=0


def draw_pendulum(theta,w=1000,h=1000,m=1,l=1):
    #create image with width=w and height=h
    img = Image.new("RGB", (w, h), "white")
    #convert the length of the pendulum to some image units
    L=int(0.3*h*l)
    #define a diameter for the pendulums mass
    d=int(0.04*h)*m**(1/3)
    #create the draw objects of the image
    draw = ImageDraw.Draw(img)
    #calculate the cartesian coordinates
    x0=int(w/2)
    y0=int(h/2)
    x=x0+L*np.sin(theta)
    y=y0+L*np.cos(theta)
    #draw the pendulum
    draw.line([(x0,y0),(x,y)],fill=(0,0,0),width=1)
    draw.ellipse([(x-d,y-d),(x+d,y+d)], fill=(255,0,0), outline=None)
    return img


#--example of draw_pendulum()----
img=draw_pendulum(theta_init)
img.show()





def calculate_trajectory(theta_init,theta_d_init,n_iter=30000,dt=0.0005,g=10,l=1):
    phase_traject=np.zeros((n_iter,2))#phase-space trajectory
    phase_traject[0,:]=np.array([theta_init,theta_d_init])
    k=200
    n=1#mass is referred as n, as m is already taken

    for i in range(n_iter-1):
        theta_dd=-g/l*np.sin(phase_traject[i,0]) -k/n*np.sin(phase_traject[i,0])*np.cos(phase_traject[i,0])
        phase_traject[i+1,1]=phase_traject[i,1]+dt*theta_dd
        phase_traject[i+1,0]=phase_traject[i,0]+dt*phase_traject[i,1]
    return phase_traject

dt=0.0005
n_iter=30000

phase_traject=calculate_trajectory(theta_init,theta_d_init,dt=0.0005,n_iter=30000)
plt.plot(phase_traject[:,0])
plt.ylabel('theta')
plt.xlabel('iteration')
plt.show()




frames_per_second=20
take_frame_every=int(1/(dt*frames_per_second))

def pil_list_to_cv2(pil_list):
#converts a list of pil images to a list of cv2 images
    png_list=[]
    for pil_img in pil_list:
        pil_img.save('trash_image.png',format='png')
        png_list.append(cv2.imread('trash_image.png'))
    os.remove('trash_image.png')
    return png_list

def generate_video(cv2_list,path='pendul.avi',fps=10): 
    #makes a video from a given cv2 image list
    if len(cv2_list)==0:
        raise ValueError('the given png list is empty!')
    video_name = path
    frame=cv2_list[0] 
    # setting the frame width, height width 
    # the width, height of first image 
    height, width, layers = frame.shape   
    video = cv2.VideoWriter(video_name, 0, fps, (width, height))  
    # Appending the images to the video one by one 
    for cv2_image in cv2_list:  
        video.write(cv2_image) 
    # Deallocating memories taken for window creation 
    cv2.destroyAllWindows()  
    video.release()  # releasing the video generated

import cv2
import os
def render_traject(phase_traject,m=1,l=1,g=10,save_path='',take_frame_every=1):
    frames=[]#here we clollect the frames
    for i in range(phase_traject.shape[0]):
        if i%take_frame_every==0:
            #get the i-th angle and angular velocity
            theta=phase_traject[i,0]
            theta_d=phase_traject[i,1]
            #draw the corresponding image and add to our frame list
            img=draw_pendulum(theta,w=200,h=200,m=m,l=l)
            frames.append(img)


    

    cv2_list=pil_list_to_cv2(frames)
    generate_video(cv2_list,path=save_path+'pendulum.avi',fps=1000/40)

render_traject(phase_traject,take_frame_every=take_frame_every)