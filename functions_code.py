"""
PEDRO HENRIQUE JABER CAVALCANTE
16/05/2022
"""
import datetime

from class_banho import Banho, extrair_dados
from functions_bd import *
from datetime import date, timedelta  # time
# import time
import os

# Graficos
# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt  # , dates
# import numpy as np

from dotenv.main import load_dotenv

load_dotenv()
banco_dados = os.environ['BD']


def gerar_data():  # função para gerar a data do Banho
    data = date.today()
    data_str = data.strftime("%Y-%m-%d")

    return data_str


def select_auto(mode=1):  # Encapsula o Select e a Conecção
    connection = open_connection()
    cursor = connection.cursor()

    select_banhos(cursor, mode)

    cursor.close()
    close_connection(connection)


def get_last_idt():  # Lê a Identificação do ultimo registro
    connection = open_connection()
    cursor = connection.cursor()

    sql_last = "call select_last_tb_banho"
    cursor.execute(sql_last)
    last_tupla = cursor.fetchone()
    v_last_idt = last_tupla[0]
    return v_last_idt


def deletar_do_txt(v_idt):
    alerta = ''
    # Procura a linha =====================================================================
    with open('registro_backup.txt', 'r') as arquivo_origem:
        linha_zero = arquivo_origem.readline()  # [000]*[mm:ss]--[dd/mm/yy]\n
        linha_retirar = ''
        while True:
            linha = arquivo_origem.readline()
            if linha == '':
                break
            elif int(linha[1:4]) == v_idt:
                linha_retirar = linha
                break
    # =====================================================================================

    # Apaga a linha caso tenha encontrado =================================================
    if linha_retirar == '':
        alerta = "Linha não encontrada"
    else:
        with open('registro_backup.txt', 'r') as arquivo_origem:  # lê o arquivo de backup
            with open('registro_temp.txt', 'w') as arquivo_destino:  # cria um arquivo temp
                arquivo_destino.write(linha_zero[:25])

                while True:
                    linha = arquivo_origem.readline()  # verifica linha por linha

                    if linha == '':  # para quando acabar as linhas
                        break

                    elif linha[1:4] != '000':
                        banho = extrair_dados(linha)

                    # print(f"[#{linha}#]")

                    if linha != linha_retirar and linha[1:4] != '000':  # filtra as linhas
                        # print("sim, escrever")
                        arquivo_destino.write(banho.registro())
                    # else:
                    #     print("não escrever")

        os.remove('registro_backup.txt')  # Deleta o arquivo desatualizado
        os.rename('registro_temp.txt', 'registro_backup.txt')  # Renomeia o arquivo temp para ser definitivo
    # =====================================================================================
    return alerta


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# + MENU -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


def criar_registro():  # Função para solicitar as informações e cria o registro
    try:
        minuto = int(input("Minuto   > "))
        segundo = int(input("Segundos > "))
        # ^^^ pede um valor inteiro, mas caso o usuario coloque algo diferente, alerta o problema
    except ValueError:
        alerta = "Valor Invalido"
    else:
        banho = Banho(minuto, segundo)

        # Registrar no banco de dados #########################

        tempo = f"00:{minuto:02d}:{segundo:02d}"
        data = gerar_data()

        connection = open_connection(1)
        cursor = connection.cursor()

        if banco_dados:
            erro = insert_banhos(cursor, tempo, data)
        else:
            erro = False

        alerta = ''
        # #####################################################

        if not erro:
            # Registrar no bloco de notas #####################
            with open("registro_backup.txt", 'a') as arq_registro:
                arq_registro.write(banho.registro())
            connection.commit()

            alerta = "Banho Registrado"
            # #################################################
        elif erro:
            alerta = "Erro Banco de dados"

        # time.sleep(0.5)
        #
        cursor.close()
        close_connection(connection, 1)
        #
        # time.sleep(0.5)

    return alerta  # Devolve o alerta para o menu


def cal_media_bd():  # Função para calcular a média

    # Pegar a media no banco de dados ##################################################################################
    connection = open_connection()
    cursor = connection.cursor()

    sql_time = "select sec_to_time(avg(time_to_sec(tmp_banho))) from tb_banho"

    cursor.execute(sql_time)
    tb_media = cursor.fetchall()

    cursor.close()
    close_connection(connection)

    media = tb_media[0][0]
    media_str = str(media)[2:7]
    # ^^^ transforma o tempo em string -> (0:00:00.0000) e filtra para tetirar o 0 das horas e milésimos -> (00:00)
    # ##################################################################################################################

    return f"Média: {media_str}"


def cal_media_bd_14():  # Função para calcular a média dos ultimos 14 registros (Media Movel?)

    # Pegar a media no banco de dados ##################################################################################
    connection = open_connection()
    cursor = connection.cursor()

    sql_time = """select sec_to_time(avg(time_to_sec(tmp_banho))) from (
                  select tmp_banho from tb_banho order by num_banho DESC limit 14
                  ) as sub
               """

    cursor.execute(sql_time)
    tb_media = cursor.fetchall()

    cursor.close()
    close_connection(connection)

    media = tb_media[0][0]
    media_str = str(media)[2:7]
    # ^^^ transforma o tempo em string -> (0:00:00.0000) e filtra para tetirar o 0 das horas e milésimos -> (00:00)
    # ##################################################################################################################

    return f"Média: {media_str}"


def cal_media_txt():
    # Metodo Bloco de notas ############################################################################################
    lista_tempo = []
    qtt_registros = 0

    with open("registro_backup.txt", 'r') as registro:
        for linha in registro:                   # [000]*[mm:ss]--[dd/mm/yy]
            if linha[0:5] != "[000]":            # verificação para ignorar o primeiro registro de exemplo
                lista_tempo.append(linha[7:12])  # adciona a lista de tempos o tempo (mm:ss)
                qtt_registros = int(linha[1:4])  # salva o numero do ultimo registro que a o mesmo da quantidade (000)

    soma_tempos = timedelta(seconds=0)  # cria uma variavel to tipo timedelta para fazer a soma dos tempo
    # 00:00:00.0000

    # ["06:27", "09:07","08:10"]

    # ["06", "27"]

    for tempo in lista_tempo:             # inicia um for para cada tempo na lista de tempos
        tempo_in_list = tempo.split(':')  # separa o tempo em uma lista de duas posições lista = ['mm','ss']
        minuto = int(tempo_in_list[0])    # pega o minuto do tempo
        segundos = int(tempo_in_list[1])  # pega o segundo do tempo
        tempo_time = timedelta(minutes=minuto, seconds=segundos)
        # ^^^ cria um variel do tipo timedelta usando o minuto e segundo do tempo para fazer a soma dos tempos

        soma_tempos += tempo_time  # soma todos os tempo

    media = soma_tempos / qtt_registros  # faz a media dos tempos
    media_str = str(media)[2:7]
    # ^^^ transforma o tempo em string -> (0:00:00.0000) e filtra para tetirar o 0 das horas e milésimos -> (00:00)
    # ##################################################################################################################

    return f"Média: {media_str}"


def mostrar_registros(mode=1):

    while True:
        os.system('cls')

        print("\n===== Tabelas de Registros =====")

        select_auto(mode)  # Mostrar os registros

        print("==== Menu ======================")
        print("| 1 | - Atualizar")
        print("| 0 | - Menu")
        print("|-1 | - Troca o modo de exibição")

        opc_num = input(" > ")

        if opc_num == "1":
            pass
        elif opc_num == "0":
            break
        elif opc_num == "-1" and mode == 1:
            mode = -1
        elif opc_num == "-1" and mode == -1:
            mode = 1
        else:
            print("Opção Invalida")


def editar_registro():
    # [ V ] - Editar no Banco de Dados
    # [ V ] - Editar no Arquivo de Backup

    alerta = ''
    erro = ''
    mode = -1   # [ -1 ] - Mostrar ultimos 10 registros
    #           # [  1 ] - Mostra todos os registros

    while True:
        os.system('cls')

        # Menu ######################################################

        print("\n====== Edição de registro ======")
        print("=== 0  - Voltar para o Menu")
        print("=== -1 - Troca o modo de exibição")

        select_auto(mode)  # Mostrar os registros

        # Printa um alerta caso tenha
        print(f"[{alerta.center(20)}]")
        alerta = ''  # Reseta o Alerta

        # Printa um erro caso ocorra
        print(f"{erro}\n"
              if erro != ''
              else '')
        erro = ''  # Reseta o Erro

        print("Qual Regsitro deseja editar ? (Idt)")
        # ###########################################################
        v_idt = input(" > ")
        # ^^^ pede um valor inteiro, mas caso o usuario coloque algo diferente, alerta o problema

        last_idt = get_last_idt()  # Lê a Identificação do ultimo registro

        if v_idt == "0":  # 0 para sair
            break
        elif v_idt == "-1" and mode == -1:  # Trocar o modo de exibição
            mode = 1
        elif v_idt == "-1" and mode == 1:   # Trocar o modo de exibição
            mode = -1

        elif 0 < int(v_idt) <= last_idt:  # Verifica se o valor do input é valido
            print("[1] - Tempo <| OU |> [2] - Data")
            opc = input(" > ")
            connection = open_connection()
            cursor = connection.cursor()
            tempo = ''
            data = ''
            try:  # Para tratar os erros dos inputs de data e tempo

                # Editar do  Banco de Dados ===============================
                if opc == "1":
                    print("Tempo formato [00:00]")
                    tempo = input(" > ")

                    if banco_dados:
                        v_tempo = f"0:{tempo}"  # Formata o input para ser valido no banco de dados

                        sql_update = "call update_tempo_tb_banho(%s,%s)"

                        registro = (v_tempo, v_idt)
                        cursor.execute(sql_update, registro)
                        connection.commit()

                elif opc == "2":
                    print("Data formato [dd/mm/yyyy]")
                    data = input(" > ")

                    if banco_dados:
                        v_data = data.split('/')  # Separa o input para formatar
                        dia = int(v_data[0])
                        mes = int(v_data[1])
                        ano = int(v_data[2])
                        v_data = f"{ano}/{mes:02d}/{dia:02d}"  # Formata o input para ser valido no banco de dados

                        sql_update = "call update_data_tb_banho(%s,%s)"

                        registro = (v_data, v_idt)
                        cursor.execute(sql_update, registro)
                        connection.commit()

                else:
                    alerta = "!Opção Invalido!"
                # =========================================================
            except Error as erro_exe:
                alerta = "Erro"
                erro = erro_exe  # passa o erro para o menu

            else:
                with open('registro_backup.txt', 'r+') as arq_registro:
                    linha_zero = arq_registro.readline()  # [000]*[mm:ss]--[dd/mm/yy]
                    seek = int(v_idt) * (len(linha_zero) + 1)  # Cacula a posisão do registro

                    arq_registro.seek(seek)  # Coloca o cursor no registro escolhido
                    linha = arq_registro.readline()  # Captura a linha
                    arq_registro.seek(seek)  # Volta o cursor para a posição desejada

                    banho = extrair_dados(linha)  # extrai os dados da linha e cria um obj da classe Banho

                    if opc == "1":
                        # 00:00
                        tempo = tempo.split(':')  # separa o valores
                        banho.minuto = int(tempo[0])  # set o minuto
                        banho.segundo = int(tempo[1])  # set o segundo

                        # print(banho)

                        arq_registro.write(banho.registro(True))  # Atualiza no arquivo TXT

                    elif opc == "2":
                        # dd/mm/yyyy
                        v_data = data.split('/')  # separa o valores
                        dia = int(v_data[0])
                        mes = int(v_data[1])
                        ano = v_data[2]
                        v_data = f"{dia:02d}/{mes:02d}/{ano[2:]}"  # Formata o input para ser valido no TXT

                        banho.data = v_data  # set a data

                        # print(banho)

                        arq_registro.write(banho.registro(True))  # Atualiza no arquivo TXT

                    else:
                        alerta = "!Opção Invalido!"

                # =========================================================

            finally:
                cursor.close()
                close_connection(connection)

        else:
            alerta = "!Registro Invalido!"
        # ##############################################################


def deletar_registro():
    # [ V ] - Deletar do Banco de Dados
    # [ V ] - Deletar do Arquivo de Backup

    alerta = ''
    erro = ''
    while True:
        os.system('cls')

        # Menu ######################################################
        print("\n======= Deletar registro =======")
        print("=== 0 - Voltar para o Menu")

        # Mostrar ultimos 10 registros
        select_auto(-1)

        # Printa um alerta caso tenha
        print(f"[{alerta.center(20)}]")
        alerta = ''

        # Printa um erro caso ocorra
        print(f"{erro}\n"
              if erro != ''
              else '')
        erro = ''

        print("Qual Regsitro deseja deletar ? (Idt)")
        # ###########################################################

        try:
            v_idt = int(input(" > "))
            # ^^^ pede um valor inteiro, mas caso o usuario coloque algo diferente, alerta o problema
        except ValueError:
            alerta = "!Registro Invalido!"
        else:
            last_idt = get_last_idt()

            if v_idt == 0:  # 0 para sair
                break
            elif v_idt < 0 or v_idt > last_idt:  # Verifica se o valor do input é valido
                alerta = "!Registro Invalido!"
            else:
                connection = open_connection()
                cursor = connection.cursor()
                try:
                    # Deletar do  Banco de Dados ==============================
                    if banco_dados:
                        sql_del = "call delete_tb_banho(%s)"
                        cursor.execute(sql_del, [v_idt])
                        connection.commit()

                        if v_idt == last_idt:
                            last_idt = get_last_idt() + 1
                            sql_auto_increment = "alter table tb_banho auto_increment = %s"
                            cursor.execute(sql_auto_increment, [last_idt])
                            connection.commit()
                    # =========================================================
                except Error as erro_exe:
                    alerta = "Erro"
                    erro = erro_exe
                else:

                    alerta = deletar_do_txt(v_idt)

                    # =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
                finally:
                    cursor.close()
                    close_connection(connection)


def menu(alerta):  # Função menu

    os.system('cls')  # Limpa o terminal

    # Alerta
    texto = alerta.center(20)  # Centraliza o alerta
    print(f"\n[  {texto}  ]")  # Printa o alerta
    #      [                        ]
    print(" ========= Menu =========  ")
    print("| 1 | - Registrar")
    print("| 2 | - Calcular Média")
    print("| 3 | - Mostrar Registros")
    print("| 4 | - Editar Registros")
    print("| 5 | - Deletar Registro")
    print("| 0 | - Fechar")

    opc = input(" > ")  # Opção do usuario
    return opc


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# + GRAFICOS E TABELAS -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


def grafico():
    connection = open_connection()

    if connection:
        cursor = connection.cursor()

        sql_select = ''  # [-1 ] - lista inversa com os ultimos 10 registros

        sql_select = "call select_sep_tb_banho();"

        cursor.execute(sql_select)
        registro = cursor.fetchall()

        lista_tempos = []
        lista_dias = []

        for idt, minutos, segundos, dia, mes, ano in registro:
            # print(f"[{idt:3d}] - {minutos:02d}:{segundos:02d} | {dia:02d}/{mes:02d}/{ano}")
            # segundo += minuto*60
            # print(segundo)

            # time(0, minutos, segundos)
            tempo_sec = (minutos * 60) + segundos

            lista_tempos.append(tempo_sec)
            lista_dias.append(datetime.date(ano, mes, dia))

        # grafico #####################
        plt.plot(lista_dias, lista_tempos, linewidth=0.5)




        plt.ylabel("Tempo em Segundos")




        plt.xlabel("Dias")

        lista_labels_dias = []
        for dia in lista_dias:
            lista_labels_dias.append(f"{dia.month:02d}/{dia.day:02d}")

        plt.xticks(lista_dias, lista_labels_dias, rotation=90)

        plt.axis([lista_dias[0], lista_dias[-1], 0, 1000])
        plt.fill_between(lista_dias,lista_tempos, alpha=0.5)
        plt.show()

        connection.close()
        print("")
        print("Data Base: [Not connected]")
        print(f"Conexão: [CLOSE]")
        print("")


def tabela():  # XXXXXXXXXXXXXXXX
    connection = open_connection()

    if connection:
        cursor = connection.cursor()

        sql_select = "call select_sep_tb_banho();"

        cursor.execute(sql_select)
        registro = cursor.fetchall()

        lista_tempos_sec = []

        for idt, minutos, segundos, dia, mes, ano in registro:
            # print(f"[{idt:3d}] - {minutos:02d}:{segundos:02d} | {dia:02d}/{mes:02d}/{ano}")
            tempo_sec = (minutos * 60) + segundos

            lista_tempos_sec.append(tempo_sec)

        connection.close()
        print("")
        print("Data Base: [Not connected]")
        print(f"Conexão: [CLOSE]")
        print("")

        classe_um = 0
        classe_dois = 0
        classe_tres = 0
        classe_quatro = 0
        classe_cinco = 0
        classe_seis = 0
        classe_sete = 0
        classe_oito = 0
        classe_nove = 0
        classe_dez = 0
        classe_onze = 0

        for tempo in lista_tempos_sec:
            if 240 < tempo < 300:
                classe_um += 1
            elif 300 < tempo < 360:
                classe_dois += 1
            elif 360 < tempo < 420:
                classe_tres += 1
            elif 420 < tempo < 540:
                classe_quatro += 1
            elif 540 < tempo < 600:
                classe_cinco += 1
            elif 600 < tempo < 660:
                classe_seis += 1
            elif 660 < tempo < 720:
                classe_sete += 1
            elif 720 < tempo < 780:
                classe_oito += 1
            elif 780 < tempo < 840:
                classe_nove += 1
            elif 840 < tempo < 900:
                classe_dez += 1
            elif 900 < tempo < 960:
                classe_onze += 1

        print(f"┌────────────────┬───────┬─────┬─────┬─────┐")
        print(f"│ CLASSES        │ xj    │ fj  │ Fac │ Fad │")
        print(f"├────────────────┼───────┼─────┼─────┼─────┤")
        #       │ 00:00 ├─ 00:00 │ 00:00 │ 000 │ 000 │ 000 │
        print(f"│  4:00 ├─  5:00 │  4:30 │ {classe_um:3d} │ {fa_c_d(classe_um,0,'c')} │     │")  # classe 1
        print(f"│  5:00 ├─  6:00 │  5:30 │ {classe_dois:3d} │ {fa_c_d(classe_dois,classe_um,'c')} │     │")  # classe 2
        print(f"│  6:00 ├─  5:00 │  6:30 │ {classe_tres:3d} │ {fa_c_d(classe_um,0,'c')} │     │")  # classe 3
        print(f"│  7:00 ├─  8:00 │  7:30 │ {classe_quatro:3d} │ {fa_c_d(classe_um,0,'c')} │     │")  # classe 4
        print(f"│  8:00 ├─  9:00 │  8:30 │ {classe_cinco:3d} │ {fa_c_d(classe_um,0,'c')} │     │")  # classe 5
        print(f"│  9:00 ├─ 10:00 │  9:30 │ {classe_seis:3d} │ {fa_c_d(classe_um,0,'c')} │     │")  # classe 6
        print(f"│ 10:00 ├─ 11:00 │ 10:30 │ {classe_sete:3d} │ {fa_c_d(classe_um,0,'c')} │     │")  # classe 7
        print(f"│ 11:00 ├─ 12:00 │ 11:30 │ {classe_oito:3d} │ {fa_c_d(classe_um,0,'c')} │     │")  # classe 8
        print(f"│ 12:00 ├─ 13:00 │ 12:30 │ {classe_nove:3d} │ {fa_c_d(classe_um,0,'c')} │     │")  # classe 9
        print(f"│ 13:00 ├─ 14:00 │ 13:30 │ {classe_dez:3d} │ {fa_c_d(classe_um,0,'c')} │     │")  # classe 10
        print(f"│ 14:00 ├─ 15:00 │ 14:30 │ {classe_onze:3d} │ {fa_c_d(classe_um,0,'c')} │     │")  # classe 11
        #       │ 00:00 ├─ 00:00 │ 00:00 │ 000 │ 000 │ 000 │
        print(f"└────────────────┴───────┴─────┴─────┴─────┘")


def fa_c_d(classe_a, classe_ant, modo):
    if modo == 'c':
        return classe_a + classe_ant
    if modo == 'd':
        return 0



"""
┌─┬─┐
│ │ │
├─┼─┤
│ │ │
└─┴─┘
"""
if __name__ == '__main__':
    tabela()









