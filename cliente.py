#!/usr/bin/env python
import getopt
import socket
import sys

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon import defines

# Autor: Danilo Fernandes de Assis

client = None

#imprime como usar os comandos do arquivo cliente.py
def usage():
    print "Command:\tpython cliente.py -o -p [-P]"
    print "Options:"
    print "\t-o, --operation=\tGET|PUT|OBSERVE"
    print "\t-p, --path=\t\tPath of the request"
    print "\t-P, --payload=\t\tPayload of the request"


#funcao a ser executada caso haja alteracao nos valores limites de temperatura e pressao armazenados no mesmo
def callback(response):
    global client
    print ("Limites atuais no servidor")
    if(response.payload):
        limites = response.payload.split()
        print ("Temperatura: {}".format(limites[0]))
        print ("Pressao: {}".format(limites[1]))
    else:
        print ("Nao ha lmites armazenados")
    check = True
    while check:
        chosen = raw_input("Continuar a monitorar limites no servidor? [y/N]: ")
        print ("------------------------")
        if chosen != "" and not (chosen == "n" or chosen == "N" or chosen == "y" or chosen == "Y"):
            print "Escolha nao reconhecida."
            continue
        elif chosen == "n" or chosen == "N":
            while True:
                client.cancel_observing(response, True)
                check = False
                break
        else:
            break

#funcao principal
def main():  
    global client
    op = None
    path = None
    payload = None

    #verifica se todos os argumentos passados estao corretos
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:p:P:f:", ["help", "operation=", "path=", "payload="])
    except getopt.GetoptError as err:
        print str(err)  
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-o", "--operation"):
            op = a
        elif o in ("-p", "--path"):
            path = a
        elif o in ("-P", "--payload"):
            payload = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(2)
    if op is None:
        print "Operacao deve ser especificada"
        usage()
        sys.exit(2)

    if path is None:
        print "Caminho deve ser especificado"
        usage()
        sys.exit(2)

    if not path.startswith("coap://"):
        print "Caminho deve ser do tipo coap://host:port/path"
        usage()
        sys.exit(2)

    #separa host, porta e path do argumento passado no comando    
    host, port, path = parse_uri(path)
    try:
        tmp = socket.gethostbyname(host)
        host = tmp
    except socket.gaierror:
        pass
    client = HelperClient(server=(host, port))

    #verifica qual foi a operacao passada no comando e a executa
    if op == "GET": #faz requisao para verificar quais limites estao armazenados no servidor
        if path is None:
            print "Caminho nao pode ser vazio"
            usage()
            sys.exit(2)
        response = client.get(path)
        print response.pretty_print()
        client.stop()
    elif op == "OBSERVE": #faz o monitoramento dos limites armazenados no servidor
        if path is None:
            print "Caminho nao pode ser vazio"
            usage()
            sys.exit(2)
        client.observe(path, callback)    
    elif op == "PUT": #armazena limites no servidor
        if path is None:
            print "Caminho nao pode ser vazio"
            usage()
            sys.exit(2)
        if payload is None:
            print "Payload nao pode ser vazio"
            usage()
            sys.exit(2)
        response = client.put(path, payload)
        print response.pretty_print()
        client.observe(path, callback)
    else:
        print "Operacao nao reconhecida"
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main()