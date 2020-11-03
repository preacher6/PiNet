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

class ScrollMatrix(pygame.sprite.Sprite):
	""" Clase para dibujar scrolling en matrix"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.lista_barra_mat = self.__init_barra()

	def __init_barra(self): 
		"""Inicializar propiedades para scroll matrices incidencia"""
		lista_barra = list()
		down = pygame.image.load(os.path.join('Pictures', 'down.png')) # elemento 0 de la lista
		down_rect = down.get_rect()  # elemento 5 de la lista
		down_rect.center = (727.5, 538.5)
		up = pygame.image.load(os.path.join('Pictures', 'up.png')) # elemento 1 de la lista
		up_rect = up.get_rect()  # elemento 6 de la lista
		up_rect.center = (727.5, 148.5)
		left = pygame.image.load(os.path.join('Pictures', 'left.png')) # elemento 2 de la lista
		left_rect = left.get_rect()  # elemento 7 de la lista
		left_rect.center = (313.5, 562.5)
		right = pygame.image.load(os.path.join('Pictures', 'right.png')) # elemento 3 de la lista
		right_rect = right.get_rect()  # elemento 8 de la lista
		right_rect.center = (702.5, 562.5)
		plus = pygame.image.load(os.path.join('Pictures', 'plus.png')) # elemento 4 de la lista
		plus_rect = plus.get_rect()  # elemento 9 de la lista
		plus_rect.center = (705, 617.5)
		lista_barra.append(down); lista_barra.append(up); lista_barra.append(left);lista_barra.append(right)		
		lista_barra.append(plus)
		lista_barra.append(down_rect); lista_barra.append(up_rect); lista_barra.append(left_rect);lista_barra.append(right_rect)		
		lista_barra.append(plus_rect)

		barra_v = barra_v_1 = pygame.Surface((17, 364))  # elemento 10 y 11 de la lista
		barra_v_rect = barra_v.get_rect() # elemento 12 de la lista
		barra_v_rect.center = (727.5, 327.5)
		barra_v.fill((0, 0, 0))
		fondo_barra_v = pygame.Surface((25, 364))
		fondo_barra_v.fill((118, 118, 118))
		lista_barra.append(barra_v); lista_barra.append(barra_v_1); lista_barra.append(barra_v_rect)		

		barra_h = barra_h_1 = pygame.Surface((364, 17)) # elemento 13 y 14 de la lista
		barra_h_rect = barra_h.get_rect() # elemento 15 de la lista
		barra_h_rect.center = (414, 562.5)
		barra_h.fill((0, 0, 0))
		fondo_barra_h = pygame.Surface((364, 25))
		fondo_barra_h.fill((118, 118, 118))
		lista_barra.append(barra_h); lista_barra.append(barra_h_1); lista_barra.append(barra_h_rect)
		lista_barra.append(fondo_barra_v); lista_barra.append(fondo_barra_h) # elemento 16 y 17	 de la lista

		return lista_barra

	def dibujar_barra(self, superficie, desp):
		#print(desp)
		#superficie.blit(self.fondo_dibujo, (-desp[0], -desp[1])) # Area de trabajo
		#superficie.blit(self.lista_barra[4], (675, 555))
		superficie.blit(self.lista_barra_mat[2], (111, 493)) # Izquierda
		superficie.blit(self.lista_barra_mat[3], (500, 493)) # Derecha
		superficie.blit(self.lista_barra_mat[1], (525, 79))  # Arriba
		superficie.blit(self.lista_barra_mat[0], (525, 468)) # Abajo
		superficie.blit(self.lista_barra_mat[16], (525, 104)) # Fondo barra V
		superficie.blit(self.lista_barra_mat[10], (529, 104+desp[1])) # Barra_V
		superficie.blit(self.lista_barra_mat[17], (136, 493)) # Fondo barra H
		superficie.blit(self.lista_barra_mat[13], (136+desp[0], 497)) # Barra_H

	def acciones_barra_mat(self, pos, desp, pasos, size_sheet, barra_actual, center_bar):
		barra_actual = [364, 364]
		if self.lista_barra_mat[7].collidepoint(pos): # Presiona boton izquierda
			print('left')
			if size_sheet[0] >= 1 and pasos[0] > 0:
				desp[0] -= 10
				pasos[0] -= 1
		if self.lista_barra_mat[8].collidepoint(pos): # Presiona boton derecha
			print('right')
			if size_sheet[0] >= 1 and pasos[0] < size_sheet[0]: # Condicion q evalua q el desplazamiento no supere el máximo de la hoja					
				desp[0] += 10
				pasos[0] += 1
		if self.lista_barra_mat[5].collidepoint(pos): # Presiona boton abajo
			print('down')
			if size_sheet[1] >= 1 and pasos[1] < size_sheet[1]:
				desp[1] += 10
				pasos[1] += 1
		if self.lista_barra_mat[6].collidepoint(pos): # Presiona boton arriba
			print('up')
			if size_sheet[1] >= 1 and pasos[1] > 0:
				desp[1] -= 10
				pasos[1] -= 1
				
		barra_actual[0] = 364 - 10 * size_sheet[0] 
		self.lista_barra_mat[13] = pygame.transform.scale(self.lista_barra_mat[13], (barra_actual[0], 17)) # Redimensionar barra Horizontal

		barra_actual[1] = 364 - 10 * size_sheet[1]
		self.lista_barra_mat[10] = pygame.transform.scale(self.lista_barra_mat[10], (17, barra_actual[1])) # Redimensionar barra Vertical

		return barra_actual, size_sheet, desp, pasos