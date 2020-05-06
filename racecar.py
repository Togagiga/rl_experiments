# wee race car game

# need to add proper map --> possibly improve algorithm
#__________________________________________________________________________
# need to ensure windows size, tile size and car initial position work!!!!!
#__________________________________________________________________________

import numpy as np
import pygame
import time

pygame.init()
size = width, height = 700, 700
win = pygame.display.set_mode(size)
pygame.display.set_caption('Car Race')

background = win.fill((255, 255, 255))       # white 8-bit
car_img = pygame.image.load('assets/car-top-view.png').convert_alpha()
car_width = 100
car_height = 200
car_img = pygame.transform.scale(car_img, (car_width,car_height))

clock = pygame.time.Clock()

class Map():

	def __init__(self):
		self.tilesize = 10
		self.map = np.zeros((int(width/self.tilesize), int(height/self.tilesize)), dtype = int)

		shape = self.map.shape
		road_width = 100/self.tilesize
		self.map[:,int(shape[0]/2-road_width):int(shape[1]/2+road_width)] = 1   # make road of ones

	def draw(self):

		# # draw grid
		# for x in range(0, width, self.tilesize):
		# 	pygame.draw.line(win, (0,0,0), (x,0), (x, height))
		# for y in range(0, height, self.tilesize):
		# 	pygame.draw.line(win, (0,0,0), (0,y), (width, y))

		map_shape =self.map.shape
		for i in range(0, width, self.tilesize):
			for j in range(0, height, self.tilesize):
				if self.map[int(i/self.tilesize),int(j/self.tilesize)] == 0:
					green = pygame.draw.rect(win, (3, 206, 78), (j, i, 0+self.tilesize, 0+self.tilesize))
				elif self.map[int(i/self.tilesize),int(j/self.tilesize)] == 1:
					green = pygame.draw.rect(win, (67, 67, 67), (j, i, 0+self.tilesize, 0+self.tilesize))



class Car():

	# need to initialise car position --> need to occupy whole number of squares
	def __init__(self, x=width/2-car_width/2, y=height*(2/3), width=car_width, height=car_height):
		self.x = x
		self.y = y
		self.stationary = True # initially not moving (before player input)
		self.left = False
		self.right = False
		self.vel = 10          # how far car moves (in pixels) with each press of a button

	# def checkLegalMove(self, initMap):
		# need to check if move is allowed

	def draw(self):
		win.blit(car_img, (self.x, self.y))


def redrawGameWindow():
	win.fill((255,255,255))
	race_map.draw()
	car.draw()

	# add more func to Car class

	pygame.display.update()


######### Main Loop ##########
car = Car()
race_map = Map()
run = True
while run:
	clock.tick(27)  # 27 frames per second

	for event in pygame.event.get():    # if exit button is pressed loop breaks
		if  event.type == pygame.QUIT:
			run = False


	keys = pygame.key.get_pressed()

	# filters so car cannot go off screen
	if keys[pygame.K_LEFT] and car.x >= car.vel:
		car.x -= car.vel
	elif keys[pygame.K_RIGHT] and car.x < width-car_width - car.vel:
		car.x += car.vel

	redrawGameWindow()

pygame.quit()