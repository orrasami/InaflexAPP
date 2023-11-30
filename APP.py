# pyinstaller --onefile --noconsole --icon="static\favicon.ico" APP.py
from aux_login import log_in
import pymysql.cursors
from janelas.janela_inicio import *
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import json
from modulo_arquivos_orcamentos import Pedidos, JanelaCliente, JanelaArquivos
from modulo_faturamento import Faturamento
from modulo_workflow import Workflow
from modulo_relatorios import Relatorios
from modulo_uteis import Uteis
from modulo_entregas import Entregas
import cx_Oracle
from modulo_background import Background
from modulo_acabamento import Acabamento

global logado
global direito
global bd_oracle_ok
global bd_workflow_ok
global bd_arquivos_ok


class AppPrincipal(QMainWindow, Ui_SII):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnPedidos.clicked.connect(self.abrir_inaflex_pedidos)
        self.btnAcabamento.clicked.connect(self.abrir_acabamento)
        self.btnFaturamento.clicked.connect(self.abrir_faturamento)
        self.btnWorkflow.clicked.connect(self.abrir_workflow)
        self.btnRelatorios.clicked.connect(self.abrir_relatorios)
        self.btnUteis.clicked.connect(self.abrir_uteis)
        self.btnEntregas.clicked.connect(self.abrir_entregas)

    @staticmethod
    def abrir_acabamento():
        widget_acabamento.show()

    @staticmethod
    def abrir_faturamento():
        widget_faturamento.show()

    @staticmethod
    def abrir_inaflex_pedidos():
        widget_pedidos.show()

    @staticmethod
    def abrir_workflow():
        widget_workflow.show()

    @staticmethod
    def abrir_relatorios():
        widget_relatorios.show()

    @staticmethod
    def abrir_uteis():
        widget_uteis.show()

    @staticmethod
    def abrir_entregas():
        widget_entregas.show()


if __name__ == "__main__":
    qt = QApplication(sys.argv)

    bd_worflow_ok = ''
    bd_worflow = pymysql.connect(
            host='mysql.inaflex-app.kinghost.net',
            user='inaflexapp',
            password='zt4cr3',
            db='inaflexapp',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    cursor = bd_worflow.cursor()
    try:
        cursor.execute("SELECT VERSION()")
        results = cursor.fetchone()
        ver = results['VERSION()']
        if ver is None:
            bd_worflow_ok = 'Falha'
        else:
            bd_worflow_ok = 'OK'
    except:
        pass

    bd_arquivos_ok = ''
    bd_arquivos = pymysql.connect(
            host='mysql.inaflex-app.kinghost.net',
            user='inaflexapp',
            password='zt4cr3',
            db='inaflexapp',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    cursor = bd_arquivos.cursor()
    try:
        cursor.execute("SELECT VERSION()")
        results = cursor.fetchone()
        ver = results['VERSION()']
        if ver is None:
            bd_arquivos_ok = 'Falha'
        else:
            bd_arquivos_ok = 'OK'
    except:
        pass

    bd_oracle_ok = ''
    path_oracle_client = ''
    with open('setup.json', 'r') as file:
        d1_json = file.read()
        d1_json = json.loads(d1_json)

    for x, y in d1_json.items():
        path_oracle_client = y['oracle_client']
    try:
        cx_Oracle.init_oracle_client(lib_dir=path_oracle_client)
    except:
        bd_oracle_ok = 'Falha'
    try:
        bd_oracle = cx_Oracle.connect('CONSULTA/INAFLEX@INAFLEX')
        bd_oracle_ok = 'OK'
    except:
        bd_oracle_ok = 'Falha'
    try:
        conexao = bd_oracle.cursor()
        bd_oracle_ok = 'OK'
    except:
        bd_oracle_ok = 'Falha'

    # ACERTAR ISSO PARA MODO DESENVOLVIMENTO. ELE VAI LOGAR COM O nome-usuario QUE ESTIVER AI
    desenvolvimento = False
    nome_usuario = 'SAMI'

    if not desenvolvimento:
        resultado_login, logado = log_in(bd_worflow_ok, bd_arquivos_ok, bd_oracle_ok)
        try:
            direito = resultado_login['direito']
            usuario = resultado_login['id']
            nome_usuario = resultado_login['nomeUsuario']
            if not logado:
                exit()
        except:
            exit()
    else:
        resultado_login = {'ativo': b'\x01', 'direito': '1', 'email': 'sami@inaflex.com.br', 'email_responsavel': '0',
                           'id': 1, 'orcamentista': '0', 'senhaUsuario': '0048', 'nomeUsuario': nome_usuario}
        direito = resultado_login['direito']
        usuario = resultado_login['id']
        nome_usuario = resultado_login['nomeUsuario']
        logado = True
        bd_worflow_ok = 'OK'
        bd_arquivos_ok = 'OK'
        bd_oracle_ok = 'OK'

    if nome_usuario == 'SAMI':
        desenvolvimento = True
        Background(bd_oracle_ok)
    else:
        desenvolvimento = False

    # Janelas Arquivos Orçamentos
    widget_pedidos = QtWidgets.QStackedWidget()
    janela_cliente = JanelaCliente(widget_pedidos, direito, bd_oracle_ok)
    janela_arquivo = JanelaArquivos(widget_pedidos)
    janela_pedidos = Pedidos(widget_pedidos, janela_cliente, janela_arquivo, direito)
    widget_pedidos.addWidget(janela_pedidos)
    widget_pedidos.addWidget(janela_cliente)
    widget_pedidos.addWidget(janela_arquivo)
    widget_pedidos.setFixedSize(722, 479)

    # Janela Acabamento
    widget_acabamento = QtWidgets.QStackedWidget()
    janela_acabamento = Acabamento(bd_oracle_ok)
    widget_acabamento.addWidget(janela_acabamento)
    widget_acabamento.setFixedSize(795, 574)

    # Janela Faturamento
    widget_faturamento = QtWidgets.QStackedWidget()
    janela_faturamento = Faturamento(bd_oracle_ok)
    widget_faturamento.addWidget(janela_faturamento)
    widget_faturamento.setFixedSize(790, 670)

    # Janela Workflow
    widget_workflow = QtWidgets.QStackedWidget()
    janela_workflow = Workflow(widget_workflow, resultado_login)
    widget_workflow.addWidget(janela_workflow)
    widget_workflow.setFixedSize(1064, 676)

    # Janela Relatorios
    widget_relatorios = QtWidgets.QStackedWidget()
    janela_relatorios = Relatorios(widget_relatorios, bd_oracle_ok)
    widget_relatorios.addWidget(janela_relatorios)
    widget_relatorios.setFixedSize(399, 317)

    # Janela Uteis
    widget_uteis = QtWidgets.QStackedWidget()
    janela_uteis = Uteis(widget_uteis, bd_oracle_ok, desenvolvimento, nome_usuario)
    widget_uteis.addWidget(janela_uteis)
    widget_uteis.setFixedSize(406, 258)

    # Janela Entregas
    widget_entregas = QtWidgets.QStackedWidget()
    janela_entregas = Entregas(bd_oracle_ok)
    widget_entregas.addWidget(janela_entregas)
    widget_entregas.setFixedSize(790, 381)

    # Janela Inicial
    widget_inicio = QtWidgets.QStackedWidget()
    janela_inicio = AppPrincipal()
    widget_inicio.addWidget(janela_inicio)

    widget_inicio.setFixedSize(406, 336)
    widget_inicio.show()

    qt.exec()
