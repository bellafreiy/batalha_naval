#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

from constantes import *
from servidor import *
from threading import Thread
from maneja_tabuleiros import *
from testando_entradas import *

tabuleiro_principal_j1 = list()
tabuleiro_principal_j2 = list()
jogadas_j1 = list()
jogadas_j2 = list()
bombas_jogadas_j1 = list()
bombas_jogadas_j2 = list()


def inicio_contato_jogadores():
    """
    FUNÇÃO INICIAL DO PROGRAMA, FAZ A CONEXÃO DOS DOIS JOGADORES E JÁ MANDA PARA A FUNÇÃO DE INTERFACE EM SI.
    :return:
    """
    conexao_inicial()

    if len_de_clients() == 2:

        controla_informacoes_jogadores()


def controla_informacoes_jogadores():

    sleep(1)
    mensagem_global(f'\n~~~~~~~~~~~~~~~~~~~~~~~~~~ BEM-VINDO À BATALHA NAVAL ~~~~~~~~~~~~~~~~~~~~~~~~~~'.encode('UTF-8'))

    mensagem_global(f'\n\nPREPAREM-SE PARA O GAME E ATENTEM-SE ÀS REGRAS :)'.encode('UTF-8'))

    mensagem_global(f'\n\n1. O JOGADOR 1 TERÁ O PODER DE DECIDIR O TAMANHO DOS TABULEIROS DO JOGO QUE SERÃO '
                  f'QUADRADOS. PODENDO SER DE 5x5 ATÉ 10x10'.encode('UTF-8'))

    mensagem_global(f'\n\n2.  CADA JOGADOR TERÁ O SEU TABULEIRO ONDE PODERÁ ORGANIZAR SUAS EMBARCAÇÕES. '
                  f'O GAME INFORMARÁ QUAIS EMBARCAÇÕES ESTARÃO DISPONÍVEIS PARA CADA TAMANHO DE'
                  f' TABULEIRO'.encode('UTF-8'))

    mensagem_global(f'\n\n3.   EM UM PRIMEIRO MOMENTO, OS JOGADORES PODERÃO ORGANIZAR SUAS EMBARCAÇÕES NO'
                    f' MAPA. O PRIMEIRO JOGADOR PODERÁ DEFINIR AS COORDENADAS DE SUAS EMBARCAÇÕES, E, APÓS'
                    f' O SEU OK, O SEGUNDO JOGADOR TERÁ A POSSIBILIDADE DE DEFINIR AS SUAS COORDENADAS.'.encode('UTF-8'))

    mensagem_global(f'\n\n4.   APÓS DEFINIDAS AS COORDENADAS, O JOGO COMEÇA COM O JOGADOR 1 ATACANDO A '
                    f'COORDENADA DE SUA ESCOLHA NO TABULEIRO DO JOGADOR 2. E ASSIM POR DIANTE.'.encode('UTF-8'))

    mensagem_global(f'\n\n5. CASO O JOGADOR ACERTE UMA EMBARCAÇÃO, PODERÁ JOGAR NOVAMENTE. CASO NÃO, '
                    f'A VEZ DE JOGO SERÁ PASSADA PARA O PRÓXIMO JOGADOR.'.encode('UTF-8'))

    mensagem_global(f'\n\n6. VENCE QUEM BOMBARDEAR TODAS AS EMBARCAÇÕES DO OPONENTE PRIMEIRO!'.encode('UTF-8'))

    mensagem_global(f'\n\n--------------------------------------------------------------------------------'
                    .encode('UTF-8'))

    mensagem_global(f'\n\n                         CÓDIGO DE CORES E SÍMBOLOS'.encode('UTF-8'))

    mensagem_global(f'\n\n1. NO MOMENTO DO BOMBARDEIO, AS BOMBAS QUE VOCÊ JOGAR SERÃO UM "x" NO'
                    f' SEU TABULEIRO'.encode('UTF-8'))

    mensagem_global(f'\n{VERDE}        1.1. CASO VOCÊ ACERTE UMA EMBARCAÇÃO O SEU "X" FICARÁ VERDE.'
                    f'{FIMCOR}'.encode('UTF-8'))

    mensagem_global(f'\n{VERMELHO}        1.2. CASO VOCÊ ERRE, O SEU "X" FICARÁ VERMELHO.{FIMCOR}'.encode('UTF-8'))

    mensagem_global(f'\n\n2. AINDA DURANTE O BOMBARDEIO, AS JOGADAS DO OUTRO JOGADOR TAMBÉM SERÃO MOSTRADAS'
                    f' EM SEU TABULEIRO, MAS COMO UM "o"'.encode('UTF-8'))

    mensagem_global(f'\n{CINZA}        2.1. CASO A JOGADA TENHA SIDO EM UMA CASA VAZIA, TERÁ UM "o" BRANCO. {FIMCOR}'
                    f''.encode('UTF-8'))

    mensagem_global(f'\n{VERMELHO}        2.2. CASO A JOGADA TENHA SIDO EM UMA CASA OCUPADA, TERÁ UM "o"'
                    f' VERMELHO{FIMCOR}'.encode('UTF-8'))

    mensagem_global(f'\n\n--------------------------------------------------------------------------------'
                    f''.encode('UTF-8'))

    mensagem_global(f'\n\nAGORA O JOGADOR 1 DEVERÁ DEFINIR O TAMANHO DOS TABULEIROS DA PARTIDA.'.encode('UTF-8'))

    tamanho_tabuleiro = testa_entrada_tamanho_tabuleiro()

    letras_tabuleiro = define_letras_tabuleiro(tamanho_tabuleiro)

    if tamanho_tabuleiro == 5:
        embarcacoes = ['SUBMARINO', 'CRUZADOR']

    elif tamanho_tabuleiro == 6:
        embarcacoes = ['SUBMARINO', 'SUBMARINO', 'CRUZADOR']

    elif tamanho_tabuleiro == 7:
        embarcacoes = ['SUBMARINO', 'SUBMARINO', 'CRUZADOR', 'CRUZADOR']

    elif tamanho_tabuleiro == 8:
        embarcacoes = ['SUBMARINO', 'SUBMARINO', 'HIDROAVIAO', 'CRUZADOR']

    elif tamanho_tabuleiro == 9:
        embarcacoes = ['SUBMARINO', 'HIDROAVIAO', 'PORTA-AVIOES', 'ENCOURACADO']

    elif 10 <= tamanho_tabuleiro <= 12:
        embarcacoes = ['SUBMARINO', 'HIDROAVIAO', 'HIDROAVIAO', 'CRUZADOR', 'CRUZADOR', 'ENCOURACADO']

    elif 13 <= tamanho_tabuleiro <= 15:
        embarcacoes = ['SUBMARINO', 'SUBMARINO', 'HIDROAVIAO', 'HIDROAVIAO', 'CRUZADOR', 'CRUZADOR', 'PORTA-AVIOES',
                       'ENCOURACADO']

    elif 16 == tamanho_tabuleiro:
        embarcacoes = ['PORTA-AVIOES', 'SUBMARINO', 'SUBMARINO', 'HIDROAVIAO', 'HIDROAVIAO', 'PORTA-AVIOES',
                       'CRUZADOR', 'CRUZADOR', 'ENCOURACADO', 'ENCOURACADO']

    print(embarcacoes)

    cria_tabuleiro(tabuleiro_principal_j1, tamanho_tabuleiro)

    cria_tabuleiro(jogadas_j1, tamanho_tabuleiro)
    preenche_espacos_til(jogadas_j1, tamanho_tabuleiro)

    cria_tabuleiro(tabuleiro_principal_j2, tamanho_tabuleiro)

    cria_tabuleiro(jogadas_j2, tamanho_tabuleiro)
    preenche_espacos_til(jogadas_j2, tamanho_tabuleiro)

    mensagem_global(f'\n\nO TABULEIRO ESCOLHIDO FOI O {tamanho_tabuleiro} x {tamanho_tabuleiro}:'.encode('UTF-8'))

    printa_tabuleiro(tabuleiro_principal_j1, tamanho_tabuleiro, letras_tabuleiro)


    mensagem_global(f'\n\n'.encode('UTF-8'))
    mensagem_global(f'AGORA O JOGADOR 1 IRÁ DIFINIR AS SUAS COORDENADAS. LEMBRE-SE: SUAS EMBARCAÇÕES'
                    f' NÃO PODEM ENCOSTAR UMA NA OUTRA. ALÉM DISSO, SUA EMBARCAÇÃO NÃO PODE SER INSERIDA'
                    f' EM COORDENADA QUE A DIVIDA.'.encode('UTF-8'))

    # perguntando ao jogador 1 se ele deseja o preenchimento suas peças randomicamente
    preenchimento_random_j1 = testa_entrada_preenchimento_random(ENDERECO_J1)

    if preenchimento_random_j1 is False:

        # JOGADOR 1 PODE INSERIR EMBARCACOES NO TABULEIRO DO J1, VAMOS E OBTER COORD DOS BARCOS
        coord_embarcacoes_j1 = insere_embarcacao_no_tabuleiro(
            embarcacoes, tamanho_tabuleiro, letras_tabuleiro, tabuleiro_principal_j1, ENDERECO_J1)

        # printando o tabuleiro
        mensagem_unitaria(f'\n\nSEU TABULEIRO FINAL É:'.encode('UTF-8'), 1)
        printa_tabuleiro(tabuleiro_principal_j2, tamanho_tabuleiro, letras_tabuleiro, ENDERECO_J1)

    else:
        # computador preenche o tabuleiro por completo
        coord_embarcacoes_j1 = preenchendo_randomicamente(embarcacoes, tamanho_tabuleiro, tabuleiro_principal_j1,
                                                          ENDERECO_J1)

        # printa o tabuleiro
        mensagem_unitaria(f'\n\nSEU TABULEIRO FINAL É:'.encode('UTF-8'), ENDERECO_J1)
        printa_tabuleiro(tabuleiro_principal_j1, tamanho_tabuleiro, letras_tabuleiro, ENDERECO_J1)

    mensagem_global('\n\n'.encode('UTF-8'))
    mensagem_global(f'AGORA O JOGADOR 2 IRÁ DIFINIR AS SUAS COORDENADAS. LEMBRE-SE: SUAS EMBARCAÇÕES'
                    f' NÃO PODEM ENCOSTAR UMA NA OUTRA. ALÉM DISSO, SUA EMBARCAÇÃO NÃO PODE SER INSERIDA'
                    f' EM COORDENADA QUE A DIVIDA.'.encode('UTF-8'))

    # perguntando ao jogador 2 se ele deseja o preenchimento suas peças randomicamente
    preenchimento_random_j2 = testa_entrada_preenchimento_random(ENDERECO_J2)

    if preenchimento_random_j2 is False:

        # JOGADOR 2 PODE INSERIR EMBARCACOES NO TABULEIRO DO J1, VAMOS E OBTER COORD DOS BARCOS
        coord_embarcacoes_j2 = insere_embarcacao_no_tabuleiro(
            embarcacoes, tamanho_tabuleiro, letras_tabuleiro, tabuleiro_principal_j2, ENDERECO_J2)

        # printando o tabuleiro
        mensagem_unitaria(f'\n\nSEU TABULEIRO FINAL É:'.encode('UTF-8'), ENDERECO_J2)
        printa_tabuleiro(tabuleiro_principal_j2, tamanho_tabuleiro, letras_tabuleiro, ENDERECO_J2)

    else:
        # computador preenche o tabuleiro por completo
        coord_embarcacoes_j2 = preenchendo_randomicamente(embarcacoes, tamanho_tabuleiro, tabuleiro_principal_j2,
                                                          ENDERECO_J2)

        # printando o tabuleiro
        mensagem_unitaria(f'\n\nSEU TABULEIRO FINAL É:'.encode('UTF-8'), ENDERECO_J2)
        printa_tabuleiro(tabuleiro_principal_j2, tamanho_tabuleiro, letras_tabuleiro, ENDERECO_J2)

    mensagem_global('\n\n! AGORA É A HORA DO BOMBARDEIO !'.encode('UTF-8'))
    mensagem_global('\n\nESTE É O MOMENTO DE ESCOLHER QUAL COORDENADA EXISTENTE NO TABULEIRO VOCÊ QUER BOMBARDEAR.'
                    '\nAS RODADAS INICIAM-SE COM O JOGADOR 1.'.encode('UTF-8'))

    vez_jogador_1 = True
    vez_jogador_2 = False
    mais_uma_vez = True

    while True:

        # entra aqui se for vez do j1
        if vez_jogador_1 is True:
            mais_uma_vez, vez_jogador_1, vez_jogador_2 = soltando_bombas\
                    (letras_tabuleiro, tamanho_tabuleiro, jogadas_j1, jogadas_j2, coord_embarcacoes_j2,
                     ENDERECO_J1, bombas_jogadas_j1)

            if mais_uma_vez is True:
                printa_tabuleiro(jogadas_j1, tamanho_tabuleiro, letras_tabuleiro, ENDERECO_J1)
                printa_tabuleiro(jogadas_j2, tamanho_tabuleiro, letras_tabuleiro, ENDERECO_J2)

        # entra aqui se for vez do j2
        elif vez_jogador_2 is True:
            mais_uma_vez, vez_jogador_2, vez_jogador_1 = soltando_bombas\
                (letras_tabuleiro, tamanho_tabuleiro, jogadas_j2, jogadas_j1, coord_embarcacoes_j1,
                 ENDERECO_J2, bombas_jogadas_j2)

            if mais_uma_vez is True:
                printa_tabuleiro(jogadas_j2, tamanho_tabuleiro, letras_tabuleiro, ENDERECO_J2)
                printa_tabuleiro(jogadas_j1, tamanho_tabuleiro, letras_tabuleiro, ENDERECO_J1)

        # entra aqui quando um dos jogadores acertar todas as embarcações
        if mais_uma_vez is False:
            break


inicio_contato_jogadores()


thread_inicio_contato_jogadores = Thread(target=inicio_contato_jogadores(), args=())
thread_retorna_entradas_unitarias_J1 = Thread(target=retorna_entradas_unitarias(ENDERECO_J1), args=())
thread_retorna_entradas_unitarias_J2 = Thread(target=retorna_entradas_unitarias(ENDERECO_J2), args=())

thread_inicio_contato_jogadores.start()
thread_retorna_entradas_unitarias_J1.start()
thread_retorna_entradas_unitarias_J2.start()
