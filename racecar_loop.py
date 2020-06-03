# wee race car game

import numpy as np
import pygame as pg
import math
import time

play = True
size = width, height = 1200, 1200                                    # size of window
car_width, car_height = 25, 50                                      # size of car

vel_inc = 0.4
theta_inc = 4
drag_const = 0.001

GREEN = (0, 138, 55)                                                 # RGB Colours
GREY = (67, 67, 67)
RED = (253, 8, 8)
BLUE = (0, 188, 255)

clock = pg.time.Clock()


class Map():

    def __init__(self):
        self.tilesize = 10
        self.map = np.zeros((int(width/self.tilesize), int(height/self.tilesize)), dtype = int)
        
        shape = self.map.shape

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




class Car():

    def __init__(self, x=1000, y=1000, vel = 0, theta = 0):
        self.x = int(x)
        self.y = int(y)
        self.theta = theta
        self.vel = vel                                         # how far car moves (in pixels) with each press of a button

    def update_pos(self, vel, theta):
        self.y -= np.cos(theta*(2*np.pi)/360)*vel              # calculates new x,y coordinates based on current x,y,vel,theta 
        self.x -= np.sin(theta*(2*np.pi)/360)*vel

    def rot_center(self, img, theta):

        loc = img.get_rect().center                                # rot_image is not defined 
        rot_sprite = pg.transform.rotate(img, theta)
        rot_sprite.get_rect().center = loc
        return rot_sprite

    def checkLegalMove(self, vel, theta):

        self.update_pos(vel, theta)
        img_check = self.rot_center(car_img, theta)                 # rotating image of car

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
        img = self.rot_center(car_img, self.theta)                  # calls function to rotate image around centre point
        # drawing retangle representing actual car width and height #
        pg.draw.rect(win, RED, (self.x - (img.get_rect().width - car_width)/2, self.y - (img.get_rect().height - car_height)/2, img.get_rect().width, img.get_rect().height))
        win.blit(img, (self.x - (img.get_rect().width - car_width)/2, self.y - (img.get_rect().height - car_height)/2)) #subtracting from x and y to ensure smooth rotation


    def sensor(self, sensor_type='FRONT'):

        # defining sensor props 'TYPE':[sensor_range, sensor_angle]
        sensor_dict = {'FRONT':[400, 0], 'LEFT':[300, np.pi/2], 'RIGHT':[300, -np.pi/2], 'F_RIGHT':[300, -np.pi*1/4], 'F_LEFT':[300, np.pi*1/4]}
        sensor_range, sensor_angle = sensor_dict[sensor_type]

        ### Visulisation ###
        img_check = self.rot_center(car_img, self.theta)                                    # rotating original image of car
        centre = img_check.get_rect().center                                           # get centre coords from top corner of car image

        centre_x = self.x - (img_check.get_rect().width - car_width)/2 + centre[0]                             # centre of car image in x
                   
        centre_y = self.y - (img_check.get_rect().height - car_height)/2 + centre[1]                           # centre of car image in y
        beam_length_y = centre_y - sensor_range*np.cos(self.theta*(2*np.pi)/360 + sensor_angle)                # length of beam in y

                                  # draw beam

        ### Obstacle Detection ###
        sensorx = centre_x
        sensory = centre_y
        for i in range(int(sensor_range/5)):                                                            # interate from centre of car until beam length reached
            point = (math.floor(sensorx/Map().tilesize), math.floor(sensory/Map().tilesize))

            if point[0] > width/Map().tilesize -1 or point[1] > height/Map().tilesize -1:               # prevent crash of codeif no wall between car and edge of map
                sensor_read = sensor_range
                break
        
            if Map().map[point[1],point[0]] == 0:                                                       # check current point along beam again map
                break
            else:
                pass

            sensorx -= 5*np.sin(self.theta*(2*np.pi)/360 + sensor_angle)                                # next point along line
            sensory -= 5*np.cos(self.theta*(2*np.pi)/360 + sensor_angle)

        ### Return Sensor Readings (relative to car) ###
        sensor_read = math.sqrt((centre_x - sensorx)**2 + (centre_y - sensory)**2)                      # distance formula in x
        
        
        beam_length_x = centre_x - sensor_read*np.sin(self.theta*(2*np.pi)/360 + sensor_angle)     # length of beam in x
        beam_length_y = centre_y - sensor_read*np.cos(self.theta*(2*np.pi)/360 + sensor_angle)                # length of beam in y
        pg.draw.line(win, BLUE, (centre_x, centre_y), (beam_length_x, beam_length_y))
        
        return round(sensor_read)

### function to produce drag effect ###
def drag(vel):
    if vel >= 0: 
        vel -= drag_const*np.square(vel)  
    else:
        vel += drag_const*np.square(vel)
        
    return vel


def controls():
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
    


def redrawGameWindow():
    race_map.draw()
    car.draw()
    print('--> Front sensor reading: {}'.format(car.sensor('FRONT')))
    print('--> Left sensor reading: {}'.format(car.sensor('LEFT')))
    print('--> Right sensor reading: {}'.format(car.sensor('RIGHT')))
    print('--> Front right sensor reading: {}'.format(car.sensor('F_RIGHT')))
    print('--> Front left sensor reading: {}'.format(car.sensor('F_LEFT')))

    pg.display.update()


def resetGame():
    pg.init()
    win = pg.display.set_mode(size)
    pg.display.set_caption('Car Race')
    car = Car()
    race_map = Map()
    run = True
    car_img = pg.image.load('assets/car-top-view.png').convert_alpha()   # loading car image
    car_img = pg.transform.scale(car_img, (car_width,car_height))        # scaling car image
    return win, car, race_map, run, car_img


######################## MAIN GAME LOOP ########################
def playGame(run, play):
    while run:
        clock.tick(27)                                              # 27 frames per second

        controls()        #registers key strokes 
        car.vel = drag(car.vel) #call drag function
        redrawGameWindow()

        if not car.checkLegalMove(car.vel, car.theta):             # checks whether car is on road or not
            run = False
        else: 
            pass

        for event in pg.event.get():                                                       # if exit button is pressed loop breaks
            if  event.type == pg.QUIT:
                play = False
                print('User Quit Game!')
                run = False

    pg.quit()
    return play


while play:
    win, car, race_map, run, car_img = resetGame()
    play = playGame(run, play)
    time.sleep(0.5)