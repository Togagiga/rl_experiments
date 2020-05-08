# ghetto code: no classes, hard coded numbers, bare bones
import pygame as pg
import random
pg.init()
win_width, win_height = 700, 700
win = pg.display.set_mode((win_width,win_height))
pg.display.set_caption('Simple Game')
win.fill((255, 255, 255))
clock = pg.time.Clock()
car_img = pg.image.load('assets/car-top-view.png')
car_height, car_width = 200, 100
car_img = pg.transform.scale(car_img, (car_width, car_height))

# score function
def score(count):
	font = pg.font.SysFont(None, 25)
	text = font.render("Score: "+str(count), True, (0, 0, 0))
	win.blit(text, (10, 10))

# function to overlay car image on display
def car(x,y):
	win.blit(car_img, (x,y))

# function to display boxes
def box(box_x, box_y, box_w=50, box_h=50, colour=(255, 23, 23)):
	pg.draw.rect(win, colour, [box_x, box_y, box_w, box_h])

def mainLoop():
	# initialising values
	crashed = False
	count = 0
	x = 300
	y = 450
	x_change = 0

	box_w = 50
	box_h = 50
	box_startx = random.randrange(0, win_width-box_w)
	box_starty = - box_h
	box_speed = 10

	# main loop
	while not crashed:

		for event in pg.event.get():
			if event.type == pg.QUIT:
				crashed = True

		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT] and x > 0:
			x_change -= 10
		if keys[pg.K_RIGHT] and x < win_width-car_width:
			x_change += 10

		x += x_change
		x_change = 0

		win.fill((255, 255, 255))
		box(box_startx, box_starty)
		box_starty += box_speed
		car(x,y)
		score(count)

		if box_starty > win_height:   # regenerating box
			box_starty = 0 - box_h
			box_startx = random.randrange(0, win_width-box_w)
			count += 1                # keep score
			box_speed += 0.5          # make boxes move faster incrementially


		if y < box_starty + box_h:
			if x + car_width > box_startx and x < box_startx + box_w:
				crashed = True

		pg.display.update()
		clock.tick(60)

	print('Your score was: {}'.format(count))

mainLoop()
pg.quit()
quit()
