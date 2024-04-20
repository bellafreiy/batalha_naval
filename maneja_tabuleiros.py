from servidor import *
from testando_entradas import *
from random import choice
from time import sleep


def soltando_bombas(letras_tabuleiro, tamanho_tabuleiro, tabuleiro_de_jogadas_jog_atual,
                    tabuleiro_de_jogadas_jog_seguinte, lista_coord_embarcacoes, num_jogador_atual,
                    bombas_jogadas_jogador_atual):
    """
    função que checará se as coordenadas onde as bombas foram soltas alcançam alguma embarcação.
    :param letras_tabuleiro: as letras do tabuleiro. Serão usadas para impressão do tabuleiro na tela.
    :param tamanho_tabuleiro: tamanho do tabuleiro pré-definida pelo jogador 1.
    :param tabuleiro_de_jogadas_jog_atual: é o tabuleiro que mostrará cada bomba jogada pelo jogador.
    :param lista_coord_embarcacoes: lista que guarda todas as coordenadas onde existem embarcações.
    :param num_jogador_atual: id do jogador para quem vamos enviar a mensagem
    :param bombas_jogadas_jogador_atual: lista com as coordenadas já jogadas
    :return: Se é a vez do jogador atual e se é a vez do próximo jogador.
    """

    mais_uma_vez = True

    linha_coord, coluna_coord = testa_entrada_solta_bomba(num_jogador_atual, tamanho_tabuleiro, letras_tabuleiro)

    if [linha_coord, coluna_coord] not in bombas_jogadas_jogador_atual:

        bombas_jogadas_jogador_atual.append([linha_coord, coluna_coord])

        for coord in lista_coord_embarcacoes:
            # entra aqui se a entrada do jogador for igual a alguma das combinações em lista_coord_embarcacoes
            if coord[0] == linha_coord and coord[1] == coluna_coord:

                # acrescentando a jogada correta no tabuleiro de jogadas do jogador atual
                tabuleiro_de_jogadas_jog_atual[linha_coord][coluna_coord] = f'{VERDE}' + 'x' + f'{FIMCOR}'

                # acrescentando a explosão no tabuleiro de jogadas do jogador seguinte
                tabuleiro_de_jogadas_jog_seguinte[linha_coord][coluna_coord] = f'{VERMELHO}' + 'o' + f'{FIMCOR}'

                # remove a combinacao
                lista_coord_embarcacoes.remove([linha_coord, coluna_coord])

                mensagem_global(f'\033[1;34m\n\nO JOGADOR {num_jogador_atual + 1} EXPLODIU EMBARCAÇÃO NA COORDENADA:'
                                f'\n{linha_coord:>17} x {letras_tabuleiro[coluna_coord]}\033[0;0m'.encode('UTF-8'))

                # se ainda existirem embarcacoes a serem explodidas
                if lista_coord_embarcacoes:
                    vez_jogador_atual = True
                    vez_jogador_seguinte = False

                    return mais_uma_vez, vez_jogador_atual, vez_jogador_seguinte

                # se a lista de embarcacoes a serem explodidas estiver limpa
                else:
                    mais_uma_vez = False
                    vez_jogador_atual = False
                    vez_jogador_seguinte = False

                    mensagem_global(f'\n\n\n        .                            .'.encode('UTF-8'))
                    sleep(0.2)
                    mensagem_global(f'        . .                        . .'.encode('UTF-8'))
                    sleep(0.2)
                    mensagem_global(f'        . . .                    . . .'.encode('UTF-8'))
                    sleep(0.2)
                    mensagem_global(f'\n{CIANO}           !!! VENCE O JOGADOR {num_jogador_atual + 1} '
                                    f'!!!{FIMCOR}'.encode('UTF-8'))
                    sleep(0.2)
                    mensagem_global(f'\n        . . .                    . . .'.encode('UTF-8'))
                    sleep(0.2)
                    mensagem_global(f'        . .                        . .'.encode('UTF-8'))
                    sleep(0.2)
                    mensagem_global(f'        .                            .'.encode('UTF-8'))

                    return mais_uma_vez, vez_jogador_atual, vez_jogador_seguinte

        # cai aqui se a bomba não explodiu nenhuma embarcacao
        vez_jogador_atual = False
        vez_jogador_seguinte = True

        # acrescentando a jogada errada no tabuleiro de jogadas do jogador atual
        tabuleiro_de_jogadas_jog_atual[linha_coord][coluna_coord] = f'{VERMELHO}' + f'x' + f'{FIMCOR}'

        # acrescentando a jogada errada no tabuleiro do jogador seguinte
        tabuleiro_de_jogadas_jog_seguinte[linha_coord][coluna_coord] = f'{CINZA}' + f'o' + f'{FIMCOR}'

        mensagem_global(f'{ROXO}\n\nO JOGADOR {num_jogador_atual + 1} BOMBARDEOU A COORD:'
                        f'\n{linha_coord} x {letras_tabuleiro[coluna_coord]}'
                        f'\nMAS NÃO ATINGIU EMBARCAÇÃO ALGUMA.{FIMCOR}'
                        f''.encode('UTF-8'))

        return mais_uma_vez, vez_jogador_atual, vez_jogador_seguinte

    # entra aqui se a coordenada já foi escolhida pelo jogador.
    else:
        mais_uma_vez = True
        vez_jogador_atual = True
        vez_jogador_seguinte = False

        mensagem_global(f'{VERMELHO}\n\nO JOGADOR {num_jogador_atual + 1} TENTOU BOMBARDEAR A COORD JÁ BOMBARDEADA:'
                        f'\n{linha_coord} x {letras_tabuleiro[coluna_coord]}'
                        f'\nJOGUE NOVAMENTE EM OUTRA COORDENADA.{FIMCOR}'.encode('UTF-8'))

        return mais_uma_vez, vez_jogador_atual, vez_jogador_seguinte


def preenche_espacos_til(tabuleiro, tamanho_tabuleiro):
    """
    preenche os espaços ainda em branco com 'til's.
    :param tabuleiro: tabuleiro a ser preenchido
    :param tamanho_tabuleiro: tamanho do tabuleiro
    :return: sem retorno
    """
    for a in range(0, tamanho_tabuleiro):
        for b in range(0, tamanho_tabuleiro):

            if tabuleiro[a][b] == '_':
                tabuleiro[a][b] = '~'


def preenche_coord_inucopavel_aprox(tabuleiro, lista_coord_inocupaveis_por_aprox):
    """
    função que preenche as coordenadas inocupáveis por aproximação a cada nova embarcação inserida.
    :param tabuleiro: tabuleiro a ter coordenada preenchida
    :param lista_coord_inocupaveis_por_aprox: lista com as coordenas inocupáveis por aprocimação.
    :return: sem retorno
    """
    for coord in lista_coord_inocupaveis_por_aprox:

        if tabuleiro[coord[0]][coord[1] != '~']:
            tabuleiro[coord[0]][coord[1]] = '~'


def aloca_randomicamente_vertical(embarcacao, tamanho_embarcacao, tamanho_tabuleiro,
                                  tabuleiro, lista_coord_inocupaveis, lista_coord_aprox):
    """
    função que alocará embarcação *randomicamente* na vertical
    :param embarcacao: embarcação a ser alocada
    :param tamanho_embarcacao: tamanho da embarcação a ser alocada
    :param tamanho_tabuleiro: tamanho do tabuleiro (definido pelo jogador)
    :param tabuleiro: tabuleiro a ser preenchido.
    :param lista_coord_inocupaveis: coordenadas que contem embarcações alocadas
    :param lista_coord_aprox: coordenadas inocupáveis por estarem próximas às embarcações
    :return: sem retorno
    """
    while True:
        a_coord_eh_inocupavel = False

        # lista que armazenará linhas e colunas disponíveis
        lista_numeros = list()

        # preenchendo a lista com as linhas e colunas disponíveis
        for a in range(0, tamanho_tabuleiro):
            lista_numeros.append(a)

        linha_coord = choice(lista_numeros)
        coluna_coord = choice(lista_numeros)

        # FOR QUE CHECA SE LINHA E COLUNA JÁ ESTÃO EM LISTA_COORD_INOCUPAVEIS
        for a in lista_coord_inocupaveis:
            if (a[0] == linha_coord) and (a[1] == coluna_coord):
                a_coord_eh_inocupavel = True
                break

        if a_coord_eh_inocupavel:
            continue

        # FOR QUE CHECA SE A COORDENADA ESCOLHIDA EH INOCUPAVEL POR APROXIMACAO
        for a in lista_coord_aprox:
            if (a[0] == linha_coord) and (a[1] == coluna_coord):
                a_coord_eh_inocupavel = True

                break

        if a_coord_eh_inocupavel:
            continue

        # if que entramos se for submarino, acrescenta no tabuleiro e depois
        if tamanho_embarcacao == 1:
            tabuleiro[linha_coord][coluna_coord] = 'x'
            # roda a lista procurando os x, acrescentando as novas coord inocupaveis na lista
            for a in range(0, tamanho_tabuleiro):
                for b in range(0, tamanho_tabuleiro):
                    if tabuleiro[a][b] == 'x':
                        if [a, b] not in lista_coord_inocupaveis:
                            lista_coord_inocupaveis.append([a, b])

            return

        # entra aqui quando a embarcacao for maior que submarino
        else:
            if embarcacao != 'HIDROAVIAO':

                # if que checa se a embarcacao cabe no tabuleiro a partir da linha inicial
                if linha_coord + tamanho_embarcacao <= tamanho_tabuleiro:

                    # for que roda as linhas abaixo verificando se sao inocupaveis
                    for linhas_check in range(linha_coord, linha_coord + tamanho_embarcacao):
                        if tabuleiro[linhas_check][coluna_coord] == 'x':
                            a_coord_eh_inocupavel = True

                            break

                    if a_coord_eh_inocupavel:
                        continue

                    # FOR QUE CHECA SE AS LINHAS SEGUINTES SAO INOCUPAVEIS POS APROXIMACAO
                    for linha in range(linha_coord, linha_coord + tamanho_embarcacao):
                        if [linha, coluna_coord] in lista_coord_aprox:
                            a_coord_eh_inocupavel = True

                            break

                    if a_coord_eh_inocupavel:
                        continue

                    # coloca o x nas colunas a frente
                    for linhas_check in range(linha_coord, linha_coord + tamanho_embarcacao):
                        tabuleiro[linhas_check][coluna_coord] = 'x'

                    # roda o tabuleiro procurando os novos inocupaveis para lista
                    for a in range(0, tamanho_tabuleiro):
                        for b in range(0, tamanho_tabuleiro):
                            if tabuleiro[a][b] == 'x':
                                if [a, b] not in lista_coord_inocupaveis:
                                    lista_coord_inocupaveis.append([a, b])

                    return

                # entra aqui se o barco nao cabe no tabuleiro
                else:

                    continue

            elif embarcacao == 'HIDROAVIAO':
                # checando se cabe no tabuleiro a partir da coluna e linha inicial
                if (linha_coord + 1 < tamanho_tabuleiro) and (coluna_coord + 1 < tamanho_tabuleiro) and \
                        (linha_coord - 1 >= 0):

                    # verificando se as casas do hidroaviao estao livres em inocupaveis:
                    if [linha_coord - 1, coluna_coord + 1] in lista_coord_inocupaveis or \
                            [linha_coord + 1, coluna_coord + 1] in lista_coord_inocupaveis:
                        continue

                    # verificando se as casas do hidroaviao estao livres em inocupaveis por aprox
                    if [linha_coord - 1, coluna_coord + 1] in lista_coord_aprox or \
                            [linha_coord + 1, coluna_coord + 1] in lista_coord_aprox:
                        continue

                    # adicionando as casas no tabuleiro:
                    tabuleiro[linha_coord][coluna_coord] = 'x'
                    tabuleiro[linha_coord - 1][coluna_coord + 1] = 'x'
                    tabuleiro[linha_coord + 1][coluna_coord + 1] = 'x'

                    # roda o tabuleiro procurando os novos inocupaveis para lista
                    for a in range(0, tamanho_tabuleiro):
                        for b in range(0, tamanho_tabuleiro):
                            if tabuleiro[a][b] == 'x':
                                if [a, b] not in lista_coord_inocupaveis:
                                    lista_coord_inocupaveis.append([a, b])

                    return

                # entra aqui se o hidroaviao nao cabe no tabuleiro
                else:

                    continue


def aloca_randomicamente_horizontal(embarcacao, tamanho_embarcacao, tamanho_tabuleiro,
                                    tabuleiro, lista_coord_inocupaveis, lista_coord_aprox):
    """
    função que alocará embarcação *randomicamente* na horizontal
    :param embarcacao: embarcação a ser alocada
    :param tamanho_embarcacao: tamanho da embarcação a ser alocada
    :param tamanho_tabuleiro: tamanho do tabuleiro (definido pelo jogador)
    :param tabuleiro: tabuleiro a ser preenchido.
    :param lista_coord_inocupaveis: coordenadas que contem embarcações alocadas
    :param lista_coord_aprox: coordenadas inocupáveis por estarem próximas às embarcações
    :return: sem retorno
    """
    while True:

        a_coord_eh_inocupavel = False

        # lista que armazenará linhas e colunas disponíveis
        lista_numeros = list()

        # preenchendo a lista com as linhas e colunas disponíveis
        for a in range(0, tamanho_tabuleiro):
            lista_numeros.append(a)

        linha_coord = choice(lista_numeros)
        coluna_coord = choice(lista_numeros)

        # FOR QUE CHECA SE LINHA E COLUNA JÁ ESTÃO EM LISTA_COORD_INOCUPAVEIS
        for a in lista_coord_inocupaveis:
            if (a[0] == linha_coord) and (a[1] == coluna_coord):
                a_coord_eh_inocupavel = True
                break

        if a_coord_eh_inocupavel:
            continue

        # FOR QUE CHECA SE A COORDENADA ESCOLHIDA EH INOCUPAVEL POR APROXIMACAO
        for a in lista_coord_aprox:
            if (a[0] == linha_coord) and (a[1] == coluna_coord):
                a_coord_eh_inocupavel = True
                break

        if a_coord_eh_inocupavel:
            continue

        # if que entramos se for submarino, acrescenta no tabuleiro e depois
        if tamanho_embarcacao == 1:

            tabuleiro[linha_coord][coluna_coord] = 'x'
            # roda a lista procurando os x, acrescentando as novas coord inocupaveis na lista
            for a in range(0, tamanho_tabuleiro):
                for b in range(0, tamanho_tabuleiro):
                    if tabuleiro[a][b] == 'x':
                        if [a, b] not in lista_coord_inocupaveis:
                            lista_coord_inocupaveis.append([a, b])

            return

        # entra aqui quando a embarcacao for maior que submarino
        else:

            # if somente para embarcacoes em linha reta
            if embarcacao != 'HIDROAVIAO':

                # if que checa se a embarcacao cabe no tabuleiro a partir da coluna inicial
                if coluna_coord + tamanho_embarcacao <= tamanho_tabuleiro:

                    # for que roda as colunas seguintes verificando se sao inocupaveis
                    for colunas_check in range(coluna_coord, coluna_coord + tamanho_embarcacao):
                        if tabuleiro[linha_coord][colunas_check] == 'x':
                            a_coord_eh_inocupavel = True

                            break

                    # dá break e volta a pedir os dados
                    if a_coord_eh_inocupavel:
                        continue

                    # FOR QUE CHECA SE AS COLUNAS SEGUINTES SAO INOCUPAVEIS POS APROXIMACAO
                    for coluna in range(coluna_coord, coluna_coord + tamanho_embarcacao):
                        if [linha_coord, coluna] in lista_coord_aprox:
                            a_coord_eh_inocupavel = True

                    # dá break e volta a pedir os dados
                    if a_coord_eh_inocupavel:
                        continue

                    # coloca o x nas colunas a frente
                    for colunas_check in range(coluna_coord, coluna_coord + tamanho_embarcacao):
                        tabuleiro[linha_coord][colunas_check] = 'x'

                    # roda o tabuleiro procurando os novos inocupaveis para lista
                    for a in range(0, tamanho_tabuleiro):
                        for b in range(0, tamanho_tabuleiro):
                            if tabuleiro[a][b] == 'x':
                                if [a, b] not in lista_coord_inocupaveis:
                                    lista_coord_inocupaveis.append([a, b])

                    return

            # entramos aqui se a embarcacao for um hidroaviao
            else:
                # if que checa se a embarcacao cabe no tabuleiro a partir da coluna inicial
                if (coluna_coord + 1 < tamanho_tabuleiro) and (linha_coord + 1 < tamanho_tabuleiro) and \
                        (coluna_coord - 1 >= 0):

                    # verificando se as casas do hidroaviao estao livres em inocupaveis
                    if [linha_coord + 1, coluna_coord - 1] in lista_coord_inocupaveis or \
                            [linha_coord + 1, coluna_coord + 1] in lista_coord_inocupaveis:
                        continue

                    # verificando se as casas do hidroaviao estao livres em inocupaveis por aprox
                    if [linha_coord + 1, coluna_coord - 1] in lista_coord_aprox or \
                            [linha_coord + 1, coluna_coord + 1] in lista_coord_aprox:
                        continue

                    # adicionando as casas no tabuleiro
                    tabuleiro[linha_coord][coluna_coord] = 'x'
                    tabuleiro[linha_coord + 1][coluna_coord - 1] = 'x'
                    tabuleiro[linha_coord + 1][coluna_coord + 1] = 'x'

                    # roda o tabuleiro procurando os novos inocupaveis para lista
                    for a in range(0, tamanho_tabuleiro):
                        for b in range(0, tamanho_tabuleiro):
                            if tabuleiro[a][b] == 'x':
                                if [a, b] not in lista_coord_inocupaveis:
                                    lista_coord_inocupaveis.append([a, b])

                    return

                # entra aqui se o barco nao cabe no tabuleiro
                else:

                    continue


def preenchendo_randomicamente(embarcacoes, tamanho_tabuleiro, tabuleiro, num_jogador):
    """
    FUNÇÃO CHAMADA QUANDO A MÁQUINA FOR CHAMADA PARA PREENCHER O TABULEIRO

    :param embarcacoes: lista com as embarcações pré-definidas
    :param tamanho_tabuleiro: tamanho pré-definido de linhas e colunas do tabuleiro
    :param tabuleiro: é o tabuleiro a ser preenchido
    :param num_jogador: número que permite enviar mensagem ao jogador desejado
    :return: lista_coord_inocupaveis_principal
    """
    lista_coord_inocupaveis_principal = list()
    lista_coord_inocupaveis_por_aprox = list()
    lista_auxiliar_inocup_por_aprox = list()

    TAM_SUBMARINO = 1
    TAM_CRUZADOR = 2
    TAM_ENCOURACADO = 4
    TAM_PORTAAVIOES = 5
    TAM_HIDROAVIAO = 3

    for embarcacao in embarcacoes:

        if embarcacao != 'SUBMARINO':

            orientacao = choice(['HORIZONTAL', 'VERTICAL'])

            if orientacao == 'HORIZONTAL':

                if embarcacao == 'HIDROAVIAO':

                    aloca_randomicamente_horizontal(embarcacao, TAM_HIDROAVIAO, tamanho_tabuleiro, tabuleiro,
                                                    lista_coord_inocupaveis_principal,
                                                    lista_coord_inocupaveis_por_aprox)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                elif embarcacao == 'CRUZADOR':

                    aloca_randomicamente_horizontal(embarcacao, TAM_CRUZADOR, tamanho_tabuleiro, tabuleiro,
                                                    lista_coord_inocupaveis_principal,
                                                    lista_coord_inocupaveis_por_aprox)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                elif embarcacao == 'PORTA-AVIOES':

                    aloca_randomicamente_horizontal(embarcacao, TAM_PORTAAVIOES, tamanho_tabuleiro, tabuleiro,
                                                    lista_coord_inocupaveis_principal,
                                                    lista_coord_inocupaveis_por_aprox)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                elif embarcacao == 'ENCOURACADO':

                    aloca_randomicamente_horizontal(embarcacao, TAM_ENCOURACADO, tamanho_tabuleiro, tabuleiro,
                                                    lista_coord_inocupaveis_principal,
                                                    lista_coord_inocupaveis_por_aprox)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

            elif orientacao == 'VERTICAL':

                if embarcacao == 'HIDROAVIAO':

                    aloca_randomicamente_vertical(embarcacao, TAM_HIDROAVIAO, tamanho_tabuleiro, tabuleiro,
                                                  lista_coord_inocupaveis_principal,
                                                  lista_coord_inocupaveis_por_aprox)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                elif embarcacao == 'CRUZADOR':

                    aloca_randomicamente_vertical(embarcacao, TAM_CRUZADOR, tamanho_tabuleiro, tabuleiro,
                                                  lista_coord_inocupaveis_principal,
                                                  lista_coord_inocupaveis_por_aprox)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                elif embarcacao == 'PORTA-AVIOES':

                    aloca_randomicamente_vertical(embarcacao, TAM_PORTAAVIOES, tamanho_tabuleiro, tabuleiro,
                                                  lista_coord_inocupaveis_principal,
                                                  lista_coord_inocupaveis_por_aprox)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                elif embarcacao == 'ENCOURACADO':
                    aloca_randomicamente_vertical(embarcacao, TAM_ENCOURACADO, tamanho_tabuleiro, tabuleiro,
                                                  lista_coord_inocupaveis_principal,
                                                  lista_coord_inocupaveis_por_aprox)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

        # se a embarcacao for submarino entra aqui
        else:

            aloca_randomicamente_horizontal(embarcacao, TAM_SUBMARINO, tamanho_tabuleiro, tabuleiro,
                                            lista_coord_inocupaveis_principal,
                                            lista_coord_inocupaveis_por_aprox)

            encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                 lista_coord_inocupaveis_por_aprox,
                                                 lista_auxiliar_inocup_por_aprox)

    preenche_espacos_til(tabuleiro, tamanho_tabuleiro)

    return lista_coord_inocupaveis_principal


def encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro, lista_inocupaveis_por_aprox, lista_auxiliar):
    """
    FUNÇÃO QUE BUSCARÁ TODOS OS X NO TABULEIRO E VERIFICARÁ AS CASAS INOCUPÁVEIS POR APROXIMAÇÃO DE CADA X.
    POR FIM, ACRESCENTANDO AS INOCUPAVEIS POR APROXIMAÇÃO NA lista_inocupaveis_por_aprox, MAS APENAS SE A
    CASA AINDA NÃO ESTIVER LÁ.

    :param tamanho_tabuleiro: tamanho do tabuleiro escolhido pelo jogador1
    :param tabuleiro: tabuleiro do jogador que está alocando os barcos atualmente
    :param lista_inocupaveis_por_aprox: lista em que ficarão as casas inocupáveis por aproximação.
    :param lista_auxiliar: é a lista usada de parâmetro para sabermos se as casas
    próximas à casa com 'x' já foram adicionadas a lista_inocupaveis_por_aprox
    :return: sem retorno
    """
    for linha in range(0, tamanho_tabuleiro):
        for coluna in range(0, tamanho_tabuleiro):
            if tabuleiro[linha][coluna] == 'x' and [linha, coluna] not in lista_auxiliar:

                adiciona_coord_acima = True
                adiciona_coord_abaixo = True
                adiciona_coord_esquerda = True
                adiciona_coord_direita = True

                if linha == 0:
                    adiciona_coord_acima = False

                if coluna == 0:
                    adiciona_coord_esquerda = False

                if coluna == (tamanho_tabuleiro - 1):
                    adiciona_coord_direita = False

                if linha == (tamanho_tabuleiro - 1):
                    adiciona_coord_abaixo = False

                # adiciona casa acima em inocupaveis por aproximacao
                if adiciona_coord_acima is True and tabuleiro[linha - 1][coluna] != 'x' \
                        and [linha - 1, coluna] not in lista_inocupaveis_por_aprox:
                    lista_inocupaveis_por_aprox.append([linha - 1, coluna])

                # adiciona casa a direita em inocupaveis por aproximacao
                if adiciona_coord_direita is True and tabuleiro[linha][coluna + 1] != 'x' \
                        and [linha, coluna + 1] not in lista_inocupaveis_por_aprox:
                    lista_inocupaveis_por_aprox.append([linha, coluna + 1])

                # adiciona casa abaixo em inocupaveis por aproximacao
                if adiciona_coord_abaixo is True and tabuleiro[linha + 1][coluna] != 'x' \
                        and [linha + 1, coluna] not in lista_inocupaveis_por_aprox:
                    lista_inocupaveis_por_aprox.append([linha + 1, coluna])

                # adiciona casa a esquerda em inocupaveis por aproximacao
                if adiciona_coord_esquerda is True and tabuleiro[linha][coluna - 1] != 'x' \
                        and [linha, coluna - 1] not in lista_inocupaveis_por_aprox:
                    lista_inocupaveis_por_aprox.append([linha, coluna - 1])

                if adiciona_coord_esquerda is True and adiciona_coord_acima is True and \
                        tabuleiro[linha - 1][coluna - 1] != 'x' and [linha - 1,
                                                                     coluna - 1] not in lista_inocupaveis_por_aprox:
                    lista_inocupaveis_por_aprox.append([linha - 1, coluna - 1])

                if adiciona_coord_esquerda is True and adiciona_coord_abaixo is True and \
                        tabuleiro[linha + 1][coluna - 1] != 'x' and [linha + 1,
                                                                     coluna - 1] not in lista_inocupaveis_por_aprox:
                    lista_inocupaveis_por_aprox.append([linha + 1, coluna - 1])

                if adiciona_coord_direita is True and adiciona_coord_acima is True and \
                        tabuleiro[linha - 1][coluna + 1] != 'x' and [linha - 1,
                                                                     coluna + 1] not in lista_inocupaveis_por_aprox:
                    lista_inocupaveis_por_aprox.append([linha - 1, coluna + 1])

                if adiciona_coord_direita is True and adiciona_coord_abaixo is True and \
                        tabuleiro[linha + 1][coluna + 1] != 'x' and [linha + 1,
                                                                     coluna + 1] not in lista_inocupaveis_por_aprox:
                    lista_inocupaveis_por_aprox.append([linha + 1, coluna + 1])

                lista_auxiliar.append([linha, coluna])


def aloca_embarcacoes_vertical(embarcacao, tamanho_embarcacao, tamanho_tabuleiro,
                               letras_tabuleiro, tabuleiro, lista_coord_inocupaveis, lista_coord_aprox, num_jogador):
    """
    função chamada quando a embarcação for inserida manualmente e verticalmente.
    :param embarcacao: nome da embarcação
    :param tamanho_embarcacao: tamanho da embarcação
    :param tamanho_tabuleiro: tamanho do tabuleiro (pré-definido pelo jogador)
    :param letras_tabuleiro: letras do tabuleiro
    :param tabuleiro: tabuleiro do jogador o qual irá inserir a peça
    :param lista_coord_inocupaveis: lista de coordenadas onde estão as embarcações
    :param lista_coord_aprox: lista de coordenadas próximas as embarcações
    :param num_jogador: jogador o qual receberá as mensagens
    :return: sem retorno
    """
    while True:
        a_coord_eh_inocupavel = False

        linha_coord, coluna_coord = testa_entrada_coord_barco(num_jogador, tamanho_tabuleiro,
                                                              letras_tabuleiro, embarcacao)

        # FOR QUE CHECA SE LINHA E COLUNA JÁ ESTÃO EM LISTA_COORD_INOCUPAVEIS
        for a in lista_coord_inocupaveis:
            if (a[0] == linha_coord) and (a[1] == coluna_coord):
                a_coord_eh_inocupavel = True
                mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                mensagem_unitaria(f'! A COORDENADA ESCOLHIDA JÁ ESTÁ OCUPADA !'.encode('UTF-8'), num_jogador)
                break

        if a_coord_eh_inocupavel:
            continue

        # FOR QUE CHECA SE A COORDENADA ESCOLHIDA EH INOCUPAVEL POR APROXIMACAO
        for a in lista_coord_aprox:
            if (a[0] == linha_coord) and (a[1] == coluna_coord):
                a_coord_eh_inocupavel = True
                mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                mensagem_unitaria(f'! A COORDENADA ESCOLHIDA NÃO PODE SER OCUPADA POR ESTAR GRUDADA'
                                  f' EM OUTRA EMBARCAÇÃO !'.encode('UTF-8'), num_jogador)
                break

        if a_coord_eh_inocupavel:
            continue

        # if que entramos se for submarino, acrescenta no tabuleiro e depois
        if tamanho_embarcacao == 1:
            tabuleiro[linha_coord][coluna_coord] = 'x'
            # roda a lista procurando os x, acrescentando as novas coord inocupaveis na lista
            for a in range(0, tamanho_tabuleiro):
                for b in range(0, tamanho_tabuleiro):
                    if tabuleiro[a][b] == 'x':
                        if [a, b] not in lista_coord_inocupaveis:
                            lista_coord_inocupaveis.append([a, b])

            return

        # entra aqui quando a embarcacao for maior que submarino
        else:
            if embarcacao != 'HIDROAVIAO':

                # if que checa se a embarcacao cabe no tabuleiro a partir da linha inicial
                if linha_coord + tamanho_embarcacao <= tamanho_tabuleiro:

                    # for que roda as linhas abaixo verificando se sao inocupaveis
                    for linhas_check in range(linha_coord, linha_coord + tamanho_embarcacao):
                        if tabuleiro[linhas_check][coluna_coord] == 'x':
                            a_coord_eh_inocupavel = True
                            mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                            mensagem_unitaria(f'!  EXISTEM LINHAS ABAIXO JÁ PREENCHIDAS'
                                              f' IMPEDINDO SUA ESCOLHA.VERIQUE SEU TABULEIRO'
                                              f' E ESCOLHA OUTRO PONTO INICIAL'
                                              f' !'.encode('UTF-8'), num_jogador)

                            # COLOCAR UM PRINT DO TABULEIRO SÓ DO J1 AQUI
                            printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro)

                            break

                    if a_coord_eh_inocupavel:
                        continue

                    # FOR QUE CHECA SE AS LINHAS SEGUINTES SAO INOCUPAVEIS POS APROXIMACAO
                    for linha in range(linha_coord, linha_coord + tamanho_embarcacao):
                        if [linha, coluna_coord] in lista_coord_aprox:
                            a_coord_eh_inocupavel = True
                            mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                            mensagem_unitaria(f'!  SUA EMBARCAÇÃO NÃO PODE SER COLOCADA NESSA COORDENADA'
                                              f' POIS FICARÁ GRUDADA EM OUTRA EMBARCAÇÃO. VERIFIQUE SEU'
                                              f' TABULEIRO E ESCOLHA OUTRO PONTO'
                                              f' INICIAL'.encode('UTF-8'), num_jogador)

                            # COLOCAR UM PRINT DO TABULEIRO SÓ DO J1 AQUI
                            printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro)

                            break

                    if a_coord_eh_inocupavel:
                        continue

                    # coloca o x nas colunas a frente
                    for linhas_check in range(linha_coord, linha_coord + tamanho_embarcacao):
                        tabuleiro[linhas_check][coluna_coord] = 'x'

                    # roda o tabuleiro procurando os novos inocupaveis para lista
                    for a in range(0, tamanho_tabuleiro):
                        for b in range(0, tamanho_tabuleiro):
                            if tabuleiro[a][b] == 'x':
                                if [a, b] not in lista_coord_inocupaveis:
                                    lista_coord_inocupaveis.append([a, b])

                    return

                # entra aqui se o barco nao cabe no tabuleiro
                else:
                    mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                    mensagem_unitaria(f'! A EMBARCAÇÃO NÃO PODE SER COLOCADA NA COORDENADA'
                                      f' ESCOLHIDA, POIS SERÁ PARTIDA AO MEIO'
                                      f' !'.encode('UTF-8'), num_jogador)

                    continue

            elif embarcacao == 'HIDROAVIAO':
                # checando se cabe no tabuleiro a partir da coluna e linha inicial
                if (linha_coord + 1 < tamanho_tabuleiro) and (coluna_coord + 1 < tamanho_tabuleiro) and \
                        (linha_coord - 1 >= 0):

                    # verificando se as casas do hidroaviao estao livres em inocupaveis:
                    if [linha_coord - 1, coluna_coord + 1] in lista_coord_inocupaveis or \
                            [linha_coord + 1, coluna_coord + 1] in lista_coord_inocupaveis:
                        mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                        mensagem_unitaria(f'!  EXISTEM COLUNAS Á FRENTE JÁ PREENCHIDAS'
                                          f' IMPEDINDO SUA ESCOLHA.VERIQUE SEU TABULEIRO'
                                          f' E ESCOLHA OUTRO PONTO INICIAL'
                                          f' !'.encode('UTF-8'), num_jogador)
                        continue

                    # verificando se as casas do hidroaviao estao livres em inocupaveis por aprox
                    if [linha_coord - 1, coluna_coord + 1] in lista_coord_aprox or \
                            [linha_coord + 1, coluna_coord + 1] in lista_coord_aprox:
                        mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                        mensagem_unitaria(f'!  SUA EMBARCAÇÃO NÃO PODE SER COLOCADA NESSA COORDENADA'
                                          f' POIS FICARÁ GRUDADA EM OUTRA EMBARCAÇÃO. VERIFIQUE SEU'
                                          f' TABULEIRO E ESCOLHA OUTRO PONTO'
                                          f' INICIAL'.encode('UTF-8'), num_jogador)

                        continue

                    # adicionando as casas no tabuleiro:
                    tabuleiro[linha_coord][coluna_coord] = 'x'
                    tabuleiro[linha_coord - 1][coluna_coord + 1] = 'x'
                    tabuleiro[linha_coord + 1][coluna_coord + 1] = 'x'

                    # roda o tabuleiro procurando os novos inocupaveis para lista
                    for a in range(0, tamanho_tabuleiro):
                        for b in range(0, tamanho_tabuleiro):
                            if tabuleiro[a][b] == 'x':
                                if [a, b] not in lista_coord_inocupaveis:
                                    lista_coord_inocupaveis.append([a, b])

                    return

                # entra aqui se o hidroaviao nao cabe no tabuleiro
                else:
                    mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                    mensagem_unitaria(f'! A EMBARCAÇÃO NÃO PODE SER COLOCADA NA COORDENADA'
                                      f' ESCOLHIDA, POIS SERÁ PARTIDA AO MEIO'
                                      f' !'.encode('UTF-8'), num_jogador)
                    continue


def aloca_embarcacoes_horizontal(embarcacao, tamanho_embarcacao, tamanho_tabuleiro,
                                 letras_tabuleiro, tabuleiro, lista_coord_inocupaveis, lista_coord_aprox, num_jogador):
    """
    ESSA É A FUNÇÃO A QUAL RECEBE AS COORDENADA DO JOGADOR E TESTARÁ SE ELAS SÃO VÁLIDAS.
    :param embarcacao: NOME DA EMBARCAÇÃO
    :param tamanho_embarcacao: QUANTAS CASAS A EMBARCAÇÃO OCUPA
    :param tamanho_tabuleiro: TAMANHO DO TABULEIRO DEFINIDO NO INÍCIO
    :param letras_tabuleiro: LETRAS PRINTADAS NO TABULEIRO
    :param tabuleiro: TABULEIRO NO QUAL IREMOS ALOCAR AS EMBARCAÇÕES
    :param lista_coord_inocupaveis: ESSA É A LISTA QUE NOS INFORMA QUAIS COORDENADAS NÃO PODEM SER OCUPADAS.
    :param lista_coord_aprox: é a lista que usaremos para testar se a casa escolhida é inocupavel por
    aproximação.
    :param num_jogador: é o índice do jogador que vamos mandar mensagem
    :return: sem retorno
    """

    while True:
        a_coord_eh_inocupavel = False

        linha_coord, coluna_coord = testa_entrada_coord_barco(num_jogador, tamanho_tabuleiro,
                                                              letras_tabuleiro, embarcacao)

        # FOR QUE CHECA SE LINHA E COLUNA JÁ ESTÃO EM LISTA_COORD_INOCUPAVEIS
        for a in lista_coord_inocupaveis:
            if (a[0] == linha_coord) and (a[1] == coluna_coord):
                a_coord_eh_inocupavel = True
                mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                mensagem_unitaria(f'! A COORDENADA ESCOLHIDA JÁ ESTÁ OCUPADA !'.encode('UTF-8'), num_jogador)
                break

        if a_coord_eh_inocupavel:
            continue

        # FOR QUE CHECA SE A COORDENADA ESCOLHIDA EH INOCUPAVEL POR APROXIMACAO
        for a in lista_coord_aprox:
            if (a[0] == linha_coord) and (a[1] == coluna_coord):
                a_coord_eh_inocupavel = True
                mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                mensagem_unitaria(f'! A COORDENADA ESCOLHIDA NÃO PODE SER OCUPADA POR ESTAR GRUDADA'
                                  f' EM OUTRA EMBARCAÇÃO !'.encode('UTF-8'), num_jogador)
                break

        if a_coord_eh_inocupavel:
            continue

        # if que entramos se for submarino, acrescenta no tabuleiro e depois
        if tamanho_embarcacao == 1:
            tabuleiro[linha_coord][coluna_coord] = 'x'
            # roda a lista procurando os x, acrescentando as novas coord inocupaveis na lista
            for a in range(0, tamanho_tabuleiro):
                for b in range(0, tamanho_tabuleiro):
                    if tabuleiro[a][b] == 'x':
                        if [a, b] not in lista_coord_inocupaveis:
                            lista_coord_inocupaveis.append([a, b])

            return

        # entra aqui quando a embarcacao for maior que submarino
        else:

            # if somente para embarcacoes em linha reta
            if embarcacao != 'HIDROAVIAO':

                # if que checa se a embarcacao cabe no tabuleiro a partir da coluna inicial
                if coluna_coord + tamanho_embarcacao <= tamanho_tabuleiro:

                    # for que roda as colunas seguintes verificando se sao inocupaveis
                    for colunas_check in range(coluna_coord, coluna_coord + tamanho_embarcacao):
                        if tabuleiro[linha_coord][colunas_check] == 'x':
                            a_coord_eh_inocupavel = True
                            mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)

                            mensagem_unitaria(f'!  EXISTEM COLUNAS Á FRENTE JÁ PREENCHIDAS'
                                              f' IMPEDINDO SUA ESCOLHA.VERIQUE SEU TABULEIRO'
                                              f' E ESCOLHA OUTRO PONTO INICIAL'
                                              f' !'.encode('UTF-8'), num_jogador)
                            # COLOCAR UM PRINT DO TABULEIRO SÓ DO J1 AQUI
                            printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro)

                            break

                    # dá break e volta a pedir os dados
                    if a_coord_eh_inocupavel:
                        continue

                    # FOR QUE CHECA SE AS COLUNAS SEGUINTES SAO INOCUPAVEIS POS APROXIMACAO
                    for coluna in range(coluna_coord, coluna_coord + tamanho_embarcacao):
                        if [linha_coord, coluna] in lista_coord_aprox:
                            a_coord_eh_inocupavel = True
                            mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                            mensagem_unitaria(f'!  SUA EMBARCAÇÃO NÃO PODE SER COLOCADA NESSA COORDENADA'
                                              f' POIS FICARÁ GRUDADA EM OUTRA EMBARCAÇÃO. VERIFIQUE SEU'
                                              f' TABULEIRO E ESCOLHA OUTRO PONTO'
                                              f' INICIAL'.encode('UTF-8'), num_jogador)

                            # COLOCAR UM PRINT DO TABULEIRO SÓ DO J1 AQUI
                            printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro)

                    # dá break e volta a pedir os dados
                    if a_coord_eh_inocupavel:
                        continue

                    # coloca o x nas colunas a frente
                    for colunas_check in range(coluna_coord, coluna_coord + tamanho_embarcacao):
                        tabuleiro[linha_coord][colunas_check] = 'x'

                    # roda o tabuleiro procurando os novos inocupaveis para lista
                    for a in range(0, tamanho_tabuleiro):
                        for b in range(0, tamanho_tabuleiro):
                            if tabuleiro[a][b] == 'x':
                                if [a, b] not in lista_coord_inocupaveis:
                                    lista_coord_inocupaveis.append([a, b])

                    return

                # entra aqui se o barco nao cabe no tabuleiro
                else:
                    mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                    mensagem_unitaria(f'! A EMBARCAÇÃO NÃO PODE SER COLOCADA NA COORDENADA'
                                      f' ESCOLHIDA, POIS SERÁ PARTIDA AO MEIO'
                                      f' !'.encode('UTF-8'), num_jogador)
                    continue

            # entramos aqui se a embarcacao for um hidroaviao
            else:
                # if que checa se a embarcacao cabe no tabuleiro a partir da coluna inicial
                if (coluna_coord + 1 < tamanho_tabuleiro) and (linha_coord + 1 < tamanho_tabuleiro) and \
                        (coluna_coord - 1 >= 0):

                    # verificando se as casas do hidroaviao estao livres em inocupaveis
                    if [linha_coord + 1, coluna_coord - 1] in lista_coord_inocupaveis or \
                            [linha_coord + 1, coluna_coord + 1] in lista_coord_inocupaveis:
                        mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                        mensagem_unitaria(f'!  EXISTEM COLUNAS Á FRENTE JÁ PREENCHIDAS'
                                          f' IMPEDINDO SUA ESCOLHA.VERIQUE SEU TABULEIRO'
                                          f' E ESCOLHA OUTRO PONTO INICIAL'
                                          f' !'.encode('UTF-8'), num_jogador)
                        continue

                    # verificando se as casas do hidroaviao estao livres em inocupaveis por aprox
                    if [linha_coord + 1, coluna_coord - 1] in lista_coord_aprox or \
                            [linha_coord + 1, coluna_coord + 1] in lista_coord_aprox:
                        mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                        mensagem_unitaria(f'!  SUA EMBARCAÇÃO NÃO PODE SER COLOCADA NESSA COORDENADA'
                                          f' POIS FICARÁ GRUDADA EM OUTRA EMBARCAÇÃO. VERIFIQUE SEU'
                                          f' TABULEIRO E ESCOLHA OUTRO PONTO'
                                          f' INICIAL'.encode('UTF-8'), num_jogador)

                        continue

                    # adicionando as casas no tabuleiro
                    tabuleiro[linha_coord][coluna_coord] = 'x'
                    tabuleiro[linha_coord + 1][coluna_coord - 1] = 'x'
                    tabuleiro[linha_coord + 1][coluna_coord + 1] = 'x'

                    # roda o tabuleiro procurando os novos inocupaveis para lista
                    for a in range(0, tamanho_tabuleiro):
                        for b in range(0, tamanho_tabuleiro):
                            if tabuleiro[a][b] == 'x':
                                if [a, b] not in lista_coord_inocupaveis:
                                    lista_coord_inocupaveis.append([a, b])

                    return

                # entra aqui se o hidroaviao nao cabe no tabuleiro
                else:
                    mensagem_unitaria(f'\n\n'.encode('UTF-8'), num_jogador)
                    mensagem_unitaria(f'! A EMBARCAÇÃO NÃO PODE SER COLOCADA NA COORDENADA'
                                      f' ESCOLHIDA, POIS SERÁ PARTIDA AO MEIO'
                                      f' !'.encode('UTF-8'), num_jogador)
                    continue


def insere_embarcacao_no_tabuleiro(embarcacoes, tamanho_tabuleiro, letras_tabuleiro, tabuleiro, num_jogador):
    """
    FUNÇÃO QUE RECEBE A LISTA DE EMBARCAÇÕES E ENVIA CADA TIPO PARA O ALOCADOR COM O TAMANHO DA EMBARCACAO.
    :param embarcacoes: É A LISTA DE EMBARCAÇOES QUE OBTEMOS DE ACORDO COM O TAMANHO DO TABULEIRO
    :param tamanho_tabuleiro: CONTÉM O TAMANHO DE LINHAS E COLUNAS DO TABULEIRO
    :param letras_tabuleiro: SÃO AS LETRAS EXISTENTES NESSE TABULEIRO
    :param tabuleiro: É O TABULEIRO SELECIONADO P/ INSERIR AS EMBARCAÇÕES
    :param num_jogador: É A STRING QUE VAI INFORMAR SE A MENSAGEM EH PRO J1 OU J2
    :return: lista_coord_inocupaveis_principal
    """

    lista_coord_inocupaveis_principal = list()
    lista_coord_inocupaveis_por_aprox = list()
    lista_auxiliar_inocup_por_aprox = list()

    TAM_SUBMARINO = 1
    TAM_CRUZADOR = 2
    TAM_ENCOURACADO = 4
    TAM_PORTAAVIOES = 5
    TAM_HIDROAVIAO = 3

    for embarcacao in embarcacoes:

        if embarcacao != 'SUBMARINO':

            orientacao = testa_vertical_horizontal(num_jogador, embarcacao)

            if orientacao == 'HORIZONTAL':

                if embarcacao == 'HIDROAVIAO':
                    aloca_embarcacoes_horizontal(embarcacao, TAM_HIDROAVIAO, tamanho_tabuleiro, letras_tabuleiro,
                                                 tabuleiro, lista_coord_inocupaveis_principal,
                                                 lista_coord_inocupaveis_por_aprox, num_jogador)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                    # insere os @'s nas coord inocupaveis por aproximacao
                    preenche_coord_inucopavel_aprox(tabuleiro, lista_coord_inocupaveis_por_aprox)

                    # printa o tabuleiro com a peça no lugar e os inocupaveis por aproximacao
                    printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro, num_jogador)

                elif embarcacao == 'CRUZADOR':
                    aloca_embarcacoes_horizontal(embarcacao, TAM_CRUZADOR, tamanho_tabuleiro, letras_tabuleiro,
                                                 tabuleiro, lista_coord_inocupaveis_principal,
                                                 lista_coord_inocupaveis_por_aprox, num_jogador)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                    # insere os @'s nas coord inocupaveis por aproximacao
                    preenche_coord_inucopavel_aprox(tabuleiro, lista_coord_inocupaveis_por_aprox)

                    # printa o tabuleiro com a peça no lugar e os inocupaveis por aproximacao
                    printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro, num_jogador)

                elif embarcacao == 'PORTA-AVIOES':
                    aloca_embarcacoes_horizontal(embarcacao, TAM_PORTAAVIOES, tamanho_tabuleiro, letras_tabuleiro,
                                                 tabuleiro, lista_coord_inocupaveis_principal,
                                                 lista_coord_inocupaveis_por_aprox, num_jogador)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                    # insere os @'s nas coord inocupaveis por aproximacao
                    preenche_coord_inucopavel_aprox(tabuleiro, lista_coord_inocupaveis_por_aprox)

                    # printa o tabuleiro com a peça no lugar e os inocupaveis por aproximacao
                    printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro, num_jogador)

                elif embarcacao == 'ENCOURACADO':
                    aloca_embarcacoes_horizontal(embarcacao, TAM_ENCOURACADO, tamanho_tabuleiro, letras_tabuleiro,
                                                 tabuleiro, lista_coord_inocupaveis_principal,
                                                 lista_coord_inocupaveis_por_aprox, num_jogador)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                    # insere os @'s nas coord inocupaveis por aproximacao
                    preenche_coord_inucopavel_aprox(tabuleiro, lista_coord_inocupaveis_por_aprox)

                    # printa o tabuleiro com a peça no lugar e os inocupaveis por aproximacao
                    printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro, num_jogador)

            elif orientacao == 'VERTICAL':

                if embarcacao == 'HIDROAVIAO':
                    aloca_embarcacoes_vertical(embarcacao, TAM_HIDROAVIAO, tamanho_tabuleiro, letras_tabuleiro,
                                               tabuleiro, lista_coord_inocupaveis_principal,
                                               lista_coord_inocupaveis_por_aprox, num_jogador)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                    # insere os @'s nas coord inocupaveis por aproximacao
                    preenche_coord_inucopavel_aprox(tabuleiro, lista_coord_inocupaveis_por_aprox)

                    # printa o tabuleiro com a peça no lugar e os inocupaveis por aproximacao
                    printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro, num_jogador)

                elif embarcacao == 'CRUZADOR':
                    aloca_embarcacoes_vertical(embarcacao, TAM_CRUZADOR, tamanho_tabuleiro, letras_tabuleiro,
                                               tabuleiro, lista_coord_inocupaveis_principal,
                                               lista_coord_inocupaveis_por_aprox, num_jogador)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                    # insere os @'s nas coord inocupaveis por aproximacao
                    preenche_coord_inucopavel_aprox(tabuleiro, lista_coord_inocupaveis_por_aprox)

                    # printa o tabuleiro com a peça no lugar e os inocupaveis por aproximacao
                    printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro, num_jogador)

                elif embarcacao == 'PORTA-AVIOES':
                    aloca_embarcacoes_vertical(embarcacao, TAM_PORTAAVIOES, tamanho_tabuleiro, letras_tabuleiro,
                                               tabuleiro, lista_coord_inocupaveis_principal,
                                               lista_coord_inocupaveis_por_aprox, num_jogador)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                    # insere os @'s nas coord inocupaveis por aproximacao
                    preenche_coord_inucopavel_aprox(tabuleiro, lista_coord_inocupaveis_por_aprox)

                    # printa o tabuleiro com a peça no lugar e os inocupaveis por aproximacao
                    printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro, num_jogador)

                elif embarcacao == 'ENCOURACADO':
                    aloca_embarcacoes_vertical(embarcacao, TAM_ENCOURACADO, tamanho_tabuleiro, letras_tabuleiro,
                                               tabuleiro, lista_coord_inocupaveis_principal,
                                               lista_coord_inocupaveis_por_aprox, num_jogador)

                    encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro,
                                                         lista_coord_inocupaveis_por_aprox,
                                                         lista_auxiliar_inocup_por_aprox)

                    # insere os @'s nas coord inocupaveis por aproximacao
                    preenche_coord_inucopavel_aprox(tabuleiro, lista_coord_inocupaveis_por_aprox)

                    # printa o tabuleiro com a peça no lugar e os inocupaveis por aproximacao
                    printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro, num_jogador)

        # se a embarcacao for submarino entra aqui
        else:
            aloca_embarcacoes_horizontal(embarcacao, TAM_SUBMARINO, tamanho_tabuleiro, letras_tabuleiro,
                                         tabuleiro, lista_coord_inocupaveis_principal,
                                         lista_coord_inocupaveis_por_aprox, num_jogador)

            encontra_inocupaveis_por_aproximacao(tamanho_tabuleiro, tabuleiro, lista_coord_inocupaveis_por_aprox,
                                                 lista_auxiliar_inocup_por_aprox)

            # insere os @'s nas coord inocupaveis por aproximacao
            preenche_coord_inucopavel_aprox(tabuleiro, lista_coord_inocupaveis_por_aprox)

            # printa o tabuleiro com a peça no lugar e os inocupaveis por aproximacao
            printa_tabuleiro(tabuleiro, tamanho_tabuleiro, letras_tabuleiro, num_jogador)

    preenche_espacos_til(tabuleiro, tamanho_tabuleiro)

    return lista_coord_inocupaveis_principal


def define_letras_tabuleiro(tamanho):
    """
    FUNÇÃO QUE DEFINE QUAIS SÃO AS LETRAS QUE UTILIZAREMOS DE ACORDO COM O TAMANHO DE TABULEIRO ESCOLHIDO PELO JOGADOR.
    ATÉ AGORA VAI ATÉ 10 (ACRESCENTAR ATÉ 15).
    :param tamanho: TAMANHO DO TABULEIRO DEFINIDO PELO JOGADOR 1
    :return: LISTA COM LETRAS UTILIZADAS
    """
    letras_disponiveis = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                          'S', 'T']

    letras_utilizadas = list()

    for a in range(0, tamanho):
        letras_utilizadas.append(letras_disponiveis[a])

    return letras_utilizadas


def cria_tabuleiro(tabuleiro, tamanho):
    """
    CRIA O TABULEIRO APENAS COM '_' EM TODAS AS LINHAS E COLUNAS
    :param tabuleiro: QUAL TABULEIRO ESTOU PREENCHENDO
    :param tamanho: TAMANHO DE TABULEIRO DEFINIDO PELO USUÁRIO
    :return: SEM RETORNO
    """

    simbolo = '_'

    for a in range(0, tamanho):
        linha = list()
        for b in range(0, tamanho):
            linha.append(simbolo)

        tabuleiro.append(linha)