#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "COM3"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação serial 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)


    
        while com1.rx.getIsEmpty():
            time.sleep(0.1)

        rxBuffer = com1.rx.getNData(14)
        print("recebeu {} bytes" .format(len(rxBuffer)))
    
            
        decimal_values = []
        for byte in rxBuffer:
            decimal_values.append(byte)

        ocioso = True
        if ocioso:
            while ocioso == True:
                if len(decimal_values) > 0: #se a msg1 que o jao enviouo ta certa
                    if decimal_values[1] == 1:
                        ocioso = False
                        time.sleep(1)
                else:
                    time.sleep(1)

        msg2 = bytearray([2,0,0,0,0,0,0,0,0,0,0,0,0,0])
        com1.sendData(np.asarray(msg2))
        time.sleep(.1) 
            
            

        decimal_values = []
        for byte in rxBuffer:
            decimal_values.append(byte)

        # Enviando de volta o numero de comandos
        print(decimal_values)
        if decimal_values[0] == 255:
            bytes15 = bytearray(decimal_values)
            com1.sendData(np.asarray(bytes15))

        conteudo_total = [] #conteudo junto no payload
        n_pacote = 1
        n_total_pacotes = -1
        time.sleep(0.5)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()