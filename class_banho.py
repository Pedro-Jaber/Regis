"""
PEDRO HENRIQUE JABER CAVALCANTE
16/05/2022
"""
from datetime import date


class Banho:

    def __init__(self, minuto, segundo, idt=0, data=''):

        self.minuto = minuto
        self.segundo = segundo

        if idt == 0:
            idt = definir_id()
        if data == '':
            data = gerar_data()

        self.idt = idt
        self.data = data

    def __str__(self):
        return f"[{self.idt:03d}]*[{self.minuto:02d}:{self.segundo:02d}]--[{self.data}]"

    @property
    def idt(self):
        return self._idt

    @idt.setter
    def idt(self, v_idt):
        if isinstance(v_idt, int) and v_idt < 1000:
            self._idt = v_idt

    @property
    def minuto(self):
        return self._minuto

    @minuto.setter
    def minuto(self, v_minuto):
        if isinstance(v_minuto, int) and v_minuto < 60:
            self._minuto = v_minuto

    @property
    def segundo(self):
        return self._segundo

    @segundo.setter
    def segundo(self, v_segundo):
        if isinstance(v_segundo, int) and v_segundo < 60:
            self._segundo = v_segundo

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, v_data):
        if isinstance(v_data, str):
            self._data = v_data

    def registro(self, update=False):  # Retorna o registro formatado
        if not update:
            return f"\n[{self.idt:03d}]*[{self.minuto:02d}:{self.segundo:02d}]--[{self.data}]"
            # \n[000]*[mm:ss]--[dd/mm/yy]
        elif update:
            return f"[{self.idt:03d}]*[{self.minuto:02d}:{self.segundo:02d}]--[{self.data}]"
            # [000]*[mm:ss]--[dd/mm/yy]


def gerar_data():  # função para gerar a data do Banho
    data = date.today()
    data_str = data.strftime("%d/%m/%y")
    return data_str


def definir_id():  # função para gerar o ID do Banho
    """
    # OLD
    ident = 0
    with open("registro_backup.txt", 'r') as registro:
        for linha in registro:
            ident += 1
    """

    linha = ''  # Cria uma linha vazia
    with open("registro_backup.txt", 'r') as registro:
        for x in registro:  # Ler linha por linha, finaliza com a ultima linha no registro
            linha = x
            # print(linha,end='')
    # print(f"\nLinha final:\n{linha}")

    ident = int(linha[1:4])  # Corta a string para pegar o numero do ID
    ident += 1  # Soma 1 ao ID para fazer o ID do regsitro
    # print(ident)

    # self.set_id(ident)
    return ident  # retorna o ID


def extrair_dados(v_linha):
    #     [000]*[mm:ss]--[dd/mm/yy]
    # 0   0123456789  |  |  |  |  |
    # 1             0123456789 |  |
    # 2                       01234
    idt = int(v_linha[1:4])
    minuto = int(v_linha[7:9])
    segundo = int(v_linha[10:12])
    dia = int(v_linha[16:18])
    mes = int(v_linha[19:21])
    ano = int(v_linha[22:24])
    data = f"{dia:02d}/{mes:02d}/{ano:02d}"  # %d/%m/%y

    # print(minuto)
    # print(segundo)
    # print(idt)
    # print(data)

    return Banho(minuto, segundo, idt, data)


def extrair_dados_bd(idt, minuto, segundo, dia, mes, ano):
    #     [000]*[mm:ss]--[dd/mm/yy]

    data = f"{dia:02d}/{mes:02d}/{str(ano)[2:]}"  # %d/%m/%y

    # print(minuto)
    # print(segundo)
    # print(idt)
    # print(data)

    return Banho(minuto, segundo, idt, data)
