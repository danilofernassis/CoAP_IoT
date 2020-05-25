from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP
from threading import Thread
import os
import time
import subprocess
import sys

#defini a classe sensores
class Sensor(Resource):
  def __init__(self,name="Sensor",coap_server=None):
    super(Sensor,self).__init__(name,coap_server,visible=True,observable=True,allow_children=True)
    self.payload = ""
    self.resource_type = "rt1"
    self.content_type = "application/json"
    self.interface_type = "if1"

  def render_GET(self,request):    
    return self

  def render_POST(self, request):
    seres = self.init_resource(request, Sensor())
    return seres

#defini a classe CoAPServer
class CoAPServer(CoAP):
  def __init__(self, host, port, multicast=False):
    CoAP.__init__(self,(host,port),multicast)
    self.add_resource('sensor0/',Sensor())
    print "CoAP server started on {}:{}".format(str(host),str(port))
    print self.root.dump()

#cria os recursos sensores
def pollUserInput(server):
  contador = 1
  while (contador < 64):
    nome_sensor = "sensor{}".format(int(contador))
    server.add_resource(nome_sensor, Sensor())
    contador = contador + 1
  print "Disponivel ate /sensor63"


def main():
  ip = sys.argv[1] #ip do servidor passado como argumento
  port = int(sys.argv[2]) #porta que a aplicacao escuta
  multicast=False

  #inicia as threads dos sensosres
  server = CoAPServer(ip,port,multicast)
  thread = Thread(target = pollUserInput, args=(server,))
  thread.setDaemon(True)
  thread.start()

  try:
    server.listen(10)
    print "executed after listen"
  except KeyboardInterrupt:
    print server.root.dump()
    server.close()
    sys.exit()

if __name__=="__main__":
  main()