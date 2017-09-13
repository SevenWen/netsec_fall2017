from playground.network.testing import MockTransportToStorageStream as MockTransport
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToProtocol
from playground.network.protocols.packets.vsocket_packets import VNICSocketOpenPacket, VNICSocketOpenResponsePacket, \
    PacketType
from playground.network.protocols.packets.switching_packets import WirePacket
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER
import time
import random
import io, asyncio


class KeyRequest(PacketType):  # packet for remote key requesting car's challenge
    DEFINITION_IDENTIFIER = "lab2b.student_s.KeyRequest"
    DEFINITION_VERSION = "1.0"
    FIELDS = []

class Error(PacketType):  # packet for remote key requesting car's challenge
    DEFINITION_IDENTIFIER = "lab2b.student_s.error"
    DEFINITION_VERSION = "1.0"
    FIELDS = []

class CarChallenge(PacketType):  # packet of car's challenge.
    DEFINITION_IDENTIFIER = "lab2b.student_s.CarChallenge"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
        ("time", UINT32),
        ("randnum", UINT32),
        ("ID", UINT32)]


class KeyResp(PacketType):  # packet of key's response
    DEFINITION_IDENTIFIER = "lab2b.student_s.KeyResp"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
        ("resp", STRING),
        ("ID", UINT32)]


def TheFunc(t,rand):  # this function imitate an encoding function, which key and car use to encode the random number and time in the challenge
    a = t * 1000 + rand
    return a

class ClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.status=0
        self.transport=None

    def connection_made(self, transport):
        self.transport=transport
        self._deserializer = PacketType.Deserializer()

    def start(self):
        self.transport.write(Error().__serialize__())


    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            print('{0}:{1}'.format('packet recived in client',pkt))
            if pkt!=None:
                if pkt.DEFINITION_IDENTIFIER=="lab2b.student_s.CarChallenge" and self.status==0:
                    packet3=KeyResp()
                    packet3.resp=TheFunc(pkt.time,pkt.randnum)
                    packet3.ID=3
                    self.transport.write(packet3.__serialize__())
                    self.status+=1
                else: self.transport.close()

    def connection_lost(self,exc):
        print("Clinet connection Lost:".format(exc))
        self.transport=None

class ServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.status = 0
        self.transport=None

    def connection_made(self, transport):
        self.transport = transport
        self._deserializer=PacketType.Deserializer()


    def data_received(self, data):
        self._deserializer.update(data)
        global Time
        global RandNum
        for pkt in self._deserializer.nextPackets():
            print('{0}:{1}'.format('packet recived in SERVER', pkt))
            if pkt!=None:
                if pkt.DEFINITION_IDENTIFIER=="lab2b.student_s.KeyRequest" and self.status==0:
                    packet2=CarChallenge()
                    Time = int(time.time())
                    RandNum=random.randint(0,1000)
                    packet2.time=Time
                    packet2.randnum=RandNum
                    packet2.ID=2
                    self.status+=1
                    self.transport.write(packet2.__serialize__())
                elif pkt.DEFINITION_IDENTIFIER=="lab2b.student_s.KeyResp"and self.status==1:
                    print(pkt.resp,"----",TheFunc(Time,RandNum))
                    self.status+=1
                    if(pkt.resp==str(TheFunc(Time,RandNum))):
                        print("Car's doors open")
                    else: print("Not open")
                else: self.transport.close()

    def connection_lost(self,exc):
        print("Server connection Lost:".format(exc))
        self.transport = None

def basicUnitTest():
    print('Begin')
    asyncio.set_event_loop(TestLoopEx())

    clientProtocol = ClientProtocol()
    serverProtocol = ServerProtocol()
    cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(clientProtocol, serverProtocol)
    clientProtocol.connection_made(cTransport)
    serverProtocol.connection_made(sTransport)

    clientProtocol.start()


if __name__=="__main__":
    basicUnitTest()
    print("Basic Unit Test Successful!")
