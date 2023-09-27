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
        msgt3 = False
        pckgOK = False

        while cont <= numPckg:
            timer1 = time.time()
            timer2 = time.time()

            # print('COMECAONDO A RECEBER UM PACOTE')
            # print('timer1', time.time() - timer1)
            # print('timer2', time.time() - timer2)

            while (time.time() - timer2) < 20 and msgt3 == False:
                while (time.time() - timer1) < 2 and msgt3 == False:   
                    #RECEBENDO O HEAD
                    rxBuffer = com1.rx.getNData(10)
            
                    decimal_values = []
                    for byte in rxBuffer:
                        decimal_values.append(byte)

                    if decimal_values[0] == 3 and decimal_values[1] == 1:
                        numPckg = decimal_values[3]
                        n_pacote = decimal_values[4]
                        payload = decimal_values[5]
                        ultimo_pacode =decimal_values[7]
                        print("recebeu {} bytes na head, numero pacore: {}".format(len(rxBuffer), n_pacote))

                        #RECEBENDO PAYLOAD
                        rxBuffer = com1.rx.getNData(payload)
                        print("recebeu {} bytes no payload, numero do pacote: {}" .format(len(rxBuffer), n_pacote))

                        decimal_values = []
                        for byte in rxBuffer:
                            decimal_values.append(byte)

                        conteudo_pacote = decimal_values
                        print('payload', conteudo_pacote)

                        #RECEBENDO EOP
                        rxBuffer = com1.rx.getNData(4)
                        print("recebeu {} bytes no EOP, numero do pacote: {}" .format(len(rxBuffer), n_pacote))    

                        decimal_values = []
                        for byte in rxBuffer:
                            decimal_values.append(byte) 

                        if decimal_values[0] == 170 and decimal_values[1] == 187 and decimal_values[2] == 204 and decimal_values[3] == 221:
                            msgt3 = True
                            print('enviando que msg t3 foi recebita c sucesso')
                            pckgOK = True 
                            timer1 = time.time()

                        else:
                            msgt3 = False
                            pckgOK = False
                    
                    else:
                        msgt3 = False
                        pckgOK = False

            if time.time() - timer2 > 20 and msgt3 == False:
                osioso = True 
                msgt5 = [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 170, 187, 204, 221]
                com1.sendData(np.asarray(msgt5))
                time.sleep(.1) 
                print("-------------------------")
                print("Comunicação encerrada")
                print("-------------------------")
                com1.disable()
            else:
                if pckgOK:
                    print('msg4 enviada')
                    msgt4 = [4, 0, 0, 0, 0, 0, 0, n_pacote, 0, 0, 170, 187, 204, 221]
                    print(np.asarray(msgt4))
                    com1.sendData(bytes(msgt4))
                    time.sleep(.1)
                    msgt3 = False
                    cont += 1
                else:
                    print('msg6 enviada e pckgOK:', pckgOK)
                    msgt6 = [6, 0, 0, 0, 0, 0, n_pacote, 0, 0, 0, 170, 187, 204, 221]
                    com1.sendData(np.asarray(msgt6))
                    time.sleep(.1)
                    msgt3 = False









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