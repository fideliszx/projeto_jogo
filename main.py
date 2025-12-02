import pygame
import sys
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH = 800
HEIGHT = 600
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Race - 3 Fases")
relogio = pygame.time.Clock()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (200, 0, 0)
VERDE = (0, 200, 0)
AZUL = (0, 120, 200)
AMARELO = (255, 255, 0)
CINZA = (100, 100, 100)
CINZA_ESCURO = (50, 50, 50)
VERDE_ESCURO = (0, 100, 0)

# Classe para o jogador (carro)
class CarroJogador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 50
        self.altura = 80
        self.velocidade = 8
        self.cor = VERMELHO
        self.vidas = 3
        self.invencivel = False
        self.tempo_invencivel = 0
        
    def desenhar(self):
        # Desenha o carro principal
        pontos_carro = [
            (self.x + self.largura//2, self.y),  # Topo
            (self.x + self.largura, self.y + self.altura//3),  # Direita superior
            (self.x + self.largura, self.y + 2*self.altura//3),  # Direita inferior
            (self.x + self.largura//2, self.y + self.altura),  # Fundo
            (self.x, self.y + 2*self.altura//3),  # Esquerda inferior
            (self.x, self.y + self.altura//3),  # Esquerda superior
        ]
        
        if self.invencivel and pygame.time.get_ticks() % 200 < 100:
            pygame.draw.polygon(tela, AMARELO, pontos_carro)
        else:
            pygame.draw.polygon(tela, self.cor, pontos_carro)
        
        # Janelas do carro
        pygame.draw.rect(tela, AZUL, (self.x + 5, self.y + 10, self.largura - 10, 20))
        pygame.draw.rect(tela, AZUL, (self.x + 5, self.y + 40, self.largura - 10, 20))
        
        # Rodas
        pygame.draw.rect(tela, PRETO, (self.x - 5, self.y + 20, 10, 20))
        pygame.draw.rect(tela, PRETO, (self.x + self.largura - 5, self.y + 20, 10, 20))
        pygame.draw.rect(tela, PRETO, (self.x - 5, self.y + 50, 10, 20))
        pygame.draw.rect(tela, PRETO, (self.x + self.largura - 5, self.y + 50, 10, 20))
        
    def mover(self, direcao):
        if direcao == "esquerda" and self.x > 150:
            self.x -= self.velocidade
        if direcao == "direita" and self.x < WIDTH - self.largura - 150:
            self.x += self.velocidade
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)
        
    def atualizar(self):
        if self.invencivel:
            if pygame.time.get_ticks() - self.tempo_invencivel > 2000:  # 2 segundos
                self.invencivel = False

# Classe para os obstáculos (carros inimigos)
class CarroInimigo:
    def __init__(self, fase):
        self.largura = random.randint(40, 60)
        self.altura = random.randint(70, 90)
        self.x = random.randint(150, WIDTH - self.largura - 150)
        self.y = -self.altura
        
        # Cores diferentes por fase
        if fase == 1:
            self.cor = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            self.velocidade = random.uniform(3, 5)
        elif fase == 2:
            self.cor = (random.randint(150, 255), random.randint(50, 150), random.randint(50, 150))
            self.velocidade = random.uniform(5, 7)
        else:  # Fase 3
            self.cor = (random.randint(50, 150), random.randint(150, 255), random.randint(50, 150))
            self.velocidade = random.uniform(7, 9)
            
    def desenhar(self):
        # Desenha o carro inimigo
        pontos_carro = [
            (self.x + self.largura//2, self.y),  # Topo
            (self.x + self.largura, self.y + self.altura//3),  # Direita superior
            (self.x + self.largura, self.y + 2*self.altura//3),  # Direita inferior
            (self.x + self.largura//2, self.y + self.altura),  # Fundo
            (self.x, self.y + 2*self.altura//3),  # Esquerda inferior
            (self.x, self.y + self.altura//3),  # Esquerda superior
        ]
        
        pygame.draw.polygon(tela, self.cor, pontos_carro)
        
        # Janelas
        pygame.draw.rect(tela, BRANCO, (self.x + 5, self.y + 10, self.largura - 10, 15))
        pygame.draw.rect(tela, BRANCO, (self.x + 5, self.y + 40, self.largura - 10, 15))
        
    def atualizar(self):
        self.y += self.velocidade
        return self.y > HEIGHT
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

# Classe para botões
class Botao:
    def __init__(self, x, y, largura, altura, texto, cor_normal, cor_hover):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_atual = cor_normal
        
    def desenhar(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.cor_atual = self.cor_hover
        else:
            self.cor_atual = self.cor_normal
            
        pygame.draw.rect(tela, self.cor_atual, self.rect, border_radius=10)
        pygame.draw.rect(tela, BRANCO, self.rect, 3, border_radius=10)
        
        fonte = pygame.font.SysFont(None, 36)
        texto_surf = fonte.render(self.texto, True, BRANCO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)
        
    def clique(self, pos):
        return self.rect.collidepoint(pos)

# Classe para gerenciar o jogo
class Jogo:
    def __init__(self):
        self.fase = 1
        self.pontos = 0
        self.estado = "menu"  # menu, jogando, gameover, fase_completa
        self.jogador = CarroJogador(WIDTH//2 - 25, HEIGHT - 100)
        self.inimigos = []
        self.tempo_proximo_inimigo = 0
        self.tempo_fase = 0
        self.tempo_fase_limite = 30000  # 30 segundos por fase
        self.botao_iniciar = Botao(WIDTH//2 - 100, 250, 200, 50, "INICIAR JOGO", VERDE, VERDE_ESCURO)
        self.botao_reiniciar = Botao(WIDTH//2 - 100, 350, 200, 50, "REINICIAR", VERDE, VERDE_ESCURO)
        self.botao_proxima_fase = Botao(WIDTH//2 - 100, 300, 200, 50, "PRÓXIMA FASE", AZUL, (0, 100, 200))
        
    def resetar(self):
        self.fase = 1
        self.pontos = 0
        self.estado = "menu"
        self.jogador = CarroJogador(WIDTH//2 - 25, HEIGHT - 100)
        self.inimigos = []
        self.tempo_proximo_inimigo = 0
        self.tempo_fase = 0
        
    def iniciar_fase(self):
        self.estado = "jogando"
        self.tempo_fase = pygame.time.get_ticks()
        self.inimigos = []
        
    def adicionar_inimigo(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual > self.tempo_proximo_inimigo:
            intervalo = max(500, 1500 - self.fase * 200)  # Intervalo diminui com fases mais altas
            self.tempo_proximo_inimigo = tempo_atual + intervalo
            self.inimigos.append(CarroInimigo(self.fase))
            
    def atualizar(self):
        if self.estado == "jogando":
            # Adiciona inimigos
            self.adicionar_inimigo()
            
            # Atualiza inimigos
            for inimigo in self.inimigos[:]:
                if inimigo.atualizar():
                    self.inimigos.remove(inimigo)
                    self.pontos += 10 * self.fase  # Mais pontos em fases mais altas
                    
            # Verifica colisões
            if not self.jogador.invencivel:
                for inimigo in self.inimigos:
                    if self.jogador.get_rect().colliderect(inimigo.get_rect()):
                        self.jogador.vidas -= 1
                        self.jogador.invencivel = True
                        self.jogador.tempo_invencivel = pygame.time.get_ticks()
                        self.inimigos.remove(inimigo)
                        
                        if self.jogador.vidas <= 0:
                            self.estado = "gameover"
                        break
                            
            # Atualiza jogador
            self.jogador.atualizar()
            
            # Verifica se completou a fase
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_fase > self.tempo_fase_limite:
                if self.fase < 3:
                    self.estado = "fase_completa"
                else:
                    self.estado = "gameover"  # Jogo completo
                    
    def desenhar(self):
        # Desenha fundo da estrada
        tela.fill(VERDE_ESCURO)
        
        # Grama nas laterais
        pygame.draw.rect(tela, VERDE, (0, 0, 150, HEIGHT))
        pygame.draw.rect(tela, VERDE, (WIDTH - 150, 0, 150, HEIGHT))
        
        # Estrada
        pygame.draw.rect(tela, CINZA, (150, 0, WIDTH - 300, HEIGHT))
        
        # Linhas da estrada
        for i in range(0, HEIGHT, 40):
            pygame.draw.rect(tela, AMARELO, (WIDTH//2 - 5, i, 10, 20))
            
        if self.estado == "menu":
            # Título
            fonte_titulo = pygame.font.SysFont(None, 72)
            titulo = fonte_titulo.render("CORRIDA MALUCA", True, BRANCO)
            tela.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 100))
            
            # Subtítulo
            fonte_sub = pygame.font.SysFont(None, 36)
            subtitulo = fonte_sub.render("3 FASES DESAFIADORAS", True, AMARELO)
            tela.blit(subtitulo, (WIDTH//2 - subtitulo.get_width()//2, 180))
            
            # Instruções
            fonte_inst = pygame.font.SysFont(None, 28)
            instrucoes = [
                "Use ← → para mover o carro",
                "Desvie dos carros inimigos",
                "Complete 30 segundos em cada fase",
                f"Fase atual: {self.fase}"
            ]
            
            for i, texto in enumerate(instrucoes):
                inst_surf = fonte_inst.render(texto, True, BRANCO)
                tela.blit(inst_surf, (WIDTH//2 - inst_surf.get_width()//2, 400 + i * 40))
                
            self.botao_iniciar.desenhar()
            
        elif self.estado == "jogando":
            # Desenha jogador
            self.jogador.desenhar()
            
            # Desenha inimigos
            for inimigo in self.inimigos:
                inimigo.desenhar()
                
            # HUD
            fonte = pygame.font.SysFont(None, 36)
            
            # Pontos
            pontos_texto = fonte.render(f"Pontos: {self.pontos}", True, BRANCO)
            tela.blit(pontos_texto, (20, 20))
            
            # Fase
            fase_texto = fonte.render(f"Fase: {self.fase}/3", True, BRANCO)
            tela.blit(fase_texto, (WIDTH - 150, 20))
            
            # Vidas
            vidas_texto = fonte.render(f"Vidas: {self.jogador.vidas}", True, BRANCO)
            tela.blit(vidas_texto, (20, 60))
            
            # Tempo
            tempo_atual = pygame.time.get_ticks()
            tempo_restante = max(0, self.tempo_fase_limite - (tempo_atual - self.tempo_fase))
            segundos = tempo_restante // 1000
            tempo_texto = fonte.render(f"Tempo: {segundos}s", True, BRANCO)
            tela.blit(tempo_texto, (WIDTH - 150, 60))
            
            # Dificuldade da fase
            dificuldade_texto = fonte.render(f"Dificuldade: {'Fácil' if self.fase == 1 else 'Médio' if self.fase == 2 else 'Difícil'}", True, BRANCO)
            tela.blit(dificuldade_texto, (WIDTH//2 - dificuldade_texto.get_width()//2, 20))
            
        elif self.estado == "fase_completa":
            # Fundo semitransparente
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 200))
            tela.blit(s, (0, 0))
            
            fonte_titulo = pygame.font.SysFont(None, 64)
            titulo = fonte_titulo.render(f"FASE {self.fase} COMPLETA!", True, VERDE)
            tela.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 150))
            
            fonte = pygame.font.SysFont(None, 48)
            pontos_texto = fonte.render(f"Pontuação: {self.pontos}", True, BRANCO)
            tela.blit(pontos_texto, (WIDTH//2 - pontos_texto.get_width()//2, 230))
            
            if self.fase < 3:
                self.botao_proxima_fase.desenhar()
            else:
                parabens = fonte.render("PARABÉNS! VOCÊ COMPLETOU O JOGO!", True, AMARELO)
                tela.blit(parabens, (WIDTH//2 - parabens.get_width()//2, 300))
                self.botao_reiniciar.desenhar()
                
        elif self.estado == "gameover":
            # Fundo semitransparente
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 200))
            tela.blit(s, (0, 0))
            
            fonte_titulo = pygame.font.SysFont(None, 72)
            
            if self.jogador.vidas <= 0:
                titulo = fonte_titulo.render("GAME OVER", True, VERMELHO)
            else:
                titulo = fonte_titulo.render("JOGO COMPLETO!", True, VERDE)
                
            tela.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 150))
            
            fonte = pygame.font.SysFont(None, 48)
            pontos_texto = fonte.render(f"Pontuação Final: {self.pontos}", True, BRANCO)
            tela.blit(pontos_texto, (WIDTH//2 - pontos_texto.get_width()//2, 250))
            
            fase_texto = fonte.render(f"Fase alcançada: {self.fase}/3", True, BRANCO)
            tela.blit(fase_texto, (WIDTH//2 - fase_texto.get_width()//2, 300))
            
            self.botao_reiniciar.desenhar()

# Função principal
def main():
    jogo = Jogo()
    executando = True
    
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if jogo.estado == "menu":
                    if jogo.botao_iniciar.clique(pos):
                        jogo.iniciar_fase()
                        
                elif jogo.estado == "fase_completa":
                    if jogo.botao_proxima_fase.clique(pos) and jogo.fase < 3:
                        jogo.fase += 1
                        jogo.iniciar_fase()
                    elif jogo.fase >= 3 and jogo.botao_reiniciar.clique(pos):
                        jogo.resetar()
                        
                elif jogo.estado == "gameover":
                    if jogo.botao_reiniciar.clique(pos):
                        jogo.resetar()
                        
            # Controles do jogador
            if jogo.estado == "jogando":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT:
                        jogo.jogador.mover("esquerda")
                    if evento.key == pygame.K_RIGHT:
                        jogo.jogador.mover("direita")
                        
        # Controles contínuos
        if jogo.estado == "jogando":
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                jogo.jogador.mover("esquerda")
            if teclas[pygame.K_RIGHT]:
                jogo.jogador.mover("direita")
                
        jogo.atualizar()
        jogo.desenhar()
        
        pygame.display.flip()
        relogio.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()