import select
import socket
from typing import NoReturn

from ModulesTP import glosocket

HEADER_NAME = "NOM"
HEADER_AGE = "AGE"
client_list: list[socket.socket] = []


def _prepare_socket() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 1234))
    server_socket.listen()
    return server_socket


def _new_client(server_socket: socket.socket) -> None:
    client_socket, _ = server_socket.accept()
    client_list.append(client_socket)
    glosocket.send_msg(client_socket, "Bienvenue, quel votre nom/age ?")
    return


def _get_name(data: str) -> str:
    return f"Bienvenue {data}"


def _get_age(data: str) -> str:
    return f"{data} ? Vous êtes bien jeune !"


def _process_client(client_socket: socket.socket) -> None:
    message = glosocket.recv_msg(client_socket)
    # Si le client s'est déconnecté, on le retire de la liste.
    if (message is None):
        client_list.remove(client_socket)
        client_socket.close()
        return

    header, data = message.split(maxsplit=1)
    if (header == HEADER_NAME):
        answer = _get_name(data)
    elif (header == HEADER_AGE):
        answer = _get_age(data)

    glosocket.send_msg(client_socket, answer)
    return


def main() -> NoReturn:
    server_socket = _prepare_socket()

    while True:

        waiting_list, _, _ = select.select(
        [server_socket] + client_list, [], [])

        for waiter in waiting_list:
            if (waiter == server_socket):
                _new_client(waiter)
            # Sinon, on traite le client.
            else:
                _process_client(waiter)


if __name__ == "__main__":
    main()
