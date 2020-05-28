#!/usr/bin/env python
import getopt
import socket
import sys

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon import defines


client = None


def usage():
    print "Command:\tpython cliente_v2.py -o -p [-P]"
    print "Options:"
    print "\t-o, --operation=\tGET|PUT|OBSERVE"
    print "\t-p, --path=\t\tPath of the request"
    print "\t-P, --payload=\t\tPayload of the request"


def callback(response):
    global client
    print ("Limites atuais no servidor")
    limites = response.payload.split()
    print ("Temperatura: {}".format(limites[0]))
    print ("Pressao: {}".format(limites[1]))
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


def main():  
    global client
    op = None
    path = None
    payload = None
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

    host, port, path = parse_uri(path)
    try:
        tmp = socket.gethostbyname(host)
        host = tmp
    except socket.gaierror:
        pass
    client = HelperClient(server=(host, port))
    if op == "GET":
        if path is None:
            print "Caminho nao pode ser vazio"
            usage()
            sys.exit(2)
        response = client.get(path)
        print response.pretty_print()
        client.stop()
    elif op == "OBSERVE":
        if path is None:
            print "Caminho nao pode ser vazio"
            usage()
            sys.exit(2)
        client.observe(path, callback)    
    elif op == "PUT":
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