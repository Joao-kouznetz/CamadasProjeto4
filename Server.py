#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################

# sudo chmod 777 /dev/ttyACM0

#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import sys

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada

serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
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
    
        while ocioso == True:
            if decimal_values[0] == 1 and decimal_values[10] == 170 and decimal_values[11] == 187 and decimal_values[12] == 204 and decimal_values[13] == 221: #se a msg1 que o jao enviouo ta certa
                print('Mensagem do cliente recebida')
                if decimal_values[1] == 1:
                    print('Mensagem e para mim')
                    ocioso = False
                    numPckg = decimal_values[3]
                    time.sleep(1)
                else:
                    time.sleep(1)
            else:
                time.sleep(1)


        msgt2 = bytearray([2,0,0,0,0,0,0,0,0,0,170,187,204,221])
        com1.sendData(np.asarray(msgt2))
        time.sleep(.1) 
        print('mensagem t2 enviada')
            
        cont = 1
        recebi_msgt3 = False
        pckgOK = False
        n_pacote = 0
        conteudo_total = []

        # with open('exemplo.txt', 'w') as arquivo:
        #     pass
        
        while cont <= numPckg:
            timer1 = time.time()
            timer2 = time.time()

            com1.rx.clearBuffer()
            while recebi_msgt3 == False:
                time.sleep(1)
                if time.time() - timer2 > 20:
                    ocioso == True
                    msgt5 = [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 170, 187, 204, 221]
                    com1.sendData(np.asarray(msgt5))
                    time.sleep(.1) 
                    print("-------------------------")
                    print("Comunicação encerrada")
                    print("-------------------------")
                    com1.disable()
                    sys.exit()
                else:
                    if (time.time() - timer1) > 5:
                        print('passou 2 segundos mandei t4 errado')
                        msgt4 = [4, 0, 0, 0, 0, 0, 0, n_pacote, 0, 0, 170, 187, 204, 221]
                        com1.sendData(bytes(msgt4))
                        time.sleep(.1)
                        com1.rx.clearBuffer()
                        timer1 = time.time()

                #RECEBENDO HEAD
                if com1.rx.getBufferLen() >= 10:
                    
                    rxBuffer = com1.rx.getNData(10)

                    head_msgt3 = []
                    for byte in rxBuffer:
                        head_msgt3.append(byte)

                    print(' revebi o head:', head_msgt3)
                    
                    if head_msgt3[0] == 3:
                        recebi_msgt3 = True
                    else:
                        com1.rx.clearBuffer()

            payload = head_msgt3[5]
            print('payload:', payload, 'getbuferlen', com1.rx.getBufferLen())
            if payload == com1.rx.getBufferLen() - 4 and head_msgt3[4] == n_pacote+1:  
                print("recebeu {} bytes na head, numero pacore: {}".format(len(rxBuffer), n_pacote))

                #RECEBENDO PAYLOAD
                rxBuffer = com1.rx.getNData(payload)
                print("recebeu {} bytes no payload, numero do pacote: {}" .format(len(rxBuffer), n_pacote))

                payload_msgt3 = []
                for byte in rxBuffer:
                    payload_msgt3.append(byte)

                conteudo_pacote = payload_msgt3
                print('payload', conteudo_pacote)

                #RECEBENDO EOP
                rxBuffer = com1.rx.getNData(4)
                print("recebeu {} bytes no EOP, numero do pacote: {}" .format(len(rxBuffer), n_pacote))    

                EOP_msgt3 = []
                for byte in rxBuffer:
                    EOP_msgt3.append(byte) 

                if EOP_msgt3[0] == 170 and EOP_msgt3[1] == 187 and EOP_msgt3[2] == 204 and EOP_msgt3[3] == 221:
                    print(f'{n_pacote} recebido c sucesso')
                    pckgOK = True 
                    timer1 = time.time()
                else:
                    pckgOK = False
            else:
                pckgOK = False

            if pckgOK == False:
                com1.rx.clearBuffer()
                print('enviei msgt6')
                msgt6 = [6, 0, 0, 0, 0, 0, n_pacote, 0, 0, 0, 170, 187, 204, 221]    
                com1.sendData(bytes(msgt6))
                time.sleep(.1)
                recebi_msgt3 = False
                pckgOK = False 
            else:
                numPckg = head_msgt3[3]
                n_pacote = head_msgt3[4]
                print('enviei msgt4')
                msgt4 = [4, 0, 0, 0, 0, 0, 0, n_pacote, 0, 0, 170, 187, 204, 221]
                com1.sendData(bytes(msgt4))
                time.sleep(.1)
                cont += 1
                recebi_msgt3 = False
                pckgOK = False
                for i in conteudo_pacote:
                    conteudo_total.append(i)
            
        print('payload completo', conteudo_total)

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