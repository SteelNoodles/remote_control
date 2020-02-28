#_*_ coding:utf-8 _*_
'''
@Description: In User Settings Edit
@Author: your name
@Date: 2020-02-27 17:56:02
@LastEditTime: 2020-02-28 16:02:13
@LastEditors: Please set LastEditors
'''

import socket

class MasterSocket():
    BUFFER_SIZE= 2048*100

    def __init__(self, host='', port=8080, sock_accept=5):
        self.host = host
        self.port = port
        self.connected = False
        self.socket = None
        self.sock_accept =  sock_accept


    def bind(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.connected = True
        except Exception, e:
            print "Connect socket fails: %s"%str(e)
            return 
        print "Start to connection listen!"
        self.socket.listen(self.sock_accept)
        while True:
            print "Accpet a connection!"
            conn, addr = self.socket.accept()
            # print "connect addr:%s" + addr
            while True:
                data = conn.recv(self.BUFFER_SIZE)
                if len(data):
                    print "recieve data:%s" %(data)
                    conn.send("OK")
            conn.close()



    # def connect(self):
    #     while self.connect_try:
    #         try:
    #             self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             self.socket.connect((self.host, self.port))
    #             self.connected = True
    #             return True
    #             # if self.socket > 0:
    #             #     self.socket.connect(self.host, self.port)
    #             #     self.connected = True
    #             #     return True
    #             # else:
    #             #     print"Fail to create socket!"
    #         except Exception, e:
    #             print 'socket error, because: %s ' % str(e)
    #             self.connect_try = self.connect_try - 1
    #             continue
    #     if self.connect_try==0:
    #         print "...Fail to connect socket"
    #         return False

    def close(self):
        if self.socket > 0:
            self.socket.close()
        else:
            print "Socket is not exist!"

    def send(self, command):
        '''
        send command to slave...
        '''
        if not self.connected:
            print "Socket is disconnected!"
            return False
        print "Send command %s to the server!"%str(command)
        self.socket.send(str(command).encode('utf-8'))

    # def recv(self):
    #     '''
    #     wait for command from slave
    #     '''
    #     while True:
    #         if not self.connected:
    #             print "connection is not exist!"
    #             if not self.connect():
    #                 return 
    #         else:
    #             try:
    #                 data = self.socket.recv(self.BUFFER_SIZE)
    #                 if len(data):
    #                     print data
    #                 else:
    #                     print "error"
    #             except Exception, e:
    #                 # print 'socket error： '
    #                 # self.connected = False
    #                 continue

    def run(self):
        pass

        
if __name__=='__main__':
    master = MasterSocket()
    master.bind()
            
        

