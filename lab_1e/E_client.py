import playground
from playground.network.packet import PacketType
import asyncio
from packets import KeyRequest,KeyResp,TheFunc,Shutdown
from PassThrough import *

class ClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.status=0
        self.transport=None

    def connection_made(self, transport):
        print("ServerProtocol---connection_made")
        self.transport=transport
        self.transport.write(KeyRequest().__serialize__())
        print("------------------------------")
        print("send:{}".format(KeyRequest().__serialize__()) )
        self._deserializer = PacketType.Deserializer()

    def start(self):
        self.transport.write(KeyRequest().__serialize__())


    def data_received(self, data):
        print("Client---data_received")
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            print('{0}:{1}'.format('packet recived in client',pkt))
            if pkt!=None:
                if pkt.DEFINITION_IDENTIFIER=="lab2b.student_s.CarChallenge" and self.status==0:
                    packet3=KeyResp()
                    packet3.resp=TheFunc(pkt.time,pkt.randnum)
                    packet3.ID=3
                    self.transport.write(packet3.__serialize__())
                    print("Client---send data")
                    self.status+=1

                if pkt.DEFINITION_IDENTIFIER=="lab2b.student_s.Shutdown":
                    self.transport.close()
                else:
                    self.transport.close()

    def connection_lost(self,exc):
        print("Clinet connection Lost:{}".format(exc))
        self.transport=None

loop = asyncio.get_event_loop()
loop.set_debug(enabled=True)

f=StackingProtocolFactory(lambda: HigherPassThrough() ,lambda :LowerPassThrough())
# f=StackingProtocolFactory(lambda: LowerPassThrough() ,lambda :HigherPassThrough())


ptConnector=playground.Connector(protocolStack=f)
playground.setConnector("passthrough",ptConnector)


coro = playground.getConnector('passthrough').create_playground_connection(lambda:ClientProtocol(),'20174.1.1.1',
                                                              55656)

loop.run_until_complete(coro)
# client.start()

loop.run_forever()
loop.close()