from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32,STRING,BUFFER
import time
import random

class KeyRequest(PacketType):
  DEFINITION_IDENTIFIER="lab2b.student_s.KeyRequest"
  DEFINITION_VERSION="1.0"
  FIELDS=[]
  
class CarChallenge(PacketType):
  DEFINITION_IDENTIFIER="lab2b.student_s.CarChallenge"
  DEFINITION_VERSION="1.0"
  FIELDS=[
      ("time",UINT32),
      ("randnum",UINT32),
      ("ID",UINT32)
    ]
    
 class KeyResp(PacketType):
  DEFINITION_IDENTIFIER="lab2b.student_s.KeyResp"
  DEFINITION_VERSION="1.0"
  FIELDS=[
      ("resp",STRING),
      ("ID",UINT32)
    ]
    
 def TheFunc(t,rand)
   a=t*1000+rand
   return a
 def basicUnitTest()
   packet1=KeyRequest()
   packet1Bytes=packet1.__serialize__()
   packet1a=KeyRequest.Deserialize(packet1Bytes)
   assert packet1==packet1a
    
   packet2=CarChallenge()
   packet2.time=int(time.time())
   packet2.random=random.randint(0,1000)
   packet2.ID=1
   packet2Bytes=packet2.__serialize__()
   packet2a=CarChallenge.Deserialize(packet2Bytes)
   assert packet2==packet2a
   
   packet3=KeyResp()
   packet3.resp=TheFunc(packet2a.time,packet2a.randnum)
   packet3.ID=1
   packet3Bytes=packet3.__serialize__()
   packet3a=KeyRequest.Deserialize(packet3Bytes)
   assert packet3==packet3a
    
   if(packet3a.resp==str(TheFunc(packet2.time,packet2,randnum))):
      print("Car's doors open")
   else: print("Not open")
    
 if __name__=="__main__":
    basicUnitTest()
