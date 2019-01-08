import pygame
from properties import *


class OptionPanels(Property):
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

    def draw_option(self, screen):
        """Dibujar pestañas de opciones"""
        if self.active:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image_off, self.rect)
        screen.blit(self.icon, (self.rect[0]-2, self.rect[1]+2))


class Container(Property):
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
        self.knn = pygame.sprite.Group()
        self.stand = pygame.sprite.Group()
        self.init_containter()

    def init_containter(self):
        """Inicializar elementos que tiene el contenedor"""
        self.limites.add(Init((self.pos_elem[0]+40, self.pos_elem[1]+240)))
        self.limites.add(End((self.pos_elem[0]+860, self.pos_elem[1] + 240)))

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
