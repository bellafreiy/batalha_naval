from servidor import *


def testa_entrada_solta_bomba(num_do_jogador, tamanho_tabuleiro, letras_tabuleiro):
    """
    função que  validará se a coordenada onde o jogador deseja inserir a bomba é válida.
    :param num_do_jogador: id do jogador o qual enviaremos a mensagem
    :param tamanho_tabuleiro: tamanho do tabuleiro pré-definido pelos jogadores
    :param letras_tabuleiro: letras presentes no tabuleiro e pré-definidas pelos jogadores
    :return: linha da coordenada e coluna da coordenada
    """

    while True:
        mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_do_jogador)
        mensagem_unitaria(f'//DIGITE A COORDENADA ONDE DESEJA EXPLODIR SUA BOMBA.'
                          f'\nLEMBRE-SE: DIGITE UM {CIANO}NÚMERO{FIMCOR} E UMA {CIANO}LETRA{FIMCOR}'
                          f' EXISTENTES NO TABULEIRO. SEPARE-OS POR ESPAÇO.'.encode('UTF-8'), num_do_jogador)

        coord = str(retorna_entradas_unitarias(num_do_jogador)).upper()

        if len(coord) >= 2:

            try:
                linha_coord, coluna_coord = coord.split()

            except ValueError:
                continue

            if (linha_coord.isnumeric()) and (0 <= int(linha_coord) < tamanho_tabuleiro) \
                    and (coluna_coord in letras_tabuleiro):

                linha_coord = int(linha_coord)
                coluna_coord = int(letras_tabuleiro.index(coluna_coord))

                return linha_coord, coluna_coord


def testa_entrada_tamanho_tabuleiro():
    """
    FUNÇÃO QUE TESTARÁ A ENTRADA DO TAMANHO DO TABULEIRO. O QUAL DEVE SER UM NÚMERO ENTRE 5 E 16, INCLUSOS.
    :return: TAMANHO DO TABULEIRO
    """
    while True:
        mensagem_unitaria('\n\n'.encode('UTF-8'), 0)
        mensagem_unitaria(f'//DIGITE APENAS UM NÚMERO ENTRE 5 E 16.'.encode('UTF-8'), 0)
        resp_j1 = retorna_entradas_unitarias(0)

        if resp_j1.isnumeric():
            resp_j1 = int(resp_j1)

            if 5 <= resp_j1 <= 16:
                return resp_j1


def testa_vertical_horizontal(num_do_jogador, embarcacao):
    """
    função que perguntará ao jogador em que orientação deseja inserir a peça.
    :param num_do_jogador: numero do jogador o qual desejamos enviar mensagem
    :param embarcacao: nome da embarcação a qual se deve escolher a orientação.
    :return: sem retorno
    """

    while True:
        mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_do_jogador)
        mensagem_unitaria(f'//DESEJA INSERIR A PEÇA {embarcacao} NA HORIZONTAL OU VERTICAL?\n'
                          f'1 - HORIZONTAL\n2 - VERTICAL'.encode('UTF-8'), num_do_jogador)

        resposta = retorna_entradas_unitarias(num_do_jogador)

        if str(resposta).isnumeric():

            if int(resposta) == 1:
                return 'HORIZONTAL'

            elif int(resposta) == 2:
                return 'VERTICAL'


def testa_entrada_coord_barco(num_do_jogador, tamanho_tabuleiro, letras_tabuleiro, embarcacao):
    """
    função que testará se a coordenada do barco inserida pelo jogador é válida.
    :param num_do_jogador: numero do jogador para o qual enviaremos mensagem
    :param tamanho_tabuleiro: tamanho do tabuleiro pré-definida pelo jogador.
    :param letras_tabuleiro: letras do cabecalho do tabuleiro,
    :param embarcacao: nome da embarcação a ser alocada.
    :return: linha e coluna da coordenada
    """

    while True:
        mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_do_jogador)
        mensagem_unitaria(f'//DIGITE A COORDENADA INICIAL DE ONDE DESEJA INSERIR O/A {embarcacao}.'
                          f'\nLEMBRE-SE: DIGITE UM {CIANO}NÚMERO{FIMCOR} E UMA {CIANO}LETRA{FIMCOR}'
                          f' EXISTENTES NO TABULEIRO. SEPARE-OS POR ESPAÇO.'.encode('UTF-8'), num_do_jogador)

        coord = str(retorna_entradas_unitarias(num_do_jogador)).upper()

        if len(coord) >= 2:

            try:
                linha_coord, coluna_coord = coord.split()

            except ValueError:
                continue

            if (linha_coord.isnumeric()) and (0 <= int(linha_coord) < tamanho_tabuleiro) \
                    and (coluna_coord in letras_tabuleiro):

                linha_coord = int(linha_coord)
                coluna_coord = int(letras_tabuleiro.index(coluna_coord))

                return linha_coord, coluna_coord


def testa_entrada_preenchimento_random(num_do_jogador):
    mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_do_jogador)
    mensagem_unitaria(f'//DESEJA QUE O COMPUTADOR PREENCHA SEU MAPA POR VOCÊ?\n'
                      f'1 - SIM\n'
                      f'2 - NÃO'.encode('UTF-8'), num_do_jogador)

    resposta = str(retorna_entradas_unitarias(num_do_jogador))

    if resposta.isnumeric():

        if int(resposta) == 1:
            return True

        elif int(resposta) == 2:
            return False


def printa_tabuleiro(tabuleiro, tamanho, letras, num_do_jogador=100):
    """
    FUNÇÃO QUE PRINTARÁ ***PARA OS DOIS JOGADORES*** O TABULEIRO JÁ EXISTENTE QUANDO FOR CHAMADA.
    :param tabuleiro: TABULEIRO EXISTENTE AO QUAL QUERO PRINTAR
    :param tamanho: TAMANHO DEFINIDO PELO USUÁRIO AO UNÍCIO DO JOGO
    :param letras: SÃO AS LETRAS A SEREM PRINTADAS NO TABULEIRO
    :param num_do_jogador: numero do jogador para o qual enviaremos mensagem, se não mandar o número,
    a função printará globalmente.
    :return: SEM RETORNO.
    """

    string_final = ''

    mensagem_global('\n'.encode('UTF-8'))

    letras_printar = '    ' + ' '.join(letras)

    string_final += f'{letras_printar}\n'

    for a in range(0, tamanho):
        string_final += f'{a: ^3} '
        for b in range(0, tamanho):
            if b != tamanho - 1:
                string_final += f'{tabuleiro[a][b]} '

            else:
                string_final += f'{tabuleiro[a][b]}\n'

    if num_do_jogador == 100:
        mensagem_global(string_final.encode('UTF-8'))

    else:
        mensagem_unitaria(string_final.encode('UTF-8'), num_do_jogador)