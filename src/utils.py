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
    if self._listeners == None:
      self._listeners = {}
    if name in self._listeners:
      pass
    else:
      self._listeners[name] = []
    if listener in self._listeners[name]:
      pass
    else:
      self._listeners[name].append(listener)
  def on(self, name, listener):
    self.addEventListener(name, listener)
  def hasEventListener(self, name, listener):
    """
    判断侦听是否存在
    :param  name:  事件类型
    :param  listener: 事件函数
    """
    if self._listeners == None:
      return False
    return self._listeners[name] and listener in self._listeners[name]
  def has(self, name, listener):
    self.hasEventListener(name, listener)
  def removeEventListener(self, name, listener):
    """
    删除侦听
    :param  name:  事件类型
    :param  listener: 事件函数
    """
    if self._listeners == None:
      return
    if self._listeners[name]:
      self._listeners[name].remove(listener)
  def off(self, name, listener):
    self.removeEventListener(name, listener)
  def dispatchEvent(self, event):
    """
    触发事件
    :param  event: 事件
    """
    if self._listeners == None:
      return
    if self._listeners[event.name]:
      event.target = self
      for fun in self._listeners[event.name]:
        fun(event)
  def dispatch(self, event):
    self.dispatchEvent(event)
class DisplayBase(EventDispatcher):
  """
  显示基类
  """
  x = 0
  y = 0
  visible = True
  type = None
  name = ""
  def __init__(self):
    EventDispatcher.__init__(self)
class Layer(DisplayBase):
  """
  层
  """
  def __init__(self):
    EventDispatcher.__init__(self)
    self.type = "layer"
    self.children = []
  def add(self, *layers):
    for layer in layers:
      self.children.append(layer)
  def delelte(self, *layers):
    for layer in layers:
      self.children.remove(layer)

class Sprite(DisplayBase):
  """
  精灵最终元素，没有children
  """
  def __init__(self):
    self.type = "sprite"
    self.image = None

class Graphic(DisplayBase):
  """
  图画
  """
  def __init__(self):
    self.type = "graphic"
    self.shape = None

class Renderer:
  """
  渲染器
  """
  def __init__(self, screen):
    self._screen = screen
  def show(self, layer):
    self._screen.fill((255, 255, 255))
    self.render(layer)
  def render(self, layer, x = 0, y = 0):
    if layer and layer.visible:
      x += layer.x
      y += layer.y
      if layer.type == "sprite":
        self._screen.blit(layer.image, (x, y))
      if layer.type == "graphic":
        layer.draw(self._screen, x, y)
      elif layer.type == "layer":
        for child in layer.children:
          self.render(child, x, y)
