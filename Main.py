"""
PEDRO HENRIQUE JABER CAVALCANTE
16/05/2022
"""
import scripts_bd_txt
import scripts_txt_bd
from functions_code import *


def main():  # Main
    alerta = ''
    while True:
        opc = menu(alerta)
        alerta = ''

        # Menu #############################
        if opc == '1':
            alerta = criar_registro()
        elif opc == '2':
            alerta = cal_media_bd()  # Calcula a média de tempo usando o banco de dados
        elif opc == '3':
            mostrar_registros()
        elif opc == '4':
            editar_registro()
        elif opc == '5':
            deletar_registro()
        elif opc == '0':
            break
        # ##################################

        # Graficos e estatisticas ##########
        elif opc == '-10':
            grafico()   # Gerar grafico
        elif opc == '-11':
            tabela()   # Gerar tabela

        # ##################################

        # Extras ###########################
        elif opc == '-2':
            alerta = cal_media_txt()  # Calcula a média de tempo usando arquivo_backup.txt
        elif opc == '-3':
            mostrar_registros(mode=0)
        elif opc == '-14':
            alerta = cal_media_bd_14()  # Calcula a média de tempo usando os ultimos 14 registros do banco de dados
        elif opc == '123':
            scripts_txt_bd.criar_bd()  # Cria o banco de dados e tabelas
        elif opc == '456':
            scripts_txt_bd.registrar()  # Insere os dados no banco de dados
        elif opc == '789':
            scripts_bd_txt.gerar_txt()  # Cria um arquivo TXT usando os dados do banco de dados

        # ##################################

        else:
            alerta = "Opção Invalida"


if __name__ == '__main__':
    main()  # Inicia a main
