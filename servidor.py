import sys
import getopt
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines
from threading import Thread

# Autor: Danilo Fernandes de Assis

#definicao da classe sensor e das funcoes de GET e PUT
class Sensor(Resource):

    def __init__(self,name="Sensor",coap_server=None):
        super(Sensor,self).__init__(name,coap_server,visible=True,observable=True,allow_children=True)
        self.payload = ""
        self.resource_type = "rt1"
        self.content_type = "application/json"
        self.interface_type = "if1"

    def render_GET(self,request):    
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

#definicao da classe CoAPServe
class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self,(host,port),multicast)
        self.add_resource('sensor/',Sensor())
        print "CoAP server started on {}:{}".format(str(host),str(port))
        print self.root.dump()

#funcao principal
def main():
    ip = sys.argv[1] #ip servidor
    port = int(sys.argv[2]) #porta servidor
    multicast=False

    #criacao do CoaPServer
    server = CoAPServer(ip,port,multicast)

    try:
        server.listen(10)
        print "executed after listen"
    except KeyboardInterrupt:
        print server.root.dump()
        server.close()
        sys.exit()

if __name__=="__main__":
    main()