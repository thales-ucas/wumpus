# Q&A 问题和解答


# pygame的官网


https://www.pygame.org


# pygame显示中文


```python
import pygame
pygame.init()
myfont = pygame.font.Font('freesansbold.ttf', 32)
# text = myfont.render("你好！", True, (255, 0, 0))
text = myfont.render("Hello world!", True, (255, 0, 0))
screen = pygame.display.set_mode((400, 300))
screen.blit(text, (0, 0))
pygame.display.update()
```


如果文字不是英文而是中文


```python
text = myfont.render("你好！", True, (255, 0, 0))
# text = myfont.render("Hello world!", True, (255, 0, 0))
```

这样就会出现乱码


要解决中文的显示问题，我们有两种方法。


第一种方法：外带字体


在网上下载一个中文字体文件，将这个文件与我们的程序放在同一个文件夹，如果是中文的文件名，将它改成英文文件名。例如，下载了迷你简毡笔黑.TTF，将文件名改成了mnjzbh.ttf：


```python
myfont = pygame.font.Font('mnjzbh.ttf', 32)
```


这样，中文就能正确显示了。不过，有些下载的字体文件无法正常显示，可以多下载几个试试。


第二种方法：使用系统字体


将程序的第一句更改成：


```python
myfont = pygame.font.SysFont('SimHei',32)
```


也就是用SysFont代替Font，并且使用系统自带字体，也可以正常显示中文。


不过，系统自带有很多字体，要选择其中的中文字体。如何查看系统带了哪些字体呢？


可以使用：

```python
ZiTi = pygame.font.get_font()
for i in ZiTi:
  print(i)
```


来查看所有系统字体。


# 导出exe


需要安装pyinstall


```bash
pyinstaller -F -w main.py -p const.py -p utils.py -p game.py -p item.py
```