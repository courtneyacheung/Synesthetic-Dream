# vis 142 fall 2023 

import pygame
from pygame.locals import *
from sys import exit
import random
import time

import math
import numpy as np
import string
import nltk
nltk.download('gutenberg')
from pandas.core.common import flatten

# record the start time
start_time = time.time()

#####################################################################
# producing FHD video from an image sequence
# software creates the image sequence at 1920 x 1080.
#####################################################################
width = 1920
height = 1080
#width = 1280
#height = 720

#####################################################################
# Name and title
#####################################################################
name = "Courtney Cheung"
title = "Synesthetic Dream" 

start_sequence_num = 7030000

# normal pygame stuff
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('generate 2K animation pngs')
frame_num = start_sequence_num
titles_font = pygame.font.SysFont(None, int(width/12)) 
name_f = titles_font.render(name, True, (255,255,255))
title_f = titles_font.render(title, True, (255,255,255))

# print resolution warning
if (width != 1920 and height != 1080):
    print("Warning: dimensions not FHD, be sure width and height are set to 1920 and 1080.")

# one second of black frames
def make_black():
    global frame_num
    screen.fill((0,0,0))
    pygame.display.update()
    for i in range(0, 60):
       pygame.image.save(screen, "./frames/" + str(frame_num) + ".png")
       frame_num = frame_num + 1
       clock.tick(60)
        
#############################################################
class ActiveCircle:

    def __init__(self, c, loc_X, loc_Y, r, wf):
        self.true_color = c
        self.color = [255,255,255]
        self.fade_in_factor = [0, 0, 0]
        for i in range(3):
            diff = 255 - self.true_color[i]
            if diff <= 60:
                self.fade_in_factor[i] = 1
            else:
                self.fade_in_factor[i] = math.ceil(diff / 60)
        self.locationX = loc_X
        self.locationY = loc_Y
        self.radius = r
        self.wobble_factor = wf             

    def appear(self):
        pygame.draw.circle(screen, self.color, \
            (self.locationX, self.locationY), self.radius)

    def wobble(self, fade=None):
        
        if fade == 'in':
            self.color = [self.color[i] - self.fade_in_factor[i] if self.color[i] > self.true_color[i] else self.color[i] for i in range(3)]
        elif fade == 'out':
            self.color = [x + 1 if x < 255 else x for x in self.color]
            self.wobble_factor += .1
            
        if (random.randint(0,1)):
            self.locationX = self.locationX + np.random.uniform(low=0.0, high=self.wobble_factor, size=None)
            self.locationY = self.locationY + np.random.uniform(low=0.0, high=self.wobble_factor, size=None)
        else:
            self.locationX = self.locationX - np.random.uniform(low=0.0, high=self.wobble_factor, size=None)
            self.locationY = self.locationY - np.random.uniform(low=0.0, high=self.wobble_factor, size=None)
            
        self.appear()
    
################################ end object

# credits loop
make_black() # one second black
# produce title sequence
screen.fill((0,0,0))
screen.blit(name_f, (int(width/8), int(width/8)))
screen.blit(title_f, (int(width/8), int(width/4))) 
for i in range(0, 3*60):
    pygame.display.update()
    pygame.image.save(screen, "./frames/" + str(frame_num) + ".png")
    frame_num = frame_num + 1
    clock.tick(60)
    
make_black() # one second black

# main animation loop

alice = nltk.corpus.gutenberg.words('carroll-alice.txt')
excerpts = [' '.join(alice[i*6822:i*6822+6822]).lower() for i in range(5)]

color_dict = {}
for letter in string.printable:
    color_dict[letter] = [np.random.randint(100, 255), np.random.randint(100, 255), np.random.randint(100, 255)]
    
background = [190, 237, 254]
num_chars_across = 16

active_circles = []
for text in excerpts:
    num_lines = math.ceil(len(text)/num_chars_across)
    line_height = height / num_lines
    center_y = line_height - .5*line_height
    line_counter = 0
    radius = width/num_chars_across/2
    excerpt_active = []
    for i in range(len(text)):
        if (i%num_chars_across == 0) & (i!=0):
            line_counter += 1
            center_y += line_height
        center_x = radius*(i-num_chars_across*line_counter)*2 + radius
        if text[i] == ' ':
            excerpt_active.append(ActiveCircle(background, center_x, center_y, radius, 1))
        else:
            excerpt_active.append(ActiveCircle(color_dict[text[i]], center_x, center_y, radius, 1))
    active_circles.append(excerpt_active)

in_times = list(flatten([range(i*240, i*240+60) for i in range(5)]))
still_times = list(flatten([range(i*240+60, i*240+60+60) for i in range(5)]))
out_times = list(flatten([range(i*240+120, i*240+120+120) for i in range(5)]))

caption_font = pygame.font.SysFont(None, int(width/35)) 
caption_font2 = pygame.font.SysFont(None, int(width/35), italic=True)
caption_f = caption_font.render('A Textual Data Visualization of', True, (0, 0, 0))
caption_f2 = caption_font2.render('Alice in Wonderland', True, (0, 0, 0))

current_excerpt = -1
for i in range(0, 20*60): # 20*60 frames is 20 seconds
    
    screen.fill(background)
    if i%240==0:
        current_excerpt += 1
    words = active_circles[current_excerpt]
    for char in words:
        if i in in_times:
            char.wobble('in')
        elif i in still_times:
            char.wobble()
        elif i in out_times:
            char.wobble('out')
    
    screen.blit(caption_f, (20, height- 40))
    screen.blit(caption_f2, (20+width/3-60, height - 40))
            
    #for event in pygame.event.get():
     #   if event.type == QUIT:
      #     pygame.display.quit()
       #    pygame.quit()
        #   exit()
        
    pygame.image.save(screen, "./frames/" + str(frame_num) + ".png")
    frame_num = frame_num + 1
    pygame.display.update()
    clock.tick(60)

# print out stats
print("seconds:", int(time.time() - start_time))
print("~minutes: ", int((time.time() - start_time)/60))
# quit here
pygame.display.quit()
pygame.quit()
exit()

# make your files into a movie with ffmpeg:
# ffmpeg -r 60 -start_number 7030000 -s 4096x2160 -i %d.png -vcodec libx264 -crf 5 -pix_fmt yuv420p final.mp4

