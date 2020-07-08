# wee race car game

import numpy as np
import pygame as pg
import math


pg.init()
size = width, height = 1200, 1200
win = pg.display.set_mode(size)
pg.display.set_caption('Car Race')
start_pos_x, start_pos_y = 1000, 1000


road_width = 20
car_img = pg.image.load('/home/jonas/Documents/GitHub/rl_experiments/assets/car-top-view.png').convert_alpha()   # loading car image
car_width, car_height = 25, 50                                      # specificing scaling size
car_img = pg.transform.scale(car_img, (car_width,car_height))        # scaling car image

vel_inc = 0.4
theta_inc = 5
drag_const = 0.001

GREEN = (0, 138, 55)                                                 # RGB Colours
GREY = (67, 67, 67)
RED = (253, 8, 8)
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)

clock = pg.time.Clock()

class Map():

    def __init__(self):
        self.tilesize = 10
        self.map = np.zeros((int(width/self.tilesize), int(height/self.tilesize)), dtype = int)
        
        #shape = self.map.shape
        # self.map[10:100,int(0.5*shape[1]-road_width):int(0.5*shape[1]+road_width)] = 1   # make road of ones


        ### Making Ghetto Map ###

        self.map[10:120, 90:110] = 1
        self.map[10:30, 10:110] = 1
        self.map[10:60, 10:30] = 1
        self.map[40:60, 30:80] = 1
        self.map[60:110, 60:80] = 1
        self.map[90:110, 0:80] = 1

    def draw(self):

        for i in range(0, width, self.tilesize):
            for j in range(0, height, self.tilesize):
                if self.map[int(i/self.tilesize),int(j/self.tilesize)] == 0:
                    pg.draw.rect(win, GREEN, (j, i, self.tilesize, self.tilesize))
                elif self.map[int(i/self.tilesize),int(j/self.tilesize)] == 1:
                    pg.draw.rect(win, GREY, (j, i, self.tilesize, self.tilesize))


def rot_center(img, theta):

    loc = img.get_rect().center                                #rot_image is not defined 
    rot_sprite = pg.transform.rotate(img, theta)
    rot_sprite.get_rect().center = loc
    return rot_sprite


class Car():

    def __init__(self, x = start_pos_x, y = start_pos_y, vel = 0, theta = 0):    # x=width/2-car_width/2, y=height/2 - car_height/2,
        self.x = int(x)
        self.y = int(y)
        self.theta = theta
        self.vel = vel                                         # how far car moves (in pixels) with each press of a button

    def update_pos(self, vel, theta):
        self.y -= np.cos(theta*(2*np.pi)/360)*vel              # calculates new x,y coordinates based on current x,y,vel,theta 
        self.x -= np.sin(theta*(2*np.pi)/360)*vel

    def checkLegalMove(self, vel, theta):

        self.update_pos(vel, theta)
        img_check = rot_center(car_img, theta)                 # rotating image of car

        car_h = img_check.get_rect().height                    # rotated size of car
        car_w = img_check.get_rect().width

        check_x = self.x - (car_w - car_width)/2               # position account for car turning
        check_y = self.y - (car_h - car_height)/2
        
        map_y = math.floor(check_y/Map().tilesize)             # position in tiles
        map_x = math.floor(check_x/Map().tilesize)

        car_h_tiles = math.ceil(car_h/Map().tilesize)          # getting car size in tiles
        car_w_tiles = math.ceil(car_w/Map().tilesize)

        check =  np.argwhere(Map().map[map_y:map_y + car_h_tiles, map_x:map_x + car_w_tiles] == 0)  # if car is on zeros on map
        if len(check) != 0:
            print('crashed')
            return False
        else:
            print('not crashed')
            return True


    def draw(self):
        self.update_pos(self.vel, self.theta)                  # updating x y coords          
        img = rot_center(car_img, self.theta)                  # calls function to rotate image around centre point
        # drawing retangle representing actual car width and height #
        pg.draw.rect(win, GREY, (self.x - (img.get_rect().width - car_width)/2, self.y - (img.get_rect().height - car_height)/2, img.get_rect().width, img.get_rect().height))
        win.blit(img, (self.x - (img.get_rect().width - car_width)/2, self.y - (img.get_rect().height - car_height)/2)) #subtracting from x and y to ensure smooth rotation


def reset(score, highscore):
    if score > highscore:
        highscore = score        

    start = True        
    x = int(x)
    self.y = int(y)
    self.theta = theta
    self.vel = vel         
    return jump, start, y, counter, bar_pos, y_bar, score, highscore

def text_object(text, font, colour):
    textSurf = font.render(text, True, colour)
    return textSurf, textSurf.get_rect()

def message_display(text, font_size, x_coord, y_coord, colour):
    font = pg.font.Font('freesansbold.ttf', font_size) 
    textSurf, textRect = text_object(text, font, colour) 
    textRect.center = (x_coord, y_coord)
    win.blit(textSurf, textRect)

def home_screen(self, start, jump, score, highscore):
    while start: 
        pg.time.delay(100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                
        keys = pg.key.get_pressed() #pressing space will start game          
        if keys[pg.K_SPACE]:
            jump = True
            start = False
            score = 0
            
        win.fill(black) #refreshing display
        message_display('Happy Walnut', 38, 250, 150, green)
        message_display('Highscore: %d'%highscore, 22, 250, 220, white)
        message_display('Previous score: %d'%score, 18, 250, 250, white)
        message_display('Press --space-- to begin', 26, 250, 420, white)
        win.blit(car_img,(self.x,self.y))
        pg.display.update()
        
    return jump, start, score

def score():
    generation = 1
    model = 1
    font = pg.font.SysFont(None, 25)
    text_gen = font.render("Generation: "+str(generation), True, (0, 0, 0))
    text_model = font.render("Model: "+str(model), True, (0, 0, 0))
    win.blit(text_gen, (10, 10))
    win.blit(text_model, (10, 30))


def redrawGameWindow():
    race_map.draw()
    car.draw()
    score()

    pg.display.update()


######### Main Loop ##########
car = Car()
race_map = Map()
run = True

time_start = pg.time.get_ticks()
while run:
    clock.tick(27)                                             # 27 frames per second

    for event in pg.event.get():                               # if exit button is pressed loop breaks
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
    
    #function to produce drag effect#
    if car.vel >= 0: 
        car.vel -= drag_const*np.square(car.vel)     
    else:
        car.vel += drag_const*np.square(car.vel)
        
    time = pg.time.get_ticks() - time_start
    message_display('score: %d'%time, 18, 450, 10, green)
    
    redrawGameWindow()

    if not car.checkLegalMove(car.vel, car.theta):             # checks whether car is on road or not
        run = False
    else: 
        pass

pg.quit()