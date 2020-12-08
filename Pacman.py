import pygame

#Definindo algumas cores para facilitar
preto = (0,0,0) 
branco = (255,255,255)
azul = (0,0,255)
vermelho = (255,0,0)
amarelo = (255,255,0)


#carregando a imagem do icone da aba
pacman = pygame.image.load('images/pacman.png') 
pygame.display.set_icon(pacman)

#Criando uma classe para as paredes, e parametros para as gerar facilmente
class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# Criando todas as paredes
def setuptabuleiro(all_sprites_list):
    # Criando as paredes (Lista)
    Paredes_lista=pygame.sprite.RenderPlain()
     
    #Lista de posição e tamanho das paredes[x, y, width, height]
    paredes = [ [0,0,6,600],[0,0,600,6],[0,600,606,6],
              [600,0,6,606],[300,0,6,66],[60,60,186,6],
              [360,60,186,6],[60,120,66,6],[60,120,6,126],
              [180,120,246,6],[300,120,6,66],[480,120,66,6],
              [540,120,6,126],[120,180,126,6],[120,180,6,126],
              [360,180,126,6],[480,180,6,126],[180,240,6,126],
              [180,360,246,6],[420,240,6,126],[240,240,42,6],
              [324,240,42,6],[240,240,6,66],[240,300,126,6],
              [360,240,6,66],[0,300,66,6],[540,300,66,6],
              [60,360,66,6],[60,360,6,186],[480,360,66,6],
              [540,360,6,186],[120,420,366,6],[120,420,6,66],
              [480,420,6,66],[180,480,246,6],[300,480,6,66],
              [120,540,126,6],[360,540,126,6]
            ]
     
    # Loop na lista de paredes
    for item in paredes:
        wall = Wall(item[0], item[1], item[2], item[3], vermelho)
        Paredes_lista.add(wall)
        all_sprites_list.add(wall)
         
    # Retornando a lista de paredes
    return Paredes_lista

#Renderizando a porta da caixa de fantasmas
def setupporta(all_sprites_list):
      porta = pygame.sprite.RenderPlain()
      porta.add(Wall(282,242,42,2,azul)) 
      all_sprites_list.add(porta)
      return porta

# Classe que representa a bola      
class Block(pygame.sprite.Sprite):
     
    #Contrutor que passa cores e tamanhos
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        
        #Aqui este "bloco" é criado
        self.image = pygame.Surface([width, height])
        self.image.fill(branco)
        self.image.set_colorkey(branco)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
        self.rect = self.image.get_rect() 

#Criando a classe player
class Player(pygame.sprite.Sprite):
  
    # Ajustando a velocidade
    change_x=0
    change_y=0
  
    #Função de construtor
    def __init__(self,x,y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Ajustando altura e largura das imagens
        self.image = pygame.image.load(filename).convert()
  
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Limpando a velocidade do player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Mudando a velocidade do jogador
    def changespeed(self,x,y):
        self.change_x += x
        self.change_y += y
          
    # Encontrando nova posição para o jogador
    def update(self,paredes,porta):
        #mantendo a posição antiga, em caso de necessidade
        old_x=self.rect.left
        new_x=old_x+self.change_x
        prev_x=old_x+self.prev_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        prev_y=old_y+self.prev_y

        # Atualizando para checar as colisoes com as paredes
        x_collide = pygame.sprite.spritecollide(self, paredes, False)
        if x_collide:
            # se encontrar uma parede, volta para a ultima posição registrada
            self.rect.left=old_x
           
        else:

            self.rect.top = new_y

            y_collide = pygame.sprite.spritecollide(self, paredes, False)
            if y_collide:
                # encontrou a parede, volta na antiga posição 
                self.rect.top=old_y

        #trancando a "porta"
        if porta != False:
          porta_hit = pygame.sprite.spritecollide(self, porta, False)
          if porta_hit:
            self.rect.left=old_x
            self.rect.top=old_y

#Criando a classe Ghost
class Ghost(Player):
    # Muda a velocidade do fantasma
    def changespeed(self,list,ghost,turn,steps,l):
      try:
        z=list[turn][2]
        if steps < z:
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps+=1
        else:
          if turn < l:
            turn+=1
          elif ghost == "clyde":
            turn = 2
          else:
            turn = 0
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps = 0
        return [turn,steps]
      except IndexError:
         return [0,0]
        
#Aqui, sao gerados os movimentos dos fantasmas, que os seguem aleatoriamente
Pinky_directions = [
[0,-30,4],[15,0,9],[0,15,11],
[-15,0,23],[0,15,7],[15,0,3],
[0,-15,3],[15,0,19],[0,15,3],
[15,0,3],[0,15,3],[15,0,3],
[0,-15,15],[-15,0,7],[0,15,3],
[-15,0,19],[0,-15,11],[15,0,9]
]

Blinky_directions = [
[0,-15,4],[15,0,9],[0,15,11],
[15,0,3],[0,15,7],[-15,0,11],
[0,15,3],[15,0,15],[0,-15,15],
[15,0,3],[0,-15,11],[-15,0,3],
[0,-15,11],[-15,0,3],[0,-15,3],
[-15,0,7],[0,-15,3],[15,0,15],
[0,15,15],[-15,0,3],[0,15,3],
[-15,0,3],[0,-15,7],[-15,0,3],
[0,15,7],[-15,0,11],[0,-15,7],
[15,0,5]]

Inky_directions = [
[30,0,2],[0,-15,4],[15,0,10],
[0,15,7],[15,0,3],[0,-15,3],
[15,0,3],[0,-15,15],[-15,0,15],
[0,15,3],[15,0,15],[0,15,11],
[-15,0,3],[0,-15,7],[-15,0,11],
[0,15,3],[-15,0,11],[0,15,7],
[-15,0,3],[0,-15,3],[-15,0,3],
[0,-15,15],[15,0,15],[0,15,3],
[-15,0,15],[0,15,11],[15,0,3],
[0,-15,11],[15,0,11],[0,15,3],
[15,0,1]]

pl = len(Pinky_directions)-1
bl = len(Blinky_directions)-1
il = len(Inky_directions)-1


# Aqui, se inicia o pygame
pygame.init()
  
# Aqui foi criada uma tela de 606 por 606
screen = pygame.display.set_mode([606, 606])


# Criando o titulo da janela
pygame.display.set_caption('Pacman, by Bergamo e Emily')

# Criando uma superficie para desenhar
background = pygame.Surface(screen.get_size())

# Convertendo a cor
background = background.convert()
  
# Prenchendo a tela de preto 
background.fill(preto)

#Definindo um clock para o jogo 
clock = pygame.time.Clock()

# Adicionando uma fonte diferente
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

#Criando as localizações originais para os fantasmas e para o pacman
w = 303-16 #Largura
p_h = (7*60)+19 #Altura do pacman
m_h = (4*60)+19 #Altura dos fantasmas
b_h = (3*60)+19 #Altura do Blinky
i_w = 303-16-32 #Altura do inky
p_w = 303+(32-16)# Altura do pinky

#Renderizando os paramentros para começar o jogo 
def startGame():

  all_sprites_list = pygame.sprite.RenderPlain()
  block_list = pygame.sprite.RenderPlain()
  monsta_list = pygame.sprite.RenderPlain()
  pacman_collide = pygame.sprite.RenderPlain()
  wall_list = setuptabuleiro(all_sprites_list)
  porta = setupporta(all_sprites_list)
  p_turn = 0
  p_steps = 0
  b_turn = 0
  b_steps = 0
  i_turn = 0
  i_steps = 0

  #Iniciando os sprites(pacman, e fantasmas)
  Pacman = Player( w, p_h, "images/pacman.png" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
   
  Blinky=Ghost( w, b_h, "images/Blinky.png" )
  monsta_list.add(Blinky)
  all_sprites_list.add(Blinky)

  Pinky=Ghost( w, m_h, "images/Pinky.png" )
  monsta_list.add(Pinky)
  all_sprites_list.add(Pinky)
   
  Inky=Ghost( i_w, m_h, "images/Inky.png" )
  monsta_list.add(Inky)
  all_sprites_list.add(Inky)
   

  # Desenhando o tabuleiro
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(amarelo, 4, 4)
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)
  score = 0
  done = False
  i = 0
  while done == False:
      #Processamentos de eventos do jogo
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,-30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,30)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-30)
          
      
   
      #Aqui toda a logica do jogo entra em pratica
      Pacman.update(wall_list,porta)

      returned = Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      p_turn = returned[0]
      p_steps = returned[1]
      Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      Pinky.update(wall_list,False)

      returned = Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      b_turn = returned[0]
      b_steps = returned[1]
      Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      Blinky.update(wall_list,False)

      returned = Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      i_turn = returned[0]
      i_steps = returned[1]
      Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      Inky.update(wall_list,False)

      # Checando se o bloco colide em algo 
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
       
      # Checando todas as colisoes
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      
      # Desenhando todos os elementos na tela
      screen.fill(preto)
      wall_list.draw(screen)
      porta.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)

      #Aqui foi feita a tabela de pontuação do jogo 
      text=font.render("Pontuação: "+str(score)+"/"+str(bll), True, azul)
      screen.blit(text, [10, 10])

      #Aqui foi feita a instrução do jogo
      text=font.render("Use as setas para se mover", True, azul)
      screen.blit(text, [10, 570])

      if score == bll:
        doNext("Voce venceu!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,porta)

      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

      if monsta_hit_list:
        doNext("Fim de jogo",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,porta)

      pygame.display.flip()
      clock.tick(10) #Definindo o clock 

#Função para dar continuidade aos eventos
def doNext(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,porta):
  while True:
      # O processamento do jogo 
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del pacman_collide
            del wall_list
            del porta
            startGame()

      #Ganhar ou perder
      text1=font.render(message, True, branco)
      screen.blit(text1, [left, 233])

      text2=font.render("Para jogar denovo,aperte ENTER.", True, branco)
      screen.blit(text2, [100, 303])
      text3=font.render("Para sair, aperte ESC.", True, branco)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)

startGame()

pygame.quit()
