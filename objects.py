import pygame
import os


class Init(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('pics', 'init.png'))
        self.rect = self.image.get_rect()
        self.rect.center = [position[0], position[1]]
        self.font = pygame.font.SysFont('Arial', 14)
        self.tag = "Inicio"
        self.pos = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]-10, self.pos[1]+20))


class End(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('pics', 'end.png'))
        self.rect = self.image.get_rect()
        self.rect.center = [position[0], position[1]]
        self.font = pygame.font.SysFont('Arial', 14)
        self.tag = "Fin"
        self.pos = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]-10, self.pos[1]+20))
