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

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self):
        self._deserializer=PacketType.Deserializer()
        self.transport=None

    def connection_made(self, transport):
        self.transport=transport
        packet1=KeyRequest()
        transport.write(packet1.__serialize__())
        self._deserializer=PacketType.Deserializer()

    def dataReceived(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            print(pkt)
            if pkt!=None:
                if pkt.DEFINITION_IDENTIFIER=="lab2b.student_s.CarChallenge":
                    packet3=KeyResp()
                    packet3.resp=TheFunc(pkt.time,pkt.randnum)
                    packet3.ID=3
                    self.transport.write(packet3.__serialize__())


    def connection_lost(self, exc):
        self.transport=None
        print('3.The server closed the connection')
        print('3.Stop the event loop')

class EchoServerProtocol(asyncio.Protocol):
    def __init__(self):
        self._deserializer=PacketType.Deserializer()
        self.transport=None

    def connection_made(self, transport):
        self.transport = transport
        self._deserializer=PacketType.Deserializer()

    def dataReceived(self, data):
        self._deserializer.update(data)
        global Time
        global RandNum
        for pkt in self._deserializer.nextPackets():
            print(pkt)
            if pkt!=None:
                if pkt.DEFINITION_IDENTIFIER=="lab2b.student_s.KeyRequest":
                    packet2=CarChallenge()
                    Time = int(time.time())
                    RandNum=random.randint(0,1000)
                    packet2.time=Time
                    packet2.randnum=RandNum
                    packet2.ID=2
                    self.transport.write(packet2.__serialize__())
                if pkt.DEFINITION_IDENTIFIER=="lab2b.student_s.KeyResp":
                    print(pkt.resp,"----",TheFunc(Time,RandNum))
                    if(pkt.resp==str(TheFunc(Time,RandNum))):
                        print("Car's doors open")
                    else: print("Not open")
                else: print("no proper packet")
                
        print('7.Close the client socket')

    def connection_lost(self, exc):
        self.transport = None
        print('8.Closed the connection')

def basicUnitTest():
    asyncio.set_event_loop(TestLoopEx())

    client=EchoClientProtocol()
    server=EchoServerProtocol()

    transportToServer=MockTransportToProtocol(server)
    transportToClient=MockTransportToProtocol(client)


    server.connection_made(transportToClient)
    client.connection_made(transportToServer)

if __name__=="__main__":
    basicUnitTest()
    print("Basic Unit Test Successful!")
