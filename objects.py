import pygame
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Init(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('pics', 'init.png'))
        self.rect = self.image.get_rect()
        self.rect.center = [position[0], position[1]]
        self.font = pygame.font.SysFont('Arial', 14)
        self.tag = "Inicio"
        self.pos = position
        self.nodo = Nodo((self.pos[0]+40, self.pos[1]), 1, self.tag)
        self.con = [[self.pos[0], self.pos[1]], [self.pos[0]+40, self.pos[1]]]
        self.conexiones = pygame.sprite.Group()  # Conexiones anexas al elemento

    def draw(self, screen):
        pygame.draw.aaline(screen, BLACK, self.con[0], self.con[1])
        screen.blit(self.image, self.rect)
        screen.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]-10, self.pos[1]+20))
        self.nodo.draw(screen)


class End(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('pics', 'end.png'))
        self.rect = self.image.get_rect()
        self.rect.center = [position[0], position[1]]
        self.font = pygame.font.SysFont('Arial', 14)
        self.tag = "Fin"
        self.pos = position
        self.nodo = Nodo((self.pos[0] - 40, self.pos[1]), 1, self.tag)
        self.con = [[self.pos[0], self.pos[1]], [self.pos[0] - 40, self.pos[1]]]
        self.conexiones = pygame.sprite.Group()  # Conexiones anexas al elemento

    def draw(self, screen):
        pygame.draw.aaline(screen, BLACK, self.con[0], self.con[1])
        screen.blit(self.image, self.rect)
        screen.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]-10, self.pos[1]+20))
        self.nodo.draw(screen)


class Caja(pygame.sprite.Sprite):
    def __init__(self, pos, cont, name=""):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('pics', 'caja.png'))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.tag = name+'Caja_'+str(cont)
        self.id = cont
        self.name = name
        self.font = pygame.font.SysFont('Arial', 14)
        self.pos = pos
        self.conexiones = pygame.sprite.Group()  # Conexiones anexas al elemento
        self.id_con = list()  # Id de conexiones anexas a la caja
        self.con_limite = list()  # Puntos de conexion que tocan la caja
        self.mod = 'exp'
        self.orientation = 1  # Define donde van los nodos. Solo se permite para cajas individuales
        self.enable = 'H'
        self.alpha = '1'
        self.betha = '1'
        self.nodos = pygame.sprite.Group()
        self.nodos.add(Nodo((self.pos[0] - 20, self.pos[1] + 40), 1, self.tag))
        self.nodos.add(Nodo((self.pos[0] + 100, self.pos[1] + 40), 2, self.tag))

    def calc_nodes(self):
        self.nodos = pygame.sprite.Group()
        self.nodos.add(Nodo((self.pos[0] - 20, self.pos[1] + 40), 1, self.tag))
        self.nodos.add(Nodo((self.pos[0] + 100, self.pos[1] + 40), 2, self.tag))

    def draw(self, screen):
        """Dibujar elemento sobre superficie"""
        if self.name == "":
            for nodo in self.nodos:
                pygame.draw.aaline(screen, BLACK, (self.pos[0]+40, nodo.pos[1]), nodo.pos)
                nodo.draw(screen)
        screen.blit(self.image, self.rect)
        screen.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]+10, self.pos[1] + 80))
        self.surf_text = pygame.Surface((50, 22))
        self.surf_text.fill(BLACK)
        self.image = pygame.image.load(os.path.join('pics', 'caja.png'))
        if self.mod == "exp":
            self.betha = str(1)
            self.image.blit(self.surf_text, (20, 25))
            screen.blit(self.font.render('a', True, (0, 0, 0)), (self.pos[0]+10, self.pos[1]+27))
            screen.blit(self.font.render(self.alpha, True, WHITE), (self.pos[0] + 25, self.pos[1] + 27))
        elif self.mod == "ray":
            self.betha = str(2)
            self.image.blit(self.surf_text, (20, 25))
            screen.blit(self.font.render('a', True, (0, 0, 0)), (self.pos[0] + 10, self.pos[1] + 27))
            screen.blit(self.font.render(self.alpha, True, WHITE), (self.pos[0] + 25, self.pos[1] + 27))
        elif self.mod == "wei":
            self.image.blit(self.surf_text, (20, 15))
            self.image.blit(self.surf_text, (20, 45))
            screen.blit(self.font.render('a', True, (0, 0, 0)), (self.pos[0]+10, self.pos[1]+17))
            screen.blit(self.font.render('b', True, (0, 0, 0)), (self.pos[0]+10, self.pos[1]+47))
            screen.blit(self.font.render(self.alpha, True, WHITE), (self.pos[0] + 25, self.pos[1] + 17))
            screen.blit(self.font.render(self.betha, True, WHITE), (self.pos[0] + 25, self.pos[1] + 47))
        self.calc_nodes()

    def type(self):
        pass


class Knn(pygame.sprite.Sprite):
    def __init__(self, pos, cont, num_rows=2):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('Arial', 14)
        self.image = pygame.image.load(os.path.join('pics', 'knn_back.png'))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]+24
        self.rect.y = pos[1]-20
        self.cont = cont
        self.tag = 'KNN_'+str(cont)
        self.pos = pos
        self.aum = 0
        self.rest_h = pos[1]+200  # Donde s
        self.max_h = 670  # Maximo permitido para dibujar
        self.cajas_fin = 100  # Donde esta la ultima caja
        self.enable = 1
        self.con_der_ini = [(self.pos[0]+100, self.pos[1]+40), (self.pos[0]+120, self.pos[1]+40), (self.pos[0]+120, self.pos[1]+140)]
        self.con_der_fin = [(self.pos[0]+120, self.pos[1]+40), (self.pos[0]+120, self.pos[1]+140), (self.pos[0]+100, self.pos[1]+140)]
        self.con_izq_ini = [(self.pos[0]+20, self.pos[1]+40), (self.pos[0], self.pos[1]+40), (self.pos[0], self.pos[1]+140)]
        self.con_izq_fin = [(self.pos[0], self.pos[1]+40), (self.pos[0], self.pos[1]+140), (self.pos[0]+20, self.pos[1]+140)]
        self.num_rows = num_rows  # Indica el numero de paralelos. Cada paralelo tiene su propio número de elementos en serie
        self.cols = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                     pygame.sprite.Group()]  # En orden, cada indice representa un nivel del paralelo.
        self.dt = 100  # Define la distancia entre cajas. Altura de cada adicion
        self.left = [[0, 0], [0, 0]]
        self.right = [[0, 0], [0, 0]]
        self.up = [[0, 0], [0, 0]]
        self.down = [[0, 0], [0, 0]]
        self.node_dt = 40  # Indica cuanto se desplaza el nodo principal
        for ind, value in enumerate(range(self.num_rows)):
            self.cols[value].add(Caja((pos[0]+20, pos[1]+value*self.dt), 1, name=self.tag+"_"+str(ind)))
        self.calc_num_cols()  # Indica el maximo de paralelos existente
        self.calc_lines()
        self.calc_nodes()  # Determinar posiciones de los nodos
        self.conexiones = pygame.sprite.Group()  # Conexiones anexas al elemento

    def calc_num_cols(self):
        """Calcula el maximo de columnas existentes (elementos en serie en una o varias lineas)"""
        self.num_cols = 1
        for col in self.cols:
            if len(col) > self.num_cols:
                self.num_cols = len(col)
        self.rect.x = self.pos[0] + (24 * self.num_cols)

    def calc_nodes(self):
        height_nodes = self.pos[1]+self.node_dt*self.num_rows+20
        self.nodos = pygame.sprite.Group()
        self.nodos.add(Nodo((self.up[0][0], height_nodes), 1, self.tag))
        self.nodos.add(Nodo((self.up[1][0], height_nodes), 2, self.tag))

    def calc_lines(self):
        """Calcula las posiciones para las lineas tanto horizontales como verticales"""
        for index, col in enumerate(self.cols):
            if index == 0:
                for caja in col:
                    if caja.id == 1:
                        for nodo in caja.nodos:
                            if nodo.id == 1:  # Posicion de arriba
                                self.up[0][1] = nodo.pos[1]
                                self.up[1][1] = nodo.pos[1]
            if index == self.num_rows-1:
                for caja in col:
                    if caja.id == 1:
                        for nodo in caja.nodos:
                            if nodo.id == 1:  # Posicion de abajo
                                self.down[0][1] = nodo.pos[1]
                                self.down[1][1] = nodo.pos[1]
            if len(col) == self.num_cols:  # Mediante esta condicion se encuentra la fila que contenga mas cajas, esta determinara la distancia de los nodos
                for caja in col:
                    if caja.id == 1:
                        for nodo in caja.nodos:
                            if nodo.id == 1:
                                self.up[0][0] = nodo.pos[0]  # Primer posicion de la izquierda
                                self.down[0][0] = nodo.pos[0]
                    if caja.id == self.num_cols:
                        for nodo in caja.nodos:
                            if nodo.id == 2:
                                self.up[1][0] = nodo.pos[0]  # Posicion de la derecha
                                self.down[1][0] = nodo.pos[0]
        self.left = []
        self.right = []
        for row in (range(self.num_rows)):
            self.left.append([self.up[0][0], self.up[0][1]+self.dt*row])
            self.right.append([self.up[1][0], self.up[1][1]+self.dt*row])

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0] + 38, self.pos[1] - 20))
        for ini, fin in zip(self.up, self.down):
            pygame.draw.aaline(screen, BLACK, ini, fin)
        for ini, fin in zip(self.left, self.right):
            pygame.draw.aaline(screen, BLACK, ini, fin)
        for col in self.cols:
            for caja in col:
                caja.draw(screen)
        for nodo in self.nodos:
            nodo.draw(screen)
        self.calc_num_cols()
        self.calc_lines()
        self.calc_nodes()


class Stand(pygame.sprite.Sprite):
    def __init__(self, pos, cont, num_rows=2):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('Arial', 14)
        self.image = pygame.image.load(os.path.join('pics', 'stand.png'))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]+35
        self.cont = cont
        self.tag = 'StandBy_' + str(cont)
        self.pos = pos
        self.num_rows = num_rows
        self.cajas = pygame.sprite.Group()
        self.node_dt = 100
        for ind in range(num_rows):
            self.cajas.add(Caja((pos[0]+80, pos[1]+self.node_dt*ind), ind+1, name=self.tag+'_'))
        self.nodos = pygame.sprite.Group()
        self.calc_lines()
        self.calc_nodes()
        self.conexiones = pygame.sprite.Group()  # Conexiones anexas al elemento

    def calc_nodes(self):
        height_nodes = (self.pos[1]+self.node_dt*(self.num_rows-1))-(20*(self.num_rows-1))
        self.nodos = pygame.sprite.Group()
        self.nodos.add(Nodo((self.pos[0]-20, self.pos[1]+80), 1, self.tag))
        self.nodos.add(Nodo((self.pos[0]+180, height_nodes), 2, self.tag))

    def calc_lines(self):
        self.line_ini = [[self.pos[0]+180, self.pos[1]+40], [self.pos[0]+160, self.pos[1]+40],
                         [self.pos[0]+160, (self.pos[1]+40)+self.node_dt*(self.num_rows-1)],
                         [self.pos[0]-20, self.pos[1]+80]]
        self.line_end = [[self.pos[0]+180, (self.pos[1]+40)+self.node_dt*(self.num_rows-1)],
                         [self.pos[0]+180, self.pos[1]+40], [self.pos[0]+180,
                                                             (self.pos[1]+40)+self.node_dt*(self.num_rows-1)],
                         [self.pos[0], self.pos[1]+80]]

    def draw(self, screen):
        screen.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]-10, self.pos[1]+100))
        screen.blit(self.image, self.rect)
        for caja in self.cajas:
            caja.draw(screen)
        for ini, fin in zip(self.line_ini, self.line_end):
            pygame.draw.aaline(screen, BLACK, ini, fin)
        for nodo in self.nodos:
            nodo.draw(screen)
        self.calc_lines()
        self.calc_nodes()


class Nodo(pygame.sprite.Sprite):
    def __init__(self, pos, cont, name_element):
        pygame.sprite.Sprite.__init__(self)
        self.name_element = name_element  # Este debe renombrarse a la par con el elemento que se encuentra conectado
        self.pos = pos
        self.image_on = pygame.image.load(os.path.join('pics', 'nodo_on.png'))
        self.image_off = pygame.image.load(os.path.join('pics', 'nodo_off.png'))
        self.rect = self.image_on.get_rect()
        self.rect.center = [pos[0], pos[1]]
        self.tag = 'Nodo_'+str(cont)
        self.recta_trabajo = pygame.Rect(80, 170, 760, 480)
        self.id = cont
        self.connected = False

    def draw(self, screen):
        """Dibujar elemento sobre superficie"""
        if self.connected:
            screen.blit(self.image_on, self.rect)
        else:
            screen.blit(self.image_off, self.rect)


class Conexion(pygame.sprite.Sprite):
    def __init__(self, puntos, elem1, elem2):
        pygame.sprite.Sprite.__init__(self)
        self.puntos = puntos
        self.elem1 = elem1
        self.elem2 = elem2  # Este elemento es una etiqueta si pertenece a las conexiones de propiedades, y es un numero si pertence a un elemento

    def draw(self, screen):
        for linea in self.puntos:
            pygame.draw.aaline(screen, BLACK, linea[0], linea[1])
