import socket
from threading import Thread, Event
from ucl.common import pretty_print_obj

from ucl.highState import highState

listenPort = 8090
sendPort_low = 8007
sendPort_high = 8082

local_ip_wifi = '192.168.12.14'
local_ip_eth = '192.168.123.16'
addr_wifi = '192.168.12.1'
addr_low = '192.168.123.10'
addr_high = '192.168.123.161'


LOW_WIRED_DEFAULTS = (listenPort, addr_low, sendPort_low, local_ip_eth)
LOW_WIFI_DEFAULTS = (listenPort, addr_low, sendPort_low, local_ip_wifi)
HIGH_WIRED_DEFAULTS = (listenPort, addr_high, sendPort_high, local_ip_eth)
HIGH_WIFI_DEFAULTS = (listenPort, addr_wifi, sendPort_high, local_ip_wifi)

class unitreeConnection:
    def __init__(self, settings=HIGH_WIFI_DEFAULTS):
        self.listenPort = settings[0]
        self.addr = settings[1]
        self.sendPort = settings[2]
        self.localIP = settings[3]
        self.sock = self.connect()
        self.runRecv = Event()
        self.recvThreadID = None
        self.data = []

    def startRecv(self):
        self.recvThreadID = Thread(target=self.recvThread, args=(self.runRecv,))
        self.recvThreadID.daemon = True
        self.recvThreadID.start()

    def stopRecv(self):
        self.runRecv.set()
        self.recvThreadID.join()

    def connect(self):
        sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

        # sock.bind((self.localIP, self.listenPort))
        sock.settimeout(1)
        return sock

    def send(self, cmd):
        self.sock.sendto(cmd, (self.addr, self.sendPort))

    def recvThread(self, event):
        # print('[*] Start receive Thread ...\n')
        while not event.isSet():
            try:
                self.data.append(self.sock.recv(2048))
            except Exception as e:
                # print(e)
                pass
        # print('[*] Exited receive Thread ...')

    def getData(self):
        ret = self.data.copy()
        # Clear data buffer after handing it out
        self.data.clear()
        return ret
