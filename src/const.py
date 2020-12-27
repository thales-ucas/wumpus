class Const:
  """
  常量
  """
  class ConstError(TypeError):pass
  def __setattr__(self, name, value):
    if name in self.__dict__:
      raise self.ConstError("Can't rebind const (%s)" %name)
    self.__dict__[name]=value

LAYOUT = Const()
"""
布局
"""
LAYOUT.SCREEN_WIDTH = 500
LAYOUT.SCREEN_HEIGHT = 400
LAYOUT.SIZE = 4
LAYOUT.TERRAIN_X = 50
LAYOUT.TERRAIN_Y = 20
LAYOUT.TILE_WIDTH = 100
LAYOUT.TILE_HEIGHT = 90

IMAGE = Const()
"""
图片
"""
IMAGE.TILE = "assets/tile.png"# 地砖
IMAGE.MIST = "assets/mist.png"# 战争迷雾
IMAGE.HERO = "assets/hero.png" # 英雄
IMAGE.MONSTER = "assets/monster.png" # 怪物
IMAGE.PIT = "assets/pit.png" # 陷阱
IMAGE.GOLD = "assets/gold.png" # 黄金
