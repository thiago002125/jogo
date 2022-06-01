import pygame

class Fighters():
    def __init__(self, x, y,):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.atacando = False
        self.attack_type =  0
        self.vida =  100

    def move(self, largura, altura, surface, target):
        velocidade = 10
        gravidade = 2
        dx = 0
        dy= 0

        # teclas
        key = pygame.key.get_pressed()
        #só consegue executar as ações se não estiver atacando
        if self.atacando ==  False:

            # movimento
            if key[pygame.K_a]:
                dx = -velocidade
            if key[pygame.K_d]:
                dx = velocidade
            # pulo
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True

            #ataque
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                #tipo de ataque
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

        #gravidade
        self.vel_y += gravidade
        dy += self.vel_y
        
        # limite da tela
        if self.rect.left + dx < 0:
            dx = 0 -self.rect.left
        if self.rect.right + dx > largura:
            dx = largura - self.rect.right
        if self.rect.bottom + dy > altura - 110:
            self.vel_y = 0
            self.jump = False
            dy = altura - 110 - self.rect.bottom

        # posição do player
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, target):
        self.atacando = True
        attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.vida -= 10

        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)



    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)