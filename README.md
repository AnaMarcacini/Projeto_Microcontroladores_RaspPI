# Projeto Aleoled - jogo competitivo de reação 
Esse trabalho se trata de um jogo interativo para todas as idades. Ele trabalha a parte reativa e competitiva do jogador, ao acender leds em uma ordem aleatória o jogador deverá apertar o botão correspondente antes de seu oponente.
<br>
<br>**Autores**:
<br> Ana Helena Marcacini 20.01305-0
<br>Isabelle Franchi Dinardi 20.00364-0
<br> Laura Caroline P. Correia 20.00171-0
<br>
## 1. Objetivo do projeto
Criação de um jogo iterativo utilizando raspberrypypico (usando a linguagem: micropython) que treina a parte reativa do jogador de uma maneira divertida.
## 2. Lista/ levantamento de custo de componentes 
Para o desenvolvimento do projeto foi utilizado os materiais listados na tabela abaixo, tendo um custo total de R$203,97, pretendemos vender por R$250,00 assim o lucro por venda será R$46,03.

<img src =  https://github.com/AnaMarcacini/Projeto_Microcontroladores/blob/main/Hardware/tabela%20de%20pre%C3%A7o%20final.png>  </img>

## 3. Hardware
### 3.1 Esquema elétrico
<img src = https://github.com/AnaMarcacini/Projeto_Microcontroladores/blob/main/Hardware/Esquema%20Eletrico.jpeg > </img>
### 3.2 Diagrama de blocos
<img src =https://github.com/AnaMarcacini/Projeto_Microcontroladores/blob/main/Hardware/diagrama%20de%20blocos.jpeg> </img>
### 3.3 Montagem
Neste ponto foi idealizado como seriam predispostos os componentes para um melhor entendimento e visualização aos jogadores, como mostrado na figura abaixo.

<img src = https://github.com/AnaMarcacini/Projeto_Microcontroladores/blob/main/Hardware/esquema%20de%20montagem.jpeg> </img>
### 3.4 Finalização
Para a finalização do projeto, foi feita,  com apoio do FabLab, uma caixa em MDF 3mm. 

A caixa é dividida em 6 peças. Para a criação de cada peça, foi necessário a modelagem no software SolidWorks em arquivo .DXF.

[- Arquivos para montagem da caixa](https://github.com/AnaMarcacini/Projeto_Microcontroladores/tree/main/Montagem%20da%20Caixa)
### 3.5 Projeto Final
[- Vídeo de explicação do projeto](https://youtu.be/n8cgg-nnSlI)

[- Vídeo do jogo funcionando](https://youtu.be/rbLJBuj3GkU)


* Placa eletrônica fora da caixa: 

<img src = https://github.com/AnaMarcacini/Projeto_Microcontroladores/blob/main/Hardware/Hardware%20soldado.jpeg> </img>

* Montagem final:

<img src = https://github.com/AnaMarcacini/Projeto_Microcontroladores/blob/main/Hardware/Trabalho%20Pronto.jpeg> </img>


## 4. Software
### 4.1 Código principal
```python
# Importa as classes Pin e I2C da biblioteca machine para controlar o hardware do Raspberry Pi Pico

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import math
import micropython

import random
import Display_Pontuacao as dp
# Configuração do display OLED
disp1 = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)
oled = SSD1306_I2C(128, 32, disp1)
clock = 0 # tempo para iniciar
Tempo_de_Partida = 40 #tempo em segundos da partida
# Função para converter um valor de hora, minuto ou segundo em um formato "hh:mm:ss"
def segundos_para_hms(segundos):
    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60
    return "{:02d}:{:02d}:{:02d}".format(h, m, s)

# Função para atualizar o display OLED com o tempo restante
def atualizar_display(tempo_restante):
    oled.fill(0)
    oled.text("Tempo restante:", 0, 0)
    oled.text(segundos_para_hms(tempo_restante), 0, 10)
    oled.show()

# Função a ser executada a cada segundo pelo temporizador
def callback_temporizador(timer):
    global tempo_restante, clock
    tempo_restante -= 1
    atualizar_display(tempo_restante)
    if tempo_restante <= 0:#Fim do temporizador
        temporizador.deinit()
        clock = 0 #fim do tempo

def setup():
    # Define o pino do Raspberry Pi Pico conectado ao módulo PIR HC-SR501
    Led_Amarelo = 22
    Led_Vermelho = 21
    Led_Verde = 20
    Led_Amarelo2 = 19

    # Configura o pino da saída digital do sensorLed1 = Pin(Led_Amarelo, Pin.OUT)
    Led1 = Pin(Led_Amarelo, Pin.OUT)
    Led2 = Pin(Led_Vermelho, Pin.OUT)
    Led3 = Pin(Led_Verde, Pin.OUT)
    Led4 = Pin(Led_Amarelo2, Pin.OUT)
    bot11 = Pin(18, Pin.IN,Pin.PULL_DOWN) #botao do led 1 (amarelo)--> jog1
    bot21 = Pin(17, Pin.IN,Pin.PULL_DOWN) #botao do led 1 (amarelo)--> jog2
    bot12 = Pin(16, Pin.IN,Pin.PULL_DOWN) #botao do led 2 (vermelho)--> jog1
    bot22 = Pin(15, Pin.IN,Pin.PULL_DOWN) #botao do led 2 (vermelho)--> jog2
    bot13 = Pin(14, Pin.IN,Pin.PULL_DOWN) #botao do led 3 (verde)--> jog1
    bot23 = Pin(13, Pin.IN,Pin.PULL_DOWN) #botao do led 3 (verde)--> jog2
    bot14 = Pin(12, Pin.IN,Pin.PULL_DOWN) #botao do led 4 (amarelo2)--> jog1
    bot24 = Pin(11, Pin.IN,Pin.PULL_DOWN) #botao do led 4 (amarelo2)--> jog2
    Leds = [Led1,Led2,Led3,Led4]
    button1 = [bot11,bot12,bot13,bot14]
    button2 = [bot21,bot22,bot23,bot24]
    
    for led in Leds:
        led.value(0)
    return Leds,button1,button2
def sorteio(Leds):
    numero_sorteio = random.randint(0, 3)
    Selecionado = Leds[numero_sorteio]
    Selecionado.value(1)
    
    print(Selecionado)
    return numero_sorteio
def visualizar():
    print("Jogador 1:")
    print(j1)
    print("Jogador 2: ")
    print(j2)
    
def vitorioso(j1,j2):
    if j1>j2:
        oled.fill(0)
        oled.text("Vencedor:", 30, 10)
        oled.text("Jogador 1", 30, 20)
        oled.show()
        return "J1"
    if j2>j1:
        oled.fill(0)
        oled.text("Vencedor:", 30, 10)
        oled.text("Jogador 2", 30, 20)
        oled.show()
        return "J2"
    else:
        oled.fill(0)
        oled.text("Empate :(", 30, 20)
        oled.show()
        return "Empate"


#--------Codigo_Principal---------------------
Leds, button1, button2 = setup()
reset = Pin(4, Pin.IN,Pin.PULL_DOWN) #botao reset
j1=0
j2=0
visualizar()
ativos1 = [0,0,0,0]
ativos2 = [0,0,0,0]
primeira_vez = True
while(1):
    while(not clock):
        for led in Leds:
            led.value(0)
        #chamar display vitorioso
        if(not primeira_vez):
            vitorioso(j1,j2)
        #print(vitorioso(j1,j2))
        for led in Leds:
            led.value(1)
            time.sleep(0.25)
        if reset.value() ==1:#botão recomeçar
            clock = 1
            j1=0
            j2=0
            tempo_restante = Tempo_de_Partida
            temporizador = machine.Timer(-1)
            temporizador.init(period=1000, mode=machine.Timer.PERIODIC, callback=callback_temporizador)
            atualizar_display(tempo_restante)
    for led in Leds:
        led.value(0)
    numero_sorteio = sorteio(Leds)
    p = dp.display(j1,j2)
    print("___________________________________________________")
    while(clock):
        primeira_vez = False
        if button1[numero_sorteio].value() == 1 and ativos1[numero_sorteio] == 0  :
            Leds[numero_sorteio].value(0)#Apaga led selecionado ao clicar
            j1+=1
            visualizar()
            ativos1[numero_sorteio] = 1
            print("vencedor j1")
        elif button1[numero_sorteio].value() == 0 and ativos1[numero_sorteio] == 1:
            ativos1[numero_sorteio] = 0
            break

        if button2[numero_sorteio].value() == 1 and ativos2[numero_sorteio] == 0 :
            Leds[numero_sorteio].value(0)#Apaga led selecionado ao clicar
            j2+=1
            visualizar()
            ativos2[numero_sorteio] = 1
            print("vencedor j2")
        elif button2[numero_sorteio].value() == 0 and ativos2[numero_sorteio] == 1:
            ativos2[numero_sorteio] = 0
            break
```
### 4.2 Display Pontuação
```python
"""!
@file display_oled_i2c_128x64_exemplo.py
@brief Programa para escrever em um display OLED I2C de 128x64 usando o Raspberry Pi Pico.
@details Este programa utiliza a biblioteca ssd1306 para escrever em um display OLED de 128x64 via barramento I2C.
         Referência: https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
@author Rodrigo França
@date 2023-03-17
"""

# Importa as classes Pin e I2C da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin, I2C
# Importa a classe SSD1306_I2C da biblioteca ssd1306.py
from ssd1306 import SSD1306_I2C
#importa a classe j1 e j2 da aleatoriedade_led
#from aleatoriedade_led import j1, j2
def display(j1,j2):
    # Define os pinos do Raspberry Pi Pico conectados ao barramento I2C 0
    i2c0_slc_pin = 9
    i2c0_sda_pin = 8
    #Parametros para a futura função
    pontuacao_jogador1= str(j1)
    pontuacao_jogador2= str(j2)



    # Inicializa o I2C0 com os pinos GPIO9 (SCL) e GPIO8 (SDA)
    disp2 = I2C(0, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=100000)

    # Inicializa o display OLED I2C de 128x64
    display = SSD1306_I2C(128, 64, disp2)

    # Limpa o display
    display.fill(0)
    display.show()

    # Desenha o logo do MicroPython e imprime um texto
    display.fill(0)                        # preenche toda a tela com cor = 0

    display.hline(0, 10, 200, 1)            # desenha uma linha horizontal x = 0, y = 10, altura = 200, cor = 1
    display.vline(64,5,47,1)                #desenha uma linha vertical (x,y,h,cor)

    display.text('Jog. 1 | Jog. 2', 4, 0, 1)  # desenha algum texto em x = 40, y = 0 , cor = 1

    display.text(pontuacao_jogador1, 10, 16, 1)     # desenha algum texto em x = 40, y = 12, cor = 1
    display.text(pontuacao_jogador2, 74, 16, 1)     # desenha algum texto em x = 40, y = 12, cor = 1


    # Escreve na última linha do display
    display.text("Boa Sorte!", 27, 54)

    # Atualiza o display
    display.show()
display(0,0)


```


### 4.2 Biblioteca Display
```python
# MicroPython SSD1306 OLED driver, I2C and SPI interfaces

from micropython import const
import framebuf


# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_IREF_SELECT = const(0xAD)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)


# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP,  # display off
            # address setting
            SET_MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            SET_DISP_START_LINE,  # start at line 0
            SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            SET_MUX_RATIO,
            self.height - 1,
            SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            SET_DISP_OFFSET,
            0x00,
            SET_COM_PIN_CFG,
            0x02 if self.width > 2 * self.height else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV,
            0x80,
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            SET_CONTRAST,
            0xFF,  # maximum
            SET_ENTIRE_ON,  # output follows RAM contents
            SET_NORM_INV,  # not inverted
            SET_IREF_SELECT,
            0x30,  # enable internal IREF during display on
            # charge pump
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,  # display on
        ):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def rotate(self, rotate):
        self.write_cmd(SET_COM_OUT_DIR | ((rotate & 1) << 3))
        self.write_cmd(SET_SEG_REMAP | (rotate & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width != 128:
            # narrow displays use centred columns
            col_offset = (128 - self.width) // 2
            x0 += col_offset
            x1 += col_offset
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)


class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        self.rate = 10 * 1024 * 1024
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        import time

        self.res(1)
        time.sleep_ms(1)
        self.res(0)
        time.sleep_ms(10)
        self.res(1)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)


```







