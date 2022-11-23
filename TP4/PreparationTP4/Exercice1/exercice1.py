import re

var: str = input("Donnez une valeur a var : ")

if (re.search(r"World", var) is not None):
    print("var contient le mot World")
else:
    print("var ne contient pas le mot World")


if (re.search(r".", var) is not None):
    print("var contient au moins un caractere")
else:
    print("var ne contient pas de caracteres")


if (re.search(r"^.?$", var) is not None):
    print("var contient un ou zero caractere")
else:
    print("var contient plus d’ un caractere")


if (re.search(r"\d{3}", var) is not None):
    print("var contient trois chiffres de suite")
else:
    print("var ne contient pas trois chiffres de suite")


if (re.search(r"[a-zA-Z0-9]{3,12}", var) is not None):
    print("var contient entre 3 et 12 caracteres alphanumeriques de suite")
else:
    print("var ne contient pas entre 3 et 12 caracteres alphanumeriques de suite")


if (re.search(r"[TWHQ]ello", var) is not None):
    print("var contient un T, un W, un H ou un Q suivi de ello")
else:
    print("var ne contient pas un T, un W, un H ou un Q suivi de ello")


if (re.search(r"foo|bar|ello", var) is not None):
    print("var contient foo, bar ou ello")
else:
    print("var ne contient pas foo, bar ou ello")


if (re.search(r"^(Hello)", var) is not None):
    print("var commence par Hello")
else:
    print("var ne commence pas par Hello")


if (re.search(r"!!![0-9]{3}$", var) is not None):
    print("var se termine par !!! suivi de 3 chiffres")
else:
    print("var ne se termine pas par !!! suivi de 3 chiffres")


if (re.search(r"^H.*[0-9]{3}$", var) is not None):
    print("var commence par un H et se termine par 3 chiffres")
else:
    print("var ne commence pas par un H ou ne se termine pas par 3 chiffres")


if (re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", var) is not None):
    print("var est une adresse courriel valide")
else:
    print("var n’ est pas une adresse courriel valide")


if (re.search(r"(?=[^a-z]*[a-z])(?=[^\d]*\d{3})", var) is not None):
    print("var contient une lettre et 3 chiffres de suite (peu importe l'ordre)")
else:
    print("var ne contient pas de lettre ou 3 chiffres de suite")



verificateur: re.Pattern = re.compile(r"[0-9]{3}")

if (verificateur.search(var) is not None):
    print("var contient un nombre à au moins 3 chiffres")

if (verificateur.fullmatch(var) is not None):
    print("var représente exactement un nombre à 3 chiffres")