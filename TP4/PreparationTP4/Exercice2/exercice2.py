import email.message
import smtplib
import socket


source: str = input("Mail from: ")
destination: str = input("Mail to: ")
sujet: str = input("Subject: ")
print("Body: (enter '.' on a single line to finish typing)")
corps = ""
buffer = ""
while(buffer != ".\n"):
    corps += buffer
    buffer = input() + '\n'
    message = email.message.EmailMessage()
    message["From"] = source
    message["To"] = destination
    message["Subject"] = sujet
    message.set_content(corps)
    
try:
    with smtplib.SMTP(host="smtp.ulaval.ca", timeout=10) as connexion:
        connexion.send_message(message)
        print("Message envoyé avec succès.")
except smtplib.SMTPException:
    print("Le message n'a pas pu être envoyé.")
except socket.timeout:
    print("La connexion au serveur SMTP n'a pas pu être établie.")