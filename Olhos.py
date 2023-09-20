import pygame
import sys
import math
import time
import RPi.GPIO as gpio

# Cores
black = (0, 0, 0)
white = (255, 255, 255)
vermelho = ()

# Controles
gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)
gpio.setup(21, gpio.IN, pull_up_down = gpio.PUD_UP)
btao1 = 0

def btn1_handle(pin):
    global btao1
    print(btao1)
    btao1 = 1


# INTERRUPÇÕES
gpio.add_event_detect(21, gpio.FALLING, callback=btn1_handle, bouncetime=20)




# Todas as VARIAVEIS GLOBAIS
# global eye1_x, eye2_x, eye_y,eye_speed,direcao_olho,draw_line,draw_ball,transition_start_time,transition_duration,diametro,grossura_Pisca, btao1

# Posições e velocidades iniciais dos olhos
eye1_x = 323 # esquerdo (nosso)
eye2_x = 570 # direito (nosso)
eye_y = 300
eye_speed = 1.5

# Direção dos olhos (1 para direita, -1 para esquerda)
direcao_olho = 1

# Variáveis para controlar a transição entre bolinha e reta
draw_line = False
draw_ball = True
transition_start_time = 0
transition_duration = 1 
diametro = 160
grossura_Pisca = 20


# Variáveis para controlar a expressão facial
mouth_y = 350
expression_duration = 1  # Duração da expressão de susto em segundos
expression_start_time = 0
show_expression = False
boca = 0

eye_width = 160
eye_height = 160




def olhos(pygame, running, clock):# comportamento padrão
    # Posições e velocidades iniciais dos olhos
    global eye1_x, eye2_x, eye_y,eye_speed,direcao_olho,draw_line,draw_ball,transition_start_time,transition_duration,diametro,grossura_Pisca, btao1
    eye1_x = 323 # esquerdo (nosso)
    eye2_x = 570 # direito (nosso)
    eye_y = 300
    eye_speed = 1.5

    # Direção dos olhos (1 para direita, -1 para esquerda)
    direcao_olho = 1

    # Variáveis para controlar a transição entre bolinha e reta
    draw_line = False
    draw_ball = True
    transition_start_time = 0
    transition_duration = 1 
    diametro = 160
    grossura_Pisca = 20
    while (running and not btao1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # pisca()
                gpio.output(14, gpio.HIGH)
                retas(1)
                gpio.output(14, gpio.LOW)
        # Atualizar as posições dos olhos
        eye1_x += eye_speed * direcao_olho
        eye2_x += eye_speed * direcao_olho

        # Verificar se os olhos atingiram as bordas
        if eye1_x >= screen_width - 260 - 60 or eye2_x <= 310:
            direcao_olho *= -1
            draw_line = True
            draw_ball = False
            transition_start_time = time.time()

        # Limpar a tela
        screen.fill(black)

        xx = eye1_x - 310

        if draw_line and time.time() - transition_start_time <= transition_duration:
            # print(f'draw_line : {draw_line} time.time(): {time.time()}')
            pisca()
        else:
            draw_line = False
            draw_ball = True        

        # Desenhar os olhinhos
        if draw_ball:
            eye_y = (direcao_olho * math.cos((xx) / (172)) * 2 * 3.14) * 10 + screen_height / 2
            pygame.draw.circle(screen, white, (int(eye1_x), int(eye_y)), int(diametro/2))
            pygame.draw.circle(screen, white, (int(eye2_x), int(eye_y)), int(diametro/2))
            # Atualizar a tela
            pygame.display.flip()

        # Controlar a taxa de quadros
        clock.tick(60)  # 60 quadros por segundo
    # btao1 = 0


def susto(pygame,running,clock):
    global eye1_x, eye2_x, eye_y,eye_speed,direcao_olho,draw_line,draw_ball,transition_start_time,transition_duration,diametro,grossura_Pisca, btao1
    # Variáveis para controlar a expressão facial
    eye_y = 240
    mouth_y = 350
    expression_duration = 1  # Duração da expressão de susto em segundos
    expression_start_time = 0
    show_expression = False
    boca = 0

    eye_width = 160
    eye_height = 160
    # Loop principal
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Limpar a tela
        screen.fill(black)

        

        # Ativar expressão de susto se o tempo estiver dentro da duração definida
        if show_expression and time.time() - expression_start_time <= expression_duration:
            if eye_height < 200:
                eye_height = eye_height+5
                boca = boca +10

            pygame.draw.ellipse(screen, white, (screen_width // 2 -eye_width/2- 10 -100, screen_height // 2 -100, eye_width, eye_height+20)) # Olho esquerdo
            pygame.draw.ellipse(screen, white, (screen_width // 2 +eye_width/2+ 10 -100, screen_height // 2 -100, eye_width, eye_height+20)  )# Olho direito
            pygame.draw.circle(screen, (255,255,255),  (screen_width // 2 -20 , 400 ), 60 )
            pygame.draw.circle(screen, (0,0,0),  (screen_width // 2 -20 , 400 ), 50 )
            pygame.display.flip()
        else:
            # Desenhar olhos normais
            boca = 0

            eye_height = 160
            show_expression = False
            pygame.draw.rect(screen, white, (325, mouth_y, 100, 10))
            pygame.draw.ellipse(screen, white,( screen_width // 2 -eye_width/2- 10 - 100, screen_height // 2 -100 , eye_width, eye_height) ) # Olho esquerdo
            pygame.draw.ellipse(screen, white, (screen_width // 2 +eye_width/2+ 10-100, screen_height // 2 -100 , eye_width, eye_height))  # Olho direito
            pygame.display.flip()

            time.sleep(1)
            


        # time.sleep(0.5)
        # Controlar a taxa de quadros
        clock.tick(60)  # 60 quadros por segundo

        # Iniciar a expressão de susto
        if not show_expression:
            show_expression = True
            expression_start_time = time.time()
    btao1 = 0
    


#-----------------------------------------------------------------------------

# Funções:
def retas(tempo = transition_duration/3):
    global eye1_x, eye2_x, eye_y,eye_speed,direcao_olho,draw_line,draw_ball,transition_start_time,transition_duration,diametro,grossura_Pisca, btao1
    screen.fill(black)
    pygame.draw.line(screen, white, (eye1_x - diametro/2, eye_y), (eye1_x + diametro/2, eye_y), grossura_Pisca)  #esquerdo
    pygame.draw.line(screen, white, (eye2_x - diametro/2, eye_y), (eye2_x + diametro/2, eye_y), grossura_Pisca)# direito
    pygame.display.flip()
    time.sleep(tempo)


def bolinhas():
    global eye1_x, eye2_x, eye_y,eye_speed,direcao_olho,draw_line,draw_ball,transition_start_time,transition_duration,diametro,grossura_Pisca, btao1
    screen.fill(black)
    pygame.draw.circle(screen, white, (int(eye1_x), int(eye_y)), 80)
    pygame.draw.circle(screen, white, (int(eye2_x), int(eye_y)), 80)
    pygame.display.flip()
    time.sleep(transition_duration/3)

def pisca():
    retas()
    bolinhas()
    retas()
#___________________________________________________



# Inicialização do pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Anisa")



# Loop principal
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # pisca()
            gpio.output(14, gpio.HIGH)
            retas(1)
            gpio.output(14, gpio.LOW)

    # time.sleep(10)
    olhos(pygame,running,clock)
    susto(pygame,running,clock)




# Encerramento do pygame
pygame.quit()
sys.exit()