import pygame
import sys
import math
import time
import RPi.GPIO as gpio
import Motores
import threading
#Motores

# Servo

gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT) #pwm1
gpio.setup(4, gpio.OUT) #pwm2

pwm1 = gpio.PWM(17, 50)
pwm2 = gpio.PWM(4, 50)

# Timer PWM (print: DEU CERTO!) ---------------------------------------------------
gpio.setup(27, gpio.OUT)
timerPwm = gpio.PWM(27, 1) # 1 segundo
gpio.setup(22, gpio.IN, pull_up_down = gpio.PUD_UP)

# -------------------------------------------------------------

# Cores
black = (0, 0, 0)
white = (255, 255, 255)
vermelho = ()
branco =(255,255,255)


# Controles
gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT) #dado servo1
gpio.setup(21, gpio.IN, pull_up_down = gpio.PUD_UP) #pin para o botão1 (susto)
gpio.setup(20, gpio.IN, gpio.PUD_UP) #pin para o nodered (susto)
gpio.setup(26, gpio.IN, pull_up_down = gpio.PUD_UP) #pin para o botão2 (choro) !!! AINDA  NÃO DEFINIDO!!!!!
gpio.setup(19, gpio.IN, gpio.PUD_UP) #pin para o nodered (choro) !!! AINDA  NÃO DEFINIDO!!!!!
gpio.setup(25, gpio.IN, pull_up_down = gpio.PUD_UP) #pin para o botão3 (tonto) !!! AINDA  NÃO DEFINIDO!!!!!
gpio.setup(5, gpio.IN, gpio.PUD_UP) #pin para o nodered (tonto) !!! AINDA  NÃO DEFINIDO!!!!!
gpio.setup(16, gpio.IN, pull_up_down = gpio.PUD_UP) #pin para o botão4 (envergonhado) !!! AINDA  NÃO DEFINIDO!!!!!
gpio.setup(12, gpio.IN, gpio.PUD_UP) #pin para o nodered (envergonhado) !!! AINDA  NÃO DEFINIDO!!!!!

btao1 = 0
btao2 = 0
btao3 = 0
btao4 = 0

def btn1_handle(pin):
    global btao1
    print(f"btao1 {btao1}")
    btao1 = 1

def btn2_handle(pin):
    global btao2
    print(f"btao2 {btao2}")
    btao2 = 1

def btn3_handle(pin):
    global btao3
    print(f"btao3 {btao3}")
    btao3 = 1

def btn4_handle(pin):
    global btao4
    print(f"btao4 {btao4}")
    btao4 = 1

    
# INTERRUPÇÕES
gpio.add_event_detect(21, gpio.FALLING, callback=btn1_handle, bouncetime=20) # tempo de demora bouncetime
gpio.add_event_detect(26, gpio.FALLING, callback=btn2_handle, bouncetime=20) # tempo de demora bouncetime
gpio.add_event_detect(25, gpio.FALLING, callback=btn3_handle, bouncetime=20) # tempo de demora bouncetime
gpio.add_event_detect(16, gpio.FALLING, callback=btn4_handle, bouncetime=20) # tempo de demora bouncetime








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


def olhoSonoAberto(tempoSono, cor = white):
    # Desenhar os olhinhos
    screen.fill(black)
    pygame.draw.circle(screen, cor, (screen_width//2 -130, screen_height//2), 80)
    pygame.draw.circle(screen, cor,  (screen_width//2 +130, screen_height//2), 80)
    pygame.display.flip()
    time.sleep(tempoSono)
def olhoSonoFechado(tempoSono, zzz = False,cor = white):
    diametro =160
    grossura_Pisca = 20
    screen.fill(black)
    
    if zzz:
        font = pygame.font.Font(None, 50)
        text = font.render("Z", True, white) 
        screen.blit(text, (500 - text.get_width() // 2, 100))
        font = pygame.font.Font(None, 80)
        text2 = font.render("Z", True, white) 
        screen.blit(text2, (600 - text.get_width() // 2, 150))
        pygame.display.flip()
    pygame.draw.line(screen, cor, (screen_width//2 -130 - diametro//2, screen_height//2), (screen_width//2 -130 + diametro//2, screen_height//2), grossura_Pisca)  #esquerdo
    pygame.draw.line(screen, cor, (screen_width//2 +130 - diametro//2, screen_height//2), (screen_width//2 +130 + diametro//2, screen_height//2), grossura_Pisca)# direito
    
    pygame.display.flip()
    time.sleep(tempoSono)

def olhos(pygame, clock):# comportamento padrão
    # Posições e velocidades iniciais dos olhos
    global running
    global dado 

    global eye1_x, eye2_x, eye_y,eye_speed,direcao_olho,draw_line,draw_ball,transition_start_time,transition_duration,diametro,grossura_Pisca, btao1
    eye1_x = 323 # esquerdo (nosso)
    eye2_x = 570 # direito (nosso)
    eye_y = 300
    eye_speed = 1.5
    dado= "EBA MUDEI DEI CERTO D DE NOVO"
    # Direção dos olhos (1 para direita, -1 para esquerda)
    direcao_olho = 1

    # Variáveis para controlar a transição entre bolinha e reta
    draw_line = False
    draw_ball = True
    transition_start_time = 0
    transition_duration = 1 
    diametro = 160
    grossura_Pisca = 20
    while (running and not btao1 and not btao2 and not btao3 and not btao4 ):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print(f'running {running}')

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # pisca()
                gpio.output(14, gpio.HIGH)
                pwm1.start(2.5) #posição inicial 0°
                pwm2.start(6) #posição inicial 90°
                pwm1.ChangeDutyCycle(6) #posição inicial 0°
                pwm2.ChangeDutyCycle(2.5) #posição inicial 90°
                retas(1)
                gpio.output(14, gpio.LOW)
                pwm1.ChangeDutyCycle(2.5) #posição inicial 0°
                pwm2.ChangeDutyCycle(6) #posição inicial 90°
                time.sleep(0.5)
                pwm1.ChangeDutyCycle(0) #posição inicial 0°
                pwm2.ChangeDutyCycle(0) #posição inicial 90°
             
                
            
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


def susto(pygame,clock):
    global eye1_x, eye2_x, eye_y,eye_speed,direcao_olho,draw_line,draw_ball,transition_start_time,transition_duration,diametro,grossura_Pisca, btao1
    global running
    
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
    # while (running and btao1):
    inicio = time.time()
    while (running and btao1):
        if not (time.time() - inicio <= 3): #20 segundos
            #print(f"time : {time.time()} inicio : {expression_start_time} TRUE OU FALSE:${time.time() - expression_start_time <= expression_duration}" )
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print(f'running {running}')


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
    
def choro(pygame,clock):
    global eye1_x, eye2_x, eye_y,eye_speed,direcao_olho,draw_line,draw_ball,transition_start_time,transition_duration,diametro,grossura_Pisca, btao1
    global running
    global btao2

    # Variáveis para controlar a expressão facial
    eye_y = 240
    mouth_height = 40
    mouth_y = 320
    expression_duration = 3  # Duração da expressão de susto em segundos
    expression_start_time = 0
    show_expression = False

    eye_width = 160
    eye_height = 160+20

    diametro = 160
    inicio = time.time()
    # Loop principal
    clock = pygame.time.Clock()
    while running:
        if not (time.time() - inicio <= 3): #20 segundos
            #print(f"time : {time.time()} inicio : {expression_start_time} TRUE OU FALSE:${time.time() - expression_start_time <= expression_duration}" )
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print(f'running {running}')

        # Limpar a tela
        screen.fill(black)
        pygame.draw.circle(screen, branco, (int(screen_width // 2 -diametro/2 -30), int(screen_height // 2)), int(diametro/2))
        pygame.draw.circle(screen, branco, (int(screen_width // 2+diametro/2+30), int(screen_height // 2)), int(diametro/2))


        # Ativar expressão de susto se o tempo estiver dentro da duração definida
        if show_expression and time.time() - expression_start_time <= expression_duration:

            pygame.draw.ellipse(screen, (0,0,255), (screen_width // 2 -eye_width/2- 10 -100, screen_height // 2 -15, eye_width, eye_height+20)) # Olho esquerdo
            pygame.draw.ellipse(screen, (0,0,255), (screen_width // 2 +eye_width/2+ 10 -60, screen_height // 2 -15, eye_width, eye_height+20)  )# Olho direito
            pygame.draw.rect(screen, white, (350, mouth_y + 20, 100, mouth_height - 20))  # Boca assustada
            eye_height = eye_height+10

        else:
            # Desenhar olhos normais
            eye_height = 160+20
            show_expression = False
            pygame.draw.rect(screen, white, (350, mouth_y, 100, mouth_height))
            pygame.draw.ellipse(screen, white,( screen_width // 2 -eye_width/2- 10 - 100, screen_height // 2 -15 , eye_width, eye_height) ) # Olho esquerdo
            pygame.draw.ellipse(screen, white, (screen_width // 2 +eye_width/2+ 10-100, screen_height // 2 -15 , eye_width, eye_height))  # Olho direito
            
        pygame.draw.circle(screen, branco, (int(screen_width // 2 -diametro/2 -30), int(screen_height // 2)), int(diametro/2))
        pygame.draw.circle(screen, branco, (int(screen_width // 2+diametro/2+30), int(screen_height // 2)), int(diametro/2))


        # Atualizar a tela
        pygame.display.flip()
        # time.sleep(0.5)
        # Controlar a taxa de quadros
        clock.tick(60)  # 60 quadros por segundo

        # Iniciar a expressão de susto
        if not show_expression:
            show_expression = True
            expression_start_time = time.time()
    btao2 = 0
    print(f"Zerei o 2 {btao2}")




def tonto(pygame,clock):
    global running
    global btao3
    # Posições e velocidades iniciais dos olhos
    # eye1_x = 30
    eye1_x = 303
    eye2_x = 570
    eye_y = 300
    eye_speed = 3

    # Direção dos olhos (1 para direita, -1 para esquerda)
    eye_direction = 1

    # Loop principal
    inicio = time.time()
    clock = pygame.time.Clock()
    while  running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print(f'running {running}')
        print(f"time : {time.time()} inicio : {expression_start_time} TRUE OU FALSE:${time.time() - expression_start_time <= expression_duration}" )
  
        if not (time.time() - inicio <= 3): 
            break
        # Atualizar as posições dos olhos
        eye1_x += eye_speed * eye_direction
        eye2_x += eye_speed * eye_direction

        if eye1_x >= screen_width -260-60 or eye2_x <= 310:
            eye_direction *= -1

        # Limpar a tela
        screen.fill(black)

        eye_y= (eye_direction* math.sin(eye1_x/screen_width*80)*100) + screen_height/2 ## pula pula

        # Desenhar os olhinhos
        pygame.draw.circle(screen, white, (int(eye1_x), int(eye_y)), 80)
        pygame.draw.circle(screen, white, (int(eye2_x), int(eye_y)), 80)

        # Atualizar a tela
        pygame.display.flip()

        # Controlar a taxa de quadros
        clock.tick(60)  # 60 quadros por segundo

        if eye_y<220:
            eye_speed *= 0.94
    btao3 = 0
    print(f"Zerei btoa3 {btao3}")

def frustrado(pygame,clock):
    # Posições e velocidades iniciais dos olhos
    # eye1_x = 30
    eye1_x = 323 -50
    eye2_x = 570 - 50
    eye_y = 200
    global btao4
    # Loop principal
    inicio = time.time()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        print(f"time : {time.time()} inicio : {inicio} TRUE OU FALSE:${time.time() - inicio >= 3}" )
         
        if (time.time() - inicio >= 3): #20 segundos
            break
        # Limpar a tela
        screen.fill(black)
        # Desenhar os olhinhos
        pygame.draw.circle(screen, white, (int(eye1_x), int(eye_y)), 80)
        pygame.draw.circle(screen, white, (int(eye2_x), int(eye_y)), 80)


        pygame.draw.circle(screen, black, (int(eye1_x-80), int(eye_y-90)), 80)
        pygame.draw.circle(screen, black, (int(eye2_x+80), int(eye_y-90)), 80)
        pygame.draw.rect(screen, white, ((323+570 -200)//2, 300, 130, 10))



        # Atualizar a tela
        pygame.display.flip()

        # Controlar a taxa de quadros
        clock.tick(60)  # 60 quadros por segundo
    print(f"SAI btoa 4 = 0")
    btao4 = 0
#-----------------------------------------------------------------------------

# Funções:
def retas(tempo = transition_duration/3):
    global eye1_x, eye2_x, eye_y,eye_speed,direcao_olho,draw_line,draw_ball,transition_start_time,transition_duration,diametro,grossura_Pisca, btao1
    screen.fill(black)
    pygame.draw.line(screen, white, (eye1_x - diametro//2, eye_y), (eye1_x + diametro//2, eye_y), (grossura_Pisca))  #esquerdo
    #pygame.draw.line(screen, white, (eye1_x - diametro/2, eye_y), (eye1_x + diametro/2, eye_y), (grossura_Pisca))  #esquerdo
    pygame.draw.line(screen, white, (eye2_x - diametro//2, eye_y), (eye2_x + diametro//2, eye_y), (grossura_Pisca))# direito
    #pygame.draw.line(screen, white, (eye2_x - diametro/2, eye_y), (eye2_x + diametro/2, eye_y), (grossura_Pisca))# direito
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

    #timer = threading.Timer(1.0, Motores.Motor )
    #timer.start()
#time.sleep(5)
# Loop principal
clock = pygame.time.Clock()
running = True

#acordando
screen.fill(black)
olhoSonoFechado(2,True)
olhoSonoAberto(0.6)
olhoSonoFechado(0.2)
olhoSonoAberto(0.6)
olhoSonoFechado(0.2)
olhoSonoAberto(1)

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
    olhos(pygame,clock)
    print(f'running fora {running}')
    
    susto(pygame,clock)
    if btao2:
        print(f"entrei no choro")
        choro(pygame,clock)
    if btao3:
        print(f"entrei no tonto")
        tonto(pygame,clock)
    if btao4:
        print(f"entrei no frustrado ")
        frustrado(pygame,clock)

# dormiu
olhoSonoAberto(0.6)
olhoSonoFechado(0.2)
olhoSonoAberto(0.6)
olhoSonoFechado(0.2)
olhoSonoAberto(1)
olhoSonoFechado(2,True)


# Encerramento do pygame
pygame.quit()
sys.exit()