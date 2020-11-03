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
modo_temp = [1, 0, 0] #0 No temp, 1 T-Temp, 2 P-Temp 
KEY_REPEAT_SETTING = (200,70)

class Propiedades(pygame.sprite.Sprite):
	""" La idea de esta clase es que recopile todo lo 
	relacionado a las propiedades del software"""
	def __init__(self, superficie):
		pygame.sprite.Sprite.__init__(self)		
		#self.s_t = superficie_total # Define la superficie total de la interfaz
		self.rectangulo_trabajo = pygame.Rect(203, 76, 655, 530) # Rectangulo de trabajo
		self.area_trabajo = pygame.Surface((700, 580)); self.area_trabajo.fill(VERDE) # Superficie que contendra el area de trabajo
		self.fondo_dibujo = pygame.Surface((1250, 1110)); self.fondo_dibujo.fill(BLANCO)
		self.logo = pygame.image.load(os.path.join('Pictures', 'logo_u.png')) # Carga logo utp
		self.lista_barra = self.init_barra()

	def init_barra(self): 
		"""Inicializar propiedades para scroll pantalla principal"""
		lista_barra = list()
		down = pygame.image.load(os.path.join('Pictures', 'down.png')) # elemento 0 de la lista
		down_rect = down.get_rect()  # elemento 5 de la lista
		down_rect.center = (867.5, 592.5)
		up = pygame.image.load(os.path.join('Pictures', 'up.png')) # elemento 1 de la lista
		up_rect = up.get_rect()  # elemento 6 de la lista
		up_rect.center = (867.5, 62.5)
		left = pygame.image.load(os.path.join('Pictures', 'left.png')) # elemento 2 de la lista
		left_rect = left.get_rect()  # elemento 7 de la lista
		left_rect.center = (192.5, 617.5)
		right = pygame.image.load(os.path.join('Pictures', 'right.png')) # elemento 3 de la lista
		right_rect = right.get_rect()  # elemento 8 de la lista
		right_rect.center = (842.5, 617.5)
		plus = pygame.image.load(os.path.join('Pictures', 'plus.png')) # elemento 4 de la lista
		plus_rect = plus.get_rect()  # elemento 9 de la lista
		plus_rect.center = (867.5, 617.5)
		lista_barra.append(down); lista_barra.append(up); lista_barra.append(left);lista_barra.append(right)		
		lista_barra.append(plus)
		lista_barra.append(down_rect); lista_barra.append(up_rect); lista_barra.append(left_rect);lista_barra.append(right_rect)		
		lista_barra.append(plus_rect)

		barra_v = barra_v_1 = pygame.Surface((17, 505))  # elemento 10 y 11 de la lista
		barra_v_rect = barra_v.get_rect() # elemento 12 de la lista
		barra_v_rect.center = (867.5, 327.5)
		barra_v.fill((0, 0, 0))
		fondo_barra_v = pygame.Surface((25, 505))
		fondo_barra_v.fill((118, 118, 118))
		lista_barra.append(barra_v); lista_barra.append(barra_v_1); lista_barra.append(barra_v_rect)		

		barra_h = barra_h_1 = pygame.Surface((625, 17)) # elemento 13 y 14 de la lista
		barra_h_rect = barra_h.get_rect() # elemento 15 de la lista
		barra_h_rect.center = (517.5, 617.5)
		barra_h.fill((0, 0, 0))
		fondo_barra_h = pygame.Surface((625, 25))
		fondo_barra_h.fill((118, 118, 118))
		lista_barra.append(barra_h); lista_barra.append(barra_h_1); lista_barra.append(barra_h_rect)
		lista_barra.append(fondo_barra_v); lista_barra.append(fondo_barra_h) # elemento 16 y 17	 de la lista

		return lista_barra

	def dibujar_supercicies(self, superficie):
		font = pygame.font.SysFont('Arial', 15)	
		font_2 = pygame.font.SysFont('Arial', 26)
		superficie.blit(self.logo, (30, 10))
		self.area_trabajo.blit(self.fondo_dibujo, (0, 0))
		superficie.blit(self.area_trabajo, (180, 50))
		rectangulo_usuario = pygame.Rect(20, 120, 140, 370) # Rectangulo de panel
		pygame.draw.rect(superficie, NEGRO, rectangulo_usuario, 3)
		rectangulo_acciones = pygame.Rect(20, 510, 140, 120) # Rectangulo de acciones
		pygame.draw.rect(superficie, NEGRO, rectangulo_acciones, 3)
		#Añadir etiqueas de elementos
		superficie.blit(font.render('Lugar', True, (0, 0, 0)), (75, 130))
		superficie.blit(font.render('Transición', True, (0, 0, 0)), (62, 230))
		superficie.blit(font.render('Arco', True, (0, 0, 0)), (78, 310))
		superficie.blit(font.render('Marca', True, (0, 0, 0)), (75, 415))
		superficie.blit(font_2.render('PiNet', True, (0, 0, 0)), (510, 16))

	def dibujar_barra(self, superficie, desp):
		self.area_trabajo.blit(self.fondo_dibujo, (-desp[0], -desp[1])) # Area de trabajo
		self.area_trabajo.blit(self.lista_barra[4], (675, 555))
		self.area_trabajo.blit(self.lista_barra[2], (0, 555))
		self.area_trabajo.blit(self.lista_barra[3], (650, 555))
		self.area_trabajo.blit(self.lista_barra[1], (675, 0))
		self.area_trabajo.blit(self.lista_barra[0], (675, 530))
		self.area_trabajo.blit(self.lista_barra[16], (675, 25))
		self.area_trabajo.blit(self.lista_barra[10], (679, 25+desp[1]))
		self.area_trabajo.blit(self.lista_barra[17], (25, 555))
		self.area_trabajo.blit(self.lista_barra[13], (25+desp[0], 559))
		superficie.blit(self.area_trabajo, (180, 50))
		pygame.draw.rect(superficie, NEGRO, (180, 50, 700, 580), 3) # Rectangulo área de trabajo (fisico)

	def acciones_barra(self, pos, desp, pasos, size_sheet, barra_actual, center_bar):
		if self.lista_barra[7].collidepoint(pos): # Presiona boton izquierda
			print('left')
			if size_sheet >= 1 and pasos[0] > 0:
				desp[0] -= 30
				pasos[0] -= 1
		if self.lista_barra[8].collidepoint(pos): # Presiona boton derecha
			print('right')
			if size_sheet >= 1 and pasos[0] < size_sheet:						
				desp[0] += 30
				pasos[0] += 1
		if self.lista_barra[5].collidepoint(pos): # Presiona boton abajo
			print('down')
			if size_sheet >= 1 and pasos[1] < size_sheet:
				desp[1] += 24
				pasos[1] += 1
		if self.lista_barra[6].collidepoint(pos): # Presiona boton arriba
			print('up')
			if size_sheet >= 1 and pasos[1] > 0:
				desp[1] -= 24
				pasos[1] -= 1
		if self.lista_barra[9].collidepoint(pos):
			print('plus')
			if size_sheet < 10: # Seaumenta máximo 10, osea el doble del área original
				barra_actual[1] -= 24 # Aumento en vertical, se disminuye tamaño barra V
				barra_actual[0] -= 30 # Aumento en horizontal, se disminuye tamaño barra H
				size_sheet += 1 # Aumento de tamaño del área de trabajo
				center_bar[0] -= 5 
				center_bar[1] -= 5
			self.lista_barra[13] = pygame.transform.scale(self.lista_barra[14], (barra_actual[0], 17))
			#self.lista_barra[15] = self.lista_barra[13].get_rect()
			#self.lista_barra[15].center = (center_bar[0] , 385) # Barra H Rect

			self.lista_barra[10] = pygame.transform.scale(self.lista_barra[11], (17, barra_actual[1]))
			#self.lista_barra[12] = self.lista_barra[10].get_rect()
			#self.lista_barra[12].center = (385, center_bar[1]) # Barra V Rect

		return barra_actual, size_sheet, desp, pasos

	def cargar_play(self, pantalla):   # Carga propiedades de la opcion play
		play_e = pygame.image.load(os.path.join('Pictures', 'play_empty.png'))
		play_f = pygame.image.load(os.path.join('Pictures', 'play_filled.png'))
		pause_e = pygame.image.load(os.path.join('Pictures', 'pause_empty.png'))
		pause_f = pygame.image.load(os.path.join('Pictures', 'pause_filled.png'))
		play_rect = play_e.get_rect(center = (50, 545))
		play_pos = pantalla.blit(play_e, play_rect)
		return play_e, play_f, pause_e, pause_f, play_pos

	def cargar_erase(self, pantalla):   # Carga propiedades de la opcion erase
		erase_e = pygame.image.load(os.path.join('Pictures', 'erase_empty.png'))
		erase_f = pygame.image.load(os.path.join('Pictures', 'erase_filled.png'))
		erase_rect = erase_e.get_rect(center = (115, 545))
		erase_pos = pantalla.blit(erase_e, erase_rect)
		return erase_e, erase_f, erase_pos

	def cargar_set(self, pantalla):  # Carga propiedades de la opcion set
		set_e = pygame.image.load(os.path.join('Pictures', 'set_empty.png'))
		set_f = pygame.image.load(os.path.join('Pictures', 'set_filled.png'))
		set_rect = set_e.get_rect(center = (50, 600))
		set_pos = pantalla.blit(set_e, set_rect)
		return set_e, set_f, set_pos

	def cargar_help(self, pantalla): # Carga propiedades de la opcion help
		help_e = pygame.image.load(os.path.join('Pictures', 'help_empty.png'))
		help_f = pygame.image.load(os.path.join('Pictures', 'help_filled.png'))
		help_rect = help_e.get_rect(center = (115, 600))
		help_pos = pantalla.blit(help_e, help_rect)
		return help_e, help_f, help_pos

	def propiedad_estado(self, pantalla, font, estado, modo_temp):	# Sub ventana para las propiedades de los estados
		close = pygame.image.load(os.path.join('Pictures', 'close.png'))
		if modo_temp == [0, 0, 1]:
			panel = pygame.Surface((220, 200))
			panel_personal = pygame.image.load(os.path.join('Pictures', 'panel_config.png'))
			#panel.blit(font.render('Tiempo: '+str(estado.time) + 'ms', True, (0, 0 , 0)), (20, 55))	
		else:
			panel = pygame.Surface((220, 130))
			panel_personal = pygame.image.load(os.path.join('Pictures', 'panel_config2.png'))
		panel.fill(BLANCO)
		panel.blit(panel_personal, (0, 0))
		if estado.limite >= 100:
			limite = 'infinito'
		else:
			limite = estado.limite
		panel.blit(font.render('Propiedades Lugar '+str(estado.tag), True, (255, 0 , 0)), (15, 10))
		panel.blit(font.render('Limite de Tokens: '+str(limite), True, (0, 0 , 0)), (20, 35))
		panel.blit(font.render('Tiempo: '+str(estado.time) + 'ms', True, (0, 0 , 0)), (20, 55))	
		panel.blit(font.render('Limite:', True, (0, 0 , 0)), (55, 100))
		if modo_temp == [0, 0, 1]:
			panel.blit(font.render('Tiempo:', True, (0, 0 , 0)), (47, 140))
		panel.blit(close, (180, 5))
		pantalla.blit(panel, (375, 190))

	def propiedad_trans(self, pantalla, font, trans):  # Sub ventana para las propiedades de las transiciones
		#close = pygame.image.load(os.path.join('Pictures', 'close.png'))
		panel = pygame.Surface((300, 200))
		panel_personal = pygame.image.load(os.path.join('Pictures', 'panel_config2.png'))
		panel.fill(BLANCO)
		panel.blit(panel_personal, (0, 0))
		panel.blit(font.render('Propiedades Transición '+ str(trans.tag), True, (255, 0 , 0)), (15, 10))
		panel.blit(font.render('Tiempo: '+str(trans.time) + "ms", True, (0, 0 , 0)), (20, 35))
		panel.blit(font.render('Tiempo:', True, (0, 0 , 0)), (45, 80))
		#panel.blit(close, (100, 10))
		pantalla.blit(panel, (375, 210))

	def propiedad_conexion(self, pantalla, font, conexion):  # Sub ventana para las propiedades de las conexiones
		#close = pygame.image.load(os.path.join('Pictures', 'os.path.join(close.png'))
		panel = pygame.Surface((220, 130))
		panel_personal = pygame.image.load(os.path.join('Pictures', 'panel_config2.png'))
		panel.fill(BLANCO)
		panel.blit(panel_personal, (0, 0))
		panel.blit(font.render('Propiedades Conexión entre lugar '+ str(conexion.interconectados[1]), True, (255, 0 , 0)), (6, 10))
		panel.blit(font.render('y transición '+ str(conexion.interconectados[0]), True, (255, 0 , 0)), (6, 28))
		panel.blit(font.render('Tokens actuales: '+str(conexion.token) , True, (0, 0 , 0)), (20, 45))
		panel.blit(font.render('Tokens:', True, (0, 0 , 0)), (45, 80))
		#panel.blit(close, (100, 10))
		pantalla.blit(panel, (375, 210))

	def configurar(self, pantalla, posi, modo, vel, delay_evo, modo_temp):  # Sub ventana para configurar propiedades del sistema
		#Crear ventana de configuración
		#global modo
		font = pygame.font.SysFont('Arial', 15)	
		config = pygame.Surface((300, 300))
		#close = pygame.image.load(os.path.join('Pictures', 'close.png'))
		config_panel = pygame.image.load(os.path.join('Pictures', 'panel_config_1.png'))
		config_check_off = pygame.image.load(os.path.join('Pictures', 'check_off.png'))
		config_check_on = pygame.image.load(os.path.join('Pictures', 'check_on.png'))
		rect_manual = config_check_off.get_rect()
		rect_manual.center = (505, 270) # Checkbox manual
		rect_auto = config_check_off.get_rect()
		rect_auto.center = (505, 240) # Check automatico
		rect_vel_1 = config_check_off.get_rect()
		rect_vel_1.center = (585, 300) # Check 200ms
		rect_vel_2 = config_check_off.get_rect()
		rect_vel_2.center = (585, 320) # Check 500ms
		rect_vel_3 = config_check_off.get_rect()
		rect_vel_3.center = (585, 340) # Check 1s
		rect_vel_4 = config_check_off.get_rect()
		rect_vel_4.center = (585, 360) # Check 2s
		rect_temp_no = config_check_off.get_rect()
		rect_temp_no.center = (480, 410) # No_temp
		rect_temp_t = config_check_off.get_rect()
		rect_temp_t.center = (480, 430) # P_temp
		rect_temp_p = config_check_off.get_rect()
		rect_temp_p.center = (480, 450) # T_temp
		config_auto = pygame.image.load(os.path.join('Pictures', 'check_off.png'))
		config.fill(BLANCO)
		config.blit(config_panel, (0, 0))
		config.blit(font.render('Configuración', True, (255, 0 , 0)), (15, 10))
		config.blit(font.render('Automático', True, (0, 0 , 0)), (40,40))
		config.blit(font.render('Manual', True, (0, 0, 0)), (40, 70))
		config.blit(font.render('200ms', True, (0, 0, 0)), (160, 100))
		config.blit(font.render('500ms', True, (0, 0, 0)), (160, 120))
		config.blit(font.render('1s', True, (0, 0, 0)), (160, 140))
		config.blit(font.render('2s', True, (0, 0, 0)), (160, 160))
		config.blit(font.render('No-Temp', True, (0, 0 , 0)), (40, 210))
		config.blit(font.render('T-Temp', True, (0, 0 , 0)), (46,230))
		config.blit(font.render('P-Temp', True, (0, 0, 0)), (47, 250))
		#config.blit(close, (260, 8))

		if rect_auto.collidepoint(posi) or modo == [1, 0]:  # Elegir modo automatico
			modo = [1, 0]		
			config.blit(config_check_on, (120, 40)) #Auto
			config.blit(config_check_off, (120, 70)) #Manual
			if rect_vel_1.collidepoint(posi) or vel == 1:
				config.blit(config_check_on, (200, 100)) #200ms
				config.blit(config_check_off, (200, 120)) #500ms
				config.blit(config_check_off, (200, 140)) #1s
				config.blit(config_check_off, (200, 160)) #2s
				vel = 1
				delay_evo = 200
			if rect_vel_2.collidepoint(posi) or vel == 2:
				config.blit(config_check_off, (200, 100)) #200ms
				config.blit(config_check_on, (200, 120)) #500ms
				config.blit(config_check_off, (200, 140)) #1s
				config.blit(config_check_off, (200, 160)) #2s
				vel = 2
				delay_evo = 500
			if rect_vel_3.collidepoint(posi) or vel == 3:
				config.blit(config_check_off, (200, 100)) #200ms
				config.blit(config_check_off, (200, 120)) #500ms
				config.blit(config_check_on, (200, 140)) #1s
				config.blit(config_check_off, (200, 160)) #2s
				vel = 3
				delay_evo = 1000
			if rect_vel_4.collidepoint(posi) or vel == 4:
				config.blit(config_check_off, (200, 100)) #200ms
				config.blit(config_check_off, (200, 120)) #500ms
				config.blit(config_check_off, (200, 140)) #1s
				config.blit(config_check_on, (200, 160)) #2s
				vel = 4
				delay_evo = 2000

			config.blit(font.render('Velocidad ejecución:', True, (0, 0, 0)), (40, 100))

			if rect_temp_no.collidepoint(posi)	or modo_temp == [1, 0, 0]:
				config.blit(config_check_on, (95, 210)) #Manual
				config.blit(config_check_off, (95, 230)) #Auto
				config.blit(config_check_off, (95, 250)) #200ms
				modo_temp = [1, 0, 0]
			if rect_temp_t.collidepoint(posi)	or modo_temp == [0, 1, 0]:
				config.blit(config_check_off, (95, 210)) #Manual
				config.blit(config_check_on, (95, 230)) #Auto
				config.blit(config_check_off, (95, 250)) #200ms
				modo_temp = [0, 1, 0]
			if rect_temp_p.collidepoint(posi)	or modo_temp == [0, 0, 1]:
				config.blit(config_check_off, (95, 210)) #Manual
				config.blit(config_check_off, (95, 230)) #Auto
				config.blit(config_check_on, (95, 250)) #200ms
				modo_temp = [0, 0, 1]

		if rect_manual.collidepoint(posi) or modo == [0, 1]:	# Elegir modo automatico
			modo = [0, 1]
			config.blit(config_check_on, (120, 70)) #Manual
			config.blit(config_check_off, (120, 40)) #Auto
			config.blit(config_check_off, (200, 100)) #200ms
			config.blit(config_check_off, (200, 120)) #500ms
			config.blit(config_check_off, (200, 140)) #1s
			config.blit(config_check_off, (200, 160)) #2s
			config.blit(config_check_off, (95, 210)) #Manual
			config.blit(config_check_off, (95, 230)) #Auto
			config.blit(config_check_off, (95, 250)) #200ms
			config.blit(font.render('Velocidad ejecución:', True, (128,128,128)), (40, 100))	

		pantalla.blit(config, (375, 190))
		return modo, vel, delay_evo, modo_temp

	def show_structure(self, pantalla):
		matrix_e = pygame.image.load(os.path.join('Pictures', 'matrix_empty.png'))
		matrix_f = pygame.image.load(os.path.join('Pictures', 'matrix_filled.png'))
		change_rect = matrix_e.get_rect(center = (530, 665))
		change_pos = pantalla.blit(matrix_e, change_rect)
		return matrix_e, matrix_f, change_pos

	def show_proper(self, pantalla):
		proper_e = pygame.image.load(os.path.join('Pictures', 'proper_empty.png'))
		proper_f = pygame.image.load(os.path.join('Pictures', 'proper_filled.png'))
		proper_rect = proper_e.get_rect(center = (460, 665))
		proper_pos = pantalla.blit(proper_e, proper_rect)
		return proper_e, proper_f, proper_pos

	def show_trans(self, pantalla):
		trans_e = pygame.image.load(os.path.join('Pictures', 'tree_empty.png'))
		trans_f = pygame.image.load(os.path.join('Pictures', 'tree_filled.png'))
		trans_rect = trans_e.get_rect(center = (590, 665))
		trans_pos = pantalla.blit(trans_e, trans_rect)
		return trans_e, trans_f, trans_pos

	def save_load(self, pantalla):
		load_f = pygame.image.load(os.path.join('Pictures', 'load_filled.png'))
		load_e = pygame.image.load(os.path.join('Pictures', 'load_empty.png'))
		save_f = pygame.image.load(os.path.join('Pictures', 'save_filled.png'))
		save_e = pygame.image.load(os.path.join('Pictures', 'save_empty.png'))
		save_rect = save_f.get_rect(center = (795, 30))
		save_pos = pantalla.blit(save_f, save_rect)
		load_rect = load_f.get_rect(center = (840, 30))
		load_pos = pantalla.blit(load_f, load_rect)
		return load_f, load_e, save_f, save_e, load_pos, save_pos


