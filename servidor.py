#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

from constantes import *
import socket
from time import sleep

HOST = "127.0.0.1"  # ENDEREÇO IP DO MEU HOST = 127.0.0.1

PORTA = PORTA_SERVER # PORTA DE COMUNICAÇÃO / MELHOR SER ELEVADA

clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4 E TCP

server.bind((HOST, PORTA))  # COLOCANDO ESTE COMO HOST DO SERVIDOR

server.listen(2)

print('O SERVIDOR ESTÁ EM "LISTENING"....')


def len_de_clients():
    """
    FUNÇÃO QUE INFORMA A QUANTIDADE DE CLIENTES ATIVOS AGORA
    :return: CLIENTES ATIVOS
    """
    return len(clients)


def mensagem_global(message):
    """
    FUNÇÃO QUE MANDA MENSAGEM PARA OS DOIS JOGADORES
    :param message: É A MENSAGEM QUE DESEJAMOS MANDAR, DEVE ESTAR .encode('UTF-8')
    :return: SEM RETORNO
    """
    for client in clients:
        client.send(message)


def mensagem_unitaria(message, num_do_jogador=0):
    """
    FUNÇÃO QUE MANDA MENSAGEM PARA O JOGADOR UM JOGADOR SÓ
    :param message: É A MENSAGEM QUE DESEJAMOS MANDAR, DEVE ESTAR .encode('UTF-8')
    :param num_do_jogador: É O NÚMERO DO JOGADOR O QUAL QUERO MANDAR MENSAGEM - 0 OU 1
    :return: SEM RETORNO
    """
    sleep(0.2)
    clients[num_do_jogador].send(message)


def retorna_entradas_unitarias(num_jogador=0):
    """
    É A FUNÇÃO QUE RECEBE AS ENTRADAS DO JOGADOR 1 E NOS RETORNA A MESMA JÁ PRONTA PARA IMPRIMIR
    :param num_jogador: define se a mensagem eh para o jagador 1 (0) ou para o jogador 2 (1)
    :return: ENTRADA DO JOGADOR 1
    """
    entrada = clients[num_jogador].recv(4096).decode('UTF-8')
    print(entrada)

    return entrada


'''def fecha_conexao():
    """
    FUNÇÃO QUE FECHA O SOCKET
    :return: SEM RETORNO
    """
    for client in clients:
        client.close()
        clients.remove(client)'''


def conexao_inicial():
    """
    ESTA É A FUNÇÃO QUE CONECTARÁ OS NOSSOS CLIENTES
    :return: SEM RETORNO
    """

    try:
        client, address = server.accept()  # SEMPRE QUE UM CLIENTE SE CONECTA TEMOS O NOME DO CLIENTE E SEU ENDEREÇO
        print(f' O IP {address} ACABOU DE SE CONECTAR')
        clients.append(client)  # COLOCAMOS O ENDEREÇO NOVO NA LISTA CLIENTS
        if len(clients) == 1:
            mensagem_unitaria(f'\n\n{CIANO}VOCÊ É O JOGADOR 1{FIMCOR}'.encode('UTF-8'), 0)

        if len(clients) == 2:
            mensagem_unitaria(f'\n\n{CIANO}VOCÊ É O JOGADOR 2{FIMCOR}'.encode('UTF-8'), 1)

    except:
        print('\033[A CONEXÃO NÃO FOI POSSÍVEL')