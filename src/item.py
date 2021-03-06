import pygame
import numpy as np
from utils import Layer, Sprite, Graphic, Event
from const import LAYOUT, IMAGE, EVENT, ENCOUNTER

class Hero(Layer):
  """
  英雄
  """
  m = 0 # 横坐标
  n = 0 # 纵坐标
  __tips = None # 射击提示
  _archery = 1 # 弓箭数量
  def __init__(self):
    Layer.__init__(self)
    s = Sprite()
    image = pygame.image.load(IMAGE.HERO).convert_alpha()
    rect = image.get_rect()
    s.surface = image
    s.x = (LAYOUT.TILE_WIDTH - rect.width) / 2
    s.y = (LAYOUT.TILE_HEIGHT - rect.height) / 2
    self.__tips = Sprite()
    myfont  = pygame.font.SysFont('SimHei',14)
    text = myfont.render("请选择方向", True, (0,0,0))
    textObj = text.get_rect()
    self.__tips.surface = text
    self.__tips.x = (LAYOUT.TILE_WIDTH - textObj.width) / 2
    self.__tips.y = (LAYOUT.TILE_HEIGHT - textObj.height) / 2
    self.add(s, self.__tips)
    self.__tips.visible = False
  def pos(self, m, n):
    """
    位置改变
    """
    if self.__tips.visible:
      e = Event(EVENT.HERO_ATTACK)
      self.__tips.visible = False
      self._archery -= 1
    else:
      self.m = m
      self.n = n
      self.x = self.n * LAYOUT.TILE_WIDTH
      self.y = self.m * LAYOUT.TILE_HEIGHT
      e = Event(EVENT.HERO_WALK)
    e.m = m
    e.n = n
    self.dispatch(e)
  def attack(self):
    if self._archery > 0:
      self.__tips.visible = not self.__tips.visible
  def reset(self):
    self.__tips.visible = False
    self.pos(0, 0)
  def up(self):
    if self.m > 0:
      self.pos(self.m - 1, self.n)
  def down(self):
    if self.m < LAYOUT.SIZE - 1:
      self.pos(self.m + 1, self.n)
  def left(self):
    if self.n > 0:
      self.pos(self.m, self.n - 1)
  def right(self):
    if self.n < LAYOUT.SIZE - 1:
      self.pos(self.m, self.n + 1)
class Tile(Sprite):
  """
  地板
  """
  def __init__(self):
    Sprite.__init__(self)
    self.surface = pygame.image.load(IMAGE.TILE).convert_alpha()
class Terrain(Layer):
  """
  地形层
  """
  _data = None
  def __init__(self, data):
    Layer.__init__(self)
    self._data = data
    for m, row in enumerate(self._data):
      for n, col in enumerate(row):
        if col == 1:
          tile = Tile()
          tile.x = n * LAYOUT.TILE_WIDTH
          tile.y = m * LAYOUT.TILE_HEIGHT
          self.add(tile) # 初始化地形
          # myfont  = pygame.font.SysFont('SimHei',14)
          # text = myfont.render("(%d,%d)" % (m, n), True, (0,0,0))
          # t = Sprite()
          # t.surface = text
          # t.x = n * LAYOUT.TILE_WIDTH + 2
          # t.y = m * LAYOUT.TILE_HEIGHT + 2
          # self.add(t)

class Mist(Sprite):
  """
  迷雾
  """
  name = ""
  def __init__(self):
    Sprite.__init__(self)
    self.surface = pygame.image.load(IMAGE.MIST).convert_alpha()
class Mists(Layer):
  """
  迷雾层
  """
  _data = None
  def __init__(self, data):
    Layer.__init__(self)
    self._data = data
    for m, row in enumerate(self._data):
      for n, col in enumerate(row):
        if col == 1:
          mist = Mist()
          mist.name = "mist_%s_%s" % (m, n)
          mist.x = n * LAYOUT.TILE_WIDTH
          mist.y = m * LAYOUT.TILE_HEIGHT
          self.add(mist)
  def scan(self, m, n):
    if self._data[m][n] == 1:
      self._data[m][n] = 0
      for child in self.children:
        if child.name == "mist_%s_%s" % (m, n):
          self.children.remove(child)
      self.dispatch({"name": "dissipate"})
class Encounter(Layer):
  """
  遭遇层
  """
  _data = None # 数据
  def __init__(self):
    Layer.__init__(self)
    data = np.zeros(LAYOUT.SIZE * LAYOUT.SIZE - 5 - 3)
    data = np.append(data, [ENCOUNTER.GOLD, ENCOUNTER.MONSTER, ENCOUNTER.PIT, ENCOUNTER.PIT, ENCOUNTER.PIT])
    np.random.shuffle(data)
    data = np.insert(data, 0, 0) # 最初位置和上下不能有怪
    data = np.insert(data, 1, 0)
    data = np.insert(data, LAYOUT.SIZE, 0)
    self._data = data.reshape((LAYOUT.SIZE, LAYOUT.SIZE))
    self.ready()
  def ready(self):
    for m, row in enumerate(self._data):
      for n, col in enumerate(row):
        x = n * LAYOUT.TILE_WIDTH
        y = m * LAYOUT.TILE_HEIGHT
        trip = None
        if col == ENCOUNTER.GOLD:
          trip = Sprite()
          image = pygame.image.load(IMAGE.GOLD).convert_alpha()
          rect = image.get_rect()
          trip.surface = image
          trip.x = x + (LAYOUT.TILE_WIDTH - rect.width) / 2
          trip.y = y + (LAYOUT.TILE_HEIGHT - rect.height) / 2
        elif col == ENCOUNTER.MONSTER:
          trip = Sprite()
          image = pygame.image.load(IMAGE.MONSTER).convert_alpha()
          rect = image.get_rect()
          trip.surface = image
          trip.name = "monster"
          trip.x = x + (LAYOUT.TILE_WIDTH - rect.width) / 2
          trip.y = y + (LAYOUT.TILE_HEIGHT - rect.height) / 2
        elif col == ENCOUNTER.PIT:
          trip = Sprite()
          image = pygame.image.load(IMAGE.PIT).convert_alpha()
          rect = image.get_rect()
          trip.surface = image
          trip.x = x + (LAYOUT.TILE_WIDTH - rect.width) / 2
          trip.y = y + (LAYOUT.TILE_HEIGHT - rect.height) / 2
        if trip:
          self.add(trip)
        # myfont  = pygame.font.SysFont('SimHei',14)
        # text = myfont.render("%d" % col, True, (0,0,0))
        # t = Sprite()
        # t.surface = text
        # t.x = x + 2
        # t.y = y + 2
        # self.add(t)
  def hit(self, m, n):
    code = self._data[m][n]
    if code == ENCOUNTER.GOLD: # 碰到黄金通关
      e = Event(EVENT.GAME_CLEAR)
      self.dispatch(e)
    elif code == ENCOUNTER.MONSTER or code == ENCOUNTER.PIT: # 碰到怪兽或者坑洞失败
      e = Event(EVENT.GAME_OVER)
      e.code = code
      self.dispatch(e)
  def shot(self, m, n):
    code = self._data[m][n]
    if code == ENCOUNTER.MONSTER:
      self._data[m][n] = 0 # 怪兽死亡要清空位置所在数据
      for child in self.children:
        if child.name == "monster":
          self.children.remove(child)
      e = Event(EVENT.MONSTER_DEAD)
      e.m = m
      e.n = n
      self.dispatch(e)
  def getData(self):
    return self._data

class Strench(Layer):
  """
  怪物附近的臭气
  """
  def __init__(self):
    Layer.__init__(self)
    for i in [-1, 0, 1]:
      s = Sprite()
      image = pygame.image.load(IMAGE.STRENCH).convert_alpha()
      s.surface = image
      imageRect = image.get_rect()
      s.x = LAYOUT.TILE_WIDTH / 2 + imageRect.width * i - imageRect.width / 2
      s.y = LAYOUT.TILE_HEIGHT - imageRect.height + (abs(i) - 1) * imageRect.height / 2
      self.add(s)
    t = Sprite()
    myfont = pygame.font.Font('freesansbold.ttf', 14)
    text = myfont.render('stench', True, (0,0,0))
    t.surface = text
    rect = text.get_rect()
    t.x = (LAYOUT.TILE_WIDTH - rect.width) / 2
    t.y = LAYOUT.TILE_HEIGHT - rect.height
    self.add(t)
class Breeze(Layer):
  """
  洞口在附近的微风
  """
  def __init__(self):
    Layer.__init__(self)
    s = Sprite()
    image = pygame.image.load(IMAGE.BREEZE).convert_alpha()
    s.surface = image
    imageRect = image.get_rect()
    s.x = (LAYOUT.TILE_WIDTH - imageRect.width) / 2
    s.y = 3
    t = Sprite()
    myfont = pygame.font.Font('freesansbold.ttf', 14)
    text = myfont.render('breeze', True, (0,0,0))
    t.surface = text
    textRect = text.get_rect()
    t.x = (LAYOUT.TILE_WIDTH - textRect.width) / 2
    t.y = 10
    self.add(s, t)

class Smell(Layer):
  """
  气息层
  """
  _origin = None # 遭遇原始数据
  _data = None # 气息数据
  def __init__(self):
    Layer.__init__(self)
    self._data = np.zeros((LAYOUT.SIZE, LAYOUT.SIZE))
  def show(self, data):
    self.children = []
    self._origin = data
    for m, row in enumerate(data):
      for n, col in enumerate(row):
        self.warn(col, m - 1, n)
        self.warn(col, m + 1, n)
        self.warn(col, m, n - 1)
        self.warn(col, m, n + 1)
  def warn(self, code, m, n):
    if code in [ENCOUNTER.MONSTER, ENCOUNTER.PIT] and m >= 0 and m < LAYOUT.SIZE and n >= 0 and n < LAYOUT.SIZE and self._origin[m][n] == 0:
      s = None
      if code == ENCOUNTER.MONSTER:
        s = Strench()
      elif code == ENCOUNTER.PIT:
        s = Breeze()
      if s:
        s.x = n * LAYOUT.TILE_WIDTH
        s.y = m * LAYOUT.TILE_HEIGHT
        self._data[m][n] = code
        self.add(s)

  
class Scoreboard(Layer):
  """
  记分牌
  """
  _score = 0 # 分数数据
  __score = None # 分数实体
  _font = None # 字体
  __win = None # 胜利画面
  __lose= None # 失败画面
  __restart = None # 重开画面
  def __init__(self):
    Layer.__init__(self)
    self._font = pygame.font.SysFont('SimHei',28)
    self.ready()
  def ready(self):
    title = Sprite()
    text = self._font.render('SCORE:',True, (0,0,0))
    title.surface = text
    rect = text.get_rect()
    self.__score = Sprite()
    self.__score.x = rect.width
    self.__score.surface = self._font.render('%s' % self._score, True, (255,0,0))
    self.__win = Sprite()
    self.__win.surface = self._font.render("You win!", True, (255,0,0))
    self.__win.y = rect.height
    self.__lose = Sprite()
    self.__lose.surface = self._font.render("You lose!", True, (255,0,0))
    self.__lose.y = rect.height
    self.__restart = Sprite()
    self.__restart.surface = self._font.render("请按空格重新游戏", True, (255,0,0))
    self.__restart.y = rect.height * 2
    tip = Sprite()
    tip.surface = self._font.render("使用方向键移动,空格射箭", True, (0,0,0))
    tip.y = rect.height * 3
    self.__win.visible = False
    self.__lose.visible = False
    self.__restart.visible = False
    self.add(title, self.__score, self.__win, self.__lose, self.__restart, tip)
  def change(self, num):
    self._score += num
    self.__score.surface = self._font.render('%s' % self._score, True, (255,0,0))
    return self._score
  def win(self):
    self.__lose.visible = False
    self.__win.visible = True
    self.__restart.visible = True
  def lose(self):
    self.__lose.visible = True
    self.__win.visible = False
    self.__restart.visible = True
class Popup(Layer):
  """
  弹窗
  """
  __win = None # 胜利画面
  __lose= None # 失败画面
  _font = None # 字体
  def __init__(self):
    Layer.__init__(self)
    bg = Graphic()
    bg.draw = lambda screen, x, y: pygame.draw.rect(screen, (235, 235, 235, 10), (x, y, LAYOUT.POPUP_WIDTH, LAYOUT.POPUP_HEIGHT))
    self._font = pygame.font.Font('freesansbold.ttf', 28)
    self.__win = Sprite()
    self.__win.surface = self._font.render("You win!", True, (255,0,0))
    self.__win.x = 80
    self.__win.y = 50
    self.__lose = Sprite()
    self.__lose.surface = self._font.render("You lose!", True, (255,0,0))
    self.__lose.x = 80
    self.__lose.y = 50
    self.add(bg, self.__win, self.__lose)
    self.hide()
  def win(self):
    self.__lose.visible = False
    self.__win.visible = True
    self.show()
  def lose(self):
    self.__lose.visible = True
    self.__win.visible = False
    self.show()
  def show(self):
    self.visible = True
  def hide(self):
    self.visible = False