#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file   :client.py
# @time   :2023/4/10 16:03
# @Author : CHT1HTSH3212
# @Version:1.0
# @Desc   :
import socket
import datetime
import time
import json


class Client:
    def __init__(self):
        self.server = None
        self.port = None
        self.cli_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cli_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # 绑定IP和端口号
        self.cli_sock.bind(('', 60000))
        # 设置接收数据超时
        self.cli_sock.settimeout(1)

    def start_scan(self, times=10):
        """
        Scan Server
        """
        start_time = datetime.datetime.now()
        end_time = datetime.datetime.now()
        while (end_time - start_time).seconds < times:
            data, addr = self.cli_sock.recvfrom(1024)
            data = data.decode()
            print(data)
            try:
                addr_info = json.loads(data)
            except ValueError:
                print("Failed to parse addr info")
                raise ValueError("Failed to parse addr info")
                continue

            if "Server IP" in addr_info and "PORT" in addr_info:
                self.server = addr_info["Server IP"]
                self.port = int(addr_info["PORT"])
                break
            else:
                print("unknown addr info")

            time.sleep(1)
            end_time = datetime.datetime.now()

    def send_data(self, data):
        print(self.server, self.port)
        try:
            self.cli_sock.sendto(data.encode(), (self.server, self.port))
        except ValueError:
            print(ValueError)


client = Client()
client.start_scan(10)
client.send_data("shutdown")

