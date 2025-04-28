import socket


is_online = False


def init_is_online(timeout: float = 1):
    global is_online
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        is_online = True
    except (socket.timeout, OSError):
        is_online = False
