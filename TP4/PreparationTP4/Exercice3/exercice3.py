import argparse
import email.message
import re
import smtplib
import socket
from typing import NoReturn


def _get_port() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store",
                        dest="port", type=int, default=1400)
    return parser.parse_args().port


def _prepare_socket(port: int) -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", port))
    server_socket.listen()
    print(f"Listening on port {server_socket.getsockname()[1]}")
    return server_socket


def _server_loop(server_socket: socket.socket) -> NoReturn:
    address_request: bytes = "À qui dois-je envoyer un courriel ?\n".encode()
    address_error: bytes = "Saisissez une adresse valide : ".encode()
    verificator: re.Pattern = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )
    while True:
        client, _ = server_socket.accept()
        client.send(address_request)
        dest_address = client.recv(1024).decode().strip(" \n")
        while (verificator.fullmatch(dest_address) is None):
            client.send(address_error)
            dest_address = client.recv(1024).decode().strip(" \n")
        # Création du courriel
        courriel = email.message.EmailMessage()
        courriel["From"] = "exercice3@glo2000.ca"
        courriel["To"] = dest_address
        courriel["Subject"] = "Exercice 3"
        courriel.set_content("Courriel envoyé par le serveur.")
        try:
            with smtplib.SMTP(host="smtp.ulaval.ca", timeout=10) as connexion:
                connexion.send_message(courriel)
                answer = "Message envoyé avec succès."
        except smtplib.SMTPException:
            answer = "Le message n'a pas pu être envoyé."
        except socket.timeout:
            answer = "Le serveur SMTP est injoinable."
        client.send(answer.encode())
        client.close()


def main() -> NoReturn:
    port = _get_port()
    server_socket = _prepare_socket(port)
    _server_loop(server_socket)


if __name__ == "__main__":
    main()