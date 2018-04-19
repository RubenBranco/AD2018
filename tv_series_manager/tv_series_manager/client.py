import requests
import re


def request():
    cmd = raw_input("Comando? ")
    if cmd:
        request = message_parser(cmd)


def message_parser(message):
    """
    Verifica a mensagem recebida e interpreta-a
    """
    # TODO fazer as transformacoes para json e passar como dados para enviar ao servidor
    ret = "UNKNOWN COMMAND"

    if re.match(r"ADD \d+", message):
        pass
    elif re.match(r"REMOVE \d+", message):
        pass
    elif re.match(r"SHOW \d+", message):
        pass
    elif re.match(r"UPDATE \d+", message):
        pass
    return ret

if __name__ == "__main__":
    pass