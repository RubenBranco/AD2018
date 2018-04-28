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
        if re.match(r"ADD USER \.+", message):
            return request.post("/utilizadores",data={"name":elements[2],"username":elements[3],"password":elements[4]})
        elif re.match(r"ADD SERIE \.+", message):
            return request.post("/series",data={"name":elements[2],"start_date":elements[3],"synopse":elements[4],"category":elements[5]})
        elif re.match(r"ADD EPISODIO \.+", message):
            return request.post('/episodios',data = {"name":elements[2],"description":elements[3],"serie_id":elements[4]})
        elif re.match(r"ADD \.+", message):
            return request.post('/serie/'+ int(elements[2]),data={"user_id":elements[1], "classification":elements[3]})
    elif re.match(r"REMOVE \.+", message):
        if re.match(r"REMOVE USER \.+", message):
            return request.delete('/utilizadores/'+ int(elements[2]))
        elif re.match(r"REMOVE SERIE \.+", message):
            return request.delete('/series/'+ int(elements[2]))
        elif re.match(r"REMOVE EPISODIO \.+", message):
            return request.delete('/episodios/'+ int(elements[2]))
        elif re.match(r"REMOVE ALL USERS \.+", message):
            return request.delete('/utilizadores')
        elif re.match(r"REMOVE ALL SERIE \.+", message):
            return request.delete('/series')
        elif re.match(r"REMOVE ALL EPISODIO \.+", message):
            return request.delete('/episodios')
        elif re.match(r"SHOW ALL SERIE_U \.+", message):
            return request.get('/series', data={"op":elements[2]})
        elif re.match(r"SHOW ALL SERIE_C \.+", message):
            return request.get('/series', data={"op":elements[2]})
        elif re.match(r"REMOVE ALL EPISODIO \.+", message):
            return request.delete('/series/'+ int(elements[3]))
    elif re.match(r"SHOW \d+", message):
        if re.match(r"SHOW USER \.+", message):
            return request.get('/utilizadores/'+ int(elements[2]))
        elif re.match(r"SHOW SERIE \.+", message):
            return request.get('/series/'+ int(elements[2]))
        elif re.match(r"SHOW EPISODIO \.+", message):
            return request.get('/episodios/'+ int(elements[2]))
        elif re.match(r"SHOW ALL USERS \.+", message):
            return request.get('/utilizadores')
        elif re.match(r"SHOW ALL SERIE \.+", message):
            return request.get('/series')
        elif re.match(r"SHOW ALL EPISODIO \.+", message):
            return request.get('/episodios')
        elif re.match(r"SHOW ALL SERIE_U \.+", message):
            return request.get('/series', data={"op":elements[2]})
        elif re.match(r"SHOW ALL SERIE_C \.+", message):
            return request.get('/series', data={"op":elements[2]})
        elif re.match(r"SHOW ALL EPISODIO \.+", message):
            return request.get('/series/'+ int(elements[3]))
    elif re.match(r"UPDATE \.+", message):
        elif re.match(r"UPDATE SERIE \.+", message):
            return request.patch('/series/'+ int(elements[3]),data={"serie_id":elements[2],"class":elements[4]})
        elif re.match(r"UPDATE USER \.+", message):
            return request.patch('/series/'+ int(elements[2]),data={"password":elements[3]})
    return ret

if __name__ == "__main__":
    r = requests.post("http://localhost:5000/utilizadores")
