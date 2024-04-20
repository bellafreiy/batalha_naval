#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

from constantes import *
import socket

HOST = "127.0.0.1"  # IP DO SERVER
PORTA = PORTA_SERVER  # MESMA PORTA DO SERVER

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # CRIANDO A CONEXÃO IPV4 E TCP

try:
    server.connect((HOST, PORTA))

except:

    print('A conexão não foi possível...')


def recebe_mensagem():
    """
    FUNÇÃO QUE FICA RODANDO 'PARA SEMPRE', RECEBENDO MENSAGENS DO SERVIDOR
    :return: sem retorno
    """

    while True:
        try:
            message = server.recv(4096).decode('UTF-8')
            teste = message[0]
            print(message)
            if teste[0] == "/":
                server.send(input(f'{CIANO}RESPONDA AQUI: {FIMCOR}').encode('UTF-8'))

        except ValueError as erro:
            # print(erro)
            print(f'\n\n{VERMELHO}~conexão encerrada devido a falha de contato~{FIMCOR}')
            exit()


recebe_mensagem()