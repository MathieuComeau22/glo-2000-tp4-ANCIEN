import argparse
import socket

from TP4 import *


def get_arguments() -> Tuple[bool, bool, int, Optional[str]]:
    """
    Cette fonction doit :
    - ajouter les arguments attendus aux parser,
    - recuperer les arguments passes,
    - retourner un tuple contenant dans cet ordre : 
        1. est-ce que le protocole est IPv6 ? (Booleen)
        2. est-ce que le mode est « ecoute » ? (Booleen)
        3. le port choisi (entier)
        4. l’adresse du serveur (string si client, None si serveur)
    """
    parser = argparse.ArgumentParser(description="Description du programme.")
    parser.add_argument("-p", "--port", dest="port", type=int, action="store", required=True)
    parser.add_argument("-6", dest="ipv6", action="store_true", default=False)

    groupe = parser.add_mutually_exclusive_group(required=True)

    # Enfin, on ajoute les options au groupe d'exclusion
    groupe.add_argument("-l", "--listen", dest="server", action="store_true", default=False)
    groupe.add_argument("-d", "--destination", dest="destination", action="store")

    arguments = parser.parse_args()
    
    adresse = None
    if not arguments.server:
        adresse = arguments.destination

    return (arguments.ipv6, arguments.server, arguments.port, adresse)


def make_server_socket(port: int, est_ipv6: bool) -> socket.socket:
    """
    Cette fonction doit creer le socket du serveur, le lier au port
    et demarrer l’ecoute.

    Si le port est invalide ou indisponible, le programme termine.
    """

    try:
        iptype = socket.AF_INET
        if est_ipv6:
            iptype = socket.AF_INET6
        socket_serveur = socket.socket(iptype, socket.SOCK_STREAM) 
        socket_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        socket_serveur.bind(("localhost", port))
        socket_serveur.listen(5)
    except Exception:
        print("error in make_server_socket()")
        exit()

    return socket_serveur


def make_client_socket(destination: str, port: int, est_ipv6: bool) -> socket.socket:
    """
    Cette fonction doit creer le socket du client et le connecter au serveur.

    Si la connexion echoue, le programme termine.
    """
    try:
        iptype = socket.AF_INET
        if est_ipv6:
            iptype = socket.AF_INET6
        socket_client = socket.socket(iptype, socket.SOCK_STREAM)
        socket_client.connect((destination, port))
    except Exception:
        print("error in make_client_socket()")
        exit()
    return socket_client


def generate_mod_base(destination: socket.socket) -> Optional[Tuple[int, int]]:
    """
    Cette fonction doit :
    - à l’aide du module glocrypto, generer le modulo et la base, 
    - à l’aide du module glosocket, transmettre à la destination
    deux messages contenant respectivement :
        1. le modulo
        2. la base
    - retourner un tuple contenant les deux valeurs dans ce même ordre.
    """
    try:
        modulo = trouver_nombre_premier()
        base = entier_aleatoire(modulo)
        send_msg(destination, str(modulo))
        send_msg(destination, str(base))
    except Exception:
        print("error generate_mod_base")
    return (modulo, base)


def fetch_mod_base(source: socket.socket) -> Tuple[int, int]:
    """
    Cette fonction doit :
    - à l’aide du module glosocket, recevoir depuis la source
    deux messages contenant respectivement :
        1. le modulo
        2. la base
    - retourner un tuple contenant les deux valeurs dans ce même ordre.

    Si l’une des réceptions echoue, le programme termine.
    """
    modulo = recv_msg(source)
    if modulo is None:
        exit()
    base = recv_msg(source)
    if base is None:
        exit()
    return (int(modulo), int(base))


def generate_pub_prv_keys(modulo: int, base: int) -> Tuple[int, int]:
    """
    Cette fonction doit :
    - à l’aide du module glocrypto, générer une cle privee,
    - à l’aide du module glocrypto, générer une cle publique,
    - retourner un tuple contenant respectivement :
        1. la cle privee
        2. la cle publique
    """
    cle_pub = entier_aleatoire(modulo)
    cle_prv = exponentiation_modulaire(base, cle_pub, modulo)
    return (cle_prv, cle_pub)


def exchange_keys(destination: socket.socket, cle_pub: int) -> Optional[int]:
    """
    Cette fonction doit respectivement :
    1. à l’aide du module glosocket, envoyer sa cle publique à la destination,
    2. à l’aide du module glosocket, recevoir la cle publique de la destination

    Si l’envoi ou la reception echoue, la fonction retourne None.
    """
    try:
        send_msg(destination, str(cle_pub))
        cle_pub_ext = recv_msg(destination)
        if cle_pub_ext is None:
            return None
        return int(cle_pub_ext)
    except Exception:
        return None


def compute_shared_key(modulo: int, cle_prv: int, cle_pub: int) -> int:
    """
    Cette fonction doit, à l’aide du module glocrypto, deduire la cle partagee.
    """
    
    return exponentiation_modulaire(cle_prv, cle_pub, modulo)


def server(port: int, est_ipv6: bool) -> NoReturn:
    """
    Cette fonction constitue le point d’entree et la boucle principale du serveur.

    Si la connexion à un client est interrompue, le serveur abandonne ce client
    et en attend un nouveau.
    """
    socket_serveur = make_server_socket(port, est_ipv6)
    while True:
        try:
            socket_client, adresse_client = socket_serveur.accept()
            modulo, base = generate_mod_base(socket_client)
            cle_prv, cle_pub = generate_pub_prv_keys(modulo, base)
            cle_pub_ext = exchange_keys(socket_client, cle_pub)
            cle_partage = compute_shared_key(modulo, cle_prv, cle_pub_ext)
            print(cle_partage)
        except Exception:
            print("error in server()")
            continue


def client(destination: str, port: int, est_ipv6: bool) -> None:
    """
    Cette fonction constitue le point d’entree et la boucle principale du client.

    Si la connexion au serveur est interrompue, le client termine.
    """
    socket_client = make_client_socket(destination, port, est_ipv6 )
    try:
        modulo, base = fetch_mod_base(socket_client)
        cle_prv, cle_pub = generate_pub_prv_keys(modulo, base)
        cle_pub_ext = exchange_keys(socket_client, cle_pub)
        cle_partage = compute_shared_key(modulo, cle_prv, cle_pub_ext)
        print(cle_partage)
    except Exception:
        print("error in client()")
        exit()


def main() -> None:
    est_ipv6, est_serveur, port, destination = get_arguments()
    if est_serveur:
        server(port, est_ipv6)
    else:
        client(destination, port, est_ipv6)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
