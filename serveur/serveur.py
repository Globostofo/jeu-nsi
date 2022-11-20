import socket
import os
from _thread import *
import time

global msg
global game
global gameedit
global conexions
global conexionsedit
global nobredexonexion
msg=[]
game=[]
gameedit=True
conexions=[]
conexionsedit=True


ServerSocket = socket.socket()
host = '127.0.0.1'
port = 65439
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    arecherche=False
    IDgame=""
    ID=conexion()
    global nobredexonexion
    nobredexonexionprécédente=0
    
    if len(msg) >= 10:
        
        i=len(msg)-10
        
    else:
        i=0
    while True:
        
        time.sleep(0.2)

        if len(msg) > i:
            
            connection.sendall(msg[i])
            i=i+1
        elif nobredexonexionprécédente!= nobredexonexion:
            connection.sendall(bytes(str(2)+str(nobredexonexion),'utf-8'))
            nobredexonexionprécédente=nobredexonexion
        else:
            
            connection.sendall(bytes(" ",'utf-8'))
        data = connection.recv(2048)
        if not data:
            break
        conexions[ID][2]=0
        if data != bytes(" ",'utf-8'):
            
            if data.decode('utf-8')[0]==str(0):

                msg.append(data)
            elif data.decode('utf-8')[0]==str(1):
                conexions[ID][0]=True
                arecherche=True
        if arecherche==True:
            for j in range(len(game)):
                if game[j][1][0]==ID:
                    IDgame=j
                    arecherche=False
                elif game[j][1][1]==ID:
                    IDgame=j
                    arecherche=False
            print("jesuisdansla parti",IDgame,arecherche)

    connection.close()

def recherchematch():
    for i in range(0,len(conexions)):
        if conexions[i][0] == True:
            jouer1=i
            for j in range(i+1,len(conexions)):
                if conexions[j][0] == True:
                    jouer2=j
                    conexions[j][0] = False
                    conexions[i][0] = False
                    return jouer1,jouer2
    return False
def matche():
    while True:
        time.sleep(1)
        rezmatch=recherchematch()
        if rezmatch != False:
            IDgame=recherche()
            
            game[IDgame][0]=False
            game[IDgame][1][0]=rezmatch[0]
            game[IDgame][1][1]=rezmatch[1]
        
            
def updateconexion():
    global nobredexonexion
    while True:
        time.sleep(5)
        temp=0
        for i in range(len(conexions)):
            if conexions[i][2] < 5:
                temp += 1
        nobredexonexion= temp



def ingame(connection):
    pass
    






def conte():
    global conexionsedit
    
    while True:
        
        time.sleep(1)
        conexionsedit=False
        for i in range(0,len(conexions)):
            if conexions[i][2]<10:
                conexions[i][2]=int(conexions[i][2])+1
        conexionsedit=True
        print(conexions)
def conexion():
    global conexionsedit
    while conexionsedit==False:
        time.sleep(0.1)
    conexionsedit=False
    temp=[False,len(conexions)+1,0]
    
    conexions.append(temp)
    i=len(conexions)
    conexionsedit=True
    
    return i-1

def recherche():
    global gameedit
    temp=[True,[0,0]]
    while gameedit==False:
        time.sleep(0.1)
    gameedit=False
    for i in range(len(game)):
        if game[i][0]==True:
            gameedit=True
            return i
    game.append(temp)
    i=len(game)
    gameedit=True
    return i-1
start_new_thread(conte,())
start_new_thread(matche,())
start_new_thread(updateconexion,())
while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()