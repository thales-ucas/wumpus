import pygame
import sys
import numpy as np
from utils import Layer, Sprite, Renderer, Event
from const import LAYOUT, EVENT, SCORE
from item import Hero, Terrain, Encounter, Mists, Scoreboard, Popup

class Game:
  """
  游戏
  """
  _renderer = None # 渲染器
  _running = False # 游戏运行状态
  __scene = None # 场景
  __terrain = None # 地形层
  __encounter = None # 遭遇层
  __hero = None # 英雄
  __mists = None # 战争迷雾
  __scoreboard = None # 记分牌
  # __popup = None # 弹窗
  def __init__(self):
    pygame.init()
    self.fpsClock = pygame.time.Clock()
    self._renderer = Renderer(pygame.display.set_mode((LAYOUT.SCREEN_WIDTH, LAYOUT.SCREEN_HEIGHT)))
    pygame.display.set_caption("wumpus world")
    self.ready()
  def ready(self):
    self. __scene = Layer() # 初始化场景
    game = Layer() # 初始化游戏层
    game.x = LAYOUT.TERRAIN_X
    game.y = LAYOUT.TERRAIN_Y
    self.__scoreboard = Scoreboard()
    self.__scoreboard.x = LAYOUT.SCOREBOARD_X
    self.__scoreboard.y = LAYOUT.SCOREBOARD_Y
    # self.__popup = Popup()
    # self.__popup.x = LAYOUT.POPUP_X
    # self.__popup.y = LAYOUT.POPUP_Y
    self.__scene.add(game, self.__scoreboard)
    self.__terrain = Terrain(np.ones((LAYOUT.SIZE, LAYOUT.SIZE))) # 按照尺寸构造地形
    self.__mists = Mists(np.ones((LAYOUT.SIZE, LAYOUT.SIZE))) # 按照尺寸构造战争迷雾
    self.__encounter = Encounter() # 构造遭遇层
    self.__encounter.on(EVENT.GAME_CLEAR, self.onGameClear) # 侦听游戏过关
    self.__encounter.on(EVENT.GAME_OVER, self.onGameOver) # 侦听游戏结束
    self.__hero = Hero() # 构造英雄
    self.__hero.on(EVENT.HERO_WALK, self.onHeroWalk) # 侦听英雄行走
    game.add(self.__terrain, self.__encounter, self.__hero, self.__mists) # 顺序不能错，地形在最下，战争迷雾在最上
    self.__mists.scan(0, 0)
    self._renderer.show(self.__scene)
  def onHeroWalk(self, e):
    """
    英雄行走
    """
    self.__scoreboard.change(SCORE.WALK)
    self.__mists.scan(e.m, e.n)
    self.__encounter.hit(e.m, e.n)
  def onGameClear(self, e):
    """
    过关,找到黄金
    """
    self.__scoreboard.change(SCORE.WIN)
    self.__scoreboard.win()
    self.stop()
  def onGameOver(self, e):
    """
    危险,遭遇怪物或者陷坑
    """
    print(e.code)
    self.__scoreboard.change(SCORE.LOSE)
    self.__scoreboard.lose()
    self.stop()
  def restart(self):
    """
    重玩
    """ 
    self.ready()
    self.start()
  def start(self):
    """
    开始游戏
    """
    self._running = True
    self.run()
  def stop(self):
    self._running = False
  def run(self):
    while True:
      pygame.display.flip()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self._running = False
          sys.exit()
        elif event.type == pygame.KEYDOWN:
          if self._running:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
              self.__hero.left()
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
              self.__hero.right()
            if event.key == pygame.K_UP or event.key == ord('w'):
              self.__hero.up()
            if event.key == pygame.K_DOWN or event.key == ord('s'):
              self.__hero.down()
          else:
            if event.key == pygame.K_SPACE:
              self.restart()
          self._renderer.show(self.__scene)
      pygame.display.update()
