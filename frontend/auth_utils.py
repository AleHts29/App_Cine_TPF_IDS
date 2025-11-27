from flask import request, g, current_app
import requests
from dotenv import load_dotenv
import os

load_dotenv()


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:9090")
def get_current_user(request):
    token = request.cookies.get("token")
    if not token:
        return None

    try:
        resp = requests.get(
            f"{BACKEND_URL}/usuarios/me",
            cookies={"token": token},
            timeout=5
        )

        if resp.status_code == 200:
            return resp.json() 
    except:
        pass

    return None