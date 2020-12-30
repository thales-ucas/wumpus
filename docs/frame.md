# 游戏框架


pygame对于常规的游戏开发可能并不友好


## 渲染
对于canvas渲染机制，就是把矢量、图片、文字……在场景中画


比如显示一个“Hello World!”


```py
import pygame,sys
pygame.init() #初始化pygame模块
screen = pygame.display.set_mode((400,300)) #长400，宽300
font = pygame.font.Font('freesansbold.ttf', 32) # 设置文字，字体为freesansbold，字号为32
surface = font.render('Hello world!', True, (0, 255, 0), (0, 0, 255)) # 根据字体创建文字
rect = surface.get_rect() # 获得文字位置和宽高
  
while True: # 循环渲染
  screen.fill((0, 0, 0)) # 画黑色背景
  screen.blit(surface, rect) # 画文字
  for event in pygame.event.get(): # 退出处理
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    pygame.display.update() # 更新渲染
```


我们早早的定义了元素，设置了结构


```py
# 定义元素
font = pygame.font.Font('freesansbold.ttf', 32) # 设置文字，字体为freesansbold，字号为32
surface = font.render('Hello world!', True, (0, 255, 0), (0, 0, 255)) # 根据字体创建文字
rect = surface.get_rect() # 获得文字位置和宽高
```


我们必须在while的死循环中一直去渲染我们已经定义好的surface


```py
# 循环渲染
while True:
  ...
  screen.blit(surface, rect) 
  ...
```


尤其是我们要想做动画，那么也是必须最终在渲染处实现


```py
while True: # 循环渲染
  ...
  if rect.x > 400:
    rect.x = -rect.width # 飞出画面回到原点
  else:
    rect.x += 1 # 文字向右移动
  screen.blit(surface, rect) # 画文字
  ...
```


非常的不方便


# 层，精灵和渲染


纵观各类游戏语言和框架，都是拥有层和精灵的概念，比如actionscript、cocos2d、layabox……就算不说框架，我们用Photoshop之类的视觉软件也都是这样的结构


自习看完了整个的pygame文档，确实没有这个概念，里面的group和sprite并不是我们想要的“层”和“精灵”


那么我们自己来完成以下这些功能


# 精灵


我们设置一个精灵类


1. x 元素的x坐标
2. y 元素的y坐标
3. surface 元素内容，可以是图片或者文字


```py
class Sprite:
  x = 0
  y = 0
  def __init__(self):
    self.type = "sprite"
    self.surface = None
```


我们可以创造一个文字或者图片，设置在sprite里面就可以了


```py
image = Sprite()
image.surface = pygame.image.load("gold.png").convert_alpha() # 图片
image.x = 10
text = Sprite()
text.surface = pygame.font.Font('freesansbold.ttf', 32).render('gold', True, (255, 0, 0)) # 文字
text.y = 10
```


## 渲染


然后我们吧上面的图片和文字，放在一个数组里


```py
arr = []
arr.append(image)
arr.append(text)
```


在while里面写一个遍历来渲染


```py
screen = pygame.display.set_mode((400,300))
...
while True:
  ...
  if spirte and arr:
    screen.blit(spirte.surface, (spirte.x, spirte.y))
  ...
```


这样我们就可以随意设置各种sprite，不用多在意渲染部分了

# 层


一个载体，在别的语言里，有叫layer或者container，可以把各种sprite放在里面


这样做的好处是——比如我多个spite组成了元素，要改变位置，那么每个sprite都要设置一遍(x, y)


```py
image = Sprite()
image.surface = pygame.image.load("gold.png").convert_alpha() # 图片
image.x = 100
image.y = 100
text = Sprite()
text.surface = pygame.font.Font('freesansbold.ttf', 32).render('gold', True, (255, 0, 0)) # 文字
text.y = 100
text.y = 100
```


我们如果有一个“layer(层)”的概念，这些sprite放在这个layer里，我们只要每次改动layer的(x, y)就行了


```py
image = Sprite()
image.surface = pygame.image.load("gold.png").convert_alpha() # 图片
text = Sprite()
text.surface = pygame.font.Font('freesansbold.ttf', 32).render('gold', True, (255, 0, 0)) # 文字
gold = Layer() # 创建“黄金”层
gold.add(image, text)
gold.y = 100
gold.y = 100
```


所以我们的layer是包含一个children，可以放多个sprite，甚至可以layer里面继续放layer，无限递归


我们layer类里面的一个方法是add，可以添加一个或多个sprite或layer


```py
class Layer:
  x = 0
  y = 0
  def __init__(self):
    self.type = "layer"
    self.children = [] # 子元素
  def add(self, *layers):
    for layer in layers:
      self.children.append(layer)
```


## 渲染


那么我们的渲染就要改造一下了


我们专门写一个渲染函数，并且递归执行


并且，我们专门建立一个scene层，做为主layer，以后所有的东西都add到这里面，渲染时候只递归渲染这一个layer就可以了


```py
screen = pygame.display.set_mode((400,300))
...
gold
...
scene = Layer()
scene.add(gold)
...
def render(self, layer, x = 0, y = 0):
  x += layer.x
  y += layer.y
  if layer.type == "sprite":
    screen.blit(layer.surface, (x, y))
  elif layer.type == "layer":
    for child in layer.children:
      render(child, x, y) # 递归渲染
...
while True:
  ...
  render(scene) # 所有的显示，只要这一行
  ...
```


# 完善类


并且因为layer和sprite很多相似，我们创建一个“基类”，layer和sprite都以它做扩展


```py
class DisplayBase:
  x = 0
  y = 0
  type = None
  name = ""
  def __init__(self):
    pass
```


layer和sprite更简洁了，并且以后通用内容，我们都在基类增加，


精灵类


```py
class Sprite(DisplayBase):
  def __init__(self):
    DisplayBase.__init__(self)
    self.type = "sprite"
    self.surface = None
```


层类


```py
class Layer(DisplayBase):
  def __init__(self):
    DisplayBase.__init__(self)
    self.type = "layer"
    self.children = [] # 子元素
  def add(self, *layers):
    for layer in layers:
      self.children.append(layer)
  def delete(self, *layers):
    for layer in layers:
      self.children.remove(layer)
```


我们在sprite和layer中，增加一个visible属性，代表是否显示。这时候，就可以只改DisplayBase了


```py
class DisplayBase:
  x = 0
  y = 0
  visible = True # 新加的
  type = None
  name = ""
  def __init__(self):
    pass
```


我们把渲染也单独定义一个类，用screen初始化，就像sprite和layer一样


```py
class Renderer:
  def __init__(self, screen):
    self._screen = screen
  def show(self, layer):
    self._screen.fill((255, 255, 255))
    self.render(layer)
  def render(self, layer, x = 0, y = 0):
    if layer and layer.visible: # 刚增加的visible属性，决定是否渲染
      x += layer.x
      y += layer.y
      if layer.type == "sprite":
        self._screen.blit(layer.surface, (x, y))
      elif layer.type == "layer":
        for child in layer.children:
          self.render(child, x, y) # 递归渲染
```


使用的时候，更简洁


```py
renderer = Renderer(pygame.display.set_mode((400, 300))) # 构造渲染类
...
scene = Layer()
...
while True:
  ...
  renderer.show(scene) # 渲染场景
  ...
```


# 事件


为了让所有类解耦，事件分发机制是一个很好的办法


很多人喜欢回调(callback)，因为操作简洁


比如英雄(hero)移动了，让战争迷雾(mist)消散


- 我们可能会在hero类中去调用mist的scan函数


- 但是，这样除了逻辑比较乱之外，还有个问题是，一旦mist不存在了，hero就会出错，因为找不到mist了


使用事件(event)机制会更好


- 英雄(hero)移动(move)了，对外发送自己move的event，其他事情不归自己管了


- 主场景侦听hero的move


- 在侦听到hero的move的时候去调用mist的scan


- 这样逻辑非常清晰，最主要是，即使mist出错了，依然不会影响hero


在hero类中发送事件


```py
class Hero(Layer):
  m = 0 # 横坐标
  n = 0 # 纵坐标
  def __init__(self):
    Layer.__init__(self)
    ...
  def pos(self, m, n):
    self.m = m
    self.n = n
    self.x = self.n * LAYOUT.TILE_WIDTH
    self.y = self.m * LAYOUT.TILE_HEIGHT
    e = Event("heroWalk")
    e.m = m
    e.n = n
    self.dispatch(e)
```


在主场景中侦听事件


```py
mists = Mists() # 构造迷雾
hero = Hero() # 构造英雄
hero.on("heroWalk", onHeroWalk) # 侦听英雄行走
def onHeroWalk(e):
  mists.scan(e.m, e.n) # 迷雾消散
```


事件类和时间分发器


```py
class Event:
  """
  事件
  """
  def __init__(self, name):
    self.name = name
class EventDispatcher:
  """
  事件触发器
  """
  def __init__(self):
    self._listeners = None
  def addEventListener(self, name, listener):
    """
    添加侦听
    :param  name:  事件类型
    :param  listener: 事件函数
    """
    ...
  def on(self, name, listener):
    self.addEventListener(name, listener)
  def hasEventListener(self, name, listener):
    """
    判断侦听是否存在
    :param  name:  事件类型
    :param  listener: 事件函数
    """
    ...
  def has(self, name, listener):
    self.hasEventListener(name, listener)
  def removeEventListener(self, name, listener):
    """
    删除侦听
    :param  name:  事件类型
    :param  listener: 事件函数
    """
    ...
  def off(self, name, listener):
    self.removeEventListener(name, listener)
  def dispatchEvent(self, event):
    """
    触发事件
    :param  event: 事件
    """
    ...
  def dispatch(self, event):
    self.dispatchEvent(event)
```


并且把实践类继承在displayBase，所有的layer和sprite都获得事件分发的能力


```py
class DisplayBase(EventDispatcher):
  x = 0
  y = 0
  visible = True
  type = None
  name = ""
  def __init__(self):
    EventDispatcher.__init__(self)
```