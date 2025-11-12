import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def verificacion(email_destino, token):
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    servidor = "smtp.gmail.com"
    puerto = 587

    link = f"http://localhost:9090/usuarios/verify/{token}"

    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = email_destino
    mensaje["Subject"] = "Verificá tu correo"

    cuerpo = f"Hacé click en este link para verificar tu cuenta:\n\n{link}"
    mensaje.attach(MIMEText(cuerpo, "plain"))

    try:
        with smtplib.SMTP(servidor, puerto) as server:
            server.starttls()
            server.login(remitente, password)
            server.send_message(mensaje)
        print(f"✅ Mail de verificación enviado a {email_destino}")
    except Exception as e:
        print(f"❌ Error enviando mail: {e}")
        raise