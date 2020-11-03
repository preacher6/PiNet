 #!/usr/bin/python env

import pygame
import numpy as np
import sys
import os
import math
import webbrowser
import easygui as eg 
from pygame.locals import *
from usuario import Items
from propiedades import Propiedades
from textbox import TextBox

#COLORES
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = ( 0, 255, 0)
estado = None
conector = None
modo = [1, 0] #0 Automatico, 1. Manual
modo_temp = [1, 0, 0] #0 No temp, 1 T-Temp, 2 P-Temp 
KEY_REPEAT_SETTING = (200, 70)

def valor_tu(id, valor):
	global valor_1
	valor_1 = valor

def valor_td(id, valor):
	global valor_2
	valor_2 = valor

def main():
	global valor_1
	global valor_2
	global marcado_ini
	global salir_t
	marcado_ini = None
	pygame.init() # Inicializa modulo pygame
	os.environ['SDL_VIDEO_CENTERED'] = '1' # Centra la interfaz
	DIMENSION_VENTANA = [900, 700] # Dimensiones de la interfaz
	pantalla = pygame.display.set_mode(DIMENSION_VENTANA) # Define la pantalla
	pygame.display.set_caption("PiNet") 
	logo = pygame.image.load(os.path.join('Pictures', 'logo_u.png')) # Carga logo utp
	reloj = pygame.time.Clock() # Define la velocidad en que se refresca la pantalla
	ico = pygame.image.load('icono.png')
	pygame.display.set_icon(ico)
	font_1 = pygame.font.SysFont('Arial', 15)
	font_2 = pygame.font.SysFont('Arial', 26)	
	erase = pygame.Surface((1000, 1000))
	erase.fill((255, 255, 255))
	font = pygame.font.SysFont('Arial', 15)
	cont_time = 0
	modo = [1, 0]
	modo_temp = [1, 0, 0] 
	modo_inc = [1, 0, 0, 0]
	vel = 3
	rever = 0
	no_viva = 0
	no_pureza = 0
	general = 0
	limit = 0
	push = False
	bloqueo_general = False # Permite que tooltip de conexiones domine los demás
	dibujar_conex = False
	delay_evo = 1000
	close = False
	push_manual = False
	estados_dibujados = 0
	total_estados = 0
	marcado_global = np.arange(1)
	dentro = 0
	block_proper = 0
	block_mar = False
	size_sheet = 0 # Tamaño de la hoja de trabajo
	barra_actual = [625, 505]
	center_bar = [517.5, 327.5] 
	push_coli = [False, False, False] # Vector de colisiones entre propiedades
	desp = [0, 0] # X, Y # Desplazamiento del scrolling reflejado sobre la superficie
	pasos = [0, 0] # X, Y # Desplazamiento en scrolling
	center_move = (0, 0)
	posi = (0, 0)
	cont_frame = 0
	hold_play = 0; hold_erase = 0; hold_set = 0; hold_help = 0
	hold_change = 0; hold_proper = 0; hold_trans = 0
	hold_save = 0; hold_load = 0
	propiedades = Propiedades(pantalla)
	usuario = Items() # Crea objeto de la clase Items
	text_u = TextBox((470,290,80,20), command=valor_tu, clear_on_enter=True, inactive_on_enter=False)
	text_d = TextBox((470,330,80,20), command=valor_td, clear_on_enter=True, inactive_on_enter=False)
	valor_1 = None
	valor_2 = None
	play_e, play_f, pause_e, pause_f, play_pos = propiedades.cargar_play(pantalla)
	set_e, set_f, set_pos = propiedades.cargar_set(pantalla)
	erase_e, erase_f, erase_pos = propiedades.cargar_erase(pantalla)
	help_e, help_f, help_pos = propiedades.cargar_help(pantalla)
	matrix_e, matrix_f, change_pos = propiedades.show_structure(pantalla)
	proper_e, proper_f, proper_pos = propiedades.show_proper(pantalla)
	trans_e, trans_f, trans_pos = propiedades.show_trans(pantalla)
	load_f, load_e, save_f, save_e, load_pos, save_pos = propiedades.save_load(pantalla)
	erase_all = False # Reiniciar área de trabajo
	salir_t = 0

	while not close: # Loop
		try:
			keys = pygame.key.get_pressed() # Obtencion de tecla presionada
			for evento in pygame.event.get():	
				text_u.get_event(evento)
				text_d.get_event(evento)
				if evento.type == pygame.QUIT:
					close = eg.ynbox(msg='¿Desea salir de PiNet?',
						title='Salir',
						choices=('Si', 'No'),
						image=None)
				elif evento.type == pygame.MOUSEBUTTONDOWN or keys[K_ESCAPE]:
					push_manual = True
					posi = pygame.mouse.get_pos()
					barra_actual, size_sheet, desp, pasos = propiedades.acciones_barra(posi, desp, pasos, size_sheet, barra_actual, center_bar)
					if propiedades.rectangulo_trabajo.collidepoint(pygame.mouse.get_pos()):
						dentro = 1
					else:
						dentro = 0

					if keys[K_ESCAPE] == 1:
						hold_erase = 0
						select = True
						hold_load = 0
						hold_save = 0
						hold_play = 0
						hold_set = 0
						hold_change = 0
						hold_proper = 0
						hold_trans = 0
						hold_help = 0
						valor_1 = None
						valor_2 = None
						push = False
						cont_time = 0
						block_proper = 0
						usuario.marcado_act = marcado_ini
						#print('act:', usuario.marcado_act)
						push_coli = [False, False, False]
						
						for estado in usuario.sprites_estados:
							estado.push = False
						for trans in usuario.sprites_trans:
							trans.push = False
						for conexion in usuario.sprites_conexion:
							conexion.push = False
						#usuario.load_net(propiedades.fondo_dibujo, erase)
						#marcado_global = usuario.marcado_act # al presionar escape se verifica donde quedo el marcado
					else:
						select = False
					center_move = (pos[0]-180+desp[0], pos[1]-50+desp[1])
					usuario.agregar_peso(center_move)
					if pygame.mouse.get_pressed()[0] and hold_change == 0:
						usuario.dibujar_area(dentro, posi, pantalla, desp)
						usuario.conectar(center_move, dentro, pantalla, desp, posi)
						propiedades.fondo_dibujo.fill((255, 255, 255))
						dibujar_conex = True

											

					if (play_pos.collidepoint(posi) or hold_play == 1) and hold_change == 0: # Ejecutar red
						hold_play = 1
						marcado_ini = usuario.marcado_act
						#print('ini:', marcado_ini)
						block_mar = True
					if set_pos.collidepoint(posi) or hold_set == 1:  
						hold_set = 1
					if (erase_pos.collidepoint(posi) or hold_erase == 1) and hold_change == 0:
						hold_erase = 1
						usuario.hold = [0, 0, 0, 0, 0]
						hold_play = 0
						hold_proper = 0
					if help_pos.collidepoint(posi) == 1:
						hold_help = 1
					if change_pos.collidepoint(posi) or hold_change == 1:
						hold_change = 1
					if (proper_pos.collidepoint(posi) or hold_proper == 1) and hold_erase == 0: # Ventana propiedades
						hold_proper = 1
					if trans_pos.collidepoint(posi) or hold_trans == 1: # Poner transicion
						hold_trans = 1
					if save_pos.collidepoint(posi) and hold_erase == 0:
						usuario.save_net(propiedades, barra_actual, size_sheet, modo_temp)
						#hold_save = 1
					if load_pos.collidepoint(posi) and hold_erase == 0:
						propiedades.lista_barra, barra_actual, size_sheet = usuario.load_net(propiedades.fondo_dibujo, erase, propiedades.lista_barra, 
																							 barra_actual, size_sheet)
					if len(usuario.sprites_estados) > 0 and hold_play != 1: # Hallar marcado inicial
						#print(modo_temp)
						if modo_temp == [1, 0, 0] or modo == [0, 1]: 
							#print('no')
							delay_trans = usuario.marcado()
						if modo_temp == [0, 1, 0]:
							delay_trans = usuario.marcado_t()
						if modo_temp == [0, 0, 1]:
							#print('p')
							delay_status = usuario.marcado_p()
						#hold_load = 1
			"""if len(usuario.sprites_estados) > 0 and hold_play != 1: # Hallar marcado inicial
				#print('in_mar')
				if not block_mar:
					#print(1)
					delay_trans = usuario.marcado()
				else:
					#print(2)
					block_mar = False"""
					
			if hold_erase == 1 and keys[K_a]: # Borrar todo
				erase_all = eg.ynbox(msg='¿Desea reiniciar el área de trabajo?',
	                     title='Borrado total',
	                     choices=('Si', 'No'),
	                     image=None)
				
			if erase_all:
				usuario.sprites_estados.clear(propiedades.fondo_dibujo, erase)
				usuario.sprites_trans.clear(propiedades.fondo_dibujo, erase)
				usuario.sprites_conexion.clear(propiedades.fondo_dibujo, erase)
				propiedades.fondo_dibujo.fill((255, 255, 255))
				usuario.invocar_propiedades()
				hold_erase = 0
				size_sheet = 0 # Tamaño de la hoja de trabajo
				barra_actual = [625, 505]
				center_bar = [517.5, 327.5] 
				desp = [0, 0] # X, Y # Desplazamiento del scrolling reflejado sobre la superficie
				pasos = [0, 0] # X, Y # Desplazamiento en scrolling
				propiedades.lista_barra = propiedades.init_barra()
				erase_all = False
				
			pos = pygame.mouse.get_pos()
			center_move = (pos[0]-180+desp[0], pos[1]-50+desp[1])
			pantalla.fill(BLANCO)
			propiedades.dibujar_supercicies(pantalla)
			propiedades.dibujar_barra(pantalla, desp)
			usuario.dibujar_panel(pantalla)
			if hold_change == 0 and hold_erase == 0 and hold_play == 0: # Bloquea adicion de objetos durante dibujo de matrices
				usuario.consultar(pos, pantalla)
			usuario.dibujar_arco(pos, pantalla, posi, center_move, desp)
			total_estados = len(usuario.sprites_estados)
			if len(usuario.sprites_estados) > 0 :
				usuario.sprites_estados.clear(propiedades.fondo_dibujo, erase)
				usuario.sprites_estados.draw(propiedades.fondo_dibujo)
				estados_dibujados = len(usuario.sprites_estados)

			if len(usuario.ini)>0:
				for i, _ in enumerate(usuario.ini):
					pygame.draw.line(propiedades.fondo_dibujo, (255, 255, 255), usuario.ini[i], usuario.fin[i], 4)
					pygame.draw.aaline(propiedades.fondo_dibujo, (0, 0, 0), usuario.ini[i], usuario.fin[i])
					dibujar_conex = False

			if len(usuario.sprites_estados) > 0:
				for estado in usuario.sprites_estados:				
					estado.token = usuario.marcado_act[estado.tag]
					if estado.seleccionado == True:
						estado.image = pygame.image.load(os.path.join('Pictures', 'estado_on.png'))
					else:
						if estado.token == 0:
							estado.image = pygame.image.load(os.path.join('Pictures', 'estado.png'))
						elif estado.token == 1:
							estado.image = pygame.image.load(os.path.join('Pictures', 'peso_1.png'))
						elif estado.token == 2:
							estado.image = pygame.image.load(os.path.join('Pictures', 'peso_2.png'))
						elif estado.token == 3:
							estado.image = pygame.image.load(os.path.join('Pictures', 'peso_3.png'))
						elif estado.token == 4:
							estado.image = pygame.image.load(os.path.join('Pictures', 'peso_4.png'))
						elif estado.token == 5:
							estado.image = pygame.image.load(os.path.join('Pictures', 'peso_5.png'))
						elif estado.token == 6:
							estado.image = pygame.image.load(os.path.join('Pictures', 'peso_6.png'))
						elif estado.token == 7:
							estado.image = pygame.image.load(os.path.join('Pictures', 'peso_7.png'))
						elif estado.token == 8:
							estado.image = pygame.image.load(os.path.join('Pictures', 'peso_8.png'))
						elif estado.token == 9:
							estado.image = pygame.image.load(os.path.join('Pictures', 'peso_9.png'))
						else:
							estado.image = pygame.image.load(os.path.join('Pictures', 'peso_10.png'))
					if select == True:
						estado.seleccionado = False

					if estado.rect.collidepoint(center_move) and propiedades.rectangulo_trabajo.collidepoint(pos):
						if bloqueo_general == False:
							usuario.tooltip_estados(pos, pantalla, center_move, estado)
					"""if estado.rect.collidepoint(center_move) and propiedades.rectangulo_trabajo.collidepoint(pos):
						estado.tooltip(pos, pantalla, center_move)"""

					if len(usuario.borrar)>0: # En caso de borrar
						if estado.rect.collidepoint(usuario.borrar): #colisiona borrar con elemento estado 
							usuario.tag_estado -= 1
							usuario.sprites_estados.remove(estado)
							usuario.lista_estados.remove(estado.rect)
							tag = estado.tag
							np.delete(usuario.marcado_act, estado.tag)

							for con in estado.conexiones: # Elimina conexiones relacionadas al estado eliminado		
								usuario.ini.remove(con.ini)
								usuario.fin.remove(con.fin)
								usuario.sprites_conexion.remove(con)	
								con.rect[0] += 180
								con.rect[1] += 50
								usuario.rect_conec.remove(con.rect)

								if con.punto_inicial == -1:
									usuario.lista_col_t.remove(con.col)	
								elif con.punto_inicial == 1:
									usuario.lista_col_s.remove(con.col)	

								propiedades.fondo_dibujo.fill((255, 255, 255))
								for trans in usuario.sprites_trans:
									for con_t in trans.conexiones:
										if con_t.ini == con.ini and con_t.fin == con.fin:
											trans.conexiones.remove(con_t)

							for bax in usuario.sprites_estados:
								if bax.tag > tag:
									bax.tag -= 1

							for con in usuario.sprites_conexion:
								if con.col[1]>tag:
									con.col[1]-=1

			if len(usuario.sprites_trans) > 0:
				for trans in usuario.sprites_trans:
					if trans.rect.collidepoint(center_move) and propiedades.rectangulo_trabajo.collidepoint(pos):
						if bloqueo_general == False:
							usuario.tooltip_trans(pos, pantalla, center_move, trans)
					if trans.seleccionado == True:
						if trans.horizon == True:
							trans.image = pygame.image.load(os.path.join('Pictures', 'trans_on.png'))
						else:
							trans.image = pygame.image.load(os.path.join('Pictures', 'transv_on.png'))
					elif trans.active == True:
						if trans.horizon == True:
							trans.image = pygame.image.load(os.path.join('Pictures', 'trans_active.png'))
						else:
							trans.image = pygame.image.load(os.path.join('Pictures', 'transv_active.png'))
					elif trans.seleccionado == False:
						if trans.horizon == True:
							trans.image = pygame.image.load(os.path.join('Pictures', 'trans.png'))
						else:
							trans.image = pygame.image.load(os.path.join('Pictures', 'transv.png'))
					if select == True:
						trans.seleccionado = False

					if len(usuario.borrar) > 0: # Eliminar transiciones y conexiones anexas a esta
						if trans.rect.collidepoint(usuario.borrar):  # Verifica la transición a eliminar
							propiedades.fondo_dibujo.fill((255, 255, 255))
							usuario.tag_trans -= 1 # elimina el indice de la transicion borrada
							tag = trans.tag
							usuario.sprites_trans.remove(trans)
							usuario.lista_trans.remove(trans.rect)

							for con in trans.conexiones:
								usuario.ini.remove(con.ini)
								usuario.fin.remove(con.fin)
								usuario.sprites_conexion.remove(con)
								con.rect[0] += 180
								con.rect[1] += 50
								usuario.rect_conec.remove(con.rect)

								if con.punto_inicial == -1:
									usuario.lista_col_t.remove(con.col)	
								elif con.punto_inicial == 1:
									usuario.lista_col_s.remove(con.col)	

								propiedades.fondo_dibujo.fill((255, 255, 255))
								for estado in usuario.sprites_estados:
									for con_s in estado.conexiones:
										if con_s.ini == con.ini and con_s.fin == con.fin:
											estado.conexiones.remove(con_s)

							for bax in usuario.sprites_trans:
								if bax.tag>tag:  #Decrementa el indice de las transiciones que esten despues de la eliminada
									bax.tag -= 1

							for con in usuario.sprites_conexion:
								if con.col[0]>tag:
									con.col[0]-=1

			if len(usuario.sprites_conexion) > 0:
				for conex in usuario.sprites_conexion:
					conex.dibujar_conexion(propiedades.fondo_dibujo)
					if conex.rect.collidepoint(center_move) and propiedades.rectangulo_trabajo.collidepoint(pos):
						usuario.tooltip_conex(pos, pantalla, center_move, conex, bloqueo_general)
						bloqueo_general = True
					else:
						bloqueo_general = False
					if len(usuario.borrar) > 0: # Eliminar conexiones anexas a esta
						if conex.rect.collidepoint(usuario.borrar):  # Verifica la transición a eliminar			
							usuario.sprites_conexion.remove(conex)	
							usuario.ini.remove(conex.ini)
							usuario.fin.remove(conex.fin)
							conex.rect[0] += 180
							conex.rect[1] += 50
							usuario.rect_conec.remove(conex.rect)
							if conex.punto_inicial == -1:
								usuario.lista_col_t.remove(conex.col)	
							elif conex.punto_inicial == 1:
								usuario.lista_col_s.remove(conex.col)	

							for estado in usuario.sprites_estados:
									for con_s in estado.conexiones:
										if con_s.ini == conex.ini and con_s.fin == conex.fin:
											estado.conexiones.remove(con_s)

							for trans in usuario.sprites_trans:
									for con_t in trans.conexiones:
										if con_t.ini == conex.ini and con_t.fin == conex.fin:
											trans.conexiones.remove(con_t)
							propiedades.fondo_dibujo.fill((255, 255, 255))

			usuario.sprites_trans.clear(propiedades.fondo_dibujo, erase)
			usuario.sprites_trans.draw(propiedades.fondo_dibujo)

			#Panel propiedades estados y trans
			if pygame.mouse.get_pressed()[2] or push == True:
				for estado in usuario.sprites_estados:
					if modo == [0, 1]:
						pass
					else:
						if push_coli[1] == True or push_coli[2] == True:
							pass
						else:
							if usuario.hold[3] == 0:
								if estado.rect.collidepoint(center_move) or estado.push == True:
									push = True
									push_coli[0] = True
									estado.push = True	
									propiedades.propiedad_estado(pantalla, font, estado, modo_temp)
									text_u.update()
									text_u.draw(pantalla)
									if modo_temp == [0, 0, 1]:
										text_d.update()
										text_d.draw(pantalla)
									if valor_1 != None:
										estado.limite = int(valor_1)
									if valor_2 != None:
										estado.time = int(valor_2)

				for trans in usuario.sprites_trans:
					if modo == [0, 1]:
						pass
					else:
						if modo_temp == [0, 1, 0]:
							if push_coli[0] == True or push_coli[2] == True:
								pass
							else:
								if trans.rect.collidepoint(center_move) or trans.push == True:
									push = True
									push_coli[1] = True
									trans.push = True
									propiedades.propiedad_trans(pantalla, font, trans)
									text_u.update()
									text_u.draw(pantalla)
									if valor_1 != None:
										trans.time = int(valor_1)

				for conexion in usuario.sprites_conexion:
					if usuario.hold[3] == 0:
						if push_coli[0] == True or push_coli[1] == True:
							pass
						else:
							if conexion.rect.collidepoint(center_move) or conexion.push == True:
								push = True
								push_coli[2] = True
								conexion.push = True
								propiedades.propiedad_conexion(pantalla, font, conexion)
								text_u.update()
								text_u.draw(pantalla)
								if valor_1 != None:
									conexion.token = int(valor_1)

			if save_pos.collidepoint(pos) or hold_save == 1:
				pantalla.blit(save_f, (780, 15))	
			else:
				pantalla.blit(save_e, (780, 15))	

			if load_pos.collidepoint(pos) or hold_load == 1:
				pantalla.blit(load_f, (825, 15))	
			else:
				pantalla.blit(load_e, (825, 15))	

			if play_pos.collidepoint(pos) and hold_play == 0: # Boton play
				pantalla.blit(play_f, (30, 520))
			elif hold_play == 1:
				pantalla.blit(pause_f, (30, 520))
			else:
				pantalla.blit(play_e, (30, 520))

			if set_pos.collidepoint(pos) or hold_set == 1: # Boton set
				pantalla.blit(set_f, (30, 575))
			else:
				pantalla.blit(set_e, (30, 575))

			if erase_pos.collidepoint(pos) or hold_erase == 1: # Boton erase
				pantalla.blit(erase_f, (100, 520))
			else:
				pantalla.blit(erase_e, (100, 520))
			
			if help_pos.collidepoint(pos) == 1 and hold_help == 0: # Boton erase
				pantalla.blit(help_f, (100, 575))
			elif help_pos.collidepoint(pos) == 0 and hold_help == 0:
				pantalla.blit(help_e, (100, 575))
			else:
				webbrowser.open_new(r'Manual_Usuario.pdf')
				hold_help = 0

			if change_pos.collidepoint(pos) == 1 and hold_change == 0:
				pantalla.blit(matrix_f, (505, 640))
			elif change_pos.collidepoint(pos) == 0 and hold_change == 0:
				pantalla.blit(matrix_e, (505, 640))
			else:
				modo_inc = usuario.dibujar_matriz(pantalla, font, modo_inc, posi, pos)
				pantalla.blit(matrix_f, (505, 640))

			if proper_pos.collidepoint(pos) == 1 and hold_proper == 0:
				pantalla.blit(proper_f, (445, 640))
			elif proper_pos.collidepoint(pos) == 0 and hold_proper == 0:
				pantalla.blit(proper_e, (445, 640))
			else:
				block_proper, general, no_viva, no_pureza, limit = usuario.properties(pantalla, font, pos, posi, block_proper,
																					  general, no_viva, no_pureza, limit)
				pantalla.blit(proper_f, (445, 640))

			if trans_pos.collidepoint(pos) == 1 and hold_trans == 0:
				pantalla.blit(trans_f, (570, 640))
			elif trans_pos.collidepoint(pos) == 0 and hold_trans == 0:
				pantalla.blit(trans_e, (570, 640))
			else:
				usuario.transform(pantalla, font)
				pantalla.blit(trans_f, (570, 640))
			if salir_t == 1:
				#print('onox')
				salir_t = 0
				hold_erase = 0
				select = True
				hold_load = 0
				hold_save = 0
				hold_play = 0
				hold_set = 0
				hold_change = 0
				hold_proper = 0
				hold_trans = 0
				hold_help = 0
				valor_1 = None
				valor_2 = None
				push = False
				cont_time = 0
				block_proper = 0
			if (hold_set == 1 and hold_change == 0) and hold_erase == 0:
				modo, vel, delay_evo, modo_temp = propiedades.configurar(pantalla, posi, modo, vel, delay_evo, modo_temp)
			if hold_erase == 1:
				usuario.borrar_elemento(pantalla, center_move, pos)
			if (hold_play == 1 and hold_change == 0) and hold_erase == 0:
				#print('hola')
				if len(usuario.sprites_conexion) > 0:
					if modo == [1, 0]:
						if modo_temp == [1, 0, 0]:
							#print('no')
							if cont_time == 60*(delay_evo/1000):
								#print('iterando')
								usuario.evolucionar_no(modo, posi, delay_evo, modo_temp, center_move)
								cont_time = -1
						if modo_temp == [0, 1, 0]:
							#print(delay_trans)
							if cont_time == 60*(delay_trans/1000):
								#print('iterando')
								salir_t, delay_trans = usuario.evolucionar_t(modo, posi, delay_evo, modo_temp, center_move)
								cont_time = -1
						if modo_temp == [0, 0, 1]:
							#print('p')
							#print(delay_trans)
							if cont_time == 60*(delay_status/1000):
								#print('iterando')
								usuario.evolucionar_p(modo, posi, delay_evo, modo_temp, center_move)
								cont_time = -1
						cont_time += 1
					else:
						#print('manu')
						if push_manual == True:
							usuario.evolucionar_no(modo, posi, delay_evo, modo_temp, center_move)
				#print(cont_time)
			else:
				pass

			push_manual = False
			reloj.tick(60)
			pygame.display.flip()
		except:
			eg.msgbox('Error inesperado, el sistema debe ser reiniciado', "Advertencia", ok_button="Continuar")

if __name__.endswith('__main__'):
	main()
