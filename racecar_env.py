### NOTES ###

'''
important functions needed from environment to interface with agent (name for AI in RL):

(when env=Game(), as above)

env.reset() --- called before each episode to reset states and rewards
env.step() --- performs a single step in time and returns rewards, states and done
'''

import numpy as np
import pygame as pg
import math
import time
import random

size = width, height = 1200, 1200                                   # size of window
car_width, car_height = 25, 50                                      # size of car

vel_inc = 0.4
theta_inc = 4
drag_const = 0.001

GREEN = (0, 138, 55)                                                 # RGB Colours
GREY = (67, 67, 67)
RED = (253, 8, 8)
BLUE = (0, 188, 255)


class Map():

    def __init__(self, game):
        self.game = game
        self.tilesize = 10
        self.map = np.zeros((int(width/self.tilesize), int(height/self.tilesize)), dtype = int)
        


        ### Making Ghetto Map ###

        self.map[10:120, 90:110] = 1
        self.map[10:30, 10:110] = 1
        self.map[10:60, 10:30] = 1
        self.map[40:60, 30:80] = 1
        self.map[60:110, 60:80] = 1
        self.map[90:110, 0:80] = 1
        
        ### Drawing reward lines ###
        
        self.map[90:91, 90:110] = 2
        self.map[70:71, 90:110] = 2
        self.map[50:51, 90:110] = 2
        self.map[30:31, 90:110] = 2        
        self.map[10:30, 89:90] = 2
        self.map[10:30, 70:71] = 2
        self.map[10:30, 50:51] = 2
        self.map[10:30, 30:31] = 2        
        self.map[35:36, 10:30] = 2        
        self.map[40:60, 30:31] = 2
        self.map[40:60, 50:51] = 2        
        self.map[60:61, 60:80] = 2
        self.map[80:81, 60:80] = 2        
        self.map[90:110, 59:60] = 2
        self.map[90:110, 40:41] = 2
        self.map[90:110, 20:21] = 2

        
        
    def draw(self):

        for i in range(0, width, self.tilesize):
            for j in range(0, height, self.tilesize):
                if self.map[int(i/self.tilesize),int(j/self.tilesize)] == 0:
                    pg.draw.rect(self.game.win, GREEN, (j, i, self.tilesize, self.tilesize))
                elif self.map[int(i/self.tilesize),int(j/self.tilesize)] == 1:
                    pg.draw.rect(self.game.win, GREY, (j, i, self.tilesize, self.tilesize))
                elif self.map[int(i/self.tilesize),int(j/self.tilesize)] == 2:
                    pg.draw.rect(self.game.win, GREY, (j, i, self.tilesize, self.tilesize))



class Car():

    def __init__(self, game, map_class, x=1000, y=1000, vel = 0, theta = 0, on_red = 0):
        self.game = game                                       # instance of Game class
        self.map = map_class                                   # named map_class to avoid clash with map keyword
        self.tilesize = map_class.tilesize
        self.x = int(x)
        self.y = int(y)
        self.theta = theta
        self.vel = vel                                         # how far car moves (in pixels) with each press of a button
        self.on_red = on_red

        self.car_img = pg.image.load('assets/car-top-view.png').convert_alpha()   # loading car image
        self.car_img = pg.transform.scale(self.car_img, (car_width,car_height))        # scaling car image

    def update_pos(self, vel, theta):
        self.y -= np.cos(theta*(2*np.pi)/360)*vel              # calculates new x,y coordinates based on current x,y,vel,theta 
        self.x -= np.sin(theta*(2*np.pi)/360)*vel

    def rot_center(self, img, theta):

        loc = img.get_rect().center                                # rot_image is not defined 
        rot_sprite = pg.transform.rotate(img, theta)
        rot_sprite.get_rect().center = loc
        return rot_sprite

    ### function to produce drag effect ###
    def drag(self, vel):
        if vel >= 0: 
            vel -= drag_const*np.square(vel)  
        else:
            vel += drag_const*np.square(vel)
            
        return vel

    def checkLegalMove(self, vel, theta):

        img_check = self.rot_center(self.car_img, theta)       # rotating image of car

        car_h = img_check.get_rect().height                    # rotated size of car
        car_w = img_check.get_rect().width

        check_x = self.x - (car_w - car_width)/2               # position account for car turning
        check_y = self.y - (car_h - car_height)/2
        
        map_y = math.floor(check_y/self.tilesize)              # position in tiles
        map_x = math.floor(check_x/self.tilesize)

        car_h_tiles = math.ceil(car_h/self.tilesize)           # getting car size in tiles
        car_w_tiles = math.ceil(car_w/self.tilesize)

        check =  np.argwhere(self.map.map[map_y:map_y + car_h_tiles, map_x:map_x + car_w_tiles] == 0)  # if car is on zeros on map
        check_score = np.argwhere(self.map.map[map_y:map_y + car_h_tiles, map_x:map_x + car_w_tiles] == 2)
        
        if len(check) != 0:
            return True
            
        else:
            if len(check_score) != 0:
                self.on_red = 1
            
            else:
                if self.on_red == 1:
                    self.game.reward += 5
                self.on_red = 0
            return False
            
        

    def draw(self):
        # rotating car image
        img = self.rot_center(self.car_img, self.theta)
        # blitting over car in previous time step
        pg.draw.rect(self.game.win, GREY, (self.x - (img.get_rect().width - car_width)/2 - 1, self.y - (img.get_rect().height - car_height)/2 - 1, img.get_rect().width + 2, img.get_rect().height + 2))
        # updating the positon of car for time step
        self.update_pos(self.vel, self.theta)
        # rotating car image
        img = self.rot_center(self.car_img, self.theta)
        # drawing retangle representing actual car width and height
        pg.draw.rect(self.game.win, GREY, (self.x - (img.get_rect().width - car_width)/2, self.y - (img.get_rect().height - car_height)/2, img.get_rect().width, img.get_rect().height))
        # blitting car of current time step to game window
        self.game.win.blit(img, (self.x - (img.get_rect().width - car_width)/2, self.y - (img.get_rect().height - car_height)/2)) #subtracting from x and y to ensure smooth rotation



    def sensor(self, sensor_type='FRONT'):

        # defining sensor props 'TYPE':[sensor_range, sensor_angle]
        sensor_dict = {'FRONT':[400, 0], 'LEFT':[300, np.pi/2], 'RIGHT':[300, -np.pi/2], 'F_RIGHT':[300, -np.pi*1/4], 'F_LEFT':[300, np.pi*1/4]}
        sensor_range, sensor_angle = sensor_dict[sensor_type]

        ### Setup of Coordinates ###
        img_check = self.rot_center(self.car_img, self.theta)                                    # rotating original image of car
        centre = img_check.get_rect().center                                           # get centre coords from top corner of car image

        centre_x = self.x - (img_check.get_rect().width - car_width)/2 + centre[0]                             # centre of car image in x          
        centre_y = self.y - (img_check.get_rect().height - car_height)/2 + centre[1]                           # centre of car image in y
                                 

        ### Obstacle Detection ###
        sensorx = centre_x
        sensory = centre_y
        for i in range(int(sensor_range/5)):                                                            # interate from centre of car until beam length reached
            point = (math.floor(sensorx/self.tilesize), math.floor(sensory/self.tilesize))

            if point[0] > width/self.tilesize -1 or point[1] > height/self.tilesize -1:               # prevent crash of codeif no wall between car and edge of map
                sensor_read = sensor_range
                break
            
            # self.map.map is because of terrible naming of the map instance being passed into car class in __init__
            # cannot be arsed changing it...sorry
            if self.map.map[point[1],point[0]] == 0:                                                  # check current point along beam again map
                break
            else:
                pass

            sensorx -= 5*np.sin(self.theta*(2*np.pi)/360 + sensor_angle)                               # next point along line
            sensory -= 5*np.cos(self.theta*(2*np.pi)/360 + sensor_angle)

        ### Return Sensor Readings (relative to car) ###
        sensor_read = math.sqrt((centre_x - sensorx)**2 + (centre_y - sensory)**2)                      # distance formula in x
        
        ### Visualisation ###
        # beam_length_x = centre_x - sensor_read*np.sin(self.theta*(2*np.pi)/360 + sensor_angle)         # length of beam in x
        # beam_length_y = centre_y - sensor_read*np.cos(self.theta*(2*np.pi)/360 + sensor_angle)         # length of beam in y
        # pg.draw.line(win, BLUE, (centre_x, centre_y), (beam_length_x, beam_length_y))                  # draw beam
        
        return round(sensor_read)



class Game():

    def __init__(self):

        pg.init()
        self.win = pg.display.set_mode(size)
        self.clock = pg.time.Clock()
        pg.display.set_caption('Car Race')
        self.map = Map(self)
        self.car = Car(self, self.map)      # passing in self as the game class instance
        self.map.draw()
        self.reward = 0
        self.done = False
        self.quit = False

        self.generation = 0
        self.model = 1


    def reset(self, generation, model):

        self.generation = generation
        self.model = model

        if self.quit == True:              # allows to quit all episodes by quitting game window
        # none of the values are reset, so once current episode finishes, all following episodes
        # will be in grass and thus only perform one loop before also terminating
        # Not the most elegent solution but it quits the training process a lot faster
            return

        self.done = False
        self.car.x = 1000
        self.car.y = 1000
        self.car.vel = 0
        self.car.theta = 0
        self.car.on_red = 0
        self.reward = 0
        self.map.draw()

        state = [self.car.sensor("LEFT"),
                self.car.sensor("F_LEFT"),
                self.car.sensor("FRONT"),
                self.car.sensor("F_RIGHT"),
                self.car.sensor("RIGHT"),
                self.car.vel]

        return state


    def score(self):
        font = pg.font.SysFont(None, 25)
        text_gen = font.render("Generation: "+str(self.generation), True, (0, 0, 0))
        text_model = font.render("Model: "+str(self.model), True, (0, 0, 0))
        self.win.blit(text_gen, (10, 10))
        self.win.blit(text_model, (10, 30))


    # being called in step method
    def controls(self, action):

        # potential to add reward for different types of actions
        # right hand coord-sys: -theta==clockwise, +theta==anti-clockwise

        if action == 0:                               # forward + left
            self.car.vel += vel_inc
            self.car.vel = self.car.drag(self.car.vel)   
            self.car.theta += theta_inc
        elif action == 1:                             # forward + right
            self.car.vel += vel_inc
            self.car.vel = self.car.drag(self.car.vel)   
            self.car.theta -= theta_inc
        elif action == 2:                             # left
            self.car.theta += theta_inc
        elif action == 3:                             # right
            self.car.theta -= theta_inc
        elif action == 4:                             # forward
            self.car.vel += vel_inc
            self.car.vel = self.car.drag(self.car.vel)   



    # being called in run_frame method
    def redrawGameWindow(self):

        self.done = False
        self.car.draw()
        self.score()
        pg.display.update()


    def step(self, action):

        self.reward = 0
        self.done = False
        self.controls(action)

        self.run_frame()

        state = [self.car.sensor("LEFT"),
                self.car.sensor("F_LEFT"),
                self.car.sensor("FRONT"),
                self.car.sensor("F_RIGHT"),
                self.car.sensor("RIGHT"),
                self.car.vel]

        return self.reward, state, self.done


    # being called in step method
    def run_frame(self):

        for event in pg.event.get():                                                    # if exit button is pressed loop breaks
            if event.type == pg.QUIT:
               self.done = True
               self.quit = True                   # quit all episodes
               return self.done, self.quit

        self.redrawGameWindow()
        self.done = self.car.checkLegalMove(self.car.vel, self.car.theta)               # checks whether car is on road or not
        self.reward += np.power(self.car.vel,3)*0.0001         # velocity reward                               # add to reward for time step, reward for vel
        self.clock.tick(30)





if __name__ == "__main__":

    env = Game()
    total_reward = 0
    while env.done == False:
        reward, state, done = env.step(random.randint(0,4))    # each time step returns rewards, states, done
        total_reward += reward
        print(f"Step Reward: {reward}")
        print(f"State: {state}")
        print(f"Done: {done}")
    print(f"CUMULATIVE REWARD: {total_reward}")    # total reward of episode