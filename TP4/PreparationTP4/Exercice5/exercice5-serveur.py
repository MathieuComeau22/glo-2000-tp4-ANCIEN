import email
import json
import smtplib
import socket
from typing import NoReturn

import glosocket
import header

def _send_email(email_as_string: str) -> dict:
    try:
        message = email.message_from_string(email_as_string)
        with smtplib.SMTP(host="smtp.ulaval.ca", timeout=5) as connection:
            connection.send_message(message)
    except:
        return {"entete": header.Exercice5.ERREUR}
    return {"entete": header.Exercice5.OK}

def _process_client(socket_client: socket.socket) -> None:
    jsondata = glosocket.recv_msg(socket_client)
    if (jsondata is None):
        return

    try:
        data = json.loads(jsondata)
    except json.JSONDecodeError:
        return

    if (data["entete"] == header.Exercice5.ENVOI):
        answer = _send_email(data["donnees"])
    else:
        answer = {"entete": header.Exercice5.ERREUR}

    answer_as_json: str = json.dumps(answer)
    glosocket.send_msg(socket_client, answer_as_json)
    return

def main() -> NoReturn:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 4321))
    server_socket.listen()

    while True:
        client_socket, _ = server_socket.accept()
        _process_client(client_socket)
        client_socket.close()

if __name__ == "__main__":
    main()
