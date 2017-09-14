import playground
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING,UINT32,BOOL
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
import asyncio
import time
import random

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
        self.transport.write(KeyRequest().__serialize__())
        self._deserializer = PacketType.Deserializer()

    def start(self):
        self.transport.write(KeyRequest().__serialize__())


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

loop = asyncio.get_event_loop()

coro = playground.getConnector().create_playground_connection(lambda:ClientProtocol(),'20174.1.1.1',
                                                              101)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
