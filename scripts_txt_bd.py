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


def criar_bd(nome_do_bd=database_conn, senha_bd=password_conn):

    print("Criando banco de dados...")  # ##############################################################################

    try:
        connection = connect(user=user_conn,
                             password=senha_bd,
                             host=host_conn
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

        sql = f"CREATE DATABASE if not exists {nome_do_bd}"

        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()

    print("[Banco de dados criado]")  # ################################################################################

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

        print("Criado Tabela...")  # ###################################################################################

        sql_table_tb_banho = """create table tb_banho
                                (
                                num_banho int auto_increment primary key,
                                tmp_banho time not null,
                                dt_banho date not null
                                );
                                """
        cursor.execute(sql_table_tb_banho)
        connection.commit()

        print("[Tabela criada]")  # ####################################################################################

        print("Criado Stored Procedures...")  # ########################################################################
        sp_ctt = 0  # contador das Stored Procedures
        sp_total = 9  # total de Stored Procedures

        # Insert
        sql_sp_insert_tb_banho = """CREATE DEFINER=`root`@`localhost`
                                    PROCEDURE `insert_tb_banho`(in vtmp_banho time, vdt_banho date)
                                    BEGIN
                                    insert into tb_banho
                                    (tmp_banho,dt_banho)
                                    values
                                    (vtmp_banho,vdt_banho);
                                    END
                                    """
        cursor.execute(sql_sp_insert_tb_banho)
        sp_ctt += 1
        print(f"[{sp_ctt}/{sp_total}]")

        # Select
        sql_sp_select_10_tb_banho = """CREATE DEFINER=`root`@`localhost` PROCEDURE `select_10_tb_banho`()
                                        BEGIN
                                        select  
                                            num_banho "Numero", 
                                            min "Minutos", 
                                            sec "Segundos", 
                                            dia "Dia", 
                                            mes "Mes", 
                                            ano "Ano"
                                        from (
                                        select 
                                            num_banho, 
                                            minute(tmp_banho) as min, 
                                            second(tmp_banho) as sec, 
                                            day(dt_banho) as dia, 
                                            month(dt_banho) as mes, 
                                            year(dt_banho) as ano
                                        from tb_banho
                                        order by num_banho DESC
                                        limit 10) as aux
                                        order by num_banho;
                                        END
                                        """
        cursor.execute(sql_sp_select_10_tb_banho)
        sp_ctt += 1
        print(f"[{sp_ctt}/{sp_total}]")

        sql_sp_select_100_tb_banho = """CREATE DEFINER=`root`@`localhost` PROCEDURE `select_100_tb_banho`()
                                        BEGIN
                                        select  
                                            num_banho "Numero", 
                                            min "Minutos", 
                                            sec "Segundos", 
                                            dia "Dia", 
                                            mes "Mes", 
                                            ano "Ano"
                                        from (
                                        select 
                                            num_banho, 
                                            minute(tmp_banho) as min, 
                                            second(tmp_banho) as sec, 
                                            day(dt_banho) as dia, 
                                            month(dt_banho) as mes, 
                                            year(dt_banho) as ano
                                        from tb_banho
                                        order by num_banho DESC
                                        limit 100) as aux
                                        order by num_banho;
                                        END
                                        """
        cursor.execute(sql_sp_select_100_tb_banho)
        sp_ctt += 1
        print(f"[{sp_ctt}/{sp_total}]")

        sql_sp_select_last_tb_banho = """CREATE DEFINER=`root`@`localhost` PROCEDURE `select_last_tb_banho`()
                                            BEGIN
                                            select
                                                num_banho "Numero",
                                                minute(tmp_banho) "Minutos",
                                                second(tmp_banho) "Segundos",
                                                day(dt_banho) "Dia",
                                                month(dt_banho) "Mes",
                                                year(dt_banho) "Ano"
                                            from tb_banho
                                            order by num_banho DESC
                                            limit 1;
                                            END
                                        """
        cursor.execute(sql_sp_select_last_tb_banho)
        sp_ctt += 1
        print(f"[{sp_ctt}/{sp_total}]")

        sql_sp_select_sep_tb_banho = """CREATE DEFINER=`root`@`localhost` PROCEDURE `select_sep_tb_banho`()
                                            BEGIN
                                            select num_banho as "Numero",
                                            minute(tmp_banho) "Minutos",
                                            second(tmp_banho) "Segundo",
                                            day(dt_banho) "Dia",
                                            month(dt_banho) "Mes",
                                            year(dt_banho) "Ano"
                                            from tb_banho;
                                            END
                                            """
        cursor.execute(sql_sp_select_sep_tb_banho)
        sp_ctt += 1
        print(f"[{sp_ctt}/{sp_total}]")

        sql_sp_select_tb_banho = """CREATE DEFINER=`root`@`localhost` PROCEDURE `select_tb_banho`()
                                        BEGIN
                                        select num_banho as "Numero", tmp_banho as "Tempo", dt_banho as "Data"
                                        from tb_banho;
                                        END
                                        """
        cursor.execute(sql_sp_select_tb_banho)
        sp_ctt += 1
        print(f"[{sp_ctt}/{sp_total}]")

        # Update
        sql_sp_update_data_tb_banho = """CREATE DEFINER=`root`@`localhost`
                                    PROCEDURE `update_data_tb_banho`(in v_dt_banho date, v_num_banho int)
                                    BEGIN
                                    update tb_banho
                                    set dt_banho = v_dt_banho
                                    where num_banho = v_num_banho;
                                    END
                                    """
        cursor.execute(sql_sp_update_data_tb_banho)
        sp_ctt += 1
        print(f"[{sp_ctt}/{sp_total}]")

        sql_sp_update_tempo_tb_banho = """CREATE DEFINER=`root`@`localhost`
                                        PROCEDURE `update_tempo_tb_banho`(in v_tmp_banho time, v_num_banho int)
                                        BEGIN
                                        update tb_banho
                                        set tmp_banho = v_tmp_banho
                                        where num_banho = v_num_banho;
                                        END
                                        """
        cursor.execute(sql_sp_update_tempo_tb_banho)
        sp_ctt += 1
        print(f"[{sp_ctt}/{sp_total}]")

        # Delete
        sql_sp_delete_tb_banho = """CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_tb_banho`(in vnum_banho int)
                                            BEGIN
                                            delete from tb_banho
                                            where num_banho = vnum_banho;
                                            END
                                            """
        cursor.execute(sql_sp_delete_tb_banho)
        sp_ctt += 1
        print(f"[{sp_ctt}/{sp_total}]")

        connection.commit()
        print("[Stored Procedures criadas]")  # ########################################################################

        cursor.close()
        connection.close()
        print("")
        print("Data Base: [Not connected]")
        print(f"Conexão: [CLOSE]")
        print("")


def registrar(nome_do_bd=database_conn, senha_bd=password_conn):
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

        print("Inserindo dados nas tabelas...")  # #####################################################################

        with open('registro_backup.txt', 'r') as arquivo:

            for i, linha in enumerate(arquivo):  # [000]*[mm:ss]--[dd/mm/yy]
                if linha[1:4] != '000':
                    # print(f"[{i:02d}] - {linha}", end='')

                    banho = cb.extrair_dados(linha)

                    data = banho.data.split('/')

                    sql_registrar_banho = f"call insert_tb_banho" \
                                          f"('0:{banho.minuto:02d}:{banho.segundo:02d}', " \
                                          f"'20{data[2]}-{data[1]}-{data[0]}' )"

                    cursor.execute(sql_registrar_banho)
                    connection.commit()

        print("[Dados inserindos]")  # #################################################################################

        cursor.close()
        connection.close()
        print("")
        print("Data Base: [Not connected]")
        print(f"Conexão: [CLOSE]")
        print("")


if __name__ == '__main__':
    criar_bd()
    registrar()
