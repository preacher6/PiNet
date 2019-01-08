import os
import sys
import pygame
import numpy as np
from textbox import TextBox
from objects import *


GRAY = (128, 128, 128)
WHITE = (255, 255, 255)


class Property(pygame.sprite.Sprite):
    def __init__(self, workspace_size=(900, 520)):
        pygame.sprite.Sprite.__init__(self)
        self.load_pics()
        self.SIZE_WORKSPACE = workspace_size  # Tamaño del espacio de trabajo
        self.font = pygame.font.SysFont('Arial', 15)
        self.text_boxes()
        self.surfaces()
        self.drawing = False
        self.hold_caja = False
        self.hold_knn = False
        self.hold_stand = False

    def load_pics(self):
        self.addline = pygame.image.load(os.path.join('icons', 'addline.png'))
        self.reduceline = pygame.image.load(os.path.join('icons', 'reduceline.png'))
        self.reduceline_over = pygame.image.load(os.path.join('icons', 'reduceline_over.png'))
        self.pestana_s = pygame.image.load(os.path.join('pics', 'pesta_s.png'))
        self.pestana_n = pygame.image.load(os.path.join('pics', 'pesta_n.png'))
        self.new = pygame.image.load(os.path.join('pics', 'pesta_new.png'))
        self.option_s = pygame.image.load(os.path.join('pics', 'option_s.png'))
        self.option_n = pygame.image.load(os.path.join('pics', 'option_n.png'))
        self.close = pygame.image.load(os.path.join('icons', 'close.png'))
        self.add = pygame.image.load(os.path.join('icons', 'add.png'))
        self.grid = pygame.image.load(os.path.join('pics', 'punto.png'))
        # Acciones
        self.connect_n = pygame.image.load(os.path.join('icons', 'connect_n.png'))
        self.connect_s = pygame.image.load(os.path.join('icons', 'connect_s.png'))
        self.disconnect_n = pygame.image.load(os.path.join('icons', 'disconnect_n.png'))
        self.disconnect_s = pygame.image.load(os.path.join('icons', 'disconnect_s.png'))
        self.move_n = pygame.image.load(os.path.join('icons', 'move_n.png'))
        self.move_s = pygame.image.load(os.path.join('icons', 'move_s.png'))
        self.delete_n = pygame.image.load(os.path.join('icons', 'delete_n.png'))
        self.delete_s = pygame.image.load(os.path.join('icons', 'delete_s.png'))
        self.export_n = pygame.image.load(os.path.join('icons', 'export_n.png'))
        self.export_s = pygame.image.load(os.path.join('icons', 'export_s.png'))
        self.import_n = pygame.image.load(os.path.join('icons', 'import_n.png'))
        self.import_s = pygame.image.load(os.path.join('icons', 'import_s.png'))
        self.rename_n = pygame.image.load(os.path.join('icons', 'rename_n.png'))
        self.rename_s = pygame.image.load(os.path.join('icons', 'rename_s.png'))
        self.save_n = pygame.image.load(os.path.join('icons', 'save_n.png'))
        self.save_s = pygame.image.load(os.path.join('icons', 'save_s.png'))
        self.load_n = pygame.image.load(os.path.join('icons', 'load_n.png'))
        self.load_s = pygame.image.load(os.path.join('icons', 'load_s.png'))
        self.ok_n = pygame.image.load(os.path.join('icons', 'ok_n.png'))
        self.ok_s = pygame.image.load(os.path.join('icons', 'ok_s.png'))
        # Elementos
        self.caja_mini = pygame.image.load(os.path.join('pics', 'caja_mini.png'))
        self.stand_mini = pygame.image.load(os.path.join('pics', 'stand_by_mini.png'))
        self.knn_mini = pygame.image.load(os.path.join('pics', 'knn_mini.png'))
        # Normales
        self.caja = pygame.image.load(os.path.join('pics', 'caja.png'))
        self.stand = pygame.image.load(os.path.join('pics', 'stand_by.png'))
        self.knn = pygame.image.load(os.path.join('pics', 'knn.png'))

    def surfaces(self):
        self.pos_rename = (400, 180)  # inicio espacio de trabajo
        self.rename_panel = pygame.Surface((200, 90))  # Superficie para las acciones
        self.rename_panel.fill(GRAY)
        self.workspace = pygame.Surface(self.SIZE_WORKSPACE)
        self.workspace.fill(WHITE)
        self.pos_workspace = (60, 170)  # inicio espacio de trabajo

    def options_panel(self, position, cont):
        self.image = self.option_s  # Imagen actual de la pestaña opcion (activa)
        self.image_off = self.option_n
        self.rect = self.image.get_rect()  # Recta de la imagen
        self.rect.x = position[0]
        self.rect.y = position[1]*cont

    def text_boxes(self):
        self.name = TextBox((410, 230, 140, 20), id="name_con", active=True,
                            clear_on_enter=False, inactive_on_enter=True)

    def name_surface(self, screen, position):
        screen.blit(self.rename_panel, self.pos_rename)
        screen.blit(self.close, self.close_name_rect)
        screen.blit(self.font.render('Nombre pestaña:', True, (0, 0, 0)),
                    (self.pos_rename[0]+10, self.pos_rename[1]+10))
        if self.ok_rect.collidepoint(position):
            screen.blit(self.ok_s, self.ok_rect)
            screen.blit(self.font.render('Aceptar', True, (0, 0, 0)),
                        (position[0] + 8, position[1] + 8))
        else:
            screen.blit(self.ok_n, self.ok_rect)

    def rect_actions(self, pos_actions):
        self.connect_rect = self.connect_n.get_rect()
        self.connect_rect.x = pos_actions[0]+2
        self.connect_rect.y = pos_actions[1]+1
        self.disconnect_rect = self.disconnect_n.get_rect()
        self.disconnect_rect.x = pos_actions[0] + 52
        self.disconnect_rect.y = pos_actions[1] + 1
        self.move_rect = self.move_n.get_rect()
        self.move_rect.x = pos_actions[0] + 105
        self.move_rect.y = pos_actions[1] + 1
        # 2da fila
        self.delete_rect = self.delete_n.get_rect()
        self.delete_rect.x = pos_actions[0]+2
        self.delete_rect.y = pos_actions[1]+40
        self.export_rect = self.export_n.get_rect()
        self.export_rect.x = pos_actions[0] + 54
        self.export_rect.y = pos_actions[1] + 42
        self.import_rect = self.import_n.get_rect()
        self.import_rect.x = pos_actions[0] + 107
        self.import_rect.y = pos_actions[1] + 42
        # 3ra fila
        self.rename_rect = self.rename_n.get_rect()
        self.rename_rect.x = pos_actions[0] + 2
        self.rename_rect.y = pos_actions[1] + 81
        self.save_rect = self.save_n.get_rect()
        self.save_rect.x = pos_actions[0] + 54
        self.save_rect.y = pos_actions[1] + 83
        self.load_rect = self.load_n.get_rect()
        self.load_rect.x = pos_actions[0] + 107
        self.load_rect.y = pos_actions[1] + 83

        self.close_name_rect = self.close.get_rect()
        self.close_name_rect.x = self.pos_rename[0] + 170
        self.close_name_rect.y = self.pos_rename[1] + 5
        self.ok_rect = self.ok_n.get_rect()
        self.ok_rect.x = self.pos_rename[0] + 159
        self.ok_rect.y = self.pos_rename[1] + 45

    def draw_actions(self, screen, position):
        if self.connect_rect.collidepoint(position):
            screen.blit(self.connect_s, self.connect_rect)
            screen.blit(self.font.render('Conectar', True, (0, 0, 0)),
                        (position[0] + 8, position[1] + 8))
        else:
            screen.blit(self.connect_n, self.connect_rect)

        if self.disconnect_rect.collidepoint(position):
            screen.blit(self.disconnect_s, self.disconnect_rect)
            screen.blit(self.font.render('Desconectar', True, (0, 0, 0)),
                        (position[0] + 8, position[1] + 8))
        else:
            screen.blit(self.disconnect_n, self.disconnect_rect)

        if self.move_rect.collidepoint(position):
            screen.blit(self.move_s, self.move_rect)
            screen.blit(self.font.render('Mover', True, (0, 0, 0)),
                        (position[0] + 8, position[1] + 8))
        else:
            screen.blit(self.move_n, self.move_rect)

        if self.delete_rect.collidepoint(position):
            screen.blit(self.delete_s, self.delete_rect)
            screen.blit(self.font.render('Borrar elemento', True, (0, 0, 0)),
                        (position[0] + 8, position[1] + 8))
        else:
            screen.blit(self.delete_n, self.delete_rect)

        if self.export_rect.collidepoint(position):
            screen.blit(self.export_s, self.export_rect)
            screen.blit(self.font.render('Borrar elemento', True, (0, 0, 0)),
                        (position[0] + 8, position[1] + 8))
        else:
            screen.blit(self.export_n, self.export_rect)

        if self.import_rect.collidepoint(position):
            screen.blit(self.import_s, self.import_rect)
            screen.blit(self.font.render('Borrar elemento', True, (0, 0, 0)),
                        (position[0] + 8, position[1] + 8))
        else:
            screen.blit(self.import_n, self.import_rect)

        if self.rename_rect.collidepoint(position):
            screen.blit(self.rename_s, self.rename_rect)
            screen.blit(self.font.render('Borrar elemento', True, (0, 0, 0)),
                        (position[0] + 8, position[1] + 8))
        else:
            screen.blit(self.rename_n, self.rename_rect)

        if self.save_rect.collidepoint(position):
            screen.blit(self.save_s, self.save_rect)
            screen.blit(self.font.render('Borrar elemento', True, (0, 0, 0)),
                        (position[0] + 8, position[1] + 8))
        else:
            screen.blit(self.save_n, self.save_rect)

        if self.load_rect.collidepoint(position):
            screen.blit(self.load_s, self.load_rect)
            screen.blit(self.font.render('Borrar elemento', True, (0, 0, 0)),
                        (position[0] + 8, position[1] + 8))
        else:
            screen.blit(self.load_n, self.load_rect)

    def rect_elements(self, position):
        self.caja_mini_rect = self.caja_mini.get_rect()
        self.caja_mini_rect.x = position[0] + 15
        self.caja_mini_rect.y = position[1] + 40
        self.knn_mini_rect = self.knn_mini.get_rect()
        self.knn_mini_rect.x = position[0] + 75
        self.knn_mini_rect.y = position[1] + 40
        self.stand_mini_rect = self.stand_mini.get_rect()
        self.stand_mini_rect.x = position[0] + 125
        self.stand_mini_rect.y = position[1] + 40

    def draw_elements(self, screen):
        """Dibujar elementos a seleccionar (caja-mini, stand-by y knn)"""
        screen.blit(self.caja_mini, self.caja_mini_rect)
        screen.blit(self.knn_mini, self.knn_mini_rect)
        screen.blit(self.stand_mini, self.stand_mini_rect)

    def draw_selected(self, screen, position, pushed):
        """Dibuja sobre la interfaz el elemento seleccionado"""
        if self.caja_mini_rect.collidepoint(pushed) or self.hold_caja:
            self.hold_caja = True
            valid_workspace = pygame.Rect(self.pos_workspace[0], self.pos_workspace[1],
                                          self.SIZE_WORKSPACE[0] - 180, self.SIZE_WORKSPACE[1] - 80)
            elemento = self.caja
            self.title = 'caja'
            self.draw_inside_work(screen, position, elemento, valid_workspace)
        elif self.knn_mini_rect.collidepoint(pushed) or self.hold_knn:
            self.hold_knn = True
            valid_workspace = pygame.Rect(self.pos_workspace[0], self.pos_workspace[1],
                                          self.SIZE_WORKSPACE[0] - 200, self.SIZE_WORKSPACE[1] - 180)
            elemento = self.knn
            self.title = 'knn'
            self.draw_inside_work(screen, position, elemento, valid_workspace)
        elif self.stand_mini_rect.collidepoint(pushed) or self.hold_stand:
            self.hold_stand = True
            valid_workspace = pygame.Rect(self.pos_workspace[0], self.pos_workspace[1],
                                          self.SIZE_WORKSPACE[0] - 200, self.SIZE_WORKSPACE[1] - 180)
            elemento = self.stand
            self.title = 'stand'
            self.draw_inside_work(screen, position, elemento, valid_workspace)

    def draw_inside_work(self, screen, position, elemento, space):
        """Funcion para definir la manera en q se ubica el elemento dependiendo de donde se encuentre"""

        if space.collidepoint(position):
            self.drawing = True
            position = self.round_pos(position)
            screen.blit(elemento, position)
        else:
            self.drawing = False
            screen.blit(elemento, position)

    @staticmethod
    def round_pos(position, base=20):
        """Determinar posicion dentro de las reticulas"""
        posx = base*round(position[0]/base)+1
        posy = base*round(position[1]/base)-9
        new_pos = (posx, posy)
        return new_pos

    def put_element(self):
        """Poner elemento sobre el area de trabajo (contenedor)"""
        if self.drawing:
            if self.hold_caja:
                pass
            elif self.hold_knn:
                pass
            elif self.hold_stand:
                pass

    def draw_grid(self, screen, screen_pos):
        """Dibujar rejilla"""
        iter_fila = screen_pos[1]
        for fila in range(25):
            iter_fila += 20
            iter_col = screen_pos[0]
            for columna in range(44):
                iter_col += 20
                pos_circle = (iter_col, iter_fila)
                screen.blit(self.grid, pos_circle)

    def draw_plot(self):
        pass

    def cancel(self):
        """Cancelar acciones en ejecución"""
        self.drawing = False
        self.hold_caja = False
        self.hold_knn = False
        self.hold_stand = False
        position = (0, 0)
        return position
