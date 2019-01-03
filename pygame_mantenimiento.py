import pygame
import sys
import os
from properties import *


WHITE = (255, 255, 255)
GRAY = (112, 128, 144)


class PGManten:
    """
    Clase para trabajar con pygame
    """
    def __init__(self, window_size=(1000, 700), workspace_size=(900, 520)):
        self.initialize_pygame()
        self.clock = pygame.time.Clock()
        self.WINDOW_SIZE = window_size  # Tamaño ventana principal
        self.SIZE_WORKSPACE = workspace_size  # Tamaño del espacio de trabajo
        self.pos_workspace = (60, 170)  # inicio espacio de trabajo
        self.pos_button_action = (400, 10)  # Inicio de posiciones acciones
        self.button_act_panel = pygame.Surface((150, 120))  # Superficie para las acciones
        self.button_act_panel.fill(WHITE)
        self.pos_button_elements = (600, 10)  # Inicio de posiciones acciones
        self.button_ele_panel = pygame.Surface((150, 120))  # Superficie para las acciones
        self.button_ele_panel.fill(WHITE)
        self.workspace = pygame.Surface(self.SIZE_WORKSPACE)
        self.workspace.fill(WHITE)
        self.screen_form = pygame.display.set_mode(self.WINDOW_SIZE)
        self.elementos = {'pestañas': pygame.sprite.Group(),
                          'opciones': pygame.sprite.Group()}  # Inicializar diccionario de elementos
        self.actions = [0]*9
        self.checking_text = False  # Indica si se está usando algun campo de texto
        self.lista_text = None  # Elementos de texto a iterar

    def initialize_pygame(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centra la interfaz
        pygame.display.set_caption('Diagramas confiabilidad')

    def properties(self, position):
        """Dibujar estructuras del sistema"""
        self.screen_form.blit(self.button_act_panel, self.pos_button_action)
        self.screen_form.blit(self.button_ele_panel, self.pos_button_elements)
        self.screen_form.blit(self.workspace, self.pos_workspace)
        self.property_class.draw_actions(self.screen_form, position)
        for elemento in self.elementos['opciones']:
            if elemento.name == 'module':
                if elemento.active:
                    self.property_class.draw_grid(self.screen_form, self.pos_workspace)

    def draw_containers(self, container, cont):
        """Dibujar pestañas"""
        for pestaña in self.elementos['pestañas']:
            pestaña.draw_cont(self.screen_form)

        container.draw_new(self.screen_form, cont)

        for option in self.elementos['opciones']:
            option.draw_option(self.screen_form)

    def add_container(self, cont, tag):
        """Añadir pestañas a la interfaz. Cada pestaña es un area de trabajo diferente"""
        cont += 1  # Contador de pestañas
        tag += 1  # Etiqueta pestaña
        container_new = Container((self.pos_workspace[0], self.pos_workspace[1]-30), cont, tag)
        self.elementos['pestañas'].add(container_new)
        for pestaña in self.elementos['pestañas']:  # Verifica cuales pestañas no estan seleccionad
            if cont != pestaña.cont:
                pestaña.selected = False
        return cont, tag

    def delete_container(self, position, cont):
        """Eliminar pestaña deseada"""
        if len(self.elementos['pestañas']) > 1:
            for pestaña in self.elementos['pestañas']:
                if pestaña.recta_close.collidepoint(position):
                    print(pestaña.name)
                    self.elementos['pestañas'].remove(pestaña)
                    cont -= 1
                    for pes in self.elementos['pestañas']:  # En caso de eliminarse una se renombran las demas
                        if pes.cont > pestaña.cont:
                            pes.cont -= 1
                            if pestaña.selected:
                                pes.selected = True
                                pestaña.selected = False
        return cont

    def select_container(self, position):
        """Seleccionar pestaña a activar"""
        for pestaña in self.elementos['pestañas']:
            if pestaña.rect.collidepoint(position):
                pestaña.selected = True
                for pest in self.elementos['pestañas']:
                    if pestaña.cont != pest.cont:
                        pest.selected = False

        for option in self.elementos['opciones']:
            if option.rect.collidepoint(position):
                option.active = True
                for opt in self.elementos['opciones']:
                    if option.name != opt.name:
                        opt.active = False

    def check_actions(self, position):
        if self.property_class.connect_rect.collidepoint(position):
            print('conectar')
            print("".join(self.property_class.name.buffer))
        if self.property_class.disconnect_rect.collidepoint(position):
            print('desconectar')
        if self.property_class.rename_rect.collidepoint(position):
            self.actions = [0]*9
            print(self.actions)
            self.actions[6] = 1

    def exec_actions(self, position, abs_position):
        if self.actions[0]:  # Connect
            print('conectar')

        elif self.actions[1]:
            print('desconectar')
        elif self.actions[6]:
            self.property_class.name.active = True
            self.property_class.name_surface(self.screen_form, position)
            if self.property_class.ok_rect.collidepoint(abs_position):
                print("".join(self.property_class.name.buffer))
                for pestaña in self.elementos['pestañas']:
                    if pestaña.selected == True:
                        pestaña.name = "".join(self.property_class.name.buffer)
                        self.property_class.name.buffer = [""]
                self.actions[6] = 0

    def check_text(self, event):
        self.property_class.name.get_event(event)

    def draw_text(self):
        self.property_class.name.update()
        self.property_class.name.draw(self.screen_form)

    def close_elements(self, position):
        if self.property_class.close_name_rect.collidepoint(position):
            self.actions = [0]*9
            self.draw = False

    def execute_pygame(self):
        cont = 1
        tag = 1
        self.draw = False
        position_mouse = (0, 0)
        grid = True  # Rejilla habilitada
        self.property_class = Property()  # Instancia de propiedades
        self.property_class.rect_actions(self.pos_button_action)  # Inicializar rectas de las acciones
        container = Container((self.pos_workspace[0], self.pos_workspace[1]-30), cont, tag)  # Primera pestaña
        self.elementos['pestañas'].add(container)  # Agregar pestaña a lista de pestañas (Dentro de diccionario)
        opciones = ['module', 'plot', 'config']  # Pestañas de opciones disponibles
        for elem, opcion in enumerate(opciones):
            active = True if elem == 0 else False  # Esta activa la pestaña si es la primera opcion
            position = (self.pos_workspace[0]-30, self.pos_workspace[1])
            pestaña_opcion = OptionPanels(opcion, position, elem, active=active)
            self.elementos['opciones'].add(pestaña_opcion)
        close = False
        while not close:
            for event in pygame.event.get():
                if self.draw:
                    self.check_text(event)
                if event.type == pygame.QUIT:
                    close = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position_mouse = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0]:  # Boton izquierdo
                        print('L')
                        if container.recta_new.collidepoint(position_mouse) and cont < 7:  # Agregar pestañas
                            cont, tag = self.add_container(cont, tag)
                        cont = self.delete_container(position_mouse, cont)  # Verificar si alguna pestaña se cierra
                        self.select_container(position_mouse)  # Seleccionar pestaña
                        self.check_actions(position_mouse)
                        self.close_elements(position_mouse)

                    elif pygame.mouse.get_pressed()[2]:  # Boton derecho
                        for pestaña in self.elementos['pestañas']:  # Colision sobre prestañas
                            if pestaña.rect.collidepoint(position_mouse):
                                print('cambiar')
            abs_position = pygame.mouse.get_pos()
            self.screen_form.fill(GRAY)
            self.draw_containers(container, cont)
            self.properties(abs_position)
            self.exec_actions(abs_position, position_mouse)
            if self.actions[6]:
                self.draw_text()
                self.draw = True
            self.clock.tick(60)
            pygame.display.flip()
