from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32,STRING,BUFFER
import time
import random

class KeyRequest(PacketType): #packet for remote key requesting car's challenge
	DEFINITION_IDENTIFIER="lab2b.student_s.KeyRequest"
	DEFINITION_VERSION="1.0"
	FIELDS=[]
  
class CarChallenge(PacketType): #packet of car's challenge. 
	DEFINITION_IDENTIFIER="lab2b.student_s.CarChallenge"
	DEFINITION_VERSION="1.0"
	FIELDS=[
		("time",UINT32),
		("randnum",UINT32),
		("ID",UINT32)]
    
class KeyResp(PacketType): #packet of key's response 
	DEFINITION_IDENTIFIER="lab2b.student_s.KeyResp"
	DEFINITION_VERSION="1.0"
	FIELDS=[
		("resp",STRING),
		("ID",UINT32)]
    
def TheFunc(t,rand): #this function imitate an encoding function, which key and car use to encode the random number and time in the challenge 
	a=t*1000+rand
	return a

def basicUnitTest():
	packet1=KeyRequest() #key send the request to car
	packet1Bytes=packet1.__serialize__()
	packet1a=KeyRequest.Deserialize(packet1Bytes)
	assert packet1==packet1a
    
	packet2=CarChallenge() #if car receive a request, it will send a challenge, which includes time and a serial of random number, to the key. 
	packet2.time=int(time.time())
	packet2.randnum=random.randint(0,1000)
	packet2.ID=1
	packet2Bytes=packet2.__serialize__()
	packet2a=CarChallenge.Deserialize(packet2Bytes)
	assert packet2==packet2a
   
	packet3=KeyResp() #if key received a challenge from car, it will use TheFunc to process the challenge and send it back to the car as a response
	packet3.resp=TheFunc(packet2a.time,packet2a.randnum)
	packet3.ID=1
	packet3Bytes=packet3.__serialize__()
	packet3a=KeyResp.Deserialize(packet3Bytes)
	assert packet3==packet3a
    
	if(packet3a.resp==str(TheFunc(packet2.time,packet2.randnum))): #once recived the response from key, car will check the response. If it is correct, the doors will open. If not, the doors will not open
 		print("Car's doors open")
	else: print("Not open")
    
if __name__=="__main__":
	basicUnitTest()
