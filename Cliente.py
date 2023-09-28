#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################

# sudo chmod 777 /dev/ttyACM0

#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 
import sys
sys.path.append('../')  # Volte um diretório para chegar à pasta do projeto

from enlace import *
import time
import numpy as np
from random import *
import sys
import datetime


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
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
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        print("enviando byte sacrificio")
        time.sleep(.2)
        com1.sendData(bytes([0]))
        time.sleep(0.1)



        n_pacotes=10
        mensagem1=[1,1,0,n_pacotes,0,1,0,0,0,0,170,187,204,221]
        inicia=False

        #criando arquivo
        nomearquivo="Client4.txt"
        with open(str(nomearquivo),"w") as arquivo:
            pass
            
        mandoudenovo=False
        while inicia==False:
            mensagem1_bytes=bytes(mensagem1)
            com1.sendData(mensagem1_bytes)
            with open(str(nomearquivo),"a") as arquivo:
                arquivo.write(str(datetime.datetime.now())+ " / envio"+ "/ " + "1"+ " / " +str(len(mensagem1_bytes))+ "\n")

            time.sleep(2)
            msg2bytes=com1.rx.getNData(14)
            msg2=list(msg2bytes)
            print("msg2", msg2)
            if msg2[0]==2 and msg2[10]==170 and msg2[11]==187 and msg2[12]==204 and msg2[13]==221:
                inicia=True
                with open(str(nomearquivo),"a") as arquivo:
                    arquivo.write(str(datetime.datetime.now())+ " / receb"+ "/ " + "2"+ " / " +str(len(msg2bytes))+ "\n")
                print("mensagem certa 2 recebida com sucesso")

        print("Iniciar envio de pacotes")
        #mudar para alterar a mensagem        
        cont=1
        
        payload1=[1,2,3,4,5,6]*19
        payload2=[2,2,3,4,5,6]*19
        payload3=[3,2,3,4,5,6]*19
        payload4=[4,2,3,4,5,6]*19
        payload5=[5,2,3,4,5,6]*19
        payload6=[6,2,3,4,5,6]*19
        payload7=[7,2,3,4,5,6]*19
        payload8=[8,2,3,4,5,6]*19
        payload9=[9,2,3,4,5,6]*19
        payload10=[2,2,2,2,2]*5
        payloadt=[payload1,payload2,payload3,payload4,payload5,payload6,payload7,payload8,payload9,payload10]
        recebido_sucesso=0
        
        
        
        
        
        while cont<=n_pacotes:
            mensagem3=[3,1,0,n_pacotes,cont,len(payloadt[(cont-1)]),0,recebido_sucesso,0,0]
            for byte in payloadt[cont-1]:
                mensagem3.append(byte)
            mensagem3.append(170)
            mensagem3.append(187)
            mensagem3.append(204)
            mensagem3.append(221)
            mensagem3_bytes=bytes(mensagem3)
            
            
            print("enviado pacote",cont)
            print('mensagem normal', mensagem3)
            com1.sendData(mensagem3_bytes)
            

            with open(str(nomearquivo),"a") as arquivo:
                arquivo.write(str(datetime.datetime.now())+ " / envio"+ "/ " + "3"+ " / " +str(len(mensagem3_bytes))+ " / " + str(cont)+ " / "+ str(mensagem3[3])+ "\n")
            
            time.sleep(0.1)
            timer1=time.time()
            if mandoudenovo==False:
                timer2=time.time()
            
            recebeumsg4=False
            while recebeumsg4==False :
                print(time.time()-timer2)
                if (time.time()-timer2)>20:
                    print("envia mensagem t5")
                    mensagem5=[5,0,0,0,0,0,0,0,0,0,170,187,204,221]
                    mensagem5_bytes=bytes(mensagem5)
                    mandoudenovo=False
                    com1.sendData(mensagem5_bytes)
                    with open(str(nomearquivo),"a") as arquivo:
                        arquivo.write(str(datetime.datetime.now())+ " / envio"+ "/ " + "5"+ " / " +str(len(mensagem5_bytes))+ "\n")
                    com1.disable()
                    sys.exit()

                if (time.time()-timer1)>8:
                    recebeumsg4=True
                    print("envia pacote anterior")
                    mandoudenovo=True
                    timer1=time.time()

                if com1.rx.getBufferLen()>=13:
                    
                    msg4bytes=com1.rx.getNData(14)
                    msg4=list(msg4bytes)
                    print('recebi',msg4)
                    if msg4[0]==4:
                        with open(str(nomearquivo),"a") as arquivo:
                            arquivo.write(str(datetime.datetime.now())+ " / recebi"+ "/ " + "4"+ " / " +str(len(msg4bytes)) + "\n")

                        recebeumsg4=True
                        cont+=1
                    
                    else:
                        if msg4[0]==6:
                            recebeumsg4=True
                            with open(str(nomearquivo),"a") as arquivo:
                                arquivo.write(str(datetime.datetime.now())+ " / recebi"+ "/ " + "6"+ " / " +str(len(msg4bytes)) + "\n")

                            print("recebeu msg t6")
                            cont=msg4[6]+1
                            print("mudei o cont para", cont)
                            time.sleep(0.1)

                    

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
