import socket
import threading
import time
import copy
import os
from _thread import *
# from pythonping import ping
stop=False

def tri(data):
    for i in range(len(data)):
        temp=data[i]
        j=i
        while int(data[j-1][2])<int(temp[2]) and j>0:
            data[j]=data[j-1]
            j=j-1

        data[j]=temp

    return data

def split(data):
    data=data.decode('utf-8')
    data = data.split(' / ')
    data.pop(0)
    v=[]
    t=0
    for i in range (int(len(data)/3)):
        x=[]
        for j in range (3):
            x.append(data[t])
            t=t+1
        v.append(x)
    return v

class server:

    def connexion(pseudo, score):
        HOST = '127.0.0.1'
        PORT = 65438

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            v=(bytes(pseudo,'utf-8')+bytes(' / ','utf-8')+bytes(score,'utf-8'))
            s.sendall(v)
            data = s.recv(1024)

        return tri(split(data))

pseudo = "Ok booer"
score = "20"

#print(server.connexion(pseudo, score))


class Tchat:

    def stop():
        global stop
        stop=True
    def start():
        x=threading.Thread(target=Tchat.maine)
        x.start()

    def maine():
        HOST = '51.91.103.36'
        PORT = 65439
        global nobredexonexion

        i=0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while stop==False:


                data = s.recv(2048)

                if data != bytes(" ",'utf-8'):
                    if data.decode('utf-8')[0]==str(0):
                        data=data.decode('utf-8')
                        data=data[1:]
                        msg.append(Tchat.décripye(data))
                    elif data.decode('utf-8')[0]==str(2):
                        data=data.decode('utf-8')
                        nobredexonexion=data[1:]





                if len(inpu) >i:
                    s.sendall(bytes(inpu[i],'utf-8'))

                    i=i+1
                else:
                    s.sendall(bytes(" ",'utf-8'))

    def envoi(pseudo, message):
        aenvoiler=[]
        temp=time.localtime()
        for i in range (6):
            aenvoiler.append(temp[i])
        aenvoiler.append(pseudo)
        aenvoiler.append(message)

        msgfinal=str(aenvoiler[0])
        for i in range (1,len(aenvoiler)):
            msgfinal=msgfinal+"/"+str(aenvoiler[i])
        msgfinal=str(0)+msgfinal
        inpu.append(msgfinal)

    def listemsg():
        temp=copy.deepcopy(msg)
        while len(temp)>7:
            temp.pop(0)


        times=time.localtime()
        # print(temp)
        for i in range (len(temp)):

            temp[i][0][1] = temp[i][0][1].zfill(2)
            temp[i][0][2] = temp[i][0][2].zfill(2)
            temp[i][0][4] = temp[i][0][4].zfill(2)
            if times[4]==int(temp[i][0][4]) and times[3]==int(temp[i][0][3]) and times[2]==int(temp[i][0][2]) and times[1]==int(temp[i][0][1]) and times[0]==int(temp[i][0][0]):
                temp[i][0]="A l'instant"
            elif times[2]==int(temp[i][0][2]) and times[1]==int(temp[i][0][1]) and times[0]==int(temp[i][0][0]):
                temp[i][0]=f"Aujourd'hui à {temp[i][0][3]}:{temp[i][0][4]}"
            elif times[2]-1==int(temp[i][0][2]) and times[1]==int(temp[i][0][1]) and times[0]==int(temp[i][0][0]):
                temp[i][0]=f"Hier à {temp[i][0][3]}:{temp[i][0][4]}"
            else:
                temp[i][0]=f"Le {temp[i][0][2]}/{temp[i][0][1]}/{temp[i][0][0]} à {temp[i][0][3]}:{temp[i][0][4]}"

        return temp
    def décripye(data):
        temp=[]
        temp2=[]
        data=data.split("/",7)
        for i in range(6):
            temp.append(data[i])
        for i in range(6,8):
            temp2.append(data[i])
        data=[temp,temp2]

        return data
    def recherchedegame():
        inpu.append("1")

    def nobredexonexions():
        return nobredexonexion
global msg
msg=[]
global inpu
inpu=[]
global nobredexonexion
nobredexonexion=0

#psedo="pd"
#Tchat.start()
#for i in range(3):

# Tchat.recherchedegame()




#class multi:







class yping:
    def __init__(self):
        self.ip=["51.91.103.36","127.0.0.1"]

    def ping(hostname):
        try:
            ping(hostname, verbose=False)
            ipup.append(hostname)
        except:
            print("eror")



    def up(self):
        global ipup
        ipup=[]
        for i in range(len(self.ip)):
            start_new_thread(yping.ping,(self.ip[i],))

    def server():
        return ipup



# yping()
# yping.up(yping())
# while True:
#     print(yping.server())


