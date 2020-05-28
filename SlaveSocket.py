#_*_ coding=utf-8 _*_

'''
@Description: In User Settings Edi
@Author: your name
@Date: 2020-02-28 12:51:41
@LastEditTime: 2020-05-28 22:40:51
@LastEditors: Please set LastEditors
'''

import socket, select
import threading, signal

class SlaveSocket():
    BUFFER_SIZE = 2048*1000
    def __init__(self, host='', port=8080, connect_try=5):
        self.host = host
        self.port = port
        self.connected = False
        self.socket = None
        self.connect_try = connect_try
        self.runing = True
        self.commandList = {
            "***************************",
            "  Please Select Command    ",
            "***************************",
            "1. Shutdown PC             ",
            "2. Reboot PC               ",
        }

    def connect(self):
        if self.connected:
            print ('Socket connected!')
            return True
        connect_retry = 0
        while connect_retry<self.connect_try:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print ("host:%s"%str(self.host))
                self.socket.connect((self.host, self.port))
                self.connected = True
                print ("Connect server successful")
                return True
            except Exception as e:
                connect_retry += 1
                print ("Connection fail: %s"%str(e))
                continue
        print ("Fail to connect server!")

    def send(self, command):
        if not self.connected:
            print ("Socket is disconnected!")
            return False
        print ("Send command %s to the server!"%str(command))
        self.socket.send(str(command).encode('utf-8'))

    def recieve(self):
        if not self.connected:
            print ("Socket is disconnected!")
            return False
        while True and (self.runing == True):
            #readable , writable , exceptional = select.select(inputs, outputs, inputs, timeout)  最后一个是超时
            infd, outfd, errfd = select.select([self.socket,], [], [], 5)
            if len(infd) != 0:
                data = self.socket.recv(self.BUFFER_SIZE)
            if len(data):
                print ("Server: %s"%(data))
                #need to do 
        

    def command_select(self):
        for item in self.commandList:
            print (item)

    def signal(self, signum, frame):
        self.runing = False
        print("recive signal: %d" %signum)
    



            
        
        

if __name__=="__main__":
    slave = SlaveSocket(host='192.168.56.1', port=8080)
    slave.connect()
    signal.signal(signal.SIGINT, slave.signal)
    signal.signal(signal.SIGTERM, slave.signal)
    print ("create recv thread")
    recv_thread = threading.Thread(target=slave.recieve)
    print ("start recv thread")
    recv_thread.start()
    slave.send(1)
    
        
        

        
