import pygame

class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
    self.player = player
    self.size = data[0]
    self.image_scale = data[1]
    self.offset = data[2]
    self.flip = flip
    self.animation_list = self.load_images(sprite_sheet, animation_steps)
    self.action = 0#0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180))
    self.vel_y = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.attack_type = 0
    self.attack_cooldown = 0
    self.attack_sound = sound
    self.hit = False
    self.health = 100
    self.alive = True


  def load_images(self, sprite_sheet, animation_steps):
    #extrair os sprites
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
      animation_list.append(temp_img_list)
    return animation_list


  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED = 10
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    #tecla pressionada
    key = pygame.key.get_pressed()

    #executa ações somente quando não está atacando
    if self.attacking == False and self.alive == True and round_over == False:
      #controles do player 1
      if self.player == 1:
        #movimento
        if key[pygame.K_a]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_d]:
          dx = SPEED
          self.running = True
        #pulo
        if key[pygame.K_w] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #ataque
        if key[pygame.K_r] or key[pygame.K_t]:
          self.attack(target)
          #determina o tipo de ataque que será usado
          if key[pygame.K_r]:
            self.attack_type = 1
          if key[pygame.K_t]:
            self.attack_type = 2

######################### PLAYER 1 #############################
######## MOVIMENTAÇÃO / A(ESQUERDA) W(PULO) D(DIREITA) #########
######## ATAQUE / R(ATAQUE 1) T(ATAQUE 2) ########################

      #controles do player 2
      if self.player == 2:
        #movimento
        if key[pygame.K_LEFT]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_RIGHT]:
          dx = SPEED
          self.running = True
        #pulo
        if key[pygame.K_UP] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #ataque
        if key[pygame.K_KP1] or key[pygame.K_KP2]:
          self.attack(target)
          #determina o tipo de ataque que será usado
          if key[pygame.K_KP1]:
            self.attack_type = 1
          if key[pygame.K_KP2]:
            self.attack_type = 2

##################################### PLAYER 2 ######################################
######## MOVIMENTAÇÃO / SETA P/ ESQUERDA SETA P/ CIMA(PULO) SETA P/ DIREITA #########
######## ATAQUE / TECLA NUMÉRICA 1(ATAQUE 1) TECLA NUMÉRICA 2(ATAQUE 2) #############

    #aplica gravidade
    self.vel_y += GRAVITY
    dy += self.vel_y

    #garante que o personagem fique na tela
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #garante que os personagens fiquem de frente um para o outro
    if target.rect.centerx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True

    #cooldown de ataque
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    #atualiza a posição do personagem
    self.rect.x += dx
    self.rect.y += dy


  #atualização das animações
  def update(self):
    #verifica a ação que o personagem está executando
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:death
    elif self.hit == True:
      self.update_action(5)#5:hit
    elif self.attacking == True:
      if self.attack_type == 1:
        self.update_action(3)#3:attack1
      elif self.attack_type == 2:
        self.update_action(4)#4:attack2
    elif self.jump == True:
      self.update_action(2)#2:jump
    elif self.running == True:
      self.update_action(1)#1:run
    else:
      self.update_action(0)#0:idle

    animation_cooldown = 50
    #atualiza imagem
    self.image = self.animation_list[self.action][self.frame_index]
    #verifica o tempo passado desde a última atualização
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #verifica se a ação terminou
    if self.frame_index >= len(self.animation_list[self.action]):
      #verifica se o player está morto ao final da animação
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #verifica se o ataque foi executado
        if self.action == 3 or self.action == 4:
          self.attacking = False
          self.attack_cooldown = 20
        #verifica se o dano foi causado
        if self.action == 5:
          self.hit = False
          #bloqueio de ataque enquanto o outro player está atacando
          self.attacking = False
          self.attack_cooldown = 20


  def attack(self, target):
    if self.attack_cooldown == 0:
      #execução de ataque
      self.attacking = True
      self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        target.health -= 10
        target.hit = True


  def update_action(self, new_action):
    #verifica se a nova ação é diferente da anterior
    if new_action != self.action:
      self.action = new_action
      #atualiza as configurações de animação
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))