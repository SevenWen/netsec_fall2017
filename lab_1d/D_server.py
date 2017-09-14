import playground
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING,UINT32
from packets import CarChallenge,TheFunc,Shutdown
import time
import random
import asyncio

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
                    packet4=Shutdown()
                    self.transport.write(packet4.__serialize__())
                    self.transport.close()
                else: self.transport.close()

    def connection_lost(self,exc):
        print("Server connection Lost:".format(exc))
        self.transport = None

loop = asyncio.get_event_loop()
loop.set_debug(enabled=True)
# Each client connection will create a new protocol instance
coro = playground.getConnector().create_playground_server(lambda:ServerProtocol(),
                                                          55656)
server = loop.run_until_complete(coro)

loop.run_forever()

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()