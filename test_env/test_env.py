import pygame as pg
import random

class Car():
	def __init__(self):

		# Game
		pg.init()
		self.win_width, self.win_height = 700, 700
		self.win = pg.display.set_mode((self.win_width,self.win_height))
		pg.display.set_caption('Simple Game')
		self.win.fill((255, 255, 255))
		self.clock = pg.time.Clock()
		self.car_img = pg.image.load('car-top-view.png')
		self.car_height, self.car_width = 200, 100
		self.car_img = pg.transform.scale(self.car_img, (self.car_width, self.car_height))
		self.done = False
		self.reward = 0
		self.count = 0

		# Car
		self.x = 300
		self.y = 450
		self.x_change = 0

		# Box
		self.box_w = 50
		self.box_h = 50
		self.box_startx = random.randrange(0, self.win_width-self.box_w)
		self.box_starty = - self.box_h
		self.box_speed = 10


	def score(self):
		font = pg.font.SysFont(None, 25)
		text = font.render("Score: "+str(self.count), True, (0, 0, 0))
		self.win.blit(text, (10, 10))

	# def highScore(self, high_count):
	# 	font = pg.font.SysFont(None, 25)
	# 	text = font.render("High Score: "+str(high_count), True, (0, 0, 0))
	# 	win.blit(text, (10, 30))

	# function to overlay car image on display
	def car(self):
		self.win.blit(self.car_img, (self.x,self.y))

	# function to display boxes
	def box(self, colour=(255, 23, 23)):
		pg.draw.rect(self.win, colour, [self.box_startx, self.box_starty, self.box_w, self.box_h])

	def car_right(self):
		if self.x < self.win_width-self.car_width:
			self.x_change += 10
			self.x += self.x_change
			self.x_change = 0

	def car_left(self):
		if self.x > 0:
			self.x_change -= 10
			self.x += self.x_change
			self.x_change = 0

########## Controls for Agent #########

	def reset(self):
		self.done = False
		self.count = 0
		self.box_starty = - self.box_h
		self.x = 300
		self.y = 450
		self.box_speed = 10
		return [self.x, self.box_startx, self.box_starty, self.box_speed]

	# 0 move left
	# 1 do nothing
	# 2 move right

	def step(self, action):
		self.reward = 0
		self.done = False
 
		if action == 0:
			self.car_left()
			self.reward -= 0.1

		if action == 2:
			self.car_right()
			self.reward -= 0.1

		self.run_frame()

		state = [self.x, self.box_startx, self.box_starty, self.box_speed]
		return self.reward, state, self.done

#######################################

	def run_frame(self):

		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.done = True

		self.win.fill((255, 255, 255))
		self.box()
		self.box_starty += self.box_speed
		self.car()
		self.score()

		if self.box_starty > self.win_height:   # regenerating boxf
			self.box_starty = 0 - self.box_h
			self.box_startx = random.randrange(0, self.win_width-self.box_w)
			self.count += 1                # keep score
			self.reward += 3
			self.box_speed += 0.1          # make boxes move faster incrementially

		if self.y < self.box_starty + self.box_h:    # check for collision
			if self.x + self.car_width > self.box_startx and self.x < self.box_startx + self.box_w:
				self.done = True
				self.reward -= 3

		self.clock.tick(60)
		pg.display.update()


# env = Car()
# while env.done == False:
# 	reward, state, done = env.step(random.randint(0,2))
# 	print(f"Reward: {reward}")