class Layer:
  def __init__(self):
    self.type = "layer"
    self.children = []
    self.x = 0
    self.y = 0
  def add(self, layer):
    self.children.append(layer)

class Sprite:
  def __init__(self):
    self.type = "sprite"
    self.x = 0
    self.y = 0
    self.image = None