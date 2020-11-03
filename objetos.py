import pygame
import numpy as np
import sys
import os
import math
from pygame.locals import *

#COLORES
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = ( 0, 255, 0)
estado = None
conector = None
modo = [1, 0] #0 Manual, 1. Automatico
vel = 20

class Estados(pygame.sprite.Sprite):
	"Clase Estados"	
	def __init__(self, pos, tag, desp, ficticia = 0):
		self.font = pygame.font.SysFont('Arial', 15)
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('Pictures', 'estado.png'))
		self.imagen_estado = pygame.image.load(os.path.join('Pictures', 'estado.png'))
		self.rect = self.imagen_estado.get_rect()	
		self.rect.center = (pos[0] -180 + desp[0], pos[1] - 50 +  desp[1])
		self.token = 0 # Peso del estado
		self.seleccionado = False # Indica si está seleccionado el elemento para conexión
		self.conexiones = list() # Conexiones pertenecientes al estado
		self.tag = tag # Etiqueta de cada estado
		self.indices_conexion = 0
		self.time = 0
		self.limite = 100
		self.push = False
		self.ficticia = ficticia
		self.oct = False #Auxiliar

	def dibujar_estado(self, superficie, imagen_estado):		
		"Dibuja el objeto estado dentro del area de trabajo"
		if self.ficticia == 0:
			superficie.blit(imagen_estado, self.rect)

	def recta(self):
		"Devuelve recta del elemento actual"
		recta = self.rect
		return recta

	def add_token(self):
		"Agrega token al estado"
		if self.token <= self.limite:
			self.token += 1
		else:
			print('Superó la capacidad de tokens')

	def quitar_token(self):
		"Elimina token al estado"
		if self.token > 0:
			self.token -= 1

	"""def tooltip(self, pos, superficie, pos_dibujo):
		tag = 'Estado '+str(self.tag)
		print(tag)
		x, y = pos
		print(x, y)
		if self.rect.collidepoint(pos_dibujo):
			print('in')
			print(superficie)
			print(self.font)
			superficie.blit(self.font.render(tag, True, (255, 0, 0)), (x+10, y+10))"""

class Transiciones(pygame.sprite.Sprite):
	"Clase Transiciones"
	def __init__(self, pos, tag, desp, ficticia = 0, horizon = True):
		self.font = pygame.font.SysFont('Arial', 15)
		pygame.sprite.Sprite.__init__(self)
		if horizon == True:
			self.image = pygame.image.load(os.path.join('Pictures', 'trans.png'))
			self.rect = self.image.get_rect()	
			self.rect.center = (pos[0] -180 + desp[0], pos[1] - 50 +  desp[1])
		elif horizon == False:
			self.image = pygame.image.load(os.path.join('Pictures', 'transv.png'))
			self.rect = self.image.get_rect()	
			self.rect.center = (pos[0] -180 + desp[0], pos[1] - 50 +  desp[1])

		"""self.imagen_trans = pygame.image.load('Pictures/trans.png')
		self.imagen_transv = pygame.image.load('Pictures/transv.png')
		self.rect = self.imagen_trans.get_rect()	
		self.rect.center = pos
		self.rectv = self.imagen_transv.get_rect()	
		self.rectv.center = pos"""
		self.seleccionado = False # Indica si está seleccionado el elemento para conexión
		self.conexiones = list() # Conexiones pertenecientes a la transición
		self.tag = tag # Etiqueta de cada transición
		self.active = False
		self.active_pro = False
		self.time = 0
		self.num_conec_u = 0
		self.num_conec_d = 0
		self.push = False
		self.ficticia = ficticia
		self.horizon = horizon
		self.oct = False #Auxiliar
		#self.fict()

	def dibujar_trans(self, superficie, imagen):		
		"Dibuja el objeto estado dentro del area de trabajo"
		if self.ficticia == 0:
			if self.horizon:
				superficie.blit(imagen, self.rect)
			else:
				superficie.blit(imagen, self.rectv)

	def recta(self):
		"Devuelve recta del elemento actual"
		if self.horizon:
			recta = self.rect
		else:
			recta = self.rect
		return recta

	def tooltip(self, pos, superficie, pos_dibujo):
		tag = 'Transicion '+str(self.tag)
		print(tag)
		x, y = pos
		print(x, y)
		if self.rect.collidepoint(pos_dibujo):
			print('in')
			superficie.blit(self.font.render(tag, True, (255,0,0)), (x+10,y+10))

	def fict(self):
		if  not self.horizon:
			self.rect = self.rectv

class Conectar(pygame.sprite.Sprite):	
	arrow = pygame.Surface((20, 20))
	def __init__(self, pos_ini, pos_fini, punto_inicial, ele_1, ele_2, angle, desp, ficticia=0, horizon=True):
		self.font = pygame.font.SysFont('Arial', 15)
		pygame.sprite.Sprite.__init__(self)
		self.flecha = pygame.image.load(os.path.join('Pictures', 'flecha.png')) # Carga imagen de flecha
		nar = pygame.transform.rotate(self.flecha, angle)
		nrect = nar.get_rect(center=((pos_fini[0]-180+desp[0], pos_fini[1]-50+desp[1])))		
		self.image = nar
		self.rect = nrect
		#self.rect = self.image.get_rect()
		#self.rect.center = (pos_fini[0]-180+desp[0], pos_fini[1]-50+desp[1])
		#self.flecha = pygame.image.load('Pictures/flecha.png') # Carga imagen de flecha
		#self.rect = self.flecha.get_rect()
		self.ini = (round(pos_ini[0])-180+desp[0], round(pos_ini[1])-50+desp[1])
		self.fin = (round(pos_fini[0])-180+desp[0], round(pos_fini[1])-50+desp[1])
		self.punto_inicial = punto_inicial
		self.inicial = pos_ini
		self.final = pos_fini
		self.token = 1
		self.horizon = horizon
		self.angle = angle
		self.push = False
		self.desvio = 0
		self.repeat_d = 0
		self.repeat_u = 0		
		self.rectax = []
		self.ficticia = ficticia
		self.interconectados = [ele_1, ele_2]
		self.col = self.interconectados
		#self.calcular_angulo()		
		self.repetido = 0
		self.bloqueo = 0 # Variable que deniega la actividad de la conexion

	def calcular_angulo(self):
		if self.ficticia == 0:
			self.col = self.interconectados
			nar = pygame.transform.rotate(self.flecha, self.angle)
			#print(pos_fini)
			nrect = nar.get_rect(center=(self.final))
			self.rect = nrect
			self.rectax = nrect

	def fini(self):
		self.bloqueo = 1
	def repe(self):
		self.repetido = 1

	"""def desviox(self):
		self.inicial = tuple(np.add(self.inicial, (11.6, 0)))"""

	def dibujar_conexion(self, superficie):
		"Dibuja un poligono con forma de flecha"
		if self.repetido == 0:
			#nar = pygame.transform.rotate(self.flecha, self.angle)
			#nrect = nar.get_rect(center = (self.final))
			#self.rect = nrect
			#self.rectax = nrect
			superficie.blit(self.image, self.rect)
			#pygame.draw.aaline(superficie, NEGRO, self.inicial, self.final, 1)

	def recta(self):
		"Devuelve recta del elemento actual"
		recta = self.rect
		return recta

	def tooltip(self, pos, superficie, pos_dibujo):
		tag = 'Peso del arco: '+ str(self.token)
		x, y = pos
		if self.rect.collidepoint(pos_dibujo) and self.bloqueo == 0:
			superficie.blit(self.font.render(tag, True, (255, 0, 0)), (x+10, y+10))

	def add_token(self):
		if self.token < 100:
			self.token += 1

	def quitar_token(self):
		"Elimina token al estado"
		if self.token > 1:
			self.token -= 1
