from playground.network.common import StackingProtocol,StackingTransport,StackingProtocolFactory

class HigherPassThrough(StackingProtocol):
    def __init__(self):
        self.transport=None
        # self._higherProtocol=ServerProtocol
        print("HigherPassThrough---init")
    def connection_made(self, transport):
        print("HigherPassThrough--connection_made")
        self.transport=transport
        highertransport=StackingTransport(transport)
        self.higherProtocol().connection_made(highertransport)
        # self.higherProtocol().connection_made(transport)

    def data_received(self, data):
        print("HigherPassThrough---data_received")
        self.higherProtocol().data_received(data)
        self.data=data


    def connection_lost(self, exc):
        print ("H lost")


class LowerPassThrough(StackingProtocol):
    def __init__(self):
        self.transport=None
        # self._higherProtocol=HigherPassThrough
        print("LowerPassThrough---init")
    def connection_made(self, transport):
        print("LowerPassThrough---connection_made")
        self.transport=transport
        highertransport=StackingTransport(transport)
        self.higherProtocol().connection_made(highertransport)
        # self.higherProtocol().connection_made(self.transport)

    def data_received(self, data):
        print("LowerPassThrough---data_received")
        self.higherProtocol().data_received(data)

    def connection_lost(self, exc):
        print ("L lost")
