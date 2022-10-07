import pygame as pg
from math import *
import sys

# All ren_<shape>_ac functions mean render_<shape>_accordingly, meaning they draw according to the position you provide

def ren_triangle_ac(surface, color, global_pos, p1, p2, p3):
	pg.draw.polygon(surface, color, [
		(p1[0] + global_pos[0], p1[1] + global_pos[1]),
		(p2[0] + global_pos[0], p2[1] + global_pos[1]),
		(p3[0] + global_pos[0], p3[1] + global_pos[1])
	])

def ren_circle_ac(surface, color, global_pos, p, r):
	pg.draw.circle(surface, color, (
		p[0] + global_pos[0],
		p[1] + global_pos[1]
	), r)

class Player:
	def __init__(self):
		self.pos = pg.Vector2(100, 200)

		# How far the player goes when bobbing up and down, multiplied by sin(the time)
		self.bobbing_length = 10

		# Variable that slows down bobbing, basically does (the time)/bobbing_slowness
		self.bobbing_slowness = 400

		# Travel speed
		self.movement_speed = 4

		# Colors
		self.cloak_color = "#ff0000" # Red
		self.neck_collar_color = "#ffffff" # White
		self.skin_color = "#cccccc" # White with a tint of grey
		self.star_color = self.cloak_color # Same as cloak color
		self.projectile_color = "#6A0DAD" # Purple

		# Shoot cooldown (in frames)
		self.shoot_interval = 0
		self.shoot_wait = 30

		self.projectiles = []
		self.projectile_speed = 10

	def get_hitbox(self):
		return pg.Rect(self.pos.x, self.pos.y, 30, 30)

	# Pew, pew!
	def shoot(self):
		self.shoot_interval = self.shoot_wait
		self.projectiles.append((self.pos.x, self.pos.y))

	# Update physics without drawing anything, also requests enemy (as function argument)
	def update(self, enemy):
		# Pressed keys
		p_keys = pg.key.get_pressed()

		self.shoot_interval -= 1
		if p_keys[pg.K_UP] and self.pos.y > 0:
			self.pos.y -= self.movement_speed
		if p_keys[pg.K_DOWN] and self.pos.y < 400:
			self.pos.y += self.movement_speed
		if p_keys[pg.K_RIGHT] and self.shoot_interval < 1:
			self.shoot()

		i = 0
		for projectile in self.projectiles:
			if projectile[0] - 20 > 800:
				self.projectiles.pop(i)
				i -= 1
			else:
				self.projectiles[i] = (projectile[0] + self.projectile_speed, projectile[1])
				if enemy.get_hitbox().colliderect(pg.Rect(
					projectile[0],
					projectile[1],
					20,
					20
				)):
					print("You win!")
					sys.exit()
			i += 1

	# Display player on specified surface
	def render(self, surface):
		global_pos = self.pos.x, self.pos.y + sin(pg.time.get_ticks() / self.bobbing_slowness) * self.bobbing_length
		# Most of the body
		ren_triangle_ac(surface, self.cloak_color, global_pos, (30, 30), (-30, 30), (0, -30))
		# Neck collar
		ren_triangle_ac(surface, self.neck_collar_color, global_pos, (-20, 0), (20, -14), (-12, -15))
		# Head
		ren_circle_ac(surface, self.skin_color, global_pos, (0, -30), 14)
		# Stars (on neck collar)
		# Yes, they are just circles
		ren_circle_ac(surface, self.star_color, global_pos, (-10, -9), 3)
		ren_circle_ac(surface, self.star_color, global_pos, (-3, -10), 2)

		for projectile in self.projectiles:
			pg.draw.circle(surface, self.projectile_color, projectile, 15 + sin(pg.time.get_ticks() / 100) * 5)
