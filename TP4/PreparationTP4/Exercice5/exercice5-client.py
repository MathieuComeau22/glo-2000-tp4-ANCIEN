import email.message
import json
import socket

from ModulesTP import glosocket
from Headers import header

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect(("localhost", 4321))

courriel = email.message.EmailMessage()
courriel["From"] = "exercice5@glo2000.ca"
courriel["To"] = input("Entrez l'adresse de destination : ")
courriel["Subject"] = "Exercice 5"
courriel.set_content("Vous êtes prêt pour le TP4!")
message = json.dumps({
    "entete": header.Exercice5.ENVOI,
    "donnees": courriel.as_string()
})

glosocket.send_msg(socket_client, message)

answer = json.loads(glosocket.recv_msg(socket_client))
if (answer["entete"] == header.Exercice5.OK):
    print("Message envoyé avec succès.")
elif (answer["entete"] == header.Exercice5.ERREUR):
    print("Le message n'a pas pu être envoyé.")

socket_client.close()