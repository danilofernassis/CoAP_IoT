# CoaP_IoT
![Projeto](figura_1.png)

----------------------------------

**Instrução para a execução do código**
Requisitos:
- Python 2.7
- CoAPthon 4.0.2
- PIP

1) Abrir terminal e instalar o PIP (no servidor, caso não esteja instalado):
	- ```sudo apt-get install python-pip```

2) Instalar o CoAPthon 4.0.2 (no servidor):
	- ```sudo pip install CoAPthon```

3) Repetir os passos 1 e 2 nos clientes

4) No servidor, baixar os arquivos presentes no Github no local que desejar:
	- ```git clone https://github.com/danilofernassis/CoAP_IoT.git```

5) Copiar o arquivo cliente.py para a pasta desejada nos clientes

6) No servidor, abrir o emulador do SenseHat

7) Abrir o terminal, entrar na pasta onde foi baixado os arquivos do Github, ativar o servidor passando o endereço ip do servidor e porta 5683 (exemplo: endereço ip 192.168.1.108 e porta 5683):
	- ```python servidor.py 192.168.1.108 5683```

8) Nos clientes, abrir o terminal, entrar na pasta onde se encontra o arquivo cliente.py, configurar os sensores com os limites desejados (exemplo: configurar o sensor37 com o limite de temperatura em 58ºC e o limite de pressão em 837mbar):
	- ```python cliente.py -o POST -p coap://192.168.1.108:5683/sensor37 -P "58 837"```

9) Repetir o passo 8 para tantos outros sensores conforme desejar

10) No servidor, abrir um novo terminal, acessar a pasta onde se encontra os arquivos baixados do Github, ativar a camada de aplicação informando o ip e porta no qual o servidor está ativo:
	- ```python camada2.py 192.168.1.108 5683```

11) Esperar finalizar a atualização dos thresholds (limites)

12) Após a finalização da atualização, realizar variação nas barras de temperatura e pressão no SenseHat e verificar a alteração da cor dos LEDs conforme essa variação ultrapasse os limites de temperatura e pressão configurados em cada sensor.

----------------------------------