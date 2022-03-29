import pygame as pg
#Separação das configurações em outro arquivo para melhor controle e possiveis modificações.

#Define dimensões da janela do pygame:
largura = 1000
altura = 600

# Gera tela de jogo:
janela = pg.display.set_mode((largura, altura))
pg.display.set_caption('Kung-flu')

# Carrega os sons do jogo:
pg.mixer.init()
assets = {} #Cria dicionário de todos os assets
pg.mixer.music.load('sound/soundtrack.mp3')
pg.mixer.music.set_volume(0.1)
assets['talkei'] = pg.mixer.Sound('sound/bolsok.wav')
assets['shield_on'] = pg.mixer.Sound('sound/definicoes.wav')
assets['shield_on'].set_volume(0.6)
assets['shield_off'] = pg.mixer.Sound('sound/sneeze.wav')
assets['fire_at_will'] = pg.mixer.Sound('sound/fire_at_will.wav')


#Define diferentes possíveis estados de jogo:
QUIT = 0
GAME = 1
INTRO = 2
SCOREBOARD = 3
INSTRUCTIONS = 4


# Carrega as imagens (fundo, obstáculos e personagem):
menu = pg.image.load('imagens/menu.png').convert()
menu = pg.transform.scale(menu, (largura,altura))
assets['menu'] = menu
assets['fundo'] = pg.image.load('imagens/plano de fundo.png').convert()
assets['scoreboard'] = pg.image.load('imagens/scoreboard.png').convert()
assets['scoreboard'] = pg.transform.scale(assets['scoreboard'], (largura,altura))
personagem = pg.image.load('imagens/personagem 1 menor.png').convert_alpha()
personagem = pg.transform.rotozoom(personagem, 0, 0.3)
assets['personagem1'] = personagem
assets['mascara'] = pg.image.load('imagens/bolsonaro_mask.png').convert_alpha()
assets['mascara'] = pg.transform.rotozoom(assets['mascara'], 0, 0.8)
nuv = pg.image.load('imagens/nuvem.png').convert_alpha()
nuv = pg.transform.rotozoom(nuv, 0, 0.5)
assets['nuvem'] = nuv
projetil = pg.image.load('imagens/projetil.png').convert_alpha()
projetil = pg.transform.rotozoom(projetil, 0, 0.05)
assets['projetil'] = projetil
assets['shield'] = pg.image.load('imagens/antiVirus.png').convert_alpha()
assets['shield'] = pg.transform.rotozoom(assets['shield'], 0, 0.2)
assets['obstaculos'] = pg.image.load('imagens/obstaculos/ob02.png').convert_alpha()
assets['obstaculos'] = pg.transform.scale(assets['obstaculos'], (150, 100))
assets['emoji'] = pg.image.load('imagens/emoji.png').convert_alpha()
assets['emoji'] = pg.transform.rotozoom(assets['emoji'], 0, 0.3)
assets['instrucoes'] = pg.image.load('imagens/instrucoes.png').convert()
assets['instrucoes'] = pg.transform.scale(assets['instrucoes'], (largura,altura))