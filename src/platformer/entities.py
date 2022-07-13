import pygame as pg
import sys, json
from physics import *
from colors import *
from mutils import *

class Entity:
    def __init__(self, pos, dim, id, active = True, anchored = True, initFrame = 0):
        self.pos = pos
        self.dim = dim
        self.vel = pg.math.Vector2(0, 0)
        self.id = id
        self.active = active
        self.anchored = anchored
        self.frame = initFrame

class Player:
    class ControlPhysics:
        def __init__(self):
            self.acceleration = 0.3
            self.decelaration = 0.1
            self.maxSpeed = 1
            self.jumpPower = 2
            self.airControl = 0.02
            self.weight = 0.002
    def __init__(self, pos):
        self.pos = pos
        self.vel = pg.math.Vector2(0, 0)
        self.dim = pg.math.Vector2(40, 60)
        self.onGround = False
        self.id = 1
        self.controlPhysics = self.ControlPhysics()
    def calc_physics(self):
        self.vel.y += physics.gravity + self.controlPhysics.weight
    def do_collisions_ground_ceil(self, entities):
        def col():
            return physics.checkcol_square_square(self.pos, self.dim, entity.pos, entity.dim)
        self.onGround = False
        for entity in entities:
            if entity.id != 1:
                if col():
                    if self.vel.y > -0.2:
                        self.onGround = True
                        """if abs(self.vel.x) > self.controlPhysics.decelaration:
                            self.vel.x -= mutils.sign_of(self.vel.x) * (self.controlPhysics.decelaration + self.entityMap[entity.id]["friction"])
                        else:
                            self.vel.x = 0"""
                    while col():
                        self.pos.y -= mutils.sign_of(self.vel.y)
                    self.vel.y = 0
        print(self.onGround)
        """if abs(self.vel.x) > self.controlPhysics.decelaration:
            self.vel.x -= mutils.sign_of(self.vel.x) * (self.controlPhysics.decelaration + self.entityMap[entity.id]["friction"])
        else:
            self.vel.x = 0"""
    def do_collisions_walls(self, entities):
        def col():
            return physics.checkcol_square_square(self.pos, self.dim, entity.pos, entity.dim)
        for entity in entities:
            if entity.id != 1:
                if col():
                    while col():
                        self.pos.x -= mutils.sign_of(self.vel.x)
                    self.vel.x = 0
    def do_controls(self):
        pressedKeys = pg.key.get_pressed()
        if pressedKeys[pg.K_UP] | pressedKeys[pg.K_SPACE]:
            if self.onGround: self.vel.y = -self.controlPhysics.jumpPower
        if pressedKeys[pg.K_RIGHT] | pressedKeys[pg.K_d]:
            if self.onGround: self.vel.x += self.controlPhysics.acceleration
            else: self.vel.x += self.controlPhysics.airControl * self.controlPhysics.acceleration
            if self.vel.x > self.controlPhysics.maxSpeed: self.vel.x = self.controlPhysics.maxSpeed
        if pressedKeys[pg.K_LEFT] | pressedKeys[pg.K_a]:
            if self.onGround: self.vel.x -= self.controlPhysics.acceleration
            else: self.vel.x -= self.controlPhysics.airControl * self.controlPhysics.acceleration
            if self.vel.x < self.controlPhysics.maxSpeed: self.vel.x = -self.controlPhysics.maxSpeed
    def apply_physics(self, entities):
        self.do_controls()
        self.pos.y += self.vel.y
        self.do_collisions_ground_ceil(entities)
        self.pos.x += self.vel.x
        self.do_collisions_walls(entities)
    def render(self, display):
        pg.draw.rect(display, BLUE, (self.pos.x, self.pos.y, self.dim.x, self.dim.y))
    def update(self, display, allEntities):
        print()
        self.calc_physics()
        self.apply_physics(allEntities)
        self.render(display)

class Entities:
    def __init__(self):
        self.entities = [Player(pg.math.Vector2(500, 300)), Entity(pg.math.Vector2(0, 400), pg.math.Vector2(600, 100), 2), Entity(pg.math.Vector2(0, 50), pg.math.Vector2(600, 100), 2), Entity(pg.math.Vector2(600, 350), pg.math.Vector2(300, 150), 2)]
        if self.entities[0].id != 1:
            sys.exit("ERROR: Player is not first in entity list.\nExiting now...")
        self.entityMap = open("dat/ent/ent-map.json")
        self.entityMap = json.load(self.entityMap)
        self.entityMap = self.entityMap["entities"]
        sys.path.append("dat/ent/")
        self.entities[0].entityMap = self.entityMap
    def update(self, display, targets):
        for entity in targets:
            itemInMap = self.entityMap[entity.id]
            itemModule = __import__(itemInMap["moduleName"])
            if entity.id != 1: itemModule.update(entity, display)
            else: itemModule.update(entity, display, self.entities)

