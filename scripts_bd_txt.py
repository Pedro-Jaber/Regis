"""
PEDRO HENRIQUE JABER CAVALCANTE
16/05/2022
"""
from mysql.connector import connect, Error
import class_banho as cb
#
#
from dotenv.main import load_dotenv
import os

load_dotenv()
user_conn = os.environ['USERCONN']
password_conn = os.environ['PASSWCONN']
host_conn = os.environ['HOSTCONN']
database_conn = os.environ['DBCONN']


def gerar_txt(nome_do_bd=database_conn, senha_bd=password_conn):
    try:
        connection = connect(user=user_conn,
                             password=senha_bd,
                             host=host_conn,
                             database=nome_do_bd
                             )

    except Error as erro:
        print("")
        print("Data Base: [Not connected]")
        print("Erro na conexão.\n", erro)
        print("")

    else:
        print("")
        print("Data Base: [Connected]")
        print(f"Conexão: {connection}")
        print("")

        cursor = connection.cursor()

        sql_select = "call select_sep_tb_banho();"

        cursor.execute(sql_select)
        registro = cursor.fetchall()

        with open('registro_backup.txt', 'w') as arquivo:
            linha_zero = "[000]*[mm:ss]--[dd/mm/yy]"
            arquivo.write(linha_zero)
            for idt, minuto, segundo, dia, mes, ano in registro:
                banho = cb.extrair_dados_bd(idt, minuto, segundo, dia, mes, ano)
                print(banho)
                arquivo.write(banho.registro())

        cursor.close()
        connection.close()
        print("")
        print("Data Base: [Not connected]")
        print(f"Conexão: [CLOSE]")
        print("")


if __name__ == '__main__':
    # nome_do_bd_main = input("Nome do banco de dados > ")
    # senha_bd_main = input("Senha do Mysql > ")
    nome_do_bd_main = ''  # db_registros_banho_test
    senha_bd_main = ''
    gerar_txt()
