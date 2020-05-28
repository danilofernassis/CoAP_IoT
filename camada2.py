import getopt
import socket
import sys

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon import defines
from threading import Thread

#from sense_emu import SenseHat

client = None

#cria o emulador sensehat e defini as cores
#sense = SenseHat()

#vermelho = (255, 0, 0)
#branco = (255, 255, 255)
#pixels = [None]*64
limiar_pres = 2000
limiar_temp = 2000

path = sys.argv[2]
host, port, path = parse_uri(path)
try:
    tmp = socket.gethostbyname(host)
    host = tmp
except socket.gaierror:
    pass

client = HelperClient(server=(host, port))
resposta = client.get(path)
if(resposta.payload):
    limites = resposta.payload.split()
    limiar_temp = float(limites[0])
    limiar_pres = float(limites[1])
    

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

#captura os argumentos passados no comando de execucao (ip, porta)

client.observe(path, callback)
'''
#loop para analisar os valores das referidas posicoes dos vetores; caso valores dos vetores estejam abaixo do valor presente nas referidas barras do sensehat, aciona-se a cor vermelha no referido LED
while True:
    temperatura = sense.temperature
    pressao = sense.pressure
    verifica = False
    if(temperatura > limiar_temp):
        if(pressao > limiar_pres):
            verifica = True
    pixels = [vermelho if verifica else branco for i in range(64)]
    sense.set_pixels(pixels) '''