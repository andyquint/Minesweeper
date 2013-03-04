# Andrew Quintanilla
# CPSC254
import os, sys, pygame, math
from pygame.locals import *
from random import shuffle

white=(255,255,255)
black=(0,0,0)
grey=(169,169,169)
red=(255,0,0)
size = 20

class Tile(pygame.sprite.Sprite):
	def __init__(self,isBomb=False):
		pygame.sprite.Sprite.__init__(self)
		self.border = pygame.Surface((size,size))
		self.inside = pygame.Surface((size-2,size-2))
		self.image = pygame.Surface((size,size))
		
		self.border.fill(black)
		self.inside.fill(grey)
		self.image.blit(self.border,(0,0))
		self.image.blit(self.inside,(2,2))
		self.rect = self.image.get_rect()
		self.checked = False
		self.isBomb = isBomb
		
	def check(self):
		if (self.isBomb):
			self.inside.fill(red)
		else:
			self.inside.fill(white)
		self.image.blit(self.inside,(2,2))
		self.checked = True

class Grid(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		self.dimensions = (16,16)
		self.bombs = 40
		test = list(range(self.dimensions[0]*self.dimensions[1]))
		shuffle(test)
		for i in range(self.dimensions[0]):
			for j in range(self.dimensions[1]):
				temp = Tile()
				temp.rect.topleft = (i*size,j*size)
				if (test.pop() < self.bombs):
					temp.isBomb = True
				else:
					temp.isBomb = False
				self.add(temp)
		print(len(self.sprites()))
				
def main():
	pygame.init()
	grid = Grid()
	screen = pygame.display.set_mode((grid.dimensions[0]*size,grid.dimensions[1]*size))
	buttonpress = False
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(white)
	
	pygame.mouse.set_visible(True)
	
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == MOUSEBUTTONDOWN:
				if buttonpress == False:
					buttonpress = True
			elif event.type == MOUSEBUTTONUP:
				if buttonpress == True:
					buttonpress = False
					
					mousesprite = pygame.sprite.Sprite()
					mousesprite.rect = pygame.Rect(pygame.mouse.get_pos(), (1,1))
					intersect = pygame.sprite.spritecollide(mousesprite,grid,False)
					if intersect:
						for i in intersect:
							i.check()
							if i.isBomb:
								lose = True
		
		grid.draw(screen)
		pygame.display.flip()
	
if __name__ == '__main__':
	main()
				