import socket
import binascii
import urllib
import time

def wol(mac):
    def format(mac):
        f = lambda x: x.strip() if len(x.strip()) == 12 else x.strip().replace(x.strip()[2], "")
        mac = f(mac)
        return mac
    def sendto(r):
        s.sendto(r,(ip,port))
    ip="192.168.199.255"
    port=9
    ps="fsfafda" #password
    ps=ps.encode()
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        sendto(binascii.unhexlify('FF'*6+ format(mac) *16)+ps)
        s.close()
    except TypeError:
        print('type error' + mac)

def getlist():
    f = urllib.urlopen('http://wake.lzjwlt.cn/')
    data = f.read()
    return data.split("\n")

def delete(mac):
    f = urllib.urlopen('http://wake.lzjwlt.cn/delete/'+mac).read()


def daemon():
    while True:
        datas = getlist()
        for data in datas:
            delete(data)
            if len(data) == 12:
                wol(data)
        time.sleep(10)


if __name__ == '__main__':
    daemon()