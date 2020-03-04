#!/pygame_snake_oop/bin python

import pygame

from random import randint
from time import sleep


class Snake():

	def __init__(self, screen_width, screen_height):
		self.snake_ate = 0
		self.snake_life = 'alive'
		self.snake_direction = 'rigth'
		self.snake_body = [[10, 30], [10, 20], [10, 10]]
		self.snake_color = (255, 255, 255)
		# [y, x]

		self.screen_width = screen_width
		self.screen_height = screen_height

	def snake_walk(self, new_direction, speed, foodx, foody):
		snake_head = self.snake_body[0]
		old_snake_head = snake_head

		def pop_snake():
			if self.snake_ate == 0:
				self.snake_body.pop()
				new_direction == self.snake_direction

		if new_direction == 'rigth' and self.snake_direction != 'left':

			self.snake_direction = 'rigth'

			if snake_head[1] == self.screen_width:
				self.snake_body.insert(0, [snake_head[0], 0])
			else:
				self.snake_body.insert(0, [snake_head[0], snake_head[1] + 10])

			pop_snake()

		elif new_direction == 'left' and self.snake_direction != 'rigth':

			self.snake_direction = 'left'

			if snake_head[1] == 0:
				self.snake_body.insert(0, [snake_head[0], self.screen_width])
			else:
				self.snake_body.insert(0, [snake_head[0], snake_head[1] - 10])

			pop_snake()

		elif new_direction == 'up' and self.snake_direction != 'down':

			self.snake_direction = 'up'

			if snake_head[0] == 0:
				self.snake_body.insert(0, [self.screen_height, snake_head[1]])
			else:
				self.snake_body.insert(0, [snake_head[0] - 10, snake_head[1]])

			pop_snake()

		elif new_direction == 'down' and self.snake_direction != 'up':

			self.snake_direction = 'down'

			if snake_head[0] == self.screen_height:
				self.snake_body.insert(0, [0, snake_head[1]])
			else:
				self.snake_body.insert(0, [snake_head[0] + 10, snake_head[1]])

			pop_snake()

		self.snake_ate = 0

		print('\nfood:x={}y={}\nspeed:{}\nsnake:{}\nlength:{}\nmoving {}\nfrom:{}\nto:{}\n'.format(
			foodx, foody, speed, self.snake_body, len(self.snake_body), new_direction, old_snake_head, self.snake_body[0]))

	def is_snake_dead(self):
		body = self.snake_body
		if body[len(body) - 1] in body[:len(body) - 2]:
			self.snake_life = 'dead'

	def did_snake_ate(self, food_coords):
		if self.snake_body[0][0] == food_coords[0] and self.snake_body[0][1] == food_coords[1]:
			self.snake_ate = 1


class Food():

	def __init__(self, screen_width, screen_height):
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.food_color = (255, 0, 0)

		self.x_coord = 20
		self.y_coord = 20

	def generate_new_food(self):
		tmp_x_coord = randint(1, self.screen_height / 10)
		tmp_y_coord = randint(1, self.screen_width / 10)

		tmp_x_coord = str(tmp_x_coord) + '0'
		tmp_y_coord = str(tmp_y_coord) + '0'

		self.x_coord = int(tmp_x_coord)
		self.y_coord = int(tmp_y_coord)


class Screen():

	def __init__(self, display_width, display_heigth):
		self.display_width = display_width
		self.display_heigth = display_heigth

		pygame.init()

		self.screen = pygame.display.set_mode((display_width, display_heigth))
		self.clock = pygame.time.Clock()

		self.game_speed = .3

		self.snake = Snake(display_width, display_heigth)
		self.food = Food(display_width, display_heigth)

		self.finished = False

	def bootstrap(self):

		def snake_movement(pygame_events):
			for event in pygame_events:
				if event.type == pygame.QUIT or self.snake.snake_life == 'dead':
					self.finished = True
					pygame.quit()
					break

				if event.type == pygame.KEYDOWN:

					print(self.snake.snake_body)

					if event.key == pygame.K_LEFT:
						self.snake.snake_walk('left', self.game_speed, self.food.x_coord, self.food.y_coord)
					elif event.key == pygame.K_RIGHT:
						self.snake.snake_walk('rigth', self.game_speed, self.food.x_coord, self.food.y_coord)
					elif event.key == pygame.K_UP:
						self.snake.snake_walk('up', self.game_speed, self.food.x_coord, self.food.y_coord)
					elif event.key == pygame.K_DOWN:
						self.snake.snake_walk('down', self.game_speed, self.food.x_coord, self.food.y_coord)

			else:
				self.snake.snake_walk(self.snake.snake_direction, self.game_speed, self.food.x_coord, self.food.y_coord)

		while not self.finished:

			self.clock.tick(60)

			self.screen.fill((0, 0, 0))
			self.draw_snake()
			self.draw_food()

			self.snake.did_snake_ate([self.food.y_coord, self.food.x_coord])
			self.snake.is_snake_dead()

			if self.snake.snake_ate == 1:
				self.game_speed -= 0.001
				self.food.generate_new_food()

			snake_movement(pygame.event.get())

			pygame.display.update()

			sleep(self.game_speed)

	def draw_snake(self):
		for snake_body_part in self.snake.snake_body:
			y_coord = snake_body_part[0]
			x_coord = snake_body_part[1]

			pygame.draw.rect(self.screen, self.snake.snake_color, pygame.Rect(x_coord, y_coord, 10, 10))

	def draw_food(self):
			pygame.draw.rect(self.screen, self.food.food_color, pygame.Rect(self.food.x_coord, self.food.y_coord, 10, 10))
