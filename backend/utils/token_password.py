from itsdangerous import URLSafeTimedSerializer
import os

RECOVERY_SECRET = os.getenv("RECOVERY_SECRET_KEY", "123456")

def generar_token_password(email):
    cifrado = URLSafeTimedSerializer(RECOVERY_SECRET)
    return cifrado.dumps(email)

def verificar_token_password(token, max_age=3600):
    descifrado = URLSafeTimedSerializer(RECOVERY_SECRET)
    return descifrado.loads(token, max_age=max_age)