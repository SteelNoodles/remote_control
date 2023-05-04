#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file   :server.py
# @time   :2023/4/10 15:09
# @Author : CHT1HTSH3212
# @Version:1.0
# @Desc   :
import os
import socket
import threading
import time

PORT = "60009"


def get_host_name():
    res = socket.gethostbyname(socket.gethostname())
    return res


class Server:
    def __init__(self, port="8600"):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.host_ip = get_host_name()
        self.connected = False
        self.broadcast_running = False
        self.broadcast_thread = None

    def broadcast(self):
        """
        Broadcast Server IP:PORT
        """
        self.broadcast_running = True
        while not self.connected and self.broadcast_running:
            try:
                server_info = """{"Server IP":"%s", "PORT":%s}""" % (self.host_ip, PORT)
                self.broadcast_sock.sendto(server_info.encode('UTF-8'), ('127.0.0.1', 60000))
            except ValueError:
                raise ValueError("Failed to broadcast")
            time.sleep(1)

    def start_broadcast(self):
        """
        Start broadcast thread
        """
        self.broadcast_thread = threading.Thread(target=self.broadcast)
        self.broadcast_thread.daemon = True
        self.broadcast_thread.start()

    def stop_broadcast(self):
        print("Stop broadcast")
        self.broadcast_running = False

    def run(self):
        self.sock.bind(('', 60009))

        while True:
            data, addr = self.sock.recvfrom(1024)
            self.command_recv(data.decode())

    def command_recv(self, command):
        """
        Waiting for operation command.
        Disconnect in 60s or  client close
        """
        if command == "shutdown":
            print("Remote control: shutdown PC")
            # os.system("shutdown -f -s -t 10 -c closing...")
        else:
            print("Unknown command: %s" % command)


if __name__ == "__main__":
    server = Server()
    server.start_broadcast()
    server.run()
    server.stop_broadcast()


