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
    elements = message.split()
    if re.match(r"ADD \d+", message):
        if re.match(r"ADD USER \d+", message):
            return request.post("/utilizadores",json={"nome":elements[2],"username":elements[3],"password":elements[4]})
        elif re.match(r"ADD SERIE \d+", message):
            return request.post("/series",json={"nome_serie":elements[2],"data_inicio":elements[3],"synopse":elements[4],"id_serie":elements[5]})
        elif re.match(r"ADD EPISODIO \d+", message):
            return request.post('/episodios',json = {"nome_epis":elements[2],"descri":elements[3],"id_serie":elements[4]})
        elif re.match(r"ADD \d+", message):
            print "NOT YET DONE"
            #return {"id_user":elements[1],"id_serie":elements[2],"init_classific":elements[3]}
    elif re.match(r"REMOVE \d+", message):
        if re.match(r"REMOVE USER \d+", message):
            return request.delete('/utilizadores/'+ int(elements[2]))
        elif re.match(r"REMOVE SERIE \d+", message):
            return request.delete('/series/'+ int(elements[2]))
        elif re.match(r"REMOVE EPISODIO \d+", message):
            return request.delete('/episodios/'+ int(elements[2]))
        elif re.match(r"REMOVE ALL USERS \d+", message):
            return request.delete('/utilizadores')
        elif re.match(r"REMOVE ALL SERIE \d+", message):
            return request.delete('/series')
        elif re.match(r"REMOVE ALL EPISODIO \d+", message):
            return request.delete('/episodios')

    elif re.match(r"SHOW \d+", message):
        pass
    elif re.match(r"UPDATE \d+", message):
        pass
    return ret

if __name__ == "__main__":
    r = requests.post("http://localhost:5000/utilizadores")
