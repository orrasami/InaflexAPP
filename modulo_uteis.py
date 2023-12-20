# 1.6 UTEIS
from janelas.janela_uteis import Ui_uteis
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
from modulo_demanda import Demanda
from modulo_select import Select
from modulo_pdf import PdfMerger
from modulo_analise_necessidade import AnaliseNecessidade
from modulo_inspecao_final import Inspecao
from modulo_estudo_demanda import EstudoDemanda
from modulo_estudo_pedido import EstudoPedido


class Uteis(QMainWindow, Ui_uteis):
    def __init__(self, widget_uteis, bd_oracle_ok, desenvolvimento, nome_usuario, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.nome_usuario = nome_usuario
        self.btnDemanda.clicked.connect(self.abrir_demanda)
        self.btnPdf.clicked.connect(self.abrir_pdf)
        self.btnSelect.clicked.connect(self.select)
        self.btnInspecao.clicked.connect(self.inspecao)
        self.btnAnaliseOps.clicked.connect(self.analise_necessidade)
        self.btnEstudoDemanda.clicked.connect(self.estudo_demanda)
        self.btnEstudoPedido.clicked.connect(self.estudo_pedido)
        self.btnSelect.show()

        # Janela PDF
        self.widget_pdf = QtWidgets.QStackedWidget()
        self.janela_pdf = PdfMerger(self.widget_pdf)
        self.widget_pdf.addWidget(self.janela_pdf)
        self.widget_pdf.setFixedSize(748, 555)

        # Janela Demanda
        self.widget_demanda = QtWidgets.QStackedWidget()
        self.janela_demanda = Demanda(self.widget_demanda, bd_oracle_ok)
        self.widget_demanda.addWidget(self.janela_demanda)
        self.widget_demanda.setFixedSize(569, 420)

        # Janela Select
        self.widget_select = QtWidgets.QStackedWidget()
        self.janela_select = Select(self.widget_select, bd_oracle_ok, nome_usuario)
        self.widget_select.addWidget(self.janela_select)
        self.widget_select.setFixedSize(457, 334)

        # Janela Analise de Necessidade
        self.widget_analise_necessidade = QtWidgets.QStackedWidget()
        self.janela_analise_necessidade = AnaliseNecessidade(self.widget_analise_necessidade, bd_oracle_ok)
        self.widget_analise_necessidade.addWidget(self.janela_analise_necessidade)
        self.widget_analise_necessidade.setFixedSize(605, 649)

        # Janela Relatorios Inspeção Final
        self.widget_inspecao_final = QtWidgets.QStackedWidget()
        self.janela_inspecao_final = Inspecao(self.widget_inspecao_final, bd_oracle_ok)
        self.widget_inspecao_final.addWidget(self.janela_inspecao_final)
        self.widget_inspecao_final.setFixedSize(569, 413)

        # Janela Estudo Demanda
        self.widget_estudo_demanda = QtWidgets.QStackedWidget()
        self.janela_estudo_demanda = EstudoDemanda(self.widget_estudo_demanda)
        self.widget_estudo_demanda.addWidget(self.janela_estudo_demanda)
        self.widget_estudo_demanda.setFixedSize(400, 210)

        # Janela Estudo Pedido
        self.widget_estudo_pedido = QtWidgets.QStackedWidget()
        self.janela_estudo_pedido = EstudoPedido(self.widget_estudo_pedido)
        self.widget_estudo_pedido.addWidget(self.janela_estudo_pedido)
        self.widget_estudo_pedido.setFixedSize(400, 156)

    def abrir_demanda(self):
        self.widget_demanda.show()

    def abrir_pdf(self):
        self.widget_pdf.show()

    def select(self):
        self.widget_select.show()

    def analise_necessidade(self):
        self.widget_analise_necessidade.show()

    def inspecao(self):
        self.widget_inspecao_final.show()

    def estudo_demanda(self):
        self.widget_estudo_demanda.show()

    def estudo_pedido(self):
        self.widget_estudo_pedido.show()
