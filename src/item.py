import pygame
from utils import Layer, Sprite
from const import LAYOUT, IMAGE

class Hero(Layer):
  """
  英雄层
  """
  def __init__(self):
    Layer.__init__(self)
    s = Sprite()
    image = pygame.image.load(IMAGE.HERO).convert_alpha()
    rect = image.get_rect()
    s.image = image
    s.x = (LAYOUT.TILE_WIDTH - rect.width) / 2
    s.y = (LAYOUT.TILE_HEIGHT - rect.height) / 2
    self.add(s)
  def reset(self):
    self.x = LAYOUT.TERRAIN_X
    self.y = LAYOUT.TERRAIN_Y
  def left(self):
    self.x -= LAYOUT.TILE_WIDTH
  def right(self):
    self.x += LAYOUT.TILE_WIDTH
  def up(self):
    self.y -= LAYOUT.TILE_HEIGHT
  def down(self):
    self.y += LAYOUT.TILE_HEIGHT

class Mist(Sprite):
  """
  迷雾
  """
  name = ""
  def __init__(self):
    Sprite.__init__(self)
    self.image = pygame.image.load(IMAGE.MIST).convert_alpha()
class Mists(Layer):
  """
  迷雾层
  """
  _data = None
  def __init__(self, data):
    Layer.__init__(self)
    self._data = data
  def add(self, x, y):
    mist = Mist()
    mist.name = "mist_%s_%s" % (x, y)
    mist.x = x * LAYOUT.TILE_WIDTH
    mist.y = y * LAYOUT.TILE_HEIGHT
    super().add(mist)
  def scan(self, x, y):
    if self._data[y][x] == 1:
      self._data[y][x] = 0
      for index, child in enumerate(self.children):
        if child.name == "mist_%s_%s" % (x, y):
          self.children.pop(index)
