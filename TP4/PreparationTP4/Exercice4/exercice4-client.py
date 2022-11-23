import socket
from ModulesTP import glosocket

HEADER_NAME = "NOM"
HEADER_AGE = "AGE"

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect(("localhost", 1234))

print(glosocket.recv_msg(socket_client))

message = " ".join([HEADER_NAME, input("Nom : ")])
glosocket.send_msg(socket_client, message)

print(glosocket.recv_msg(socket_client))

message = " ".join([HEADER_AGE, input("Age : ")])
glosocket.send_msg(socket_client, message)

print(glosocket.recv_msg(socket_client))

socket_client.close()