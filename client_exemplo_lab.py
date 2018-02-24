import socket as s
import argparse
import sock_utils


def client(host, port):
    cont = True
    while cont:
        sock = sock_utils.create_tcp_client_socket(host, port)
        send_msg = raw_input("Qual a mensagem")
        if send_msg == "EXIT":
            cont = False
        else:
            sock.sendall(send_msg)
        resposta = sock_utils.receive_all(sock, 5000)
        print 'Recebi {}'.format(resposta)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente")
    parser.add_argument("port", type=int, help="Port the client will use for connection")
    parser.add_argument("host", type=str, help="host it will use")
    args = parser.parse_args()
    client(args.host, args.port)
