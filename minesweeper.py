# Andrew Quintanilla
# CPSC254
import os, sys, pygame, math
from pygame.locals import *
from random import shuffle

white=(255,255,255)
black=(0,0,0)
grey=(169,169,169)
red=(255,0,0)
orange=(255,165,0)
size = 20
pygame.init()
font = pygame.font.SysFont("calibri", 14)

class Tile(pygame.sprite.Sprite):
	def __init__(self):
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
		self.isBomb = False
		self.flagged = False
		self.num = 0
		
	def Check(self):
		if (self.isBomb):
			self.inside.fill(red)
		else:
			self.inside.fill(white)
			print(self.num)
			if (self.num != 0):
				numtext = font.render(str(self.num), True, black)
				self.inside.blit(numtext,(self.rect.width/4,numtext.get_height()/4))
				
		self.image.blit(self.inside,(2,2))
		self.checked = True
		
	def Flag(self):
		if self.flagged:
			self.inside.fill(grey)
			self.image.blit(self.inside,(2,2))
		else:
			flag = pygame.Surface((self.inside.get_width()-4,self.inside.get_height()-4))
			flag.fill(orange)
			self.inside.blit(flag,(2,2))
			self.image.blit(self.inside,(2,2))

class Grid(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		self.dimensions = (16,16)
		self.bombs = 60
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
		
		for t in self.sprites():
			if t.isBomb == False:
				temp = pygame.sprite.Sprite()
				temp.rect = t.rect.copy()
				temp.rect.inflate_ip(2,2)
				intersect = pygame.sprite.spritecollide(temp, self, False)
				for i in intersect:
					if i.isBomb:
						t.num = t.num+1
				
def main():
	grid = Grid()
	screen = pygame.display.set_mode((grid.dimensions[0]*size+2,grid.dimensions[1]*size+2))
	lbuttonpress = False
	rbuttonpress = False
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(white)
	
	pygame.mouse.set_visible(True)
	
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0] and not lbuttonpress:
					lbuttonpress = True
				if pygame.mouse.get_pressed()[2] and not rbuttonpress:
					rbuttonpress = True
			elif event.type == MOUSEBUTTONUP:
				if not pygame.mouse.get_pressed()[0] and lbuttonpress:
					print('lclick')
					lbuttonpress = False
					mousesprite = pygame.sprite.Sprite()
					mousesprite.rect = pygame.Rect(pygame.mouse.get_pos(), (1,1))
					intersect = pygame.sprite.spritecollide(mousesprite,grid,False)
					if intersect:
						for i in intersect:
							i.Check()
				if not pygame.mouse.get_pressed()[2] and rbuttonpress:
					print('rclick')
					rbuttonpress = False
					mousesprite = pygame.sprite.Sprite()
					mousesprite.rect = pygame.Rect(pygame.mouse.get_pos(), (1,1))
					intersect = pygame.sprite.spritecollide(mousesprite,grid,False)
					if intersect:
						for i in intersect:
							i.Flag()
		
		grid.draw(screen)
		pygame.display.flip()
	
if __name__ == '__main__':
	main()
				