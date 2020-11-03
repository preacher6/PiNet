import pygame
import random
import sys
import os
import math
import pickle
import numpy as np
import easygui as eg 
from pygame.locals import *
from scroll_matrix import ScrollMatrix
from objetos import Estados, Transiciones, Conectar
from sympy import Matrix

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = ( 0, 255, 0)
estado = None
conector = None
modo = [1, 0, 0] #0 Manual, 1. Automatico, 2. Temporizado
vel = 20

class Items(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.SysFont('Arial', 15)
		self.imagen_estado = None
		self.recta_estado = 0
		self.imagen_trans = None
		self.recta_trans = 0
		self.imagen_arco = None
		self.recta_arco = 0
		self.imagen_peso = None
		self.recta_peso = 0
		self.hold = [0, 0, 0, 0, 0]
		self.repeat_con_sup = 0
		self.repeat_con_inf = 0
		self.cont_int_sup = 0
		self.holding = 0
		self.dibujando = 0
		self.inicial = 0
		self.final = 0
		self.posicion_inicial = None
		self.posicion_final = None		
		self.push_proper = False
		self.invocar_propiedades()

	def invocar_propiedades(self):
		"""Invocar propiedades compartidas entre inicializador y carga"""
		self.lista_estados = []
		self.lista_trans = []		
		self.lista_conexiones = []
		self.sprites_estados = pygame.sprite.Group()
		self.sprites_trans = pygame.sprite.Group()
		self.sprites_conexion = pygame.sprite.Group() # Conexiones físicas
		self.borrar = []
		self.lista_marcado = list()
		self.marcado_act = list()
		self.tag_estado = 0
		self.tag_trans = 0
		self.lista_tags_e = list()
		self.lista_tags_t = list()
		self.inc_pos = []
		self.inc_pre = []
		self.inc_pro = []
		self.inc_pre_aux = []
		self.inc = []
		self.dual = []
		self.uk = []
		self.uk_pro = []
		self.uk_man = []
		self.active_trans_man = 0
		self.repair_disp = 0
		self.sprites_conexion_full = pygame.sprite.Group() #Conexiones reales tras la pantalla
		self.cont_create = 0 # Contador de elementos ficticios
		self.pure = 0 # Contador de impurezas
		self.pos_correc = list() #Lista que contiene todas las posiciones a corregir de pureza
		self.estados_fict = list()
		self.trans_fict = list(	)
		self.pure_act = 0
		self.rotate = 0
		self.lista_con_rectas = list()
		self.inc_pre_full = []
		self.inc_pos_full = []
		self.inc_full = []
		self.lista_col = list()
		self.lista_con_coor = list()
		self.rect_conec = list()
		self.lista_col_t = list()
		self.lista_col_s = list()
		self.ini = list()
		self.fin = list()
		self.panel = pygame.Surface((680, 560))
		self.proper_draw = ScrollMatrix()
		self.pasos = (0, 0)
		self.barra_actual = [364, 364]
		self.pasos = [0, 0]
		self.desp = [0, 0]
		self.marcado_ini = np.arange(1)

	def save_net(self, propiedades, barra_actual, size_sheet, modo_temp):
		"""Almacena red para futura evaluación"""
		container = {'lista_estados':self.lista_estados, 'lista_trans':self.lista_trans, 'sprites_estados':self.sprites_estados,
					 'sprites_trans':self.sprites_trans, 'sprites_conexion':self.sprites_conexion, 'inicial':self.inicial, 'final':self.final, 
				     'lista_marcado':self.lista_marcado, 'marcado_act':self.marcado_act, 'tag_estado':self.tag_estado, 'tag_trans':self.tag_trans,
					 'lista_tags_e':self.lista_tags_e, 'lista_tags_t':self.lista_tags_t, 'inc_pos':self.inc_pos, 'inc_pre':self.inc_pre, 
					 'inc_pre_aux':self.inc_pre_aux, 'inc':self.inc, 'dual':self.dual, 'uk':self.uk, 'uk_pro':self.uk_pro, 'uk_man':self.uk_man,
					 'sprites_conexion_full':self.sprites_conexion_full, 'cont_create':self.cont_create, 'pure':self.pure, 'pos_correc':self.pos_correc,
					 'estados_fict':self.estados_fict, 'trans_fict':self.trans_fict, 'lista_con_rectas':self.lista_con_rectas, 'inc_pre_full':self.inc_pre_full,
					 'inc_pos_full':self.inc_pos_full, 'inc_full':self.inc_full, 'lista_col':self.lista_col, 'lista_con_coor':self.lista_con_coor, 
					 'rect_conec':self.rect_conec, 'lista_col_t':self.lista_col_t, 'lista_col_s':self.lista_col_s, 'ini':self.ini, 'fin':self.fin,
					 'marcado_ini':self.marcado_ini, 'lista_barra':propiedades.lista_barra, 'barra_actual':barra_actual, 'size_sheet':size_sheet, 'modo_temp':modo_temp}
		#print(self.rect_conec)
		archivo_s = eg.filesavebox(msg="Guardar archivo",
                         title="Control: filesavebox",
                         default='',
                         filetypes="*.txt")
		#print(archivo_s)
		if archivo_s != None:
			with open(archivo_s, 'wb') as fp:
				pickle.dump(container, fp)

			eg.msgbox(archivo_s, "Archivo almacenado en:", ok_button="Continuar")
		else:
			eg.msgbox('Operación cancelada', "Advertencia", ok_button="Continuar")

	def load_net(self, superficie, erase, lista_barra, barra_actual, size_sheet):
		"""Carga red previamente almacenada"""
		lista_barra = lista_barra
		barra_actual = barra_actual
		size_sheet = size_sheet
		extension = ["*.txt"]
		archivo_o = eg.fileopenbox(msg="Abrir archivo",
                         title="Control: fileopenbox",
                         default='',
                         filetypes=extension)
		if archivo_o == None:
			eg.msgbox('Operación cancelada', "Elemento invalido", ok_button="Continuar")
			return lista_barra, barra_actual, size_sheet
		else:
			try:
				with open(archivo_o, 'rb') as fp:
					data_list= pickle.load(fp)
				self.sprites_estados.clear(superficie, erase)
				self.sprites_trans.clear(superficie, erase)
				self.sprites_conexion.clear(superficie, erase)
				superficie.fill((255, 255, 255))
				self.invocar_propiedades()
				self.lista_estados = data_list['lista_estados']
				self.lista_trans = data_list['lista_trans']
				self.sprites_estados = data_list['sprites_estados']
				for estado in self.sprites_estados:
					estado.image=pygame.image.load(os.path.join('Pictures', 'estado.png'))
				self.sprites_trans = data_list['sprites_trans']
				for trans in self.sprites_trans:
					if trans.horizon:
						trans.image = pygame.image.load(os.path.join('Pictures', 'trans.png'))
					else:
						trans.image = pygame.image.load(os.path.join('Pictures', 'transv.png'))
				self.sprites_conexion = data_list['sprites_conexion']
				flecha = pygame.image.load(os.path.join('Pictures', 'flecha.png'))
				for con in self.sprites_conexion:			
					nar = pygame.transform.rotate(flecha, con.angle)
					con.image = nar
				self.inicial = data_list['inicial']
				self.final = data_list['final']
				self.lista_marcado = data_list['lista_marcado']
				self.marcado_act = data_list['marcado_act']
				self.tag_estado = data_list['tag_estado']
				self.tag_trans = data_list['tag_trans']
				self.lista_tags_e = data_list['lista_tags_e']
				self.lista_tags_t = data_list['lista_tags_t']
				self.inc_pos = data_list['inc_pos']
				self.inc_pre = data_list['inc_pre']
				self.inc_pre_aux = data_list['inc_pre_aux']
				self.inc = data_list['inc']
				self.dual = data_list['dual']
				self.uk = data_list['uk']
				self.uk_pro = data_list['uk_pro']
				self.uk_man = data_list['uk_man']
				self.sprites_conexion_full = data_list['sprites_conexion_full']
				self.cont_create = data_list['cont_create']
				self.pure = data_list['pure']
				self.pos_correc = data_list['pos_correc']
				self.estados_fict = data_list['estados_fict']
				self.trans_fict = data_list['trans_fict']
				self.lista_con_rectas = data_list['lista_con_rectas']
				self.inc_pre_full = data_list['inc_pre_full']
				self.inc_pos_full = data_list['inc_pos_full']
				self.inc_full = data_list['inc_full']
				self.lista_col = data_list['lista_col']
				self.lista_con_coor = data_list['lista_con_coor']
				self.rect_conec = data_list['rect_conec']
				self.lista_col_t = data_list['lista_col_t']
				self.lista_col_s = data_list['lista_col_s']
				self.ini = data_list['ini']
				self.fin = data_list['fin']
				self.marcado_ini = data_list['marcado_ini']
				lista_barra = data_list['lista_barra']
				barra_actual = data_list['barra_actual']
				size_sheet = data_list['size_sheet']
				lista_barra[0] = pygame.image.load(os.path.join('Pictures', 'down.png'))
				lista_barra[1] = pygame.image.load(os.path.join('Pictures', 'up.png'))
				lista_barra[2] = pygame.image.load(os.path.join('Pictures', 'left.png'))
				lista_barra[3] = pygame.image.load(os.path.join('Pictures', 'right.png'))
				lista_barra[4] = pygame.image.load(os.path.join('Pictures', 'plus.png'))
				lista_barra[16] = fondo_barra_v = pygame.Surface((25, 505))
				lista_barra[16].fill((118, 118, 118))
				lista_barra[17] = fondo_barra_h = pygame.Surface((625, 25))
				lista_barra[17].fill((118, 118, 118))
				lista_barra[14] = pygame.Surface((625, 17))
				lista_barra[13] = pygame.transform.scale(lista_barra[14], (barra_actual[0], 17))
				lista_barra[11] = pygame.Surface((17, 505))
				lista_barra[10] = pygame.transform.scale(lista_barra[11], (17, barra_actual[1]))			
				
				if len(self.ini)>0:
					for i, _ in enumerate(self.ini):
						pygame.draw.aaline(superficie, (255, 255, 255), self.ini[i], self.fin[i])
						pygame.draw.aaline(superficie, (0, 0, 0), self.ini[i], self.fin[i])

				return lista_barra, barra_actual, size_sheet

			except:
   				eg.msgbox('El elemento seleccionado no es valido', "Error", ok_button="Continuar")
   				return lista_barra, barra_actual, size_sheet

	def tooltip_estados(self, pos, superficie, pos_dibujo, estado):
		tag = 'Lugar '+str(estado.tag)
		x, y = pos
		superficie.blit(self.font.render(tag, True, (255, 0, 0)), (x+10, y+10))

	def tooltip_trans(self, pos, superficie, pos_dibujo, trans):
		tag = 'Transicion '+str(trans.tag)
		x, y = pos
		superficie.blit(self.font.render(tag, True, (255,0,0)), (x+10,y+10))

	def tooltip_conex(self, pos, superficie, pos_dibujo, con, bloqueo_general):
		tag = 'Peso del arco: '+ str(con.token)
		x, y = pos
		superficie.blit(self.font.render(tag, True, (255, 0, 0)), (x+10, y+10))

	def dibujar_panel(self, superficie):
		"""Metodo que permite dibujar los items dentro del panel de herramientas"""
		# Estado
		self.imagen_estado = pygame.image.load(os.path.join('Pictures', 'estado.png'))
		self.recta_estado = self.imagen_estado.get_rect()
		self.recta_estado.centerx = 90
		self.recta_estado.centery = 180
		superficie.blit(self.imagen_estado, self.recta_estado)
		# Transicion
		self.imagen_trans = pygame.image.load(os.path.join('Pictures', 'trans.png'))
		self.imagen_transv = pygame.image.load(os.path.join('Pictures', 'transv.png'))
		self.recta_trans = self.imagen_trans.get_rect()
		self.recta_transv = self.imagen_transv.get_rect()
		self.recta_trans.centerx = 90
		self.recta_trans.centery = 270
		superficie.blit(self.imagen_trans, self.recta_trans)
		# Arco
		self.imagen_arco = pygame.image.load(os.path.join('Pictures', 'arco.png'))		
		self.recta_arco = self.imagen_arco.get_rect()
		self.recta_arco.centerx = 90
		self.recta_arco.centery = 360
		superficie.blit(self.imagen_arco, self.recta_arco)

		self.imagen_arco_on = pygame.image.load(os.path.join('Pictures', 'arco_on.png'))
		self.recta_arco_on = self.imagen_arco_on.get_rect()
		self.recta_arco_on.centerx = 90
		self.recta_arco_on.centery = 360

		# Peso
		self.imagen_peso = pygame.image.load(os.path.join('Pictures', 'peso.png'))
		self.rect = self.imagen_peso.get_rect()
		self.rect.centerx = 90
		self.rect.centery = 450
		superficie.blit(self.imagen_peso, self.rect)

	def consultar(self, pos, superficie):
		keys = pygame.key.get_pressed()
		panel = pygame.image.load(os.path.join('Pictures', 'panel_config.png'))

		if pygame.mouse.get_pressed()[2] and self.rotate == 0:
			self.rotate = 1
		elif pygame.mouse.get_pressed()[2] and self.rotate == 1:
			self.rotate = 0

		if self.hold[1] == 1:
			while pygame.mouse.get_pressed()[2]:
				for event in pygame.event.get():
					if event.type == pygame.MOUSEBUTTONDOWN:
						pass

		if pygame.mouse.get_pressed()[0] and self.recta_estado.collidepoint(pos) or self.hold[0] == 1: # Estado	
			self.hold = [1, 0, 0, 0, 0]
			self.recta_estado.center = pos
			superficie.blit(self.imagen_estado, self.recta_estado)

		if pygame.mouse.get_pressed()[0] and self.recta_trans.collidepoint(pos) or self.hold[1] == 1: # Transición
			self.hold = [0, 1, 0, 0, 0]	
			if self.rotate == 0:				
				self.recta_trans.center = pos
				superficie.blit(self.imagen_trans, self.recta_trans)
			elif self.rotate ==  1:
				self.recta_transv.center = pos
				superficie.blit(self.imagen_transv, self.recta_transv)

		"""if pygame.mouse.get_pressed()[2] and self.hold[1] == 1 or self.hold[4] == 1:
			self.hold = [0, 0, 0, 0, 1]
			self.recta_transv.center = pos
			superficie.blit(self.imagen_transv, self.recta_transv)"""

		if pygame.mouse.get_pressed()[0] and self.recta_arco.collidepoint(pos) or self.hold[2] == 1: # Arco
			self.hold = [0, 0, 1, 0, 0]			
			self.recta_arco_on.center = pos
			if self.dibujando == 0:
				superficie.blit(self.imagen_arco_on, self.recta_arco_on)

		if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos) or self.hold[3] == 1:	# Peso
			self.hold = [0, 0, 0, 1, 0]			
			self.rect.center = pos
			superficie.blit(self.imagen_peso, self.rect)

		if keys[K_ESCAPE] == 1:
			self.hold = [0, 0, 0, 0, 0]
			self.inicial = 0
			self.push_proper = False
			self.rotate = 0
			self.dibujando = 0

	def borrar_elemento(self, superficie, center_move, pos):
		"Eliminar elemento del área de trabajo"
		imagen_borrar = pygame.image.load(os.path.join('Pictures', 'borrar.png'))
		recta_borrar = imagen_borrar.get_rect()
		recta_borrar.center = pos
		superficie.blit(imagen_borrar, recta_borrar)
		if pygame.mouse.get_pressed()[0] == 1:
			self.borrar = center_move
		else:
			self.borrar = (0, 0)

	def dibujar_area(self, dentro, pos, superficie, desp):  # En caso de dibujarse dentro del area de trabajo se agrega el elemento 
		if self.hold[0] == 1:
			if dentro == 1:
				estado = Estados(pos, self.tag_estado, desp)
				hit_estado_e = pygame.sprite.spritecollide(estado, self.sprites_estados, False)
				hit_estado_t = pygame.sprite.spritecollide(estado, self.sprites_trans, False)
				if not hit_estado_e and not hit_estado_t:	
					self.sprites_estados.add(estado)
					self.lista_estados.append(estado.recta())
					self.lista_tags_e.append(self.tag_estado)					
					self.tag_estado += 1
				else:
					print('Colisión entre estados')
			elif dentro == 0:
				print('Es necesario dibujar dentro del área de trabajo')

		elif self.hold[1] == 1:
			if dentro == 1:
				if self.rotate == 0:
					transicion = Transiciones(pos, self.tag_trans, desp)
				elif self.rotate == 1:
					transicion = Transiciones(pos, self.tag_trans, desp, horizon = False)
				hit_transicion_t = pygame.sprite.spritecollide(transicion, self.sprites_trans, False)
				hit_transicion_e = pygame.sprite.spritecollide(transicion, self.sprites_estados, False)
				if not hit_transicion_t and not hit_transicion_e:
					self.sprites_trans.add(transicion)
					self.lista_trans.append(transicion.recta())					
					self.lista_tags_t.append(self.tag_trans)
					self.tag_trans += 1
				else:
					print('Colisión entre transiciones')
			elif dentro == 0:
				print('Es necesario dibujar dentro del área de trabajo')

		elif self.hold[4] == 1:
			if dentro == 1:
				transicion = Transiciones(pos, self.tag_trans, horizon = False)
				hit_transicion_t = pygame.sprite.spritecollide(transicion, self.sprites_trans, False)
				hit_transicion_e = pygame.sprite.spritecollide(transicion, self.sprites_estados, False)
				if not hit_transicion_t and not hit_transicion_e:
					self.sprites_trans.add(transicion)
					self.lista_trans.append(transicion.recta())					
					self.lista_tags_t.append(self.tag_trans)
					self.tag_trans += 1
					self.rotate = 0
				else:
					print('Colisión entre transiciones')
			elif dentro == 0:
				print('Es necesario dibujar dentro del área de trabajo')
		else:
			pass

	def conectar(self, pos, dentro, superficie, desp, posi):
		add = 1
		if dentro == 1 and self.hold[2] == 1: 
			self.rect.center = pos

			if self.inicial == 1: # Inicia en estado
				for status in self.sprites_estados:
					if self.rect.colliderect(status):
						print('No es posible')

				for transi in self.sprites_trans:
					if self.rect.colliderect(transi):
						#print('Final transi')
						idx = self.nrect.collidelist(self.rect_conec) # Identifica si una recta de conexion choca con alguna otra ya existente. -1 si no sobrepone otra nrect
						for status in self.sprites_estados:   # Busca dentro de la lista de sprites estados
							if status.seleccionado == True:    # Si el estado tiene la propiedad seleccionado activo entra y crea el elemento conectar
								status.oct = True
								#print('estado:', status.tag)
								self.posicion_inicial = (round(self.posicion_inicial[0]), round(self.posicion_inicial[1]))
								self.posicion_final = (round(self.posicion_final[0]), round(self.posicion_final[1]))
								conectar = Conectar(self.posicion_inicial, self.posicion_final, -1, transi.tag, status.tag, self.angle, desp, horizon = transi.horizon)					
								self.posicion_inicial = (round(self.posicion_inicial[0])-180+desp[0], round(self.posicion_inicial[1])-50+desp[1])
								self.posicion_final = (round(self.posicion_final[0])-180+desp[0], round(self.posicion_final[1])-50+desp[1])
								self.ini.append(self.posicion_inicial)
								self.fin.append(self.posicion_final)
								self.sprites_conexion.add(conectar)
								self.sprites_conexion_full.add(conectar)
								transi.conexiones.append(conectar)  # Lo adiciona dentro de las conexiones que parten de transicion a estado
								status.conexiones.append(conectar)  # Lo adiciona dentro de las conexiones que salen de estado a transicion
							status.seleccionado = False	  # El objeto deja de estar seleccionado
							
							self.dibujando = 0
							self.inicial = 0

						if conectar.col in self.lista_col_t:  # Este for es basicamente para las conexiones poseen posicion inicial y final ya existente
							add = 0
							#conectar.fini()
							for con in self.sprites_conexion:
								if con.punto_inicial == -1:
									if con.col == conectar.col:
										con.token += 1 # Adiciona peso a la conexion ya existente
						else:
							add = 1

						self.dibujando = 0	
						#print('idx', idx)					
						if idx == -1:
							self.rect_conec.append(self.nrect)
							self.lista_col_t.append(conectar.col)
							if add == 0:
								#print('borra1')	
								#print('tag: ', status.tag)							
								self.sprites_conexion.remove(conectar)
								self.sprites_conexion_full.remove(conectar)
								#self.rect_conec.remove(self.nrect)
								del self.rect_conec[-1]
								#transi.conexiones.remove(conectar)
								for status in self.sprites_estados:
									if status.oct == True:
										del status.conexiones[-1]
										status.oct = False
								del transi.conexiones[-1]
								#self.lista_col_t.remove(conectar.col)
								del self.lista_col_t[-1]
								#self.ini.remove(self.posicion_inicial)
								#self.fin.remove(self.posicion_final)
								del self.ini[-1]
								del self.fin[-1]
						else: 
							#print('colision1')
							self.inicial = 0
							#print('tag: ', status.tag)
							#self.ini.remove(self.posicion_inicial)
							#self.fin.remove(self.posicion_final)
							for status in self.sprites_estados:
								if status.oct == True:
									del status.conexiones[-1]
									status.oct = False
							del transi.conexiones[-1]
							del self.ini[-1]
							del self.fin[-1]
							self.sprites_conexion.remove(conectar)
							self.sprites_conexion_full.remove(conectar)

			elif self.inicial == 2: # Inicia en transición
				for status in self.sprites_estados: # Revisa estados
					if self.rect.colliderect(status): # Si el estado es seleccionado
						#print('Final estado')
						ids = self.nrect.collidelist(self.rect_conec) # Identifica si una recta de conexion choca con alguna otra ya existente. -1 si no sobrepone otra nrect
						for transi in self.sprites_trans:
							if transi.seleccionado == True: # Para la transicion inicial
								transi.oct = True # Auxiliar
								conectar = Conectar(self.posicion_inicial, self.posicion_final, 1, transi.tag, status.tag, self.angle, desp)
								self.posicion_inicial = (round(self.posicion_inicial[0])-180+desp[0], round(self.posicion_inicial[1])-50+desp[1])
								self.posicion_final = (round(self.posicion_final[0])-180+desp[0], round(self.posicion_final[1])-50+desp[1])
								self.ini.append(self.posicion_inicial)
								self.fin.append(self.posicion_final)
								status.conexiones.append(conectar)
								transi.conexiones.append(conectar)
								self.sprites_conexion.add(conectar)
								self.sprites_conexion_full.add(conectar)
							transi.seleccionado = False
								
							self.dibujando = 0
							self.inicial = 0
						if conectar.col in self.lista_col_s:
							add = 0
							#conectar.fini()
							for con in self.sprites_conexion:
								if con.punto_inicial == 1:
									#print('1')
									if con.col == conectar.col:
										con.token += 1
						else:
							add = 1	
						
						self.dibujando = 0
						#print('ids', ids)
						if ids == -1:
							self.rect_conec.append(self.nrect)
							self.lista_col_s.append(conectar.col)
							if add == 0:
								#print('borra2')
								#status.conexiones.remove(conectar)
								self.sprites_conexion.remove(conectar)
								self.sprites_conexion_full.remove(conectar)
								#self.rect_conec.remove(self.nrect)
								del self.rect_conec[-1]								
								del status.conexiones[-1]	
								for transi in self.sprites_trans:
									if transi.oct == True:
										del transi.conexiones[-1]
										transi.oct = False
								#self.lista_col_s.remove(conectar.col)
								del self.lista_col_s[-1]
								#self.ini.remove(self.posicion_inicial)
								#self.fin.remove(self.posicion_final)
								del self.ini[-1]
								del self.fin[-1]
						else:
							#print('colision2')
							self.inicial = 0
							#if add == 0:
								#self.ini.remove(self.posicion_inicial)
								#self.fin.remove(self.posicion_final)
							del status.conexiones[-1]	
							for transi in self.sprites_trans:
									if transi.oct == True:
										del transi.conexiones[-1]
										transi.oct = False
							del self.ini[-1]
							del self.fin[-1]
							self.sprites_conexion.remove(conectar)
							self.sprites_conexion_full.remove(conectar)

				for transi in self.sprites_trans:
					if self.rect.colliderect(transi):
						print('No es posible')

			elif self.inicial == 0:
				for status in self.sprites_estados:
					if status.rect.collidepoint(pos):
						self.posicion_ini = status.rect.center
						self.inicial = 1
						status.seleccionado = True
						#print('stax', status.tag)
					"""if self.rect.colliderect(status):
						self.posicion_ini = status.rect.center
						self.inicial = 1
						status.seleccionado = True"""

				for transi in self.sprites_trans:
					if transi.rect.collidepoint(pos):
						self.posicion_ini = transi.rect.center
						self.ini_tran = pos
						self.inicial = 2
						transi.seleccionado = True
					"""if self.rect.colliderect(transi):
						self.posicion_ini = transi.rect.center
						self.inicial = 2
						transi.seleccionado = True"""

	def dibujar_arco(self, pos, superficie, posi, center_move, desp):
		if self.hold[2] == 1:
			if self.inicial == 1:
				self.calcular_angulo(pos, superficie, posi, center_move, desp)
			elif self.inicial == 2:
				self.calcular_angulo(pos, superficie, posi, center_move, desp)

	def calcular_angulo(self, pos, superficie, posi, center_move, desp):
			self.dibujando = 1
			self.flecha = pygame.image.load(os.path.join('Pictures', 'flecha.png')) # Carga imagen de flecha
			self.posicion_inicial = (self.posicion_ini[0]+180-desp[0], self.posicion_ini[1]+50-desp[1])
			self.angle = math.atan2(-(center_move[1]-self.posicion_ini[1]), center_move[0]-self.posicion_ini[0])			
			self.angle = math.degrees(self.angle)
			if self.angle < 0:
				self.angle += 360
			nar = pygame.transform.rotate(self.flecha, self.angle)
			self.nrect = nar.get_rect(center=(center_move))
			idx = self.nrect.collidelist(self.lista_trans)
			ids = self.nrect.collidelist(self.lista_estados)
			self.nrect = nar.get_rect(center=(pos))
			hipo_1 = 25
			hipo_2 =30
			if self.inicial == 1:
				if idx != -1:
					if self.lista_trans[idx][2] == 40:
						y = self.lista_trans[idx][1] # Determina colision de la cabeza flecha con una transicion
						x = self.lista_trans[idx][0]
						fin_y = tuple(np.subtract((pos[0], y+18), pos))
						fin_x = tuple(np.subtract((x+9, pos[1]), pos))
						if self.angle <= 25:
							self.posicion_final = (x-3+180-desp[0], pos[1])
							self.posicion_inicial = (self.posicion_inicial[0]+(math.cos((self.angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]-(math.sin((self.angle*math.pi)/180)*hipo_1))
							self.nrect = nar.get_rect(center = self.posicion_final)
							pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
							superficie.blit(nar, self.nrect)
						elif self.angle < 155:
							self.posicion_inicial = (self.posicion_inicial[0]+(math.cos((self.angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]-(math.sin((self.angle*math.pi)/180)*hipo_1))
							#self.posicion_final = tuple(np.add(pos, fin_y+50))
							self.posicion_final = (pos[0], y+40+28-desp[1])
							self.nrect = nar.get_rect(center = self.posicion_final)
							pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
							superficie.blit(nar, self.nrect)
						elif self.angle < 215:
							angle = self.angle - 180
							self.posicion_inicial = (self.posicion_inicial[0]-(math.cos((angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]+(math.sin((angle*math.pi)/180)*hipo_1))
							self.posicion_final = (x+41+180-desp[0], pos[1])
							self.nrect = nar.get_rect(center = self.posicion_final)
							pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
							superficie.blit(nar, self.nrect)
						elif self.angle < 335:
							angle = self.angle - 180
							self.posicion_inicial = (self.posicion_inicial[0]-(math.cos((angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]+(math.sin((angle*math.pi)/180)*hipo_1))
							self.posicion_final = (pos[0], y-3+50-desp[1])
							self.nrect = nar.get_rect(center = self.posicion_final)
							pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
							superficie.blit(nar, self.nrect)
						elif self.angle <= 360:
							angle = self.angle - 180
							self.posicion_inicial = (self.posicion_inicial[0]-(math.cos((angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]+(math.sin((angle*math.pi)/180)*hipo_1))
							self.posicion_final = (x-3+180-desp[0], pos[1])
							self.nrect = nar.get_rect(center = self.posicion_final)
							pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
							superficie.blit(nar, self.nrect)
					elif self.lista_trans[idx][2] == 14:
						y = self.lista_trans[idx][1]
						x = self.lista_trans[idx][0]
						fin_y = tuple(np.subtract((pos[0], y+18), pos))
						fin_x = tuple(np.subtract((x+9, pos[1]), pos))					
						if self.angle <= 60:
							self.posicion_final = (x-3+180-desp[0], pos[1])
							self.posicion_inicial = (self.posicion_inicial[0]+(math.cos((self.angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]-(math.sin((self.angle*math.pi)/180)*hipo_1))
							self.nrect = nar.get_rect(center = self.posicion_final)
							pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
							superficie.blit(nar, self.nrect)
						elif self.angle < 120:
							self.posicion_inicial = (self.posicion_inicial[0]+(math.cos((self.angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]-(math.sin((self.angle*math.pi)/180)*hipo_1))
							self.posicion_final = (pos[0], y+40+50-desp[1])
							self.nrect = nar.get_rect(center = self.posicion_final)
							pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
							superficie.blit(nar, self.nrect)
						elif self.angle < 240:
							angle = self.angle - 180
							self.posicion_inicial = (self.posicion_inicial[0]-(math.cos((angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]+(math.sin((angle*math.pi)/180)*hipo_1))
							self.posicion_final = (x+14+180-desp[0], pos[1])
							self.nrect = nar.get_rect(center = self.posicion_final)
							pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
							superficie.blit(nar, self.nrect)
						elif self.angle < 300:
							angle = self.angle - 180
							self.posicion_inicial = (self.posicion_inicial[0]-(math.cos((angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]+(math.sin((angle*math.pi)/180)*hipo_1))
							self.posicion_final = (pos[0], y+50-desp[1])
							self.nrect = nar.get_rect(center = self.posicion_final)
							pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
							superficie.blit(nar, self.nrect)
						elif self.angle <= 360:
							angle = self.angle - 180
							self.posicion_inicial = (self.posicion_inicial[0]-(math.cos((angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]+(math.sin((angle*math.pi)/180)*hipo_1))
							self.posicion_final = (x-3+180-desp[0], pos[1])
							self.nrect = nar.get_rect(center = self.posicion_final)
							pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
							superficie.blit(nar, self.nrect)
				else:
					self.posicion_final=pos
					if self.angle < 90:
						self.posicion_inicial = (self.posicion_inicial[0]+(math.cos((self.angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]-(math.sin((self.angle*math.pi)/180)*hipo_1))
						superficie.blit(nar, self.nrect)
						pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, pos, 1)
					elif self.angle < 180:
						angle = self.angle
						self.posicion_inicial = (self.posicion_inicial[0]+(math.cos((angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]-(math.sin((angle*math.pi)/180)*hipo_1))
						superficie.blit(nar, self.nrect)
						pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, pos, 1)	
					elif self.angle < 270:
						angle = self.angle - 180
						self.posicion_inicial = (self.posicion_inicial[0]-(math.cos((angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]+(math.sin((angle*math.pi)/180)*hipo_1))
						superficie.blit(nar, self.nrect)
						pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, pos, 1)
					elif self.angle < 360:
						angle = self.angle - 180
						self.posicion_inicial = (self.posicion_inicial[0]-(math.cos((angle*math.pi)/180)*hipo_1), self.posicion_inicial[1]+(math.sin((angle*math.pi)/180)*hipo_1))
						superficie.blit(nar, self.nrect)
						pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, pos, 1)		
					
			elif self.inicial == 2:
				self.posicion_inicial = (self.ini_tran[0]+180-desp[0], self.ini_tran[1]+50-desp[1])
				if ids != -1:					
					fin_x = self.lista_estados[ids][0] + 25+180-desp[0]
					fin_y = self.lista_estados[ids][1] + 25+50-desp[1]
					if self.angle < 90:
						self.posicion_final = (fin_x-(math.cos((self.angle*math.pi)/180)*hipo_2), fin_y+(math.sin((self.angle*math.pi)/180)*hipo_2))
						self.nrect = nar.get_rect(center = self.posicion_final)
						pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
						superficie.blit(nar, self.nrect)
					elif self.angle <180:
						angle = self.angle - 90
						self.posicion_final = (fin_x+(math.sin((angle*math.pi)/180)*hipo_2), fin_y+(math.cos((angle*math.pi)/180)*hipo_2))
						self.nrect = nar.get_rect(center = self.posicion_final)
						pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
						superficie.blit(nar, self.nrect)
					elif self.angle <270:
						angle = self.angle - 180
						self.posicion_final = (fin_x+(math.cos((angle*math.pi)/180)*hipo_2), fin_y-(math.sin((angle*math.pi)/180)*hipo_2))
						self.nrect = nar.get_rect(center = self.posicion_final)
						pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
						superficie.blit(nar, self.nrect)
					elif self.angle <360:
						angle = self.angle - 270
						self.posicion_final = (fin_x-(math.sin((angle*math.pi)/180)*hipo_2), fin_y-(math.cos((angle*math.pi)/180)*hipo_2))
						self.nrect = nar.get_rect(center = self.posicion_final)
						pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, self.posicion_final, 1)
						superficie.blit(nar, self.nrect)
				else:
					superficie.blit(nar, self.nrect)
					pygame.draw.aaline(superficie, NEGRO, self.posicion_inicial, pos, 1)

	def agregar_peso(self, pos):
		self.rect.center = pos
		if self.hold[3] == 1 and pygame.mouse.get_pressed()[0] == 1:
			for status in self.sprites_estados:
				if self.rect.colliderect(status):
					status.add_token()

			for punto in self.sprites_conexion:
				if self.rect.colliderect(punto):
					punto.add_token()

		if self.hold[3] == 1 and pygame.mouse.get_pressed()[2] == 1:
			for status in self.sprites_estados:
				if self.rect.colliderect(status):
					status.quitar_token()

			for punto in self.sprites_conexion:
				if self.rect.colliderect(punto):
					punto.quitar_token()

	def marcado(self):
		#print('off')
		"Evolución del marcado"
		cont = 0
		value_uk = 0
		self.lista_marcado = list()
		self.marcado_act = list()

		while len(self.marcado_act) != len(self.sprites_estados):			
			for estado in self.sprites_estados:
				if estado.tag == len(self.marcado_act):
					self.marcado_act.append(estado.token)

		self.marcado_act = np.asarray(self.marcado_act)
		#print('ori:', self.marcado_act)
		#self.marcado_ini = self.marcado_act
		card_e = len(self.sprites_estados)
		card_t = len(self.sprites_trans)
		if card_e>0 and card_t>0:
			matriz_incid = np.zeros((card_e, card_t))
			self.inc_pos = np.zeros((card_e, card_t))
			self.inc_pre = np.zeros((card_e, card_t))
			self.inc_pre_aux = np.zeros((card_e, card_t))
			#incidencia previa (Estado--> Transición) (-1)
			#incidencia posterior (Transición--> Estado) (+1)
			for con in self.sprites_conexion:
				if con.punto_inicial == 1:
					self.inc_pos[con.interconectados[1], con.interconectados[0]] = con.token
				if con.punto_inicial == -1:
					self.inc_pre[con.interconectados[1], con.interconectados[0]] = con.token
					self.inc_pre_aux[con.interconectados[1], con.interconectados[0]] = 1
			self.inc = self.inc_pos-self.inc_pre
			self.dual = -(np.transpose(self.inc))
			valide_data = np.zeros(self.inc_pre.shape[0]) # Vector que deposita un 1 en caso de que elemento marcado sea mayor que elemento inc_pre
			compare_data = np.ones(self.inc_pre.shape[0]) # Vector de 1's para comparar con valide_data
			self.uk = np.zeros(self.inc_pre.shape[1]) # Vector que indica que trans. están disponibles a disparar
			for i in range(self.inc_pre.shape[1]):
				if np.sum(self.inc_pre[:,i]) > 0: 
					for j in range(self.inc_pre.shape[0]):
						if self.marcado_act[j] >= self.inc_pre[j, i]: # Compara si marcado es mayor que inc_pre
							valide_data[j] = 1 
						else:
							valide_data[j] = 0
					if (valide_data == compare_data).all(): #Compara para verificar si los elementos de marcado cumplen con la incidencia de una transicion
						self.uk[i] = 1
					else:
						self.uk[i] = 0
				else:
					self.uk[i] = 0
			self.uk_pro = self.uk
			#print('ori_uk:', self.uk)
			delay_trans = list()
			for trans in self.sprites_trans:
				if (self.uk[trans.tag]) == 1:
					trans.active = True
					delay_trans.append(trans.time)
				else:
					trans.active = False
			#print(delay_trans)
			if len(delay_trans) >= 1:
				delay_trans = min(delay_trans)

			pos_uk = list()
			for n, val in enumerate(self.uk): # Extraer posiciones = 1
			    if val == 1:
			        pos_uk.append(n)
			#print('pos_uk:', pos_uk)
			x = (sorted(self.inc_pre, key=sum, reverse=True))
			x_1 = (sorted(self.inc_pre, key=sum, reverse=True))
			#print(x)
			new_order = list()
			for i, val in enumerate(self.inc_pre): # Evaluar matriz original
			    
			    for j, val_2 in enumerate(x_1):
			        if (val == val_2).all(): # Eliminar elemento de lista copia, la idea es q esta se quede vacia
			            
			            new_order.append(j)
			            #x.pop(j)
			            x_1[j] = [20000]
			            break
			rec_comp = 0
			indice_gru = list() # Contenedor de grupo de indices
			val_prohibi = list() # Contenedor de valores que no pueden ser disparados
			uk_final = self.uk
			if len(pos_uk)>1:
				#print('pos_uk:', pos_uk)
				for i, vec in enumerate(x): # Evaluar si alguno de los recursos compartidos es de interes para el vector de disparo actual
					posi_act = list()
					cont_ind = 0
					for j, ele in enumerate(vec): # Anexar indices de cada fila que sean iguales a 1
						if ele >= 1: # Si se cumple esta condi. se anexa la posicion a un vector que permita compararlo con los indices del vector de trans. habilitadas
							if j in pos_uk:
								cont_ind +=1
					if cont_ind >=2:
						rec_comp = 1
						break

				if rec_comp == 1:
					uk_final = np.zeros([1, len(self.uk)])
					    
					for i, vec in enumerate(x):
					    sum_vec = np.sum(vec)
					    cont = 0
					    indice_ind = list() # Contenedor de indices de cada fila
					    for j, val in enumerate(vec):
					        if j in pos_uk:
					            if val == 1:
					                indice_ind.append(j)
					                cont += 1
					    indice_gru.append(indice_ind)
					    if cont == sum_vec and sum_vec != 0:			        
					        if sum_vec > 1: # Indicar si existe algun recurso compartido
					            #print('Recurso compartido en c'+ str(new_order[i]))
					            val_ran = random.choice(indice_ind)
									            
					            if val_ran in val_prohibi: # Evalua si el valor random se encuentra dentro de los valores prohibidos
					                pass
					            else:
					                uk_final[0, val_ran] = 1
					                for m, val in enumerate(indice_ind):
					                    if val not in val_prohibi:
					                        val_prohibi.append(val)			                
					            
					        else:
					            if indice_ind[0] in val_prohibi:
					                pass
					            else:
					                uk_final[0, indice_ind[0]] = 1
			if rec_comp == 1:
				if len(self.uk)==1:
					pass
				else:
					self.uk = np.squeeze(uk_final)
				#print('uk', self.uk)
			#print('----')
			return delay_trans
		
	def evolucionar_no(self, modo, posi, delay_evo, modo_temp, center_move): # Iniciar marcado en la red 
		if modo == [1, 0]:
			active_trans = 0
			#print('uk:', self.uk)
			#self.lista_marcado.append(self.marcado_act)
			self.marcado_act = self.marcado_act + np.transpose(np.dot(self.inc, self.uk))
			#print('marcado:', self.marcado_act)
			valide_data = np.zeros(self.inc_pre.shape[0]) # Vector que deposita un 1 en caso de que elemento marcado sea mayor que elemento inc_pre
			compare_data = np.ones(self.inc_pre.shape[0]) # Vector de 1's para comparar con valide_data
			self.uk = np.zeros(self.inc_pre.shape[1]) # Vector que indica que trans. están disponibles a disparar
			for i in range(self.inc_pre.shape[1]):
				if np.sum(self.inc_pre[:,i]) > 0: 
					for j in range(self.inc_pre.shape[0]):
						if (self.marcado_act[j] >= self.inc_pre[j, i]): # Compara si marcado es mayor que inc_pre
							valide_data[j] = 1 
						else:
							valide_data[j] = 0
					if (valide_data == compare_data).all(): #Compara para verificar si los elementos de marcado cumplen con la incidencia de una transicion
						self.uk[i] = 1
					else:
						self.uk[i] = 0
				else:
					self.uk[i] = 0
			#print('uk_old:', self.uk)
			self.uk_pro = self.uk
			for trans in self.sprites_trans:
				if (self.uk[trans.tag]) == 1:
					trans.active = True
				else:
					trans.active = False
			
			pos_uk = list()
			for n, val in enumerate(self.uk): # Extraer posiciones = 1
			    if val == 1:
			        pos_uk.append(n)
			#print('pos_uk:', pos_uk)
			x = (sorted(self.inc_pre, key=sum, reverse=True))
			x_1 = (sorted(self.inc_pre, key=sum, reverse=True))
			
			new_order = list()
			for i, val in enumerate(self.inc_pre): # Evaluar matriz original
			    
			    for j, val_2 in enumerate(x_1):
			        if (val == val_2).all(): # Eliminar elemento de lista copia, la idea es q esta se quede vacia
			            
			            new_order.append(j)
			            #x.pop(j)
			            x_1[j] = [20000]
			            break
			rec_comp = 0
			indice_gru = list() # Contenedor de grupo de indices
			val_prohibi = list() # Contenedor de valores que no pueden ser disparados
			uk_final = self.uk
			if len(pos_uk)>1:
				for i, vec in enumerate(x): # Evaluar si alguno de los recursos compartidos es de interes para el vector de disparo actual
					posi_act = list()
					cont_ind = 0
					for j, ele in enumerate(vec): # Anexar indices de cada fila que sean iguales a 1
						if ele >= 1: # Si se cumple esta condi. se anexa la posicion a un vector que permita compararlo con los indices del vector de trans. habilitadas
							if j in pos_uk:
								cont_ind +=1
					if cont_ind >=2:
						rec_comp = 1
						break

				if rec_comp == 1:
					uk_final = np.zeros([1, len(self.uk)])
					    
					for i, vec in enumerate(x):
					    sum_vec = np.sum(vec)
					    cont = 0
					    indice_ind = list() # Contenedor de indices de cada fila
					    for j, val in enumerate(vec):
					        if j in pos_uk:
					            if val == 1:
					                indice_ind.append(j)
					                cont += 1
					    indice_gru.append(indice_ind)
					    if cont == sum_vec and sum_vec != 0:			        
					        if sum_vec > 1: # Indicar si existe algun recurso compartido
					            #print('Recurso compartido en c'+ str(new_order[i]))
					            val_ran = random.choice(indice_ind)
									            
					            if val_ran in val_prohibi: # Evalua si el valor random se encuentra dentro de los valores prohibidos
					                pass
					            else:
					                uk_final[0, val_ran] = 1
					                for m, val in enumerate(indice_ind):
					                    if val not in val_prohibi:
					                        val_prohibi.append(val)			                
					            
					        else:
					            if indice_ind[0] in val_prohibi:
					                pass
					            else:
					                uk_final[0, indice_ind[0]] = 1
			if rec_comp == 1:
				if len(self.uk)==1:
					pass
				else:
					self.uk = np.squeeze(uk_final)
		elif modo == [0, 1]:
			delay_trans = 0
			self.uk_man = self.uk
			print('Modo manual')
			if pygame.mouse.get_pressed()[0]:
				for trans in self.sprites_trans:
					if trans.rect.collidepoint(center_move) and trans.active == True:
						for m in range(self.inc_pre.shape[0]):
							if np.sum(self.inc_pre_aux[m,:]) > 1 and self.active_trans_man:
								self.uk_man = np.zeros(len(self.uk_man))
								self.uk_man[trans.tag] = 1
						self.marcado_act = self.marcado_act + np.transpose(np.dot(self.inc,self.uk_man))
						
			valide_data = np.zeros(self.inc_pre.shape[0]) # Vector que deposita un 1 en caso de que elemento marcado sea mayor que elemento inc_pre
			compare_data = np.ones(self.inc_pre.shape[0]) # Vector de 1's para comparar con valide_data
			self.active_trans_man = 0
			for i in range(self.inc_pre.shape[1]):
				for j in range(self.inc_pre.shape[0]):
					if self.marcado_act[j] >= self.inc_pre[j, i]: # Compara si marcado es mayor que inc_pre
						valide_data[j] = 1 
					else:
						valide_data[j] = 0
				if (valide_data == compare_data).all(): #Compara para verificar si los elementos de marcado cumplen con la incidencia de una transicion
					self.uk_man[i] = 1
					self.active_trans_man += 1
				else:
					self.uk_man[i] = 0

			for trans in self.sprites_trans:
				if (self.uk_man[trans.tag]) == 1:
					trans.active = True
				else:
					trans.active = False

	def marcado_t(self):
		"Evolución del marcado"
		cont = 0
		value_uk = 0
		self.lista_marcado = list()
		self.marcado_act = list()

		while len(self.marcado_act) != len(self.sprites_estados):			
			for estado in self.sprites_estados:
				if estado.tag == len(self.marcado_act):
					self.marcado_act.append(estado.token)

		self.marcado_act = np.asarray(self.marcado_act)
		#print('ori:', self.marcado_act)
		#self.marcado_ini = self.marcado_act
		card_e = len(self.sprites_estados)
		card_t = len(self.sprites_trans)
		if card_e>0 and card_t>0:
			matriz_incid = np.zeros((card_e, card_t))
			self.inc_pos = np.zeros((card_e, card_t))
			self.inc_pre = np.zeros((card_e, card_t))
			self.inc_pre_aux = np.zeros((card_e, card_t))
			#incidencia previa (Estado--> Transición) (-1)
			#incidencia posterior (Transición--> Estado) (+1)
			for con in self.sprites_conexion:
				if con.punto_inicial == 1:
					self.inc_pos[con.interconectados[1], con.interconectados[0]] = con.token
				if con.punto_inicial == -1:
					self.inc_pre[con.interconectados[1], con.interconectados[0]] = con.token
					self.inc_pre_aux[con.interconectados[1], con.interconectados[0]] = 1
			self.inc = self.inc_pos-self.inc_pre
			self.dual = -(np.transpose(self.inc))
			valide_data = np.zeros(self.inc_pre.shape[0]) # Vector que deposita un 1 en caso de que elemento marcado sea mayor que elemento inc_pre
			compare_data = np.ones(self.inc_pre.shape[0]) # Vector de 1's para comparar con valide_data
			self.uk = np.zeros(self.inc_pre.shape[1]) # Vector que indica que trans. están disponibles a disparar
			for i in range(self.inc_pre.shape[1]):
				if np.sum(self.inc_pre[:,i]) > 0: 
					for j in range(self.inc_pre.shape[0]):
						if self.marcado_act[j] >= self.inc_pre[j, i]: # Compara si marcado es mayor que inc_pre
							valide_data[j] = 1 
						else:
							valide_data[j] = 0
					if (valide_data == compare_data).all(): #Compara para verificar si los elementos de marcado cumplen con la incidencia de una transicion
						self.uk[i] = 1
					else:
						self.uk[i] = 0
				else:
					self.uk[i] = 0
			self.uk_pro = self.uk
			delay_trans = list()
			#delay_trans.append(0)
			delay_tags = list()			
			pos_uk = list()
			for trans in self.sprites_trans:
				if (self.uk[trans.tag]) == 1:
					trans.active = True
					delay_trans.append(trans.time)
					delay_tags.append(trans.tag)
				else:
					trans.active = False
			uk_final = np.zeros([self.uk.shape[0]])
			#print(uk_final)
			#print('tags:', delay_tags)
			if len(delay_trans) >= 1: # Eleccion de transicion disponible con menor tiempo de disparo
				delay_trans = min(delay_trans)
				#print(delay_trans)
				for trans in self.sprites_trans:
					if trans.time == delay_trans and self.uk[trans.tag]==1:
						pos_uk.append(trans.tag)
				#print('position:', pos_uk)
				val_fin = random.choice(pos_uk)

			else:
				val_fin = delay_tags[0]
				"""for n, val in enumerate(self.uk): # Extraer posiciones = 1
				    if val == 1:
				        pos_uk.append(n)"""

			for trans in self.sprites_trans:
				if trans.tag == val_fin:
					uk_final[trans.tag] = 1

			self.uk = uk_final
			#print('marc', self.marcado_act)
			#print('uk_marc', self.uk)
		return delay_trans

	def evolucionar_t(self, modo, posi, delay_evo, modo_temp, center_move): # Iniciar marcado en la red 
		if modo == [1, 0]:
			try:
				salir_t = 0
				#print('-------')
				active_trans = 0
				#print('uk_old:', self.uk)
				#if (self.marcado_act == 
				self.lista_marcado.append(self.marcado_act)
				#print('marcado_1', self.marcado_act)

				#print(np.zeros([self.marcado_act.shape[0]]))

				self.marcado_act = self.marcado_act + np.transpose(np.dot(self.inc, self.uk))
				#print('marcado', self.marcado_act)
				#print(np.zeros([self.marcado_act.shape[0]]))
				if (self.marcado_act == np.zeros([self.marcado_act.shape[0]])).all():
					#print('in')
					delay_trans = 0
				
				else:
				#print('marcado:', self.marcado_act)
					valide_data = np.zeros(self.inc_pre.shape[0]) # Vector que deposita un 1 en caso de que elemento marcado sea mayor que elemento inc_pre
					compare_data = np.ones(self.inc_pre.shape[0]) # Vector de 1's para comparar con valide_data
					self.uk = np.zeros(self.inc_pre.shape[1]) # Vector que indica que trans. están disponibles a disparar
					for i in range(self.inc_pre.shape[1]):
						if np.sum(self.inc_pre[:,i]) > 0: 
							for j in range(self.inc_pre.shape[0]):
								if (self.marcado_act[j] >= self.inc_pre[j, i]): # Compara si marcado es mayor que inc_pre
									valide_data[j] = 1 
								else:
									valide_data[j] = 0
							if (valide_data == compare_data).all(): #Compara para verificar si los elementos de marcado cumplen con la incidencia de una transicion
								self.uk[i] = 1
							else:
								self.uk[i] = 0
						else:
							self.uk[i] = 0

					self.uk_pro = self.uk
					#print('uk', self.uk)
					delay_trans = list()
					delay_tags = list()		
					#print(delay_tags)	
					pos_uk = list()
					for trans in self.sprites_trans:
						if (self.uk[trans.tag]) == 1:
							trans.active = True
							delay_trans.append(trans.time)
							delay_tags.append(trans.tag)
						else:
							trans.active = False
					uk_final = np.zeros([self.uk.shape[0]])
					#print('del_trans', delay_trans)
					#print('tags:', delay_tags)
					if len(delay_trans) >= 1: # Eleccion de transicion disponible con menor tiempo de disparo
						delay_trans = min(delay_trans)
						#print(delay_trans)
						for trans in self.sprites_trans:
							if trans.time == delay_trans and self.uk[trans.tag]==1:
								pos_uk.append(trans.tag)
						#print('position:', pos_uk)
						val_fin = random.choice(pos_uk)

					else:
						delay_trans = delay_trans[0]
						val_fin = delay_tags[0]

					for trans in self.sprites_trans:
						if trans.tag == val_fin:
							uk_final[trans.tag] = 1

					self.uk = uk_final

					#print('final_uk:', self.uk)
			except:
				#print('fin')
				delay_trans = 0
				salir_t = 1
				self.marcado_act = self.lista_marcado[0] 
				self.lista_marcado = list()

		return salir_t, delay_trans

	def marcado_p(self):
		#print('off')
		"Evolución del marcado"
		cont = 0
		value_uk = 0
		self.lista_marcado = list()
		self.marcado_act = list()

		while len(self.marcado_act) != len(self.sprites_estados):			
			for estado in self.sprites_estados:
				if estado.tag == len(self.marcado_act):
					self.marcado_act.append(estado.token)

		self.marcado_act = np.asarray(self.marcado_act)
		#print('ori:', self.marcado_act)
		#self.marcado_ini = self.marcado_act
		card_e = len(self.sprites_estados)
		card_t = len(self.sprites_trans)
		if card_e>0 and card_t>0:
			matriz_incid = np.zeros((card_e, card_t))
			self.inc_pos = np.zeros((card_e, card_t))
			self.inc_pre = np.zeros((card_e, card_t))
			self.inc_pre_aux = np.zeros((card_e, card_t))
			#incidencia previa (Estado--> Transición) (-1)
			#incidencia posterior (Transición--> Estado) (+1)
			for con in self.sprites_conexion:
				if con.punto_inicial == 1:
					self.inc_pos[con.interconectados[1], con.interconectados[0]] = con.token
				if con.punto_inicial == -1:
					self.inc_pre[con.interconectados[1], con.interconectados[0]] = con.token
					self.inc_pre_aux[con.interconectados[1], con.interconectados[0]] = 1
			self.inc = self.inc_pos-self.inc_pre
			self.dual = -(np.transpose(self.inc))
			valide_data = np.zeros(self.inc_pre.shape[0]) # Vector que deposita un 1 en caso de que elemento marcado sea mayor que elemento inc_pre
			compare_data = np.ones(self.inc_pre.shape[0]) # Vector de 1's para comparar con valide_data
			self.uk = np.zeros(self.inc_pre.shape[1]) # Vector que indica que trans. están disponibles a disparar
			for i in range(self.inc_pre.shape[1]):
				if np.sum(self.inc_pre[:,i]) > 0: 
					for j in range(self.inc_pre.shape[0]):
						if self.marcado_act[j] >= self.inc_pre[j, i]: # Compara si marcado es mayor que inc_pre
							valide_data[j] = 1 
						else:
							valide_data[j] = 0
					if (valide_data == compare_data).all(): #Compara para verificar si los elementos de marcado cumplen con la incidencia de una transicion
						self.uk[i] = 1
					else:
						self.uk[i] = 0
				else:
					self.uk[i] = 0
			self.uk_pro = self.uk
			#print('ori_uk:', self.uk)
			delay_status = list()
			for status in self.sprites_estados:
				if (self.uk[status.tag]) == 1:
					status.active = True
					delay_status.append(status.time)
				else:
					status.active = False
			#print(delay_trans)
			if len(delay_status) >= 1:
				delay_status = max(delay_status)

			pos_uk = list()
			for n, val in enumerate(self.uk): # Extraer posiciones = 1
			    if val == 1:
			        pos_uk.append(n)
			#print('pos_uk:', pos_uk)
			x = (sorted(self.inc_pre, key=sum, reverse=True))
			x_1 = (sorted(self.inc_pre, key=sum, reverse=True))
			#print(x)
			new_order = list()
			for i, val in enumerate(self.inc_pre): # Evaluar matriz original
			    
			    for j, val_2 in enumerate(x_1):
			        if (val == val_2).all(): # Eliminar elemento de lista copia, la idea es q esta se quede vacia
			            
			            new_order.append(j)
			            #x.pop(j)
			            x_1[j] = [20000]
			            break
			rec_comp = 0
			indice_gru = list() # Contenedor de grupo de indices
			val_prohibi = list() # Contenedor de valores que no pueden ser disparados
			uk_final = self.uk
			if len(pos_uk)>1:
				#print('pos_uk:', pos_uk)
				for i, vec in enumerate(x): # Evaluar si alguno de los recursos compartidos es de interes para el vector de disparo actual
					posi_act = list()
					cont_ind = 0
					for j, ele in enumerate(vec): # Anexar indices de cada fila que sean iguales a 1
						if ele >= 1: # Si se cumple esta condi. se anexa la posicion a un vector que permita compararlo con los indices del vector de trans. habilitadas
							if j in pos_uk:
								cont_ind +=1
					if cont_ind >=2:
						rec_comp = 1
						break

				if rec_comp == 1:
					uk_final = np.zeros([1, len(self.uk)])
					    
					for i, vec in enumerate(x):
					    sum_vec = np.sum(vec)
					    cont = 0
					    indice_ind = list() # Contenedor de indices de cada fila
					    for j, val in enumerate(vec):
					        if j in pos_uk:
					            if val == 1:
					                indice_ind.append(j)
					                cont += 1
					    indice_gru.append(indice_ind)
					    if cont == sum_vec and sum_vec != 0:			        
					        if sum_vec > 1: # Indicar si existe algun recurso compartido
					            #print('Recurso compartido en c'+ str(new_order[i]))
					            val_ran = random.choice(indice_ind)
									            
					            if val_ran in val_prohibi: # Evalua si el valor random se encuentra dentro de los valores prohibidos
					                pass
					            else:
					                uk_final[0, val_ran] = 1
					                for m, val in enumerate(indice_ind):
					                    if val not in val_prohibi:
					                        val_prohibi.append(val)			                
					            
					        else:
					            if indice_ind[0] in val_prohibi:
					                pass
					            else:
					                uk_final[0, indice_ind[0]] = 1
			if rec_comp == 1:
				if len(self.uk)==1:
					pass
				else:
					self.uk = np.squeeze(uk_final)
				#print('uk', self.uk)
			#print('----')
			return delay_status

	def evolucionar_p(self, modo, posi, delay_evo, modo_temp, center_move): # Iniciar marcado en la red 
		if modo == [1, 0]:			
			active_trans = 0
			#print('uk:', self.uk)
			#self.lista_marcado.append(self.marcado_act)
			self.marcado_act = self.marcado_act + np.transpose(np.dot(self.inc, self.uk))
			#print('marcado:', self.marcado_act)
			valide_data = np.zeros(self.inc_pre.shape[0]) # Vector que deposita un 1 en caso de que elemento marcado sea mayor que elemento inc_pre
			compare_data = np.ones(self.inc_pre.shape[0]) # Vector de 1's para comparar con valide_data
			self.uk = np.zeros(self.inc_pre.shape[1]) # Vector que indica que trans. están disponibles a disparar
			for i in range(self.inc_pre.shape[1]):
				if np.sum(self.inc_pre[:,i]) > 0: 
					for j in range(self.inc_pre.shape[0]):
						if (self.marcado_act[j] >= self.inc_pre[j, i]): # Compara si marcado es mayor que inc_pre
							valide_data[j] = 1 
						else:
							valide_data[j] = 0
					if (valide_data == compare_data).all(): #Compara para verificar si los elementos de marcado cumplen con la incidencia de una transicion
						self.uk[i] = 1
					else:
						self.uk[i] = 0
				else:
					self.uk[i] = 0
			#print('uk_old:', self.uk)
			self.uk_pro = self.uk
			for trans in self.sprites_trans:
				if (self.uk[trans.tag]) == 1:
					trans.active = True
				else:
					trans.active = False
			
			pos_uk = list()
			for n, val in enumerate(self.uk): # Extraer posiciones = 1
			    if val == 1:
			        pos_uk.append(n)
			#print('pos_uk:', pos_uk)
			x = (sorted(self.inc_pre, key=sum, reverse=True))
			x_1 = (sorted(self.inc_pre, key=sum, reverse=True))
			
			new_order = list()
			for i, val in enumerate(self.inc_pre): # Evaluar matriz original
			    
			    for j, val_2 in enumerate(x_1):
			        if (val == val_2).all(): # Eliminar elemento de lista copia, la idea es q esta se quede vacia
			            
			            new_order.append(j)
			            #x.pop(j)
			            x_1[j] = [20000]
			            break
			rec_comp = 0
			indice_gru = list() # Contenedor de grupo de indices
			val_prohibi = list() # Contenedor de valores que no pueden ser disparados
			uk_final = self.uk
			if len(pos_uk)>1:
				for i, vec in enumerate(x): # Evaluar si alguno de los recursos compartidos es de interes para el vector de disparo actual
					posi_act = list()
					cont_ind = 0
					for j, ele in enumerate(vec): # Anexar indices de cada fila que sean iguales a 1
						if ele >= 1: # Si se cumple esta condi. se anexa la posicion a un vector que permita compararlo con los indices del vector de trans. habilitadas
							if j in pos_uk:
								cont_ind +=1
					if cont_ind >=2:
						rec_comp = 1
						break

				if rec_comp == 1:
					uk_final = np.zeros([1, len(self.uk)])
					    
					for i, vec in enumerate(x):
					    sum_vec = np.sum(vec)
					    cont = 0
					    indice_ind = list() # Contenedor de indices de cada fila
					    for j, val in enumerate(vec):
					        if j in pos_uk:
					            if val == 1:
					                indice_ind.append(j)
					                cont += 1
					    indice_gru.append(indice_ind)
					    if cont == sum_vec and sum_vec != 0:			        
					        if sum_vec > 1: # Indicar si existe algun recurso compartido
					            #print('Recurso compartido en c'+ str(new_order[i]))
					            val_ran = random.choice(indice_ind)
									            
					            if val_ran in val_prohibi: # Evalua si el valor random se encuentra dentro de los valores prohibidos
					                pass
					            else:
					                uk_final[0, val_ran] = 1
					                for m, val in enumerate(indice_ind):
					                    if val not in val_prohibi:
					                        val_prohibi.append(val)			                
					            
					        else:
					            if indice_ind[0] in val_prohibi:
					                pass
					            else:
					                uk_final[0, indice_ind[0]] = 1
			if rec_comp == 1:
				if len(self.uk)==1:
					pass
				else:
					self.uk = np.squeeze(uk_final)

	def dibujar_matriz(self, pantalla, font, modo_inc, posi, pos): # Enseñar matrices de incidencia
		"Dibuja la matriz de incidencia dentro del area de trabajo"
		keys = pygame.key.get_pressed()
		if keys[K_ESCAPE]:
			self.pasos = [0, 0]
			self.desp = [0, 0]
		card_e = len(self.sprites_estados)
		card_t = len(self.sprites_trans)
		self.card_e = card_e
		self.card_t = card_t
		if card_e>0 and card_t>0:			
			font_2 = pygame.font.SysFont('Arial', 15)	
			MARGEN = 1
			LARGO = 25
			ALTO = 25
			rojo = pygame.image.load(os.path.join('Pictures', 'blue.png'))	
			matrix_check_off = pygame.image.load(os.path.join('Pictures', 'check_off.png'))
			matrix_check_on = pygame.image.load(os.path.join('Pictures', 'check_on.png'))	
			label = pygame.image.load(os.path.join('Pictures', 'label.png'))	
			matrix_rect = matrix_check_on.get_rect()
			matrix_rect.center = (505, 240)
			rect_inc = matrix_check_on.get_rect()
			rect_inc.center = (265, 75)
			rect_inc_pos = matrix_check_on.get_rect()
			rect_inc_pos.center = (356, 75)
			rect_inc_pre = matrix_check_on.get_rect()
			rect_inc_pre.center = (447, 75)
			rect_dual = matrix_check_on.get_rect()
			rect_dual.center = (503, 75)
			center_bar = [517.5, 327.5] 
			matriz_incid = np.zeros((card_t, card_e))
			inc_pos = np.zeros((card_e, card_t))
			inc_pre = np.zeros((card_e, card_t))
			no_pureza = False
			tag_estado = card_e
			tag_trans = card_t
			#incidencia previa (Estado--> Transición) (-1)
			#incidencia posterior (Transición--> Estado) (+1)			
			panel_matriz = pygame.image.load(os.path.join('Pictures', 'matrix.png'))
			self.panel.fill(BLANCO)			
			self.panel.blit(panel_matriz, (0, 0))
			
			num_e = 0
			num_t =0
			
			# Adicion de etiquetas
			self.panel.blit(rojo, (50, 520))
			self.panel.blit(font.render('Elementos adicionados para corrección de no pureza', True, (255, 255, 255)), (80, 522))
			self.panel.blit(font.render('Incidencia', True, (255, 255, 255)), (10, 5))
			self.panel.blit(font.render('Incidencia +', True, (255, 255, 255)), (92, 5))			
			self.panel.blit(font.render('Incidencia -', True, (255, 255, 255)), (183, 5))
			self.panel.blit(font.render('Dual', True, (255, 255, 255)), (275, 5))
			#print(self.sprites_conexion)
			for con in self.sprites_conexion_full:
				if con.punto_inicial == 1:
					inc_pos[con.interconectados[1], con.interconectados[0]] = con.token
				if con.punto_inicial == -1:
					inc_pre[con.interconectados[1], con.interconectados[0]] = con.token
			self.inc_pro = inc_pos-inc_pre


			for i, _ in enumerate(range(self.inc_pre.shape[0])):
				for j, _ in enumerate(range(self.inc_pre.shape[1])):
					# Detectar que conexiones son causantes de no pureza
					if (self.inc_pre[i, j] == self.inc_pos[i, j]) and (self.inc_pre[i, j] != 0):
						no_pureza = True
						self.card_e += 1
						self.card_t += 1
						inc_ceros = np.zeros([self.inc_pro.shape[0]+1, self.inc_pro.shape[1]+1])
						for a, _ in enumerate(range(self.inc_pro.shape[0])):
							for b, _ in enumerate(range(self.inc_pro.shape[1])):
								inc_ceros[a, b] = self.inc_pro[a, b]
						inc_ceros[i, j] = 1
						inc_ceros[self.card_e-1, self.card_t-1] = 1
						inc_ceros[self.card_e-1, j] = -1
						inc_ceros[i, self.card_t-1] = -1 
						self.inc_pro = inc_ceros

			inc_pre_ceros = np.zeros([self.inc_pro.shape[0], self.inc_pro.shape[1]])
			inc_pos_ceros = np.zeros([self.inc_pro.shape[0], self.inc_pro.shape[1]])
			for i, _ in enumerate(range(inc_pre_ceros.shape[0])):
				for j, _ in enumerate(range(inc_pre_ceros.shape[1])):
					if self.inc_pro[i, j] > 0:
						inc_pos_ceros[i, j] = self.inc_pro[i, j]
					elif self.inc_pro[i, j] < 0:
						inc_pre_ceros[i, j] = abs(self.inc_pro[i, j])
			inc = self.inc_pro
			dual = -(np.transpose(self.inc_pro))
			inc_pos = inc_pos_ceros
			inc_pre = inc_pre_ceros
			if self.card_e>16: # Crear variable que indique el tamaño del scroll para estados
				num_e = self.card_e - 16

			if self.card_t>16:
				num_t = self.card_t - 16

			size_sheet = [num_t, num_e] # Tamaño de la "hoja"
			if modo_inc == [0, 0, 0, 1]:
				label = pygame.image.load(os.path.join('Pictures', 'label2.png'))
				size_sheet = [num_e, num_t] # Tamaño de la "hoja"
				i = 0
				for estado in range(self.card_e-num_e): # Visualizar etiquetas trans	
					texto = "P"+str(estado+self.pasos[0])
					self.panel.blit(font_2.render(texto, True, (255, 0, 0)), ((MARGEN + LARGO) * estado + MARGEN + 116, 55))

				i = 0
				for trans in range(self.card_t-num_t): # Visualizar etiquetas estados	
					texto = "T"+str(trans+self.pasos[1])
					self.panel.blit(font_2.render(texto, True, (255, 0, 0)), (86, (MARGEN + ALTO) * trans + MARGEN + 77))
			else:
				i = 0
				for trans in range(self.card_t-num_t): # Visualizar etiquetas trans	
					texto = "T"+str(trans+self.pasos[0])
					self.panel.blit(font_2.render(texto, True, (255, 0, 0)), ((MARGEN + LARGO) * trans + MARGEN + 116, 55))

				i = 0
				for estado in range(self.card_e-num_e): # Visualizar etiquetas estados	
					texto = "P"+str(estado+self.pasos[1])
					self.panel.blit(font_2.render(texto, True, (255, 0, 0)), (86, (MARGEN + ALTO) * estado + MARGEN + 77))
			self.panel.blit(label,(30,30))
			if rect_dual.collidepoint(pos) and rect_dual.collidepoint(posi):
				self.pasos = [0, 0]
				self.desp = [0, 0]

			if rect_inc.collidepoint(pos) and rect_inc.collidepoint(posi):
				self.pasos = [0, 0]
				self.desp = [0, 0]

			if rect_inc_pos.collidepoint(pos) and rect_inc_pos.collidepoint(posi):
				self.pasos = [0, 0]
				self.desp = [0, 0]

			if rect_inc_pre.collidepoint(pos) and rect_inc_pre.collidepoint(posi):
				self.pasos = [0, 0]
				self.desp = [0, 0]
			if self.card_e>16 or self.card_t>16: # Scroll para transiciones		
				if pygame.mouse.get_pressed()[0]:		
					barra_actual, size_sheet, self.desp, self.pasos = self.proper_draw.acciones_barra_mat(posi, self.desp, self.pasos, size_sheet, self.barra_actual, center_bar)
				self.proper_draw.dibujar_barra(self.panel, self.desp)
			if rect_inc.collidepoint(posi) or modo_inc == [1, 0, 0, 0]:
				self.panel.blit(matrix_check_on, (67, 5))				
				self.panel.blit(matrix_check_off, (158, 5))
				self.panel.blit(matrix_check_off, (249, 5))
				self.panel.blit(matrix_check_off, (305, 5))
				modo_inc = [1, 0, 0, 0]
				for fila in range(self.card_e-num_e):
					fila += self.pasos[1]
					for columna in range(self.card_t-num_t):
						columna += self.pasos[0]
						color = BLANCO
						if not columna > card_t-1:
							imagen = pygame.image.load(os.path.join('Pictures', 'empty.png'))
							if fila > card_e-1:
								imagen = pygame.image.load(os.path.join('Pictures', 'pura.png'))
						else:
							imagen = pygame.image.load(os.path.join('Pictures', 'pura.png'))							
						texto = '0'
						
						if inc[fila][columna] == 1:
							texto = '1'
						if inc[fila][columna] == -1:
							texto = '-1'
						if inc[fila][columna] == 2:
							texto = '2'
						if inc[fila][columna] == -2:
							texto = '-2'
						if inc[fila][columna] == 3:
							texto = '3'
						if inc[fila][columna] == -3:
							texto = '-3'
						if inc[fila][columna] == 4:
							texto = '4'
						if inc[fila][columna] == -4:
							texto = '-4'
						if inc[fila][columna] == 5:
							texto = '5'
						if inc[fila][columna] == -5:
							texto = '-5'
						if inc[fila][columna] == 6:
							texto = '6'
						if inc[fila][columna] == -6:
							texto = '-6'
						if inc[fila][columna] == 7:
							texto = '7'
						if inc[fila][columna] == -7:
							texto = '-7'
						if inc[fila][columna] == 8:
							texto = '8'
						if inc[fila][columna] == -8:
							texto = '-8'
						if inc[fila][columna] == 9:
							texto = '9'
						if inc[fila][columna] == -9:
							texto = '-9'
						if inc[fila][columna] > 9:
							texto = '+9'
						cuadro = pygame.draw.rect(self.panel, color, 
							[(MARGEN + LARGO) * (columna-self.pasos[0]) + MARGEN + 110, 
							(MARGEN + ALTO) * (fila-self.pasos[1]) + MARGEN + 75, LARGO, ALTO])						
						self.panel.blit(imagen, cuadro)						
						self.panel.blit(font_2.render(texto, True, (0, 0, 0)), ((MARGEN + LARGO) * (columna-self.pasos[0]) + MARGEN + 118, 
							(MARGEN + ALTO) * (fila-self.pasos[1]) + MARGEN + 78))

				#panel.blit(font.render('Matriz Incidencia', True, (255, 250, 250)), (15, 10))

			if rect_inc_pos.collidepoint(posi) or modo_inc == [0, 1, 0, 0]:
				self.panel.blit(matrix_check_off, (67, 5))				
				self.panel.blit(matrix_check_on, (158, 5))
				self.panel.blit(matrix_check_off, (249, 5))
				self.panel.blit(matrix_check_off, (305, 5))
				modo_inc = [0, 1, 0, 0]

				for fila in range(self.card_e-num_e):
					fila += self.pasos[1]
					for columna in range(self.card_t-num_t):
						columna += self.pasos[0]
						color = BLANCO
						if not columna > card_t-1:
							imagen = pygame.image.load(os.path.join('Pictures', 'empty.png'))
							if fila > card_e-1:
								imagen = pygame.image.load(os.path.join('Pictures', 'pura.png'))
						else:
							imagen = pygame.image.load(os.path.join('Pictures', 'pura.png'))
						inc_pos[fila][columna]
						texto = '0'
						#imagen = pygame.image.load(os.path.join('Pictures', 'empty.png'))
						if inc_pos[fila][columna] == 1:
							texto = '1'
						if inc_pos[fila][columna] == 2:
							texto = '2'
						if inc_pos[fila][columna] == 3:
							texto = '3'
						if inc_pos[fila][columna] == 4:
							texto = '4'
						if inc_pos[fila][columna] == 5:
							texto = '5'
						if inc_pos[fila][columna] == 6:
							texto = '6'
						if inc_pos[fila][columna] == 7:
							texto = '7'
						if inc_pos[fila][columna] == 8:
							texto = '8'
						if inc_pos[fila][columna] == 9:
							texto = '9'
						if inc_pos[fila][columna] > 9:
							texto = '+9'	
						cuadro = pygame.draw.rect(self.panel, color, 
							[(MARGEN + LARGO) * (columna-self.pasos[0]) + MARGEN + 110, 
							(MARGEN + ALTO) * (fila-self.pasos[1]) + MARGEN + 75, LARGO, ALTO])
						self.panel.blit(imagen, cuadro)
						self.panel.blit(font_2.render(texto, True, (0, 0, 0)), ((MARGEN + LARGO) * (columna-self.pasos[0]) + MARGEN + 118, 
							(MARGEN + ALTO) * (fila-self.pasos[1]) + MARGEN + 78))

				#panel.blit(font.render('Matriz Incidencia posterior', True, (255, 250, 250)), (15, 10))

			if rect_inc_pre.collidepoint(posi) or modo_inc == [0, 0, 1, 0]:
				self.panel.blit(matrix_check_off, (67, 5))				
				self.panel.blit(matrix_check_off, (158, 5))
				self.panel.blit(matrix_check_on, (249, 5))
				self.panel.blit(matrix_check_off, (305, 5))
				modo_inc = [0, 0, 1, 0]
				for fila in range(self.card_e-num_e):
					fila += self.pasos[1]
					for columna in range(self.card_t-num_t):
						columna += self.pasos[0]
						color = BLANCO
						if not columna > card_t-1:
							imagen = pygame.image.load(os.path.join('Pictures', 'empty.png'))
							if fila > card_e-1:
								imagen = pygame.image.load(os.path.join('Pictures', 'pura.png'))
						else:
							imagen = pygame.image.load(os.path.join('Pictures', 'pura.png'))
						#imagen = pygame.image.load(os.path.join('Pictures', 'empty.png'))
						texto = '0'	
						if inc_pre[fila][columna] == 1:
							texto = '1'	
						if inc_pre[fila][columna] == 2:
							texto = '2'	
						if inc_pre[fila][columna] == 3:
							texto = '3'	
						if inc_pre[fila][columna] == 4:
							texto = '4'	
						if inc_pre[fila][columna] == 5:
							texto = '5'	
						if inc_pre[fila][columna] == 6:
							texto = '6'	
						if inc_pre[fila][columna] == 7:
							texto = '7'	
						if inc_pre[fila][columna] == 8:
							texto = '8'	
						if inc_pre[fila][columna] == 9:
							texto = '9'	
						if inc_pos[fila][columna] > 9:
							texto = '+9'
						cuadro = pygame.draw.rect(self.panel, color, 
							[(MARGEN + LARGO) * (columna-self.pasos[0]) + MARGEN + 110, 
							(MARGEN + ALTO) * (fila-self.pasos[1]) + MARGEN + 75, LARGO, ALTO])
						self.panel.blit(imagen, cuadro)
						self.panel.blit(font_2.render(texto, True, (0, 0, 0)), ((MARGEN + LARGO) * (columna-self.pasos[0]) + MARGEN + 118, 
							(MARGEN + ALTO) * (fila-self.pasos[1]) + MARGEN + 78))

			if rect_dual.collidepoint(posi) or modo_inc == [0, 0, 0, 1]:
				self.panel.blit(matrix_check_off, (67, 5))				
				self.panel.blit(matrix_check_off, (158, 5))
				self.panel.blit(matrix_check_off, (249, 5))
				self.panel.blit(matrix_check_on, (305, 5))
				modo_inc = [0, 0, 0, 1]
				for fila in range(self.card_t-num_t):
					fila += self.pasos[1]
					for columna in range(self.card_e-num_e):
						columna += self.pasos[0]
						color = BLANCO
						if not columna > card_e-1:
							imagen = pygame.image.load(os.path.join('Pictures', 'empty.png'))
							if fila > card_t-1:
								imagen = pygame.image.load(os.path.join('Pictures', 'pura.png'))
						else:
							imagen = pygame.image.load(os.path.join('Pictures', 'pura.png'))
						#imagen = pygame.image.load(os.path.join('Pictures', 'empty.png'))
						texto = '0'
						
						if dual[fila][columna] == 1:
							texto = '1'
						if dual[fila][columna] == -1:
							texto = '-1'
						if dual[fila][columna] == 2:
							texto = '2'
						if dual[fila][columna] == -2:
							texto = '-2'
						if dual[fila][columna] == 3:
							texto = '3'
						if dual[fila][columna] == -3:
							texto = '-3'
						if dual[fila][columna] == 4:
							texto = '4'
						if dual[fila][columna] == -4:
							texto = '-4'
						if dual[fila][columna] == 5:
							texto = '5'
						if dual[fila][columna] == -5:
							texto = '-5'
						if dual[fila][columna] == 6:
							texto = '6'
						if dual[fila][columna] == -6:
							texto = '-6'
						if dual[fila][columna] == 7:
							texto = '7'
						if dual[fila][columna] == -7:
							texto = '-7'
						if dual[fila][columna] == 8:
							texto = '8'
						if dual[fila][columna] == -8:
							texto = '-8'
						if dual[fila][columna] == 9:
							texto = '9'
						if dual[fila][columna] == -9:
							texto = '-9'
						if dual[fila][columna] > 9:
							texto = '+9'
						cuadro = pygame.draw.rect(self.panel, color, 
							[(MARGEN + LARGO) * (columna-self.pasos[0]) + MARGEN + 110, 
							(MARGEN + ALTO) * (fila-self.pasos[1]) + MARGEN + 75, LARGO, ALTO])						
						self.panel.blit(imagen, cuadro)						
						self.panel.blit(font_2.render(texto, True, (0, 0, 0)), ((MARGEN + LARGO) * (columna-self.pasos[0]) + MARGEN + 118, 
							(MARGEN + ALTO) * (fila-self.pasos[1]) + MARGEN + 78))

			pantalla.blit(self.panel, (190, 60))
			if modo_inc == None:
				modo_inc = [1, 0, 0, 0]
			return modo_inc

	def properties(self, pantalla, font, pos, posi, block_proper, general, no_viva, no_pureza, limit):
		"""Evaluar propiedades de la red dibujada"""

		card_e = len(self.sprites_estados)
		card_t = len(self.sprites_trans)
		card_c = len(self.sprites_conexion)
		if card_e>0 and card_t>0 and card_c>0:		
			panel = pygame.Surface((300, 300))
			panel_matriz = pygame.image.load(os.path.join('Pictures', 'matrix.png'))
			panel.fill(BLANCO)
			panel.blit(panel_matriz, (0, 0))
			panel.blit(font.render('Propiedades', True, (255, 250, 250)), (15, 10))		
			
			# Reversibilidad
			# Viveza
			# Pureza
			# General - Ordinara

			if block_proper == 0:
				no_viva = 0
				no_pureza = 0
				general = 0
				limit = 0			

				for i, _ in enumerate(range(50)):
					self.marcado_montecarlo() # Iera sobre el modelo a evolucionar= 1

					# Red Viva
					if i == 0:
						pass
					else:
						if (self.marcado_act == self.lista_marcado[i-1]).all():
							no_viva = 1
					# Red limitada		
					if i > 20:
						for k, _ in enumerate(range(self.inc_pre.shape[0])):
							for l, _ in enumerate(range(self.inc_pre.shape[1])):	
								#print(i, k, l)	
								#print(self.marcado_act[l])
								#print(self.inc_pre[k, l])	
								if (self.marcado_act[k] > self.inc_pre[k, l]*3) and self.marcado_act[k] != 0:
									#print(self.marcado_act)
									#print(self.inc_pre[k])
									#print(k, l)
									#print('in')
									limit = 1

					if i == 49:					
						block_proper = 1				

				# Pureza
				for i, _ in enumerate(range(self.inc_pre.shape[0])):
					for j, _ in enumerate(range(self.inc_pre.shape[1])):
						# Ordinaria
						if self.inc_pre[i, j] >= 2 or self.inc_pre[i, j] >= 2:
							general = 1
						# Pureza	
						if (self.inc_pre[i, j] == self.inc_pos[i, j]) and (self.inc_pre[i, j] != 0):
							no_pureza = 1
				
			mat_inc = Matrix(self.inc)
			if not mat_inc.nullspace():	
				panel.blit(font.render('Red de Petri No Reversible', True, (255, 250, 250)), (25, 80))	
			else:
				panel.blit(font.render('Red de Petri Reversible', True, (255, 250, 250)), (25, 80))

			if general == 0:
				panel.blit(font.render('Red de Petri Ordinaria', True, (255, 250, 250)), (25, 50))	
			else:
				panel.blit(font.render('Red de Petri Generalizada', True, (255, 250, 250)), (25, 50))	

			if no_viva == 0:
				panel.blit(font.render('Red de Petri Viva', True, (255, 250, 250)), (25, 110))	
			else:
				panel.blit(font.render('Red de Petri No Viva', True, (255, 250, 250)), (25, 110))	

			if no_pureza == 0:
				panel.blit(font.render('Red de Petri Pura', True, (255, 250, 250)), (25, 140))	
			else:
				panel.blit(font.render('Red de Petri No Pura', True, (255, 250, 250)), (25, 140))

			if limit == 0:
				panel.blit(font.render('Red Limitada', True, (255, 250, 250)), (25, 170))	
			else:
				panel.blit(font.render('Red No Limitada', True, (255, 250, 250)), (25, 170))

			panel.blit(font.render('Red Conservativa', True, (255, 250, 250)), (25, 200))

			
		else:
			panel = pygame.Surface((300, 300))
			panel_matriz = pygame.image.load(os.path.join('Pictures', 'matrix.png'))
			panel.fill(BLANCO)
			panel.blit(panel_matriz, (0, 0))
			panel.blit(font.render('Propiedades', True, (255, 250, 250)), (15, 10))		
			panel.blit(font.render('Debe existir por lo menos una conexión', True, (255, 250, 250)), (25, 80))

		pantalla.blit(panel, (320, 130))
		return block_proper, general, no_viva, no_pureza, limit

	def marcado_montecarlo(self):
		active_trans = 0		
		self.marcado_act = self.marcado_act + np.transpose(np.dot(self.inc, self.uk))
		self.lista_marcado.append(self.marcado_act)
		valide_data = np.zeros(self.inc_pre.shape[0]) # Vector que deposita un 1 en caso de que elemento marcado sea mayor que elemento inc_pre
		compare_data = np.ones(self.inc_pre.shape[0]) # Vector de 1's para comparar con valide_data
		self.uk = np.zeros(self.inc_pre.shape[1]) # Vector que indica que trans. están disponibles a disparar
		for i in range(self.inc_pre.shape[1]):
			if np.sum(self.inc_pre[:,i]) > 0: 
				for j in range(self.inc_pre.shape[0]):
					if self.marcado_act[j] >= self.inc_pre[j, i]: # Compara si marcado es mayor que inc_pre
						valide_data[j] = 1 
					else:
						valide_data[j] = 0
				if (valide_data == compare_data).all(): #Compara para verificar si los elementos de marcado cumplen con la incidencia de una transicion
					self.uk[i] = 1
				else:
					self.uk[i] = 0
			else:
				self.uk[i] = 0
		
		self.uk_pro = self.uk
		delay_trans = list()
		for trans in self.sprites_trans:
			if (self.uk[trans.tag]) == 1:
				trans.active = True
				delay_trans.append(trans.time)
			else:
				trans.active = False

		if len(delay_trans) >= 1: # Eleccion de transicion disponible con menor tiempo de disparo
			delay_trans = min(delay_trans)
		
		pos_uk = list()
		for n, val in enumerate(self.uk): # Extraer posiciones = 1
		    if val == 1:
		        pos_uk.append(n)
    
		x = (sorted(self.inc_pre, key=sum, reverse=True))
		x_1 = (sorted(self.inc_pre, key=sum, reverse=True))
		
		new_order = list()
		for i, val in enumerate(self.inc_pre): # Evaluar matriz original
		    
		    for j, val_2 in enumerate(x_1):
		        if (val == val_2).all(): # Eliminar elemento de lista copia, la idea es q esta se quede vacia
		            
		            new_order.append(j)
		            #x.pop(j)
		            x_1[j] = [20000]
		            break

		indice_gru = list() # Contenedor de grupo de indices
		val_prohibi = list() # Contenedor de valores que no pueden ser disparados
		uk_final = np.zeros([1, len(self.uk)])
		    
		for i, vec in enumerate(x):
		    sum_vec = np.sum(vec)
		    cont = 0
		    indice_ind = list() # Contenedor de indices de cada fila
		    for j, val in enumerate(vec):
		        if j in pos_uk:
		            if val == 1:
		                indice_ind.append(j)
		                cont += 1
		    indice_gru.append(indice_ind)
		    if cont == sum_vec and sum_vec != 0:			        
		        if sum_vec > 1: # Indicar si existe algun recurso compartido
		            #print('Recurso compartido en c'+ str(new_order[i]))
		            val_ran = random.choice(indice_ind)
		            
		            if val_ran in val_prohibi: # Evalua si el valor random se encuentra dentro de los valores prohibidos
		                pass
		            else:
		                uk_final[0, val_ran] = 1
		                for m, val in enumerate(indice_ind):
		                    if val not in val_prohibi:
		                        val_prohibi.append(val)			                
		            
		        else:
		            if indice_ind[0] in val_prohibi:
		                pass
		            else:
		                uk_final[0, indice_ind[0]] = 1
		#print('final:', uk_final)
		self.uk = np.squeeze(uk_final)

	def transform(self, pantalla, font):
		font_2 = pygame.font.SysFont('Arial', 15)	
		MARGEN = 1
		LARGO = 25
		ALTO = 25
		panel = pygame.Surface((440, 440))
		panel_matriz = pygame.image.load(os.path.join('Pictures', 'matrix.png'))
		panel.fill(BLANCO)
		panel.blit(panel_matriz, (0, 0))
		panel.blit(font.render('Transformaciones', True, (255, 250, 250)), (15, 10))
		panel.blit(font.render('Anulador derecho:', True, (255, 255, 255)), (10, 50))
		panel.blit(font.render('Anulador izquierdo:', True, (255, 255, 255)), (10, 117))
		card_e = len(self.sprites_estados)
		card_t = len(self.sprites_trans)
		#C = np.asarray([[-2,0,0,0,1],[1,-1,0,0,0],[1,0,-1,0,0],[0,1,0,-1,0],[0,0,1,-1,0],[0,0,0,2,-1]])
		print('----')
		#print(C)
		#print(self.inc)
		mat_inc = Matrix(self.inc)
		#print(mat_inc)
		if not mat_inc.nullspace():			
			panel.blit(font.render('- No existe anulador derecho', True, (255, 255, 255)), (20, 80))
			panel.blit(font.render('- No existe anulador izquierdo', True, (255, 255, 255)), (20, 150))
			#pantalla.blit(panel, (320, 130))
		else:
			#print(mat_inc.nullspace())
			objetive = mat_inc.nullspace()
			#print(len(objetive))
			objetivex = np.squeeze(mat_inc.nullspace())
			if len(objetive) > 1:
				#print(objetive)
				for i, obj in enumerate(objetivex):
					#print(obj)
					x = obj[obj <0]
					if len(x) == 0:
						break
			else:
				obj = objetivex
			#print(obj)
			mat_inc_null = obj
			#mat_inc_null= np.squeeze(np.asarray(mat_inc_null))
			#print(mat_inc_null)
			dim_mat = np.size(self.inc[0])
			vec_anu = np.zeros([dim_mat, 1])
			min_mat = np.min(mat_inc_null[np.nonzero(mat_inc_null)])
			#print(min_mat)
			for i, _ in enumerate(range(dim_mat)):
				vec_anu[i, 0] = mat_inc_null[i]/min_mat

			#print(vec_anu)
				
			for fila in range(card_t):
				#fila += self.pasos[1]
				color = BLANCO
				imagen = pygame.image.load(os.path.join('Pictures', 'empty.png'))
				texto = '0'
				
				if vec_anu[fila] == 1:
					texto = '1'
				if vec_anu[fila] == -1:
					texto = '-1'
				if vec_anu[fila] == 2:
					texto = '2'
				if vec_anu[fila] == -2:
					texto = '-2'
				if vec_anu[fila] == 3:
					texto = '3'
				if vec_anu[fila] == -3:
					texto = '-3'
				if vec_anu[fila] == 4:
					texto = '4'
				if vec_anu[fila] == -4:
					texto = '-4'
				if vec_anu[fila] == 5:
					texto = '5'
				if vec_anu[fila] == -5:
					texto = '-5'
				if vec_anu[fila] == 6:
					texto = '6'
				if vec_anu[fila] == -6:
					texto = '-6'
				if vec_anu[fila] == 7:
					texto = '7'
				if vec_anu[fila] == -7:
					texto = '-7'
				if vec_anu[fila] == 8:
					texto = '8'
				if vec_anu[fila] == -8:
					texto = '-8'
				if vec_anu[fila] == 9:
					texto = '9'
				if vec_anu[fila] == -9:
					texto = '-9'
				if vec_anu[fila] > 9:
					texto = '+9'
				cuadro = pygame.draw.rect(panel, color, 
					[(MARGEN + LARGO) * (fila) + MARGEN + 50, 
					(MARGEN + ALTO) * (0) + MARGEN + 75, LARGO, ALTO])						
				panel.blit(imagen, cuadro)						
				panel.blit(font_2.render(texto, True, (0, 0, 0)), ((MARGEN + LARGO) * (fila) + MARGEN + 58, 
					(MARGEN + ALTO) * (0) + MARGEN + 78))
			#pantalla.blit(panel, (320, 130))

			try:
				#print('anu:', vec_anu)
				izq_an = np.dot(np.transpose(vec_anu), self.dual)
				#print(izq_an)
				size_izq = np.size(izq_an)
				#print(size_izq)
				if size_izq > 1:
					#print('hola')
					izq_an = np.squeeze(izq_an)
					if (izq_an == np.zeros(size_izq)).all():
						izq_an = np.ones(size_izq)
				#print(izq_an)
				anu = izq_an
				for fila in range(card_e):
					color = BLANCO
					imagen = pygame.image.load(os.path.join('Pictures', 'empty.png'))
					texto = '0'
					
					if anu[fila] == 1:
						texto = '1'
					if anu[fila] == -1:
						texto = '-1'
					if anu[fila] == 2:
						texto = '2'
					if anu[fila] == -2:
						texto = '-2'
					if anu[fila] == 3:
						texto = '3'
					if anu[fila] == -3:
						texto = '-3'
					if anu[fila] == 4:
						texto = '4'
					if anu[fila] == -4:
						texto = '-4'
					if anu[fila] == 5:
						texto = '5'
					if anu[fila] == -5:
						texto = '-5'
					if anu[fila] == 6:
						texto = '6'
					if anu[fila] == -6:
						texto = '-6'
					if anu[fila] == 7:
						texto = '7'
					if anu[fila] == -7:
						texto = '-7'
					if anu[fila] == 8:
						texto = '8'
					if anu[fila] == -8:
						texto = '-8'
					if anu[fila] == 9:
						texto = '9'
					if anu[fila] == -9:
						texto = '-9'
					if anu[fila] > 9:
						texto = '+9'
					cuadro = pygame.draw.rect(panel, color, 
						[(MARGEN + LARGO) * (fila) + MARGEN + 50, 
						(MARGEN + ALTO) * (0) + MARGEN + 140, LARGO, ALTO])						
					panel.blit(imagen, cuadro)						
					panel.blit(font_2.render(texto, True, (0, 0, 0)), ((MARGEN + LARGO) * (fila) + MARGEN + 58, 
						(MARGEN + ALTO) * (0) + MARGEN + 143))
				
				#print(np.dot(np.array([1, 1, 1, 1, 1, 1]), self.inc))
				#empty_izq = np.zeros([size_izq, 1])
				#print_(empty_izq)
				"""xc = np.dot(self.dual, vec_anu)
				for fila in range(card_t):
					#fila += self.pasos[1]
					color = BLANCO
					imagen = pygame.image.load(os.path.join('Pictures', 'empty.png'))
					texto = '0'
					panel.blit(font.render('Anulador izquierdo:', True, (255, 255, 255)), (10, 120))
					
					if vec_anu[fila] == 1:
						texto = '1'
					if vec_anu[fila] == -1:
						texto = '-1'
					if vec_anu[fila] == 2:
						texto = '2'
					if vec_anu[fila] == -2:
						texto = '-2'
					if vec_anu[fila] == 3:
						texto = '3'
					if vec_anu[fila] == -3:
						texto = '-3'
					if vec_anu[fila] == 4:
						texto = '4'
					if vec_anu[fila] == -4:
						texto = '-4'
					if vec_anu[fila] == 5:
						texto = '5'
					if vec_anu[fila] == -5:
						texto = '-5'
					if vec_anu[fila] == 6:
						texto = '6'
					if vec_anu[fila] == -6:
						texto = '-6'
					if vec_anu[fila] == 7:
						texto = '7'
					if vec_anu[fila] == -7:
						texto = '-7'
					if vec_anu[fila] == 8:
						texto = '8'
					if vec_anu[fila] == -8:
						texto = '-8'
					if vec_anu[fila] == 9:
						texto = '9'
					if vec_anu[fila] == -9:
						texto = '-9'
					if vec_anu[fila] > 9:
						texto = '+9'
					cuadro = pygame.draw.rect(pantalla, color, 
						[(MARGEN + LARGO) * (fila) + MARGEN + 50, 
						(MARGEN + ALTO) * (0) + MARGEN + 140, LARGO, ALTO])						
					panel.blit(imagen, cuadro)						
					panel.blit(font_2.render(texto, True, (0, 0, 0)), ((MARGEN + LARGO) * (fila) + MARGEN + 58, 
						(MARGEN + ALTO) * (0) + MARGEN + 144))
				pantalla.blit(panel, (320, 130))"""
			except:
				panel.blit(font.render('- No existe anulador izquierdo', True, (255, 255, 255)), (20, 150))

		pantalla.blit(panel, (320, 150))

