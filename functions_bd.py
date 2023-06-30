"""
PEDRO HENRIQUE JABER CAVALCANTE
22107003
24/06/2022
"""
from mysql.connector import connect, Error
from dotenv.main import load_dotenv
import os

load_dotenv()
user_conn = os.environ['USERCONN']
password_conn = os.environ['PASSWCONN']
host_conn = os.environ['HOSTCONN']
database_conn = os.environ['DBCONN']

"""
call insert_tb_banho('0:00:00','yyyy-mm-dd' );  # Registrar valor 
call select_tb_banho();                         # Selecionar valores
call select_sep_tb_banho()                      # Selecionar valores separados
call delete_tb_banho(0);                        # Deletar valor
     alter table tb_banho auto_increment = 1;   # resetar auto_increment
"""


def open_connection(mode=0):  # Faz conexão ao BD
    try:
        connection = connect(user=user_conn,
                             password=password_conn,
                             host=host_conn,
                             database=database_conn
                             )

    except Error as erro:
        print("")
        print("Data Base: [Not connected]")
        print("Erro na conexão.\n", erro)
        print("")
        return False

    else:
        if mode == 1:
            print("")
            print("Data Base: [Connected]")
            print(f"Conexão: {connection}")
            print("")
        return connection


def close_connection(connection, mode=0):  # Fecha a conexão com o BD
    connection.close()
    if mode == 1:
        print("")
        print("Data Base: [Not connected]")
        print(f"Conexão: [CLOSE]")
        print("")


def insert_banhos(cursor, tempo, data):
    b_erro = True
    try:
        sql_insert = """call insert_tb_banho(%s, %s);"""
        regsitro = (tempo, data)

        cursor.execute(sql_insert, regsitro)
    except Error as erro:
        print("")
        print("Erro nos parametros.\n", erro)
        print("")
    else:
        b_erro = False

    return b_erro


def select_banhos(cursor, mode=1):  # [ 1 ] - lista normal com todos os registros
    sql_select = ''                 # [-1 ] - lista inversa com os ultimos 10 registros
    if mode == 1:
        sql_select = "call select_100_tb_banho()"
    elif mode == -1:
        sql_select = "call select_10_tb_banho()"
    elif mode == 0:
        sql_select = "call select_sep_tb_banho()"
    else:
        print("Modo invalido")

    if mode == 1 or mode == -1 or mode == 0:
        cursor.execute(sql_select)
        registro = cursor.fetchall()

        print(f"┌─────┬───────┬────────────────┐")
        print(f"│Idt: │Tempo: │Data Registro:  │")
        print(f"├─────┼───────┼────────────────┤")
        #       │ 000 │ mm:ss │   dd/mm/yyyy   │
        for idt, minutos, segundos, dia, mes, ano in registro:
            print(
                f"│ {idt:03d} │ {minutos:02d}:{segundos:02d} │   {dia:02d}/{mes:02d}/{ano:4d}   │")
        #       │ 000 │ mm:ss │   dd/mm/yyyy   │
        print(f"└─────┴───────┴────────────────┘")


# ======================================================================================================================
# ======================================================================================================================


def main():
    connection = open_connection()
    cursor = connection.cursor()
    select_banhos(cursor)
    close_connection(cursor)
    cursor.close()


if __name__ == '__main__':
    main()
