from flask import request, g, current_app
import requests


def get_current_user(request):
    token = request.cookies.get("token")
    if not token:
        return None

    try:
        resp = requests.get(
            "http://localhost:9090/usuarios/me",
            cookies={"token": token},
            timeout=5
        )

        if resp.status_code == 200:
            return resp.json() 
    except:
        pass

    return None