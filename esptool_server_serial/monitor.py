# #https://stackoverflow.com/questions/61166544/readline-in-pyserial-sometimes-captures-incomplete-values-being-streamed-from
# import serial
# import time
# import os
# import argparse
# import asyncio
# import websockets


# parser = argparse.ArgumentParser(description='Serial Port Monitor')
# parser.add_argument('--port', '-p', help='端口', required=True)
# parser.add_argument('--baud', '-b', help='波特率', required=True)
# args = parser.parse_args()



# ser = serial.Serial(port=args.port,
#                     baudrate=args.baud,
#                     timeout=0)
# while True:                            
#     time.sleep(.001)                   
#     val = ser.readline()               
#     while not '\\n'in str(val):        

#         time.sleep(.001)                
#         temp = ser.readline()           
#         if not not temp.decode():       
#             val = (val.decode()+temp.decode()).encode()
#     val = val.decode()                  
#     # val = val.strip()                 
#     val = os.linesep.join([s for s in val.splitlines() if s])
#     print(val)




import asyncio
from websockets import serve

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())