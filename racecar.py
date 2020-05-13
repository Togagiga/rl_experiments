# wee race car game

# need to add proper map
# again, changed again
# need to ensure windows size, tile size and car initial position work!

import numpy as np
#from os import path
import pygame as pg


pg.init()
size = width, height = 1200, 1200
win = pg.display.set_mode(size)
pg.display.set_caption('Car Race Game')

road_width = 10000
car_img = pg.image.load('assets/car-top-view.png').convert_alpha()  # loading car image
car_width, car_height = 50, 100                                       # specificing scaling size
car_img = pg.transform.scale(car_img, (car_width,car_height))       # scaling car image

vel_inc = 0.4
theta_inc = 4
drag_const = 0.001

GREEN = (0, 138, 55)   # RGB Colours
GREY = (67, 67, 67)

clock = pg.time.Clock()

class Map():

    def __init__(self):
        self.tilesize = 10
        self.map = np.zeros((int(width/self.tilesize), int(height/self.tilesize)), dtype = int)
        
        shape = self.map.shape
        self.map[:,int(shape[0]/2-road_width):int(shape[1]/2+road_width)] = 1   # make road of ones

    def draw(self):

        for i in range(0, width, self.tilesize):
            for j in range(0, height, self.tilesize):
                if self.map[int(i/self.tilesize),int(j/self.tilesize)] == 0:
                    pg.draw.rect(win, GREEN, (j, i, self.tilesize, self.tilesize))
                elif self.map[int(i/self.tilesize),int(j/self.tilesize)] == 1:
                    pg.draw.rect(win, GREY, (j, i, self.tilesize, self.tilesize))

class Camera():
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height) # define game window size
        self.width = width
        self.height = height

    def update(self, target):

        x = -target.x + int(width/2)
        y = -target.y + int(height/2)
        self.camera = pg.Rect(x, y, self.width, self.height)

def rot_center(img, theta):

    loc = img.get_rect().center  #rot_image is not defined 
    rot_sprite = pg.transform.rotate(img, theta)
    rot_sprite.get_rect().center = loc
    return rot_sprite


class Car():

    # need to initialise car position --> need to occupy whole number of squares
    def __init__(self, x=width/2-car_width/2, y=height/2 - car_height/2, width=car_width, height=car_height, vel = 0, theta = 0 , pos_x = 0, pos_y = 0):
        self.x = int(x)
        self.y = int(y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.theta = theta
        self.stationary = True # initially not moving (before player input)
        self.left = False
        self.right = False
        self.vel = vel          # how far car moves (in pixels) with each press of a button

    def checkLegalMove(self, inpY, inpX):
        
        map_y = int(self.y/Map().tilesize + inpY)     # position in tiles
        map_x = int(self.x/Map().tilesize + inpX)

        car_height_tiles = int(car_height/Map().tilesize)
        car_width_tiles = int(car_width/Map().tilesize)

        check =  np.argwhere(Map().map[map_y:map_y + car_height_tiles, map_x:map_x + car_width_tiles] == 0)  # if car is on zeros
        if len(check) != 0:
            return False
        else:
            return True

    def draw(self):
        self.y -= np.cos(self.theta*(2*np.pi)/360)*(self.vel)              #calculates new x,y coordinates based on current x,y,vel,theta 
        self.x -= np.sin(self.theta*(2*np.pi)/360)*self.vel               
        img = rot_center(car_img, self.theta)                              #calls function to rotate image around centre point
        win.blit(img, (self.x - (img.get_rect().width - car_width)/2, self.y - (img.get_rect().height - car_height)/2)) #subtracting from x and y to ensure smooth rotation


def redrawGameWindow():
    race_map.draw()
    car.draw()

    pg.display.update()


######### Main Loop ##########
car = Car()
race_map = Map()
#camera = Camera()
run = True
while run:
    clock.tick(27)  # 27 frames per second

    for event in pg.event.get():    # if exit button is pressed loop breaks
        if  event.type == pg.QUIT:
            run = False


    keys = pg.key.get_pressed()


    if keys[pg.K_UP] and keys[pg.K_LEFT]:
        car.vel += vel_inc
        car.theta += theta_inc
    elif keys[pg.K_UP] and keys[pg.K_RIGHT]:
        car.vel += vel_inc
        car.theta -= theta_inc
    elif keys[pg.K_DOWN] and keys[pg.K_LEFT]:
        car.vel -= vel_inc
        car.theta += theta_inc
    elif keys[pg.K_DOWN] and keys[pg.K_RIGHT]:
        car.vel -= vel_inc
        car.theta -= theta_inc
    elif keys[pg.K_DOWN]:
        car.vel -= vel_inc
    elif keys[pg.K_LEFT]:
        car.theta += theta_inc
    elif keys[pg.K_RIGHT]:
        car.theta -= theta_inc
    elif keys[pg.K_UP]:
        car.vel += vel_inc
    
    #function to produce drag effect
    if car.vel >= 0: 
        car.vel -= drag_const*np.square(car.vel)     
    else:
        car.vel += drag_const*np.square(car.vel)  
    
    redrawGameWindow()

pg.quit()