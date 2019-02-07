import string
import os
import pygame
import numpy as np
from scipy.stats import dweibull
import matplotlib.pyplot as plt


WHITE = (255, 255, 255)
BLUE = (65, 105, 225)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
ACCEPTED = string.ascii_letters + '_-.' + string.digits


class TextBox(object):
    def __init__(self, rect, **kwargs):
        self.rect = pygame.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.process_kwargs(kwargs)

    def process_kwargs(self, kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "color" : pygame.Color("white"),
                    "font_color" : pygame.Color("black"),
                    "outline_color" : pygame.Color("black"),
                    "outline_width" : 1,
                    "active_color" : pygame.Color("red"),
                    "font" : pygame.font.SysFont('Arial', self.rect.height+2),
                    "clear_on_enter" : False,
                    "inactive_on_enter" : True}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.execute()
            elif event.key == pygame.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in ACCEPTED:
                self.buffer.append(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

    def execute(self):
        if self.command:
            self.command(self.id, self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def update(self):
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(x=self.rect.x+2,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width-6:
                offset = self.render_rect.width-(self.rect.width-6)
                self.render_area = pygame.Rect(offset, 0, self.rect.width-6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0, 0))
        if pygame.time.get_ticks() - self.blink_timer > 300:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def draw(self, surface):
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width*2, self.outline_width*2)
        surface.fill(outline_color, outline)
        surface.fill(self.color, self.rect)
        if self.rendered:
            surface.blit(self.rendered, self.render_rect, self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color, (curse.right+1, curse.y, 2, curse.h))


class ListBox:
    def __init__(self):
        self.container_clases = pygame.Surface((140, 210))  # listmenu de clases
        self.container_clases.fill(WHITE)
        self.posi_container = (120, 240)
        self.list_items = list()  # Contiene los elementos dentro del contenedor
        self.selected = 1  #
        self.conten_actual = 1
        self.selected_item = pygame.Rect(self.posi_container[0]+2, self.posi_container[1]+1*self.selected, 136, 28)
        self.dt = 30  # Altura de cada recta
        self.down = 0  # Indicar cuantos desplazamientos ha dado el scroll de clases
        self.rects = []
        self.num_rects = 7  # Número de rectas dentro del listbox
        self.font = pygame.font.SysFont('Arial', 14)
        self.time = np.linspace(0, 8760, 1000)
        self.make_rects()
        self.types = {'exp': 'Distribución Exponencial', 'ray': 'Distribución Rayleigh', 'wei': 'Distribución Weibull'}

    def make_rects(self):
        for index in range(self.num_rects):
            self.rects.append(pygame.Rect(self.posi_container[0] + 1, self.posi_container[1] + (1+self.dt*index), 136, 28))

    def add_data(self, element):
        self.list_items.append(element)

    def del_data(self, element):
        pass

    def consult_position(self, position):
        for index in range(self.num_rects):
            if self.rects[index].collidepoint(position):
                self.conten_actual = index+1

    def draw(self, screen):
        screen.blit(self.container_clases, self.posi_container)
        self.selected_class = pygame.Rect(self.posi_container[0] + 2,
                                          (self.posi_container[1] + (30 * (self.conten_actual - 1))) + 1, 136, 28)
        pygame.draw.rect(screen, BLUE, self.selected_class, 0)
        for index, element in enumerate(self.list_items):
            screen.blit(self.font.render(element.tag, True,
                                                  BLACK),
                                 (self.posi_container[0] + 5, self.posi_container[1] + 5 + (index * self.dt)))
        print(self.conten_actual)
        caja = self.list_items[self.conten_actual-1]
        self.make_plot(caja)

    def make_plot(self, elemento):
        #dist = dweibull(float(elemento.betha), 0, float(elemento.alpha))
        plt.style.use('seaborn')  # pretty matplotlib plots
        plt.cla()
        #plt.plot(self.time, dist.pdf(self.time), c='blue',
                 #label=r'$\beta=%.3f,\ \alpha=%.3f$' % (float(elemento.betha), float(elemento.alpha)))
        t = self.time
        plt.plot(self.time, eval(elemento.value), c='blue',
                 label=r'$\beta=%.3f,\ \alpha=%.3f$' % (float(elemento.betha), float(elemento.alpha)))
        plt.xlabel('t')
        plt.ylabel(r'$p(t|\beta,\alpha)$')
        plt.title(self.types[elemento.mod])
        plt.legend()


class RadioButton:
    def __init__(self, name, texto, position=(0, 0), size=(26, 26), color=GRAY, active=False):
        self.name = name
        self.no_pushed = pygame.image.load(os.path.join("icons", "uncheck.png"))
        self.pushed = pygame.image.load(os.path.join("icons", "check.png"))
        self.text = texto
        self.position = position
        self.size = size
        self.color = color
        self.own_surface = pygame.Surface(size)
        self.own_surface.fill(self.color)
        self.own_surface.blit(self.no_pushed, (0, 0))
        self.font = pygame.font.SysFont('Arial', 14)
        self.recta = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.over = False
        self.push = active

    def draw(self, screen):
        if self.over:
            screen.blit(self.font.render(self.text, True, BLACK), (self.position[0] + 28, self.position[1] + 5))
            self.font.set_underline(True)
        else:
            screen.blit(self.font.render(self.text, True, BLACK), (self.position[0] + 28, self.position[1] + 5))
            self.font.set_underline(False)
        if self.push:
            self.own_surface.fill(self.color)
            self.own_surface.blit(self.pushed, (0, 0))
        else:
            self.own_surface.fill(self.color)
            self.own_surface.blit(self.no_pushed, (0, 0))
        screen.blit(self.own_surface, self.position)
