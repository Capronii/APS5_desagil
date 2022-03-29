#Importando as funções das bibliotecas:
from random import randint
import pygame as pg
import json
from settings import *


#Inicializa pygame:
pg.init()
pg.mixer.init()


# Declara classes:
# Classe de obstáculos
class Obstaculo(pg.sprite.Sprite):
    """Define os parâmetros de criação dos obstáculos (vírus), como posição inicial e velocidades x e y.

    Parâmetros: 
    assets: dicionário de todos os sons e imagens carregados no início do jogo.
    """
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['obstaculos']
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura, 2000)
        self.rect.y = randint(0, altura)
        self.speedx = randint(-15, -10)
        self.speedy = randint(-3, 3)

    # Atualiza as posições ao longo do jogo
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se passar do canto da tela: novas posições e velocidades
        if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
            self.rect.x = randint(largura, 2000)
            self.rect.y = randint(0, altura)
            self.speedx = randint(-15, -10)
            self.speedy = randint(-3, 3)

class Shield(pg.sprite.Sprite):
    '''Classe do power-up shield (antivirus):
    
    Parâmetros: 
    assets: dicionário de todos os assets carregados no início do código.
    '''
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets["shield"]
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura*3, largura*5)
        self.rect.y = randint(altura*0.2, altura*0.8)
        self.speedx = randint(-7, -5) #Velocidade horizontal do shield
        self.speedy = 0
        self.assets = assets
    
    # Atualiza posições quando aparece um novo shield
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0:
            self.rect.x = randint(largura*3, largura*5)
            self.rect.y = randint(altura*0.1, altura*0.9)
            self.speedx = randint(-7, -5) #Velocidade horizontal do shield
            self.speedy = 0

# Classe do personagem
class Biroliro(pg.sprite.Sprite):
    """Define a aparência e a movimentação do jogador, englovando também suas diversas habilidades.
    Dentre elas, temos funções que possibilitam o jogador atirar, equipar o power-up antivirus e equipar o power-up rapid fire.
    
    Parâmetros da classe:
    assets: dicionário de todos os assets carregados no início do código.
    """
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['personagem1']
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = 0.1*largura
        self.rect.bottom = altura/2
        self.speedx = 0
        self.speedy = 0
        self.assets = assets

        # Limite de tiros:
        self.ultimo_tiro = pg.time.get_ticks()
        self.delay_tiro = 1000  # Mudar intervalo de tempo entre tiros.

    # Implementa a movimentação do jogador 
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > largura:
            self.rect.right = largura
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > altura:
            self.rect.bottom = altura
        if self.rect.top < 0:
            self.rect.top = 0   

    # Função para o jogador atirar.
    def atirar(self, rapidFire, all_sprites, all_bullets):
        """Função para o jogador atirar.
        
        Parâmetros:
        all_sprites = conjunto de todos os sprites do jogo.
        all_bullets = conjunto de todos os projéteis atirados.
        """
        t = pg.time.get_ticks()
        passados = t - self.ultimo_tiro
        if passados > self.delay_tiro or rapidFire == 1:
            self.ultimo_tiro = t
            # Criar novo tiro
            novo_projetil = Tiro(
                self.assets, self.rect.centery, self.rect.centerx)
            all_sprites.add(novo_projetil)
            all_bullets.add(novo_projetil)
            self.assets['talkei'].play()

    
    def mascara(self,assets):
        # Jogador passa a ter uma proteção para a próxima colisão com obstáculo:
        self.assets = assets
        self.image = assets['mascara']
        self.mask = pg.mask.from_surface(self.image)
    
    
    def tira_mascara(self,assets):
        #Tira mascara ao colidir com obstaculo:
        self.assets =  assets
        self.image = assets['personagem1']
        self.mask = pg.mask.from_surface(self.image)


class Rapid_fire(pg.sprite.Sprite):
    '''Classe do power-up rapid fire (tiros sequencias):
    
    Parâmetros: 
    assets: dicionário de todos os assets carregados no início do código.'''
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.assets = assets
        self.image = assets['emoji']
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura*3, largura*5)
        self.rect.y = randint(altura*0.2, altura*0.8)
        self.speedx = randint(-7, -5) #Velocidade horizontal do shield
        self.speedy = 0
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0:
            self.rect.x = randint(largura*3, largura*5)
            self.rect.y = randint(altura*0.1, altura*0.9)
            self.speedx = randint(-7, -5) #Velocidade horizontal do shield
            self.speedy = 0

# Classe das nuvens (composição do cenário)
class Nuvem(pg.sprite.Sprite):
    '''Define a aparencia e movimentação das nuvens do cenário 
    
    Parâmetros da classe:
    assets: dicionário de todos os assets carregados no início do código.'''
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['nuvem']
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura, 2000)
        self.rect.y = randint(0, altura/3)
        self.speedx = -2

    # Atualiza as posições das nuvens ao passarem da tela
    def update(self):
        self.rect.x += self.speedx
        # Se passar do canto da tela: novas posições e velocidades
        if self.rect.top > altura or self.rect.right < 0:
            self.rect.x = randint(largura, 2000)
            self.rect.y = randint(0, altura/3)

# Classe dos tiros 
class Tiro(pg.sprite.Sprite):
    '''Define a movimentação, a forma e a trajetória do tiro
    
    Parâmetros da classe:
    assets: dicionário de todos os assets carregados no início do código.
      '''
    def __init__(self, assets, centery, centerx):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['projetil']
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.speedx = 15

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > largura:
            self.kill()


# Codigo base para o relógio (placar):
font = pg.font.SysFont("Comic Sans MS", 30)
lugardotexto = (50, 50)
clock = pg.time.Clock()
FPS = 30
minutes = 0
seconds = 0
milliseconds = 0

def salva_tempo(milliseconds):
    """Função que salva o tempo de jogo do jogador logo após sua morte, sendo que o tempo decorrido é considerado sua pontuação.
    O tempo de jogo do jogador é salvo em um diciónario em um arquivo JSON localizado no mesmo diretório do jogo.
    
    Parâmetros:
    milliseconds: quantidade de milisegundos que passou desde que o jogador pressionou ENTER para entrar no jogo.
    """
    with open('highscore.json', 'r') as f:
        dicionario = json.load(f)
        segundos = milliseconds/1000
        dicionario["highscore"].append(segundos)
        dicionario["highscore"].sort(reverse=True)
    with open('highscore.json', 'w') as f:
        a = json.dumps(dicionario)
        f.write(a)


def mostra_tempo():
    #Função que mostra o scoreboard após a morte do jogador, de forma que os maiores tempos são as melhores pontuações
    janela.blit(assets['scoreboard'], (0,0))
    with open("highscore.json", 'r') as f:
        dicionario = json.load(f)
    scoreboard = {}
    lugarY = 130
    if len(dicionario["highscore"]) < 6:
        for i in range(len(dicionario["highscore"])):
            scoreboard["{i}"] = font.render(("{}o: {:.2f} segundos".format((i+1), dicionario["highscore"][i])), True,(255,255,255))
            janela.blit(scoreboard["{i}"], ((largura*0.35), lugarY))
            lugarY += 50
    else: 
        for i in range(6):
            scoreboard["{i}"] = font.render(("{}o: {:.2f} segundos".format((i+1), dicionario["highscore"][i])), True,(255,255,255))
            janela.blit(scoreboard["{i}"], ((largura*0.35), lugarY))
            lugarY += 50
    playAgain = font.render(("Pressione ENTER para jogar novamente"), True, (255,255,255))
    janela.blit(playAgain, (altura/2.55, altura*0.75))
    
    
    # Ao chegar no scoreboard, pode-se fechar a tela ou pressionar return para voltar ao menu do jogo
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return QUIT
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return INTRO
        pg.display.update()
        clock.tick(FPS)

#Loop menu:
def intro_game():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return QUIT
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return GAME
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    return INSTRUCTIONS
        janela.blit(assets['menu'], (0, 0))
        pg.display.update()
        clock.tick(FPS)

#Loop instrucoes
def instrucoes():
    """Explica os possíveis movimentos e diferentes power-ups que podem ser utlizados pelo jogador.

    Inputs do jogador:
    pressionar ESCAPE: leva o jogador de volta ao menu principal.
    pressionar ENTER: leva o jogador direto ao jogo.
    """
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return QUIT
            if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        return GAME
            if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return INTRO
        janela.blit(assets['instrucoes'], (0, 0))
        pg.display.update()
        clock.tick(FPS)

#Função principal do jogo:
def game_run():
    t0 = pg.time.get_ticks() #Grava o tempo inicial do jogo:

    pg.mixer.music.play(loops=-1) #Toca música de fundo em loop infitito.
    all_sprites = pg.sprite.Group()
    all_obstaculos = pg.sprite.Group()
    all_bullets = pg.sprite.Group()
    all_cenary = pg.sprite.Group()
    all_shields = pg.sprite.Group()
    all_emojis = pg.sprite.Group()
    for i in range(3):  #Define a quantidade de nuvens a serem aicionadas no cenário.
        nuvem = Nuvem(assets)
        while pg.sprite.spritecollide(nuvem, all_cenary, False):
            nuvem = Nuvem(assets)
    all_cenary.add(nuvem)
    
    #Inicializa o jogador sem máscara e sem rapid-fire:
    jogador = Biroliro(assets)
    all_sprites.add(jogador)
    comMascara = 0 
    rapidFire = 0
    # Obstáculos:
    for i in range(10):  #quantidade de obstáculos
        obs = Obstaculo(assets)
        all_sprites.add(obs)
        all_obstaculos.add(obs)
        
    #Cria power-up (shield):
    shield = Shield(assets)
    all_shields.add(shield)
    all_sprites.add(shield)

    #Cria power-up (rapid fire):
    rapidFire = Rapid_fire(assets)
    all_sprites.add(rapidFire)
    all_emojis.add(rapidFire)


    def controlaComandos(event):
            if event.type == pg.QUIT:
                return QUIT
            # Movimentação do jogador ao pressionar as setas e atirar com espaço
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    jogador.speedx -= 15
                if event.key == pg.K_RIGHT:
                    jogador.speedx += 15
                if event.key == pg.K_UP:
                    jogador.speedy -= 15
                if event.key == pg.K_DOWN:
                    jogador.speedy += 15
                if event.key == pg.K_SPACE:
                    jogador.atirar(rapidFire, all_sprites, all_bullets)
            #Cancela a movimentação ao o jogador soltar determinada tecla:
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    jogador.speedx += 15
                if event.key == pg.K_RIGHT:
                    jogador.speedx -= 15
                if event.key == pg.K_UP:
                    jogador.speedy += 15
                if event.key == pg.K_DOWN:
                    jogador.speedy -= 15
                    
    #Loop principal:
    while True:
        clock.tick(FPS)
        # Checa eventos:
        for event in pg.event.get():
            controlaComandos(event)

        # Contador: fonte: https://stackoverflow.com/questions/23717803/i-need-to-make-a-stopwatch-with-pygame
        milliseconds = pg.time.get_ticks() - t0

        # Atualiza posição dos obstáculos
        all_cenary.update()
        all_sprites.update()

        #Checa colisões:
        #Colisão entre jogador e obstaculos:
        ai = pg.sprite.spritecollide(
            jogador, all_obstaculos, True, pg.sprite.collide_mask)
        
        #Colisão entre obstáculos e bolhas:
        sabao = pg.sprite.groupcollide(
            all_obstaculos, all_bullets, True, True, pg.sprite.collide_mask)
            
        #Colisão entre jogador e shield:
        protecao = pg.sprite.spritecollide(jogador, all_shields, True, pg.sprite.collide_mask)
        
        #Colisao entre jogador e rapid-fire:
        tratra = pg.sprite.spritecollide(jogador, all_emojis, True, pg.sprite.collide_mask)
        #Retira mascara quando há colisão:
        if len(ai) > 0 and comMascara == 1:
            assets['shield_off'].play()
            jogador.tira_mascara(assets)
            comMascara = 0
            shield = Shield(assets)
            all_shields.add(shield)
            all_sprites.add(shield)
            
        #Se não tem máscara, mata jogador:
        elif len(ai) > 0:
            jogador.kill()
            pg.mixer.music.stop()
            salva_tempo(milliseconds)
            return SCOREBOARD
            
        #Mata os obstáculos com os tiros
        for obstaculo in sabao:
            obs = Obstaculo(assets)
            all_sprites.add(obs)
            all_obstaculos.add(obs)
            
        #Equipa shield:
        if len(protecao) > 0:
            jogador.mascara(assets)
            assets['shield_on'].play()
            comMascara = 1
            shield.kill()
        #Liga rapid fire:
        if len(tratra) > 0:
            assets['fire_at_will'].play()
            rapidFire = 1
            timeout = milliseconds
        #Define por quanto tempo o rapid fire ficará ativo:
        if rapidFire == 1:
            if milliseconds - timeout >= 6000: #Modificar para ajustar a duração do rapid fire:
                rapidFire = 0
                rapidFire = Rapid_fire(assets)
                all_sprites.add(rapidFire)
                all_emojis.add(rapidFire)

        #Conta o tempo jogado:
        seconds = (milliseconds//1000)
        #Mostra na janela do jogo o tempo decorrido (pontuação):
        contador = font.render('Tempo decorrido: {}'.format(seconds), True, (255, 255, 255))
        janela.blit(assets['fundo'], (0, 0))
        all_cenary.draw(janela)
        all_sprites.draw(janela)
        janela.blit(contador, lugardotexto)

        pg.display.update()

state = INTRO
while state != QUIT:
    """Loop entre os possíveis estados do jogo, sendo que esse loop é
    quebrado quando o jogador fecha a janela.
    """
    if state == INTRO:
        state = intro_game()
    elif state == INSTRUCTIONS:
        state = instrucoes()
    elif state == GAME:
        state = game_run()
    elif state == SCOREBOARD:
        state = mostra_tempo()


pg.quit()
