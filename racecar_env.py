### NOTES ###

'''
important functions needed from environment to interface with agent:

(when env=Game(), as above)

env.reset() --- called before each episode to reset states and rewards
env.step() --- performs a single step in time and returns rewards, states and done
'''

import numpy as np
import pygame as pg
import math


size = width, height = 1000, 1000                              # size of window
car_width, car_height = 25, 50                                 # size of car

vel_inc = 0.2
theta_inc = 6
drag_const = 0.001

map_type = 1                                              # 0 is Ghetto (OG), 1 is more detailed

GREEN = (0, 138, 55)                                           # RGB Colours
GREY = (67, 67, 67)
RED = (253, 8, 8)
BLUE = (0, 188, 255)


class Map():

    def __init__(self, Game):
        self.Game = Game        # instance of Game class
        self.tilesize = 10
        self.map = np.zeros((int(width/self.tilesize), int(height/self.tilesize)), dtype = int)
        
        if map_type == 0:
            ### Making Ghetto Map ###

            self.map[10:90, 70:90] = 1
            self.map[10:30, 10:90] = 1
            self.map[10:60, 10:30] = 1
            self.map[40:60, 30:60] = 1
            self.map[60:90, 40:60] = 1
            self.map[70:90, 0:60] = 1
            
            ### Drawing reward lines ###
            
            self.map[70:71, 70:90] = 2
            self.map[50:51, 70:90] = 2
            self.map[30:31, 70:90] = 2
            self.map[10:30, 69:70] = 2
            self.map[10:30, 50:51] = 2
            self.map[10:30, 30:31] = 2
            self.map[30:31, 10:30] = 2
            self.map[39:40, 10:30] = 2
            self.map[40:60, 30:31] = 2
            self.map[40:60, 39:40] = 2
            self.map[60:61, 40:60] = 2
            self.map[69:70, 40:60] = 2
            self.map[70:90, 39:40] = 2
            self.map[70:90, 20:21] = 2
    
            ### Drawing finish lines ###
    
            self.map[70:90, 0:5] = 3
            
            self.starting_pos = [800,800]
            
        else:
            ### Drawing roads ###    
            self.map[60:100, 80:95] = 1
            self.map[60:75, 50:95] = 1
            self.map[30:60, 50:65] = 1
            self.map[30:45, 65:95] = 1
            self.map[5:30, 80:95] = 1
            self.map[5:20, 30:80] = 1
            self.map[20:95, 30:45] = 1
            self.map[80:95, 5:30] = 1
            self.map[0:95, 5:20] = 1
            
            ### Drawing reward lines ###            
            self.map[85:86, 80:95] = 2
            self.map[60:75, 70:71] = 2
            self.map[48:49, 50:65] = 2
            self.map[30:45, 70:71] = 2
            self.map[23:24, 80:95] = 2
            self.map[5:20, 55:56] = 2
            self.map[25:26, 30:45] = 2
            self.map[65:66, 30:45] = 2
            self.map[80:95, 25:26] = 2
            self.map[65:66, 5:20] = 2
            self.map[25:26, 5:20] = 2    
    
            ### Drawing finish lines ###    
            self.map[0:5, 5:20] = 3
            
            self.starting_pos = [880,900]
            


    def read_map(self, filename):
        
        self.map = []
        with open(filename, "r") as file:
            for line in file:
                result = line.rstrip().split()
                result = [int(i) for i in result]
                self.map.append(result)

        self.map = np.array(self.map).reshape(len(self.map), len(self.map[0]))

        return self.map
        
        
    def draw(self):

        for i in range(0, width, self.tilesize):
            for j in range(0, height, self.tilesize):
                if self.map[int(i/self.tilesize),int(j/self.tilesize)] == 0:
                    pg.draw.rect(self.Game.win, GREEN, (j, i, self.tilesize, self.tilesize))
                elif self.map[int(i/self.tilesize),int(j/self.tilesize)] == 1:
                    pg.draw.rect(self.Game.win, GREY, (j, i, self.tilesize, self.tilesize))
                elif self.map[int(i/self.tilesize),int(j/self.tilesize)] == 2:
                    pg.draw.rect(self.Game.win, RED, (j, i, self.tilesize, self.tilesize))
                elif self.map[int(i/self.tilesize),int(j/self.tilesize)] == 3:
                    pg.draw.rect(self.Game.win, RED, (j, i, self.tilesize, self.tilesize))



class Car():

    def __init__(self, Game, Map, x, y, vel = 0, theta = 0):
        self.Game = Game                                       # instance of Game class
        self.Map = Map                                         # instance of Map class
        self.tilesize = self.Map.tilesize
        self.x = self.Map.starting_pos[0]
        self.y = self.Map.starting_pos[1]
        self.theta = theta
        self.vel = vel                                         # how far car moves (in pixels) with each press of a button
        self.on_red = 0

        self.car_img = pg.image.load('assets/car-top-view.png').convert_alpha()   # loading car image
        self.car_img = pg.transform.scale(self.car_img, (car_width,car_height))   # scaling car image

    def update_pos(self, vel, theta):
        self.y -= np.cos(theta*(2*np.pi)/360)*vel              # calculates new x,y coordinates based on current x,y,vel,theta 
        self.x -= np.sin(theta*(2*np.pi)/360)*vel

    def rot_center(self, img, theta):

        loc = img.get_rect().center                            # rot_image is not defined 
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

        check =  np.argwhere(self.Map.map[map_y:map_y + car_h_tiles, map_x:map_x + car_w_tiles] == 0)  # if car is on zeros on map
        check_score = np.argwhere(self.Map.map[map_y:map_y + car_h_tiles, map_x:map_x + car_w_tiles] == 2)
        check_finish = np.argwhere(self.Map.map[map_y:map_y + car_h_tiles, map_x:map_x + car_w_tiles] == 3)
        
        if len(check) != 0:
            return True      # sets self.done == True
        elif len(check_finish) != 0:
            self.Game.reward += 500
            return True

        ### need to catch when in finish and stop GA
            
        else:
            if len(check_score) != 0:
                self.on_red = 1
            
            else:
                if self.on_red == 1:
                    self.Game.reward += 5
                   
                self.on_red = 0
            return False
            
        

    def draw(self):
        # rotating car image
        img = self.rot_center(self.car_img, self.theta)
        # blitting over car in previous time step
        pg.draw.rect(self.Game.win, GREY, (self.x - (img.get_rect().width - car_width)/2 - 1, self.y - (img.get_rect().height - car_height)/2 - 1, img.get_rect().width + 2, img.get_rect().height + 2))
        # updating the positon of car for time step
        self.update_pos(self.vel, self.theta)
        # rotating car image
        img = self.rot_center(self.car_img, self.theta)
        # drawing retangle representing actual car width and height
        pg.draw.rect(self.Game.win, GREY, (self.x - (img.get_rect().width - car_width)/2, self.y - (img.get_rect().height - car_height)/2, img.get_rect().width, img.get_rect().height))
        # blitting car of current time step to game window
        self.Game.win.blit(img, (self.x - (img.get_rect().width - car_width)/2, self.y - (img.get_rect().height - car_height)/2)) #subtracting from x and y to ensure smooth rotation



    def sensor(self, sensor_type='FRONT'):

        # defining sensor props 'TYPE':[sensor_range, sensor_angle]
        sensor_dict = {'FRONT':[400, 0], 'LEFT':[300, np.pi/2], 'RIGHT':[300, -np.pi/2], 'F_RIGHT':[300, -np.pi*1/4], 'F_LEFT':[300, np.pi*1/4]}
        sensor_range, sensor_angle = sensor_dict[sensor_type]

        ### Setup of Coordinates ###
        img_check = self.rot_center(self.car_img, self.theta)                                          # rotating original image of car
        centre = img_check.get_rect().center                                                           # get centre coords from top corner of car image

        centre_x = self.x - (img_check.get_rect().width - car_width)/2 + centre[0]                     # centre of car image in x          
        centre_y = self.y - (img_check.get_rect().height - car_height)/2 + centre[1]                   # centre of car image in y
                                 

        ### Obstacle Detection ###
        sensorx = centre_x
        sensory = centre_y
        for i in range(int(sensor_range/5)):                                                           # interate from centre of car until beam length reached
            point = (math.floor(sensorx/self.tilesize), math.floor(sensory/self.tilesize))

            if point[0] > width/self.tilesize -1 or point[1] > height/self.tilesize -1:                # prevent crash of codeif no wall between car and edge of map
                sensor_read = sensor_range
                break
            
            if self.Map.map[point[1],point[0]] == 0:                                                   # check current point along beam again map
                break
            else:
                pass

            sensorx -= 5*np.sin(self.theta*(2*np.pi)/360 + sensor_angle)                               # next point along line
            sensory -= 5*np.cos(self.theta*(2*np.pi)/360 + sensor_angle)

        ### Return Sensor Readings (relative to car) ###
        sensor_read = math.sqrt((centre_x - sensorx)**2 + (centre_y - sensory)**2)                     # distance formula in x
        
        ### Visualisation ###
        # beam_length_x = centre_x - sensor_read*np.sin(self.theta*(2*np.pi)/360 + sensor_angle)       # length of beam in x
        # beam_length_y = centre_y - sensor_read*np.cos(self.theta*(2*np.pi)/360 + sensor_angle)       # length of beam in y
        # pg.draw.line(win, BLUE, (centre_x, centre_y), (beam_length_x, beam_length_y))                # draw beam
        
        return round(sensor_read)



class Game():

    def __init__(self):

        pg.init()
        self.win = pg.display.set_mode(size)
        self.clock = pg.time.Clock()
        pg.display.set_caption('Car Race')
        self.Map = Map(self)
        self.Car = Car(self, self.Map, self.Map.starting_pos[0], self.Map.starting_pos[1])      # passing in self as the game class instance
        self.Map.draw()
        self.reward = 0
        self.done = False
        self.quit = False

        self.generation = 0
        self.model = 1


    def reset(self, generation = 0, model = 0):

        self.generation = generation
        self.model = model

        self.done = False
        self.Car.x = self.Map.starting_pos[0]
        self.Car.y = self.Map.starting_pos[1]
        self.Car.vel = 0
        self.Car.theta = 0
        self.Car.on_red = 0
        self.reward = 0
        self.Map.draw()
        self.score()

        state = [self.Car.sensor("LEFT"),
                self.Car.sensor("F_LEFT"),
                self.Car.sensor("FRONT"),
                self.Car.sensor("F_RIGHT"),
                self.Car.sensor("RIGHT"),
                self.Car.vel]

        state = np.array(state)/max(state)

        return state


    def score(self):
        font = pg.font.SysFont(None, 25)
        text_gen = font.render("Generation: "+str(self.generation), True, (0, 0, 0))
        text_model = font.render("Model: "+str(self.model), True, (0, 0, 0))
        self.win.blit(text_gen, (10, 10))
        self.win.blit(text_model, (10, 30))


    # being called in step method
    def controls(self, action):

        # right hand coord-sys: -theta==clockwise, +theta==anti-clockwise

        if action == 0:                                         # forward + left
            self.Car.vel += vel_inc
            self.Car.theta += theta_inc
        elif action == 1:                                       # forward + right
            self.Car.vel += vel_inc
            self.Car.theta -= theta_inc
        elif action == 2:                                       # left
            self.Car.theta += theta_inc
        elif action == 3:                                       # right
            self.Car.theta -= theta_inc
        elif action == 4:                                       # forward
            self.Car.vel += vel_inc
        elif action == 5:                                       # cruise
            pass
   


    # being called in run_frame method
    def redrawGameWindow(self):

        self.done = False
        self.Car.draw()
        pg.display.update()


    def step(self, action):

        self.reward = 0
        self.done = False
        self.controls(action)

        self.run_frame()

        state = [self.Car.sensor("LEFT"),
                self.Car.sensor("F_LEFT"),
                self.Car.sensor("FRONT"),
                self.Car.sensor("F_RIGHT"),
                self.Car.sensor("RIGHT"),
                self.Car.vel]

        state = np.array(state)/max(state)

        return self.reward, state, self.done


    # being called in step method
    def run_frame(self):

        for event in pg.event.get():                                      # if exit button is pressed loop breaks
            if event.type == pg.QUIT:
               self.done = True
               self.quit = True                                           # quit all episodes
               return self.done, self.quit

        self.redrawGameWindow()
        self.done = self.Car.checkLegalMove(self.Car.vel, self.Car.theta) # checks whether car is on road or not
        self.reward += (self.Car.vel)*0.001                 # reward for vel
        self.Car.vel = self.Car.drag(self.Car.vel)                        # add drag after each step
        self.clock.tick(100)



##### FOR KEY INPUT ONLY #####

def get_user_input():

    keys = pg.key.get_pressed()

    if keys[pg.K_UP] and keys[pg.K_LEFT]:
        return 0
    elif keys[pg.K_UP] and keys[pg.K_RIGHT]:
        return 1
    elif keys[pg.K_LEFT]:
        return 2
    elif keys[pg.K_RIGHT]:
        return 3
    elif keys[pg.K_UP]:
        return 4

##############################



if __name__ == "__main__":

    env = Game()
    # env.reset()
    total_reward = 0
    while env.done == False:
        action = get_user_input()
        reward, state, done = env.step(action)                            # each time step returns rewards, states, done
        total_reward += reward
        # print(f"Step Reward: {reward}")
        # print(f"State: {state}")
        # print(f"Done: {done}")
    print(f"CUMULATIVE REWARD: {total_reward}")                           # total reward of episode