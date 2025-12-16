import pygame
import sys
import random

pygame.init()

# Tela
WIDTH, HEIGHT = 800, 600
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Corredor Espacial")
clock = pygame.time.Clock()

# Cores
PRETO = (5, 5, 20)
BRANCO = (255, 255, 255)
AZUL = (0, 180, 255)
AZUL_CLARO = (100, 220, 255)
VERMELHO = (220, 60, 60)
AMARELO = (255, 200, 0)
CINZA = (120, 120, 120)
CINZA_ESCURO = (80, 80, 80)

# Estrelas do fundo
estrelas = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(80)]

def desenhar_fundo():
    tela.fill(PRETO)
    for e in estrelas:
        pygame.draw.circle(tela, BRANCO, (e[0], e[1]), e[2])
        e[1] += e[2]
        if e[1] > HEIGHT:
            e[1] = 0
            e[0] = random.randint(0, WIDTH)

# Nave
class Nave:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 90
        self.vel = 8
        self.vidas = 3
        self.inv = False
        self.temp_inv = 0

    def mover(self, d):
        if d == "e" and self.x > 60:
            self.x -= self.vel
        if d == "d" and self.x < WIDTH - 60:
            self.x += self.vel

    def desenhar(self):
        cor = AMARELO if self.inv and pygame.time.get_ticks() % 200 < 100 else AZUL

        # Corpo
        pygame.draw.polygon(tela, cor, [
            (self.x, self.y),
            (self.x - 28, self.y + 65),
            (self.x + 28, self.y + 65)
        ])

        # Cockpit
        pygame.draw.circle(tela, AZUL_CLARO, (self.x, self.y + 30), 8)

        # Propulsão
        pygame.draw.polygon(tela, VERMELHO, [
            (self.x - 10, self.y + 65),
            (self.x + 10, self.y + 65),
            (self.x, self.y + 85)
        ])

    def rect(self):
        return pygame.Rect(self.x - 28, self.y, 56, 80)

    def atualizar(self):
        if self.inv and pygame.time.get_ticks() - self.temp_inv > 2000:
            self.inv = False

# Asteroide
class Asteroide:
    def __init__(self, fase):
        self.x = random.randint(60, WIDTH - 60)
        self.y = -40
        self.r = random.randint(20, 35)
        self.vel = random.randint(3 + fase * 2, 5 + fase * 3)

    def atualizar(self):
        self.y += self.vel
        return self.y > HEIGHT

    def desenhar(self):
        pygame.draw.circle(tela, CINZA, (self.x, self.y), self.r)
        pygame.draw.circle(tela, CINZA_ESCURO, (self.x - 6, self.y - 6), self.r // 3)

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

# Jogo
class Jogo:
    def __init__(self):
        self.estado = "menu"
        self.fase = 1
        self.pontos = 0
        self.nave = Nave()
        self.asts = []
        self.temp_fase = 0
        self.limite = 30000
        self.prox_ast = 0

    def iniciar(self):
        self.estado = "jogando"
        self.temp_fase = pygame.time.get_ticks()
        self.asts = []

    def resetar(self):
        self.__init__()

    def atualizar(self):
        if self.estado == "jogando":
            agora = pygame.time.get_ticks()

            if agora > self.prox_ast:
                self.asts.append(Asteroide(self.fase))
                self.prox_ast = agora + max(400, 1200 - self.fase * 200)

            for a in self.asts[:]:
                if a.atualizar():
                    self.asts.remove(a)
                    self.pontos += 10 * self.fase

            if not self.nave.inv:
                for a in self.asts:
                    if self.nave.rect().colliderect(a.rect()):
                        self.nave.vidas -= 1
                        self.nave.inv = True
                        self.nave.temp_inv = pygame.time.get_ticks()
                        self.asts.remove(a)
                        if self.nave.vidas <= 0:
                            self.estado = "gameover"
                        break

            self.nave.atualizar()

            if agora - self.temp_fase > self.limite:
                if self.fase < 3:
                    self.estado = "fase"
                else:
                    self.estado = "gameover"

    def texto(self, msg, tam, y):
        fonte = pygame.font.SysFont("arial", tam, bold=True)
        txt = fonte.render(msg, True, BRANCO)
        tela.blit(txt, txt.get_rect(center=(WIDTH // 2, y)))

    def desenhar(self):
        desenhar_fundo()

        if self.estado == "menu":
            self.texto("Autor: Luis Gustavo Fidelis", 32,110)
            self.texto("CORREDOR ESPACIAL", 64, 220)
            self.texto("Clique para iniciar", 32, 300)
            self.texto("Use as setas para mover para E/D ", 14, 60)

        elif self.estado == "jogando":

            self.nave.desenhar()
            for a in self.asts:
                a.desenhar()

            tempo_atual = pygame.time.get_ticks()
            tempo_restante = max(0, self.limite - (tempo_atual - self.temp_fase)) 
            segundos = tempo_restante // 1000

            fonte = pygame.font.SysFont("arial", 24, bold=True)

            tela.blit(fonte.render(f"Pontos: {self.pontos}", True, BRANCO), (20, 20))
            tela.blit(fonte.render(f"Vidas: {self.nave.vidas}", True, BRANCO), (20, 50))
            tela.blit(fonte.render(f"Tempo: {segundos}s", True, BRANCO), (20, 80))
            tela.blit(fonte.render(f"Fase: {self.fase}/3", True, BRANCO), (WIDTH - 120, 20))

        elif self.estado == "fase":
            self.texto(f"FASE {self.fase} COMPLETA!", 48, 260)
            self.texto("Clique para continuar", 28, 320)

        elif self.estado == "gameover":
            self.texto("GAME OVER", 64, 240)
            self.texto(f"Pontuação: {self.pontos}", 36, 300)
            self.texto("Clique para reiniciar", 28, 360)    

# Loop
def main():
    jogo = Jogo()
    rodando = True

    while rodando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                if jogo.estado == "menu":
                    jogo.iniciar()
                elif jogo.estado == "fase":
                    jogo.fase += 1
                    jogo.iniciar()
                elif jogo.estado == "gameover":
                    jogo.resetar()

        if jogo.estado == "jogando":
            t = pygame.key.get_pressed()
            if t[pygame.K_LEFT]:
                jogo.nave.mover("e")
            if t[pygame.K_RIGHT]:
                jogo.nave.mover("d")

        jogo.atualizar()
        jogo.desenhar()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
