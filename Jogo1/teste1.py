import pygame
from fighters import Fighters

pygame.init()

# janela
largura = 1000
altura = 600

# framerate
clock = pygame.time.Clock()
FPS = 60

screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Nome do Jogo')

# backgroud
bg_image = pygame.image.load("assets/imagens/background/bg2.png").convert_alpha()

# funçao do background
def draw_bg():
    escala_bg = pygame.transform.scale(bg_image, (largura, altura))
    screen.blit(escala_bg, (0, 0))

# instancias 
lutador_1 = Fighters(200, 310)
lutador_2 = Fighters(700, 310)

# loop
run = True
while run:

    clock.tick(FPS)

    # background
    draw_bg()

    # movimentação
    lutador_1.move(largura, altura)
    #lutador_2.move(largura, altura)

    # lutadores
    lutador_1.draw(screen)
    lutador_2.draw(screen)


    # eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.update()

# sair do pygame
pygame.quit()
