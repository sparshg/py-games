import pygame as pg
import os, sys

import player, enemy

# Main class, starts the game and manages components
class Main:
	def __init__(self):
		pg.init()
		self.running = False

		# Initialize empty variable to be used as the window
		self.window = None

		# Now for the game components,
		self.player = player.Player()
		self.enemy = enemy.Enemy()

		# Make the screen get erased with black
		self.window_clear_color = "#000000"

		# FPS regulator
		self.fps = 60
		self.clock = pg.time.Clock()

	# Initialize, seperated for __init__() so the game can be started when desired, rather than on instance creation
	def initialize(self):
		self.window = pg.display.set_mode((800, 400))

	# Check for window events (such as input device interaction/close button press)
	def check_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.running = False

	# Update graphics on the screen, doesn't get applied until pg.display.update() is called. Doesn't erase the screen
	def render(self, surface):
		self.player.render(surface)
		self.enemy.render(surface)

	# Main loop
	def loop(self):
		self.running = True
		while self.running:
			self.player.update(self.enemy)
			self.enemy.update(self.player)
			self.window.fill(self.window_clear_color)
			self.render(self.window)
			pg.display.update()
			self.check_events()
			self.clock.tick(self.fps)

	# Exit
	def finalize(self):
		pg.quit()
		sys.exit()


if __name__ == "__main__":
	main = Main()
	main.initialize()
	main.loop()
	main.finalize()
