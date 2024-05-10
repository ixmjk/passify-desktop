import platform
import re

import requests
from PyQt5.QtCore import QSettings

settings = QSettings("Passify", "Passify")


def is_valid_email(email_address):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email_address):
        return True
    return False


def get_error_message(response):
    print(response)
    print(response.text)
    try:
        error_messages = []
        for v in response.json().values():
            if isinstance(v, str):
                error_messages.append(v)
            else:
                for vv in v:
                    error_messages.append(vv)
        return "\n".join(error_messages)
    except Exception as e:
        print(e)
        return response.text


def auth_put_request(endpoint, data: dict):
    response = requests.put(
        endpoint,
        json=data,
        headers={
            "Authorization": f"JWT {settings.value('ACCESS_TOKEN')}",
        },
    )
    return response


def auth_patch_request(endpoint, data: dict):
    response = requests.patch(
        endpoint,
        json=data,
        headers={
            "Authorization": f"JWT {settings.value('ACCESS_TOKEN')}",
        },
    )
    return response


def auth_post_request(endpoint, data: dict):
    response = requests.post(
        endpoint,
        json=data,
        headers={
            "Authorization": f"JWT {settings.value('ACCESS_TOKEN')}",
        },
    )
    return response


def auth_get_request(endpoint):
    response = requests.get(
        endpoint,
        headers={
            "Authorization": f"JWT {settings.value('ACCESS_TOKEN')}",
        },
    )
    return response


def auth_delete_request(endpoint, data: dict):
    response = requests.delete(
        endpoint,
        json=data,
        headers={
            "Authorization": f"JWT {settings.value('ACCESS_TOKEN')}",
        },
    )
    return response


def post_request(endpoint, data: dict):
    os_details = f"{platform.system()} {platform.release()}"
    user_agent = f"{settings.value('PROJECT_NAME')} Desktop/1.0 ({os_details})"
    # user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Passify-Desktop/125.0"

    headers = {
        "User-Agent": user_agent,
    }

    response = requests.post(
        endpoint,
        json=data,
        headers=headers,
    )
    return response
