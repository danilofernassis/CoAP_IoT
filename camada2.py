import getopt
import socket
import sys

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon import defines
from threading import Thread

from sense_emu import SenseHat


# Autor: Danilo Fernandes de Assis


client = None

#cria o emulador sensehat e defini as cores
sense = SenseHat()
vermelho = (255, 0, 0)
branco = (255, 255, 255)
pixels = [None]*64

#variaveis usadas para compara com os valores de temperatura e pressao medidos no sensehat
#sao iniciadas com valores altos a fim de deixar os LEDs na cor branca caso nao haja nenhum limite armazenado no servidor
limiar_pres = 2000
limiar_temp = 2000

#separa host, porta e path passados no argumento do comando
path = sys.argv[2]
host, port, path = parse_uri(path)
try:
    tmp = socket.gethostbyname(host)
    host = tmp
except socket.gaierror:
    pass

#verifica se ha valores limites armazenados no servidor
client = HelperClient(server=(host, port))
resposta = client.get(path)
if(resposta.payload):
    limites = resposta.payload.split()
    limiar_temp = float(limites[0])
    limiar_pres = float(limites[1])
    

#funcao para monitorar o servidor caso haja alguma alteracao de valor nos limites armazenados no mesmo
def callback(response):
    global client
    global limiar_temp
    global limiar_pres
    if(response.payload):
        limites = response.payload.split()
        limiar_temp = float(limites[0])
        limiar_pres = float(limites[1])
        print ("Limites atuais no servidor")
        print ("Temperatura: {} C".format(limiar_temp))
        print ("Pressao: {}mbar".format(limiar_pres))

    else:
        print ("Nao ha limites configurados")
    print ("------------------------")

#executa a funcao de monitoramento do s
client.observe(path, callback)

#loop para verificar se os valores de temperatura e pressao sao ambos superiores 
#aos valores de temperatura e pressao armazenados no servidor
#caso isso ocorra, todos os LEDs do sensehat acendem na cor vermelha
while True:
    try:
        temperatura = sense.temperature
        pressao = sense.pressure
        verifica = False
        if(temperatura > limiar_temp):
            if(pressao > limiar_pres):
                verifica = True
        pixels = [vermelho if verifica else branco for i in range(64)]
        sense.set_pixels(pixels)
    except KeyboardInterrupt:
        client.close()
        sys.exit() 