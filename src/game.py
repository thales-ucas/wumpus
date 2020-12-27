import pygame
import sys
import numpy as np
from utils import Layer, Sprite
from const import LAYOUT
from item import Hero,Mists

class Game():
  """
  游戏
  """
  __scene = Layer() # 场景
  _data = None # 数据
  __terrain = None # 地形层
  __trip = None # 机关层
  __hero = None # 英雄层
  _heroPos = {"x": 0, "y": 0} # 英雄位置
  __mists = None # 战争迷雾
  def __init__(self):
    self.fpsClock = pygame.time.Clock()
    self.screen = pygame.display.set_mode((LAYOUT.SCREEN_WIDTH, LAYOUT.SCREEN_HEIGHT))
    self._data = self.getTerrain()
    self.terrainInit()
  def getTerrain(self):
    terrain = np.zeros(LAYOUT.SIZE * LAYOUT.SIZE - 5 - 3)
    terrain = np.append(terrain, [10, 21, 22, 22, 22])
    np.random.shuffle(terrain)
    terrain = np.insert(terrain, 0, 1)
    terrain = np.insert(terrain, 1, 0)
    terrain = np.insert(terrain, LAYOUT.SIZE, 0)
    terrain.resize((LAYOUT.SIZE, LAYOUT.SIZE))
    return terrain
  def terrainInit(self):
    self.__terrain = Layer()
    self.__terrain.x = LAYOUT.TERRAIN_X
    self.__terrain.y = LAYOUT.TERRAIN_Y
    self.__trip = Layer()
    self.__trip.x = LAYOUT.TERRAIN_X
    self.__trip.y = LAYOUT.TERRAIN_Y
    self.__hero = Hero()
    self.__hero.x = LAYOUT.TERRAIN_X
    self.__hero.y = LAYOUT.TERRAIN_Y
    self.__mists = Mists(np.ones((LAYOUT.SIZE, LAYOUT.SIZE)))
    self.__mists.x = LAYOUT.TERRAIN_X
    self.__mists.y = LAYOUT.TERRAIN_Y
    for m, row in enumerate(self._data):
      for n, col in enumerate(row):
        s = Sprite()
        s.image = pygame.image.load("assets/tile.png").convert_alpha()
        x = n * LAYOUT.TILE_WIDTH
        y = m * LAYOUT.TILE_HEIGHT
        s.x = x
        s.y = y
        self.__terrain.add(s) # 初始化地形
        self.__mists.add(m, n)
        trip = None
        if col == 10:
          trip = Sprite()
          image = pygame.image.load("assets/gold.png").convert_alpha()
          rect = image.get_rect()
          trip.image = image
          trip.x = x + (LAYOUT.TILE_WIDTH - rect.width) / 2
          trip.y = y + (LAYOUT.TILE_HEIGHT - rect.height) / 2
        elif col == 21:
          trip = Sprite()
          image = pygame.image.load("assets/monster.png").convert_alpha()
          rect = image.get_rect()
          trip.image = image
          trip.x = x + (LAYOUT.TILE_WIDTH - rect.width) / 2
          trip.y = y + (LAYOUT.TILE_HEIGHT - rect.height) / 2
        elif col == 22:
          trip = Sprite()
          image = pygame.image.load("assets/pit.png").convert_alpha()
          rect = image.get_rect()
          trip.image = image
          trip.x = x + (LAYOUT.TILE_WIDTH - rect.width) / 2
          trip.y = y + (LAYOUT.TILE_HEIGHT - rect.height) / 2
        if trip:
          self.__trip.add(trip)
    self.__scene.add(self.__terrain)
    self.__scene.add(self.__trip)
    self.__scene.add(self.__hero)
    self.__scene.add(self.__mists)
    self.__mists.scan(0, 0)
  def render(self, layer, x = 0, y = 0):
    if layer.type == "sprite":
      self.screen.blit(layer.image, (layer.x + x, layer.y + y))
    elif layer.type == "layer":
      for child in layer.children:
        self.render(child, layer.x, layer.y)
  def show(self):
    self.screen.fill((0,0,0))
  def run(self):
    running = True
    while running:
      self.render(self.__scene)
      pygame.display.flip()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
          sys.exit()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT or event.key == ord('a'):
            if self._heroPos["x"] > 0:
              self._heroPos["x"] -= 1
              self.__hero.left()
          if event.key == pygame.K_RIGHT or event.key == ord('d'):
            if self._heroPos["x"] < LAYOUT.SIZE - 1:
              self._heroPos["x"] += 1
              self.__hero.right()
          if event.key == pygame.K_UP or event.key == ord('w'):
            if self._heroPos["y"] > 0:
              self._heroPos["y"] -= 1
              self.__hero.up()
          if event.key == pygame.K_DOWN or event.key == ord('s'):
            if self._heroPos["y"] < LAYOUT.SIZE - 1:
              self._heroPos["y"] += 1
              self.__hero.down()
          self.__mists.scan(self._heroPos["x"], self._heroPos["y"])
