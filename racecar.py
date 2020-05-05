# race car game for testing

import numpy as np
import pygame
import time

pygame.init()
size = width, height = 700, 700
win = pygame.display.set_mode(size)
pygame.display.set_caption('Car Race')

background = win.fill((255, 255, 255))       # white 8-bit
car_img = pygame.image.load('assets/car-top-view.png')
car_width = 100
car_height = 200
car_img = pygame.transform.scale(car_img, (car_width,car_height))

clock = pygame.time.Clock()


class Car():

	def __init__(self, x=width/2-car_width/2, y=height*(2/3), width=car_width, height=car_height):
		self.x = x
		self.y = y
		self.stationary = True # initially not moving (before player input)
		self.left = False
		self.right = False
		self.vel = 10

	def draw(self, win):
		win.blit(car_img, (self.x, self.y))


def redrawGameWindow():
	win.fill((255,255,255))
	car.draw(win)
	# add more func to Car class

	pygame.display.update()


######### Main Loop ##########
car = Car()
run = True
while run:
	clock.tick(27)  # 27 frames per second

	for event in pygame.event.get():    # if exit button is pressed loop breaks
		if  event.type == pygame.QUIT:
			run = False


	keys = pygame.key.get_pressed()


	if keys[pygame.K_LEFT] and car.x >= car.vel:
		car.x -= car.vel
	elif keys[pygame.K_RIGHT] and car.x < width-car_width - car.vel:
		car.x += car.vel


	keys = pygame.key.get_pressed()

	redrawGameWindow()

pygame.quit()