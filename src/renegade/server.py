from mcstatus import JavaServer
import urllib.request
from datetime import datetime
from conf import get_config


def get_public_ip():
    """Gets the public ip of the host device by GETing ifconfig.me

    Returns:
        str: the public ip of the host
    """
    with urllib.request.urlopen("http://ifconfig.me") as response :
        return response.read().decode()


def get_server_info(address):    
    server = JavaServer.lookup(address)
    return server.status()

def get_message_text():
    uri = get_config().server_uri
    if uri == "default":
        address = f"{get_public_ip()}:{get_config().default_port}"
    elif ':' in uri:
        address = uri
    else:
        address = f"{uri}:{get_config().default_port}"
    
    try:
        status = get_server_info(address)
        now = datetime.now()

        message = f""">>> **Server Status:** `ONLINE`
**IP:** `{address}`
**Players:** `{status.players.online} / {status.players.max}`

**Last Updated:** `{now.strftime("%m/%d/%Y, %H:%M:%S")}`"""

    except:
        now = datetime.now()

        message = f""">>> **Server Status:** `OFFLINE`
**IP:** `{address}`
**Players:** `N/A`

**Last Updated:** `{now.strftime("%m/%d/%Y, %H:%M:%S")}`"""
    finally:
        return message


if __name__ == "__main__":
    print(get_message_text())