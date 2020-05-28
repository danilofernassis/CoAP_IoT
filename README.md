# CoAP_IoT
![Projeto](figura_1.png)

----------------------------------

# Instrução para a execução do código
## Requisitos:
*	Python 2.7
*	CoAPthon 4.0.2
*	SenseHat Emulator


1) Fazer download dos arquivos do Github para a pasta desejada.
Para isso abra o terminal na pasta desejada e execute o comando:

	```git clone https://github.com/danilofernassis/CoAP_IoT.git```

2) Apos download entrar no diretorio CoAP_IoT:

	```cd CoAP_IoT```

3) Iniciar o servidor no ip da maquina e na porta desejado, por exemplo, iniciando o servidor no ip 127.0.0.1 e porta 5683:

	```python servidor.py 127.0.0.1 5683```

4) Abrir outro terminal, entrar no diretorio entrar no diretorio CoAP_IoT e iniciar a Camada de Aplicação informando o ip e porta o qual o servidor foi iniciado:

	```python camada2.py -p coap://127.0.0.1:5683/sensor```

5) Abrir outro terminal, entrar no diretorio CoAP_IoT para iniciar o cliente. O cliente pode verificar qual são os limites armazenados no servidor por meio do comando GET, os valores armazenados são retornados no payload na ordem temperatura primeiro depois pressão:

	```python cliente.py -o GET -p coap://127.0.0.1:5683/sensor```

	e também pode armazenar no servidor limites de temperatura e pressão desejados por meio do comando PUT. Por exemplo, caso deseje armazenar uma temperatura de 67ºC e uma pressão de 847mbar, então:(atenção a ordem: temperatura primeiro depois pressão entre aspas duplas)

	```python cliente.py -o PUT -p coap://127.0.0.1:5683/sensor -P "67 847"```

6) Ao executar o comando para armazenar valores no servidor, será perguntado se deseja "Continuar a monitorar limites no servidor? [y/N]: ". Caso outro cliente venha a alterar os valores armazenados no servidor, se o monitorando estiver ativo, os limites no servidor, ao serem alterados serão informados a todos que estão monitorando para que os mesmos possam parar o monitoramento e enviar novos valores ou continuarem a monitorar caso desejem.

7) Variando-se as barras de temperatura e pressão no SenseHat, caso os valores aferidos pelas barras sejam simultaneamente superiores aos valores de temperatura e pressão armazenados no servidor, então a Camada de Aplicação envia comando ao SenseHat para acender todos os LEDs na cor vermelha, caso contrário branco.
----------------------------------