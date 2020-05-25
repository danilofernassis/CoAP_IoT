#!/usr/bin/env python

import getopt
import socket
import sys
import time
import os
import subprocess
import random
import logging

from threading import Thread

from datetime import datetime
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

from sense_emu import SenseHat


#cria o emulador sensehat e defini as cores
sense = SenseHat()

vermelho = (255, 0, 0)
branco = (255, 255, 255)
pixels = [None]*64

#cria o vetor de limiar de temperatura e pressao com 64 posicoes e inicializa com valores maiores que os fornecido pela barra do sensehat
limiar_temp = []
limiar_pres = []

for i in range(64):
    limiar_temp.append(float("2000"))
    limiar_pres.append(float("2000"))

#captura os argumentos passados no comando de execucao (ip, porta)
endereco = sys.argv[1] 
porta = int(sys.argv[2])
multicast=False

#funcao para requisitar os limites de temp e pres armazenados no servidor; caso a resposta seja nao vazia, sobrescreve-se o conteudo presente no sensor numero X na referida posicao X no vetor
def atualizacao_thresholds():
    print("Atualizando thresholds...")
    for i in range(64):
        path = "coap://{}:{}/sensor{}".format(endereco, porta, i)
        host, port, path = parse_uri(path)
        client = HelperClient(server=(host, port))
        response = client.get(path)
        volta_payload = response.payload
        if(volta_payload):
            volta_payload = response.payload.split()
            limiar_temp[i] = float(volta_payload[0])
            limiar_pres[i] = float(volta_payload[1])
        client.stop()
    print ("Finalizado")


#executa a funcao de atualizacao
atualizacao_thresholds()

#inicia o timout para nova autalizacao
atualizacao = time.time() + 75


#loop para analisar os valores das referidas posicoes dos vetores; caso valores dos vetores estejam abaixo do valor presente nas referidas barras do sensehat, aciona-se a cor vermelha no referido LED
while True:
    if(time.time() > atualizacao):
        thread = Thread(target = atualizacao_thresholds)
        thread.start()
        atualizacao = time.time() + 75

    temperatura = sense.temp
    pressao = sense.pressure
    for j in range(64):
        pixels[j] = branco
        if(temperatura >= limiar_temp[j]):
            if(pressao >= limiar_pres[j]):
                pixels[j] = vermelho
    sense.set_pixels(pixels)
exit()
