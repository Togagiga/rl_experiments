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

		for i in range(0, width, self.tilesize):
			for j in range(0, height, self.tilesize):
				if self.map[int(i/self.tilesize),int(j/self.tilesize)] == 0:
					green = pygame.draw.rect(win, (3, 206, 78), (j, i, self.tilesize, self.tilesize))
				elif self.map[int(i/self.tilesize),int(j/self.tilesize)] == 1:
					green = pygame.draw.rect(win, (67, 67, 67), (j, i, self.tilesize, self.tilesize))



class Car():

	# need to initialise car position --> need to occupy whole number of squares
	def __init__(self, x=width/2-car_width/2, y=height/2 - car_height/2, width=car_width, height=car_height):
		self.x = x
		self.y = y
		self.stationary = True # initially not moving (before player input)
		self.left = False
		self.right = False
		self.vel = 10          # how far car moves (in pixels) with each press of a button

	def checkLegalMove(self, inpY, inpX):
		
		map_y = int(self.y/Map().tilesize + inpY)
		map_x = int(self.x/Map().tilesize + inpX)

		check =  np.argwhere(Map().map[map_y:map_y + 20, map_x:map_x + 10] == 0)
		if len(check) != 0:
			return False
		else:
			return True
		# 	return True
		# else:
		# 	return False

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
	if keys[pygame.K_LEFT] and car.x >= car.vel and car.checkLegalMove(0,-1):
		car.x -= car.vel
	elif keys[pygame.K_RIGHT] and car.x < width-car_width - car.vel and car.checkLegalMove(0,+1):
		car.x += car.vel
	elif keys[pygame.K_UP] and car.y >= car.vel and car.checkLegalMove(-1,0):
		car.y -= car.vel
	elif keys[pygame.K_DOWN] and car.y <= height-car_height - car.vel and car.checkLegalMove(1,0):
		car.y += car.vel

	redrawGameWindow()

pygame.quit()