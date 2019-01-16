import pygame
import os
from objects import *
from textbox import ListBox

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SEMIWHITE = (245, 245, 245)
GRAY = (128, 128, 128)
LIGHTGRAY = (192, 192, 192)
GANSBORO = (220, 220, 220)
SLATEGRAY = (112, 128, 144)


class OptionPanels(pygame.sprite.Sprite):
    """Clase para pestañas de opciones"""
    def __init__(self, name, position, cont, active=False, content=None):
        pygame.sprite.Sprite.__init__(self)
        self.load_pics()
        self.name = name
        self.icon = pygame.image.load(os.path.join('icons', name+str('.png')))
        self.active = active
        self.image = self.option_s  # Imagen actual de la pestaña opcion (activa)
        self.image_off = self.option_n
        self.rect = self.image.get_rect()  # Recta de la imagen
        self.rect.x = position[0]
        self.rect.y = position[1]+cont*40
        self.content = content

    def load_pics(self):
        """Cargar imagenes"""
        self.addline_s = pygame.image.load(os.path.join('icons', 'addline_s.png'))
        self.addline_n = pygame.image.load(os.path.join('icons', 'addline_n.png'))
        self.reduceline_s = pygame.image.load(os.path.join('icons', 'reduceline_s.png'))
        self.reduceline_n = pygame.image.load(os.path.join('icons', 'reduceline_n.png'))
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

    def draw_option(self, screen):
        """Dibujar pestañas de opciones"""
        if self.active:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image_off, self.rect)
        screen.blit(self.icon, (self.rect[0]-2, self.rect[1]+2))


class Container(pygame.sprite.Sprite):
    def __init__(self, pos, cont, tag, content=None):
        pygame.sprite.Sprite.__init__(self)
        self.load_pics()
        self.pos = pos  # Posicion de la pestaña
        self.pos_elem = (pos[0], pos[1]+30)
        self.cont = cont  # Numero actual de pestañas
        self.font = pygame.font.SysFont('Arial', 13)
        self.image = self.pestana_s  # Imagen actual de la pestaña (activa)
        self.image_off = self.pestana_n  # Imagen de pestaña inactiva
        # Rectas
        self.rect = self.image.get_rect()  # Recta de la imagen
        self.rect.x = pos[0] + (120 * (cont - 1))
        self.rect.y = pos[1]
        self.recta_new = self.new.get_rect()
        self.recta_new.x = pos[0] + 120 * cont
        self.recta_new.y = pos[1]
        self.recta_add = self.add.get_rect()
        self.recta_add.x = pos[0] + 120 * cont + 8
        self.recta_add.y = pos[1] + 6
        self.recta_close = self.close.get_rect()
        self.recta_close.x = pos[0] + 89 + (120 * (cont - 1))
        self.recta_close.y = pos[1] + 5
        self.name = 'Untitled_' + str(tag)  # Nombre de la pestaña
        self.selected = True  # Indica si esta activa. Al momento de crearse siempre lo está
        self.content = content
        self.limites = pygame.sprite.Group()
        self.cajas = pygame.sprite.Group()
        self.cont_cajas = 0
        self.knn = pygame.sprite.Group()
        self.cont_knn = 0
        self.stand = pygame.sprite.Group()
        self.cont_stand = 0
        self.nodos = pygame.sprite.Group()  # Guarda los nodos disponibles para el contenedor
        self.conections = pygame.sprite.Group()  # Guarda las conexiones del contenedor
        self.list_box = ListBox()
        self.init_containter()

    def load_pics(self):
        """Cargar imagenes"""
        self.addline_s = pygame.image.load(os.path.join('icons', 'addline_s.png'))
        self.addline_n = pygame.image.load(os.path.join('icons', 'addline_n.png'))
        self.reduceline_s = pygame.image.load(os.path.join('icons', 'reduceline_s.png'))
        self.reduceline_n = pygame.image.load(os.path.join('icons', 'reduceline_n.png'))
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

    def init_containter(self):
        """Inicializar elementos que tiene el contenedor"""
        self.limites.add(Init((self.pos_elem[0]+40, self.pos_elem[1]+241)))
        self.limites.add(End((self.pos_elem[0]+860, self.pos_elem[1]+241)))
        for limite in self.limites:
            self.nodos.add(limite.nodo)

    def draw_cont(self, screen):
        """Dibujar icono de pestaña"""
        self.rect.x = self.pos[0] + (120 * (self.cont - 1))
        self.rect.y = self.pos[1]
        self.recta_close.x = self.pos[0] + 89 + (120 * (self.cont - 1))
        self.recta_close.y = self.pos[1] + 5
        if self.selected:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image_off, self.rect)
        screen.blit(self.close, self.recta_close)
        screen.blit(self.font.render(self.name, True, (255, 0, 0)),
                    (self.pos[0]+14+(120*(self.cont-1)), self.pos[1]+7))

    def draw_new(self, screen, cont):
        """Dibujar icono de nueva pestaña"""
        self.recta_new.x = self.pos[0] + 120 * cont
        self.recta_add.x = self.pos[0] + 120 * cont + 8
        screen.blit(self.new, self.recta_new)
        screen.blit(self.add, self.recta_add)

    def draw_elements(self, screen):
        """Dibujar elementos del contectedor"""
        for limit in self.limites:
            limit.draw(screen)

        for caja in self.cajas:
            caja.draw(screen)

        for knn_ind in self.knn:
            knn_ind.draw(screen)

        for stand_in in self.stand:
            stand_in.draw(screen)

        for conex_in in self.conections:
            conex_in.draw(screen)
            for limite in self.limites:  # Conexiones de limites
                if conex_in.elem1.name_element == limite.nodo.name_element and conex_in.elem1.id == limite.nodo.id:
                    limite.nodo.connected = True

                if conex_in.elem2.name_element == limite.nodo.name_element and conex_in.elem2.id == limite.nodo.id:
                    limite.nodo.connected = True

            for caja in self.cajas:  # Conexiones de cajas
                for nodo in caja.nodos:  # Se recorre un for para ver si algun elemento ha sido conectado
                    if conex_in.elem1.name_element == nodo.name_element and conex_in.elem1.id == nodo.id:
                        nodo.connected = True

                    if conex_in.elem2.name_element == nodo.name_element and conex_in.elem2.id == nodo.id:
                        nodo.connected = True

            for knn_ind in self.knn:  # Conexiones de knn
                for nodo in knn_ind.nodos:  # Se recorre un for para ver si algun elemento ha sido conectado
                    if conex_in.elem1.name_element == nodo.name_element and conex_in.elem1.id == nodo.id:
                        nodo.connected = True

                    if conex_in.elem2.name_element == nodo.name_element and conex_in.elem2.id == nodo.id:
                        nodo.connected = True

            for stand_ind in self.stand:  # Conexiones de standby
                for nodo in stand_ind.nodos:  # Se recorre un for para ver si algun elemento ha sido conectado
                    if conex_in.elem1.name_element == nodo.name_element and conex_in.elem1.id == nodo.id:
                        nodo.connected = True

                    if conex_in.elem2.name_element == nodo.name_element and conex_in.elem2.id == nodo.id:
                        nodo.connected = True


class TextButton:
    def __init__(self, text, name, position=(0, 0), size=(90, 30), text_position=(5, 5)):
        self.text = text
        self.name = name
        self.position = position
        self.size = size
        self.text_position = text_position
        self.own_surface = pygame.Surface(self.size)
        self.own_surface.fill(SEMIWHITE)
        self.recta = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.font = pygame.font.SysFont('Arial', 13)
        self.own_surface.blit(self.font.render(self.text, True,
                              BLACK), self.text_position)
        self.over = False

    def draw_button(self, screen):
        if self.over:
            self.own_surface.fill(SLATEGRAY)
            self.own_surface.blit(self.font.render(self.text, True,
                                                   BLACK), self.text_position)
            self.font.set_underline(True)
        else:
            self.own_surface.fill(SEMIWHITE)
            self.own_surface.blit(self.font.render(self.text, True,
                                                   BLACK), self.text_position)
            self.font.set_underline(False)
        screen.blit(self.own_surface, self.position)
        pygame.draw.rect(screen, BLACK, self.recta, 1)
