import pygame

class Fighters():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))

    def move(self, largura):
        velocidade = 10
        dx = 0
        dy= 0

        # teclas
        key = pygame.key.get_pressed()

        # movimento
        if key[pygame.K_a]:
            dx = -velocidade
        if key[pygame.K_d]:
            dx = velocidade

        # limite da tela
        if self.rect.left + dx < 0:
            dx = 0 -self.rect.left
        if self.rect.right + dx > largura:
            dx = largura - self.rect.right

        # posição do player
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)