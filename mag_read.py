# necessary libs
import json
import socket
import select

# udp client (sender) configuration
# set destination IP and port -> Raspberry Pi
UDP_IP = "169.254.133.53"
UDP_PORT = 8803
# udp clinet (listener) configuration
# set own IP to bind -> your PC


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock_in = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

# sock_in.bind((UDP_IP_SELF, UDP_PORT_SELF))

# send any data to Rapsberry Pi to start measurement
sock.sendto(bytes("", "utf-8"), (UDP_IP, UDP_PORT))
# receive and decode measurement data
message, address = sock.recvfrom(1024) 
data = json.loads(message.decode("utf-8"))
# display measurement data
print("From: " + str(address) + " bytes: " + str(len(message)) + " data: ", end='')
print(data)
sock.close()