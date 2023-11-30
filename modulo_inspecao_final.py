# 2.5 RELATÓRIO INSPECAO
import webbrowser
from janelas.janela_inspecao import Ui_inspecao
from PyQt5.QtWidgets import QMainWindow, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtWidgets
from banco_de_dados_arquivos import BDArquivos


class Inspecao(QMainWindow, Ui_inspecao):
    def __init__(self, widget_relatorios, bd_oracle_ok, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.shortcut_procura = QShortcut(QKeySequence('return'), self)
        self.shortcut_procura.activated.connect(self.acao)
        self.shortcut_procura_alt = QShortcut(QKeySequence('enter'), self)
        self.shortcut_procura_alt.activated.connect(self.acao)
        self.btnListar.clicked.connect(self.acao)
        self.btnLimpar.clicked.connect(self.limpar)
        self.radioTodos.toggle()
        self.radioTodos.toggled.connect(self.atualiza_radio)
        self.radioAberto.toggled.connect(self.atualiza_radio)
        self.radioFinalizado.toggled.connect(self.atualiza_radio)
        self.tableWidget.setColumnWidth(0, 170)
        self.tableWidget.setColumnWidth(1, 170)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.doubleClicked.connect(self.selecionar_dados)
        self.finalizado = "2"

    def acao(self):
        lista = []
        pedido = self.inputPedido.text()
        lote = self.inputLote.text()
        self.finalizado
        lista = BDArquivos().listar_relatorios_inspecao_final(pedido, lote, self.finalizado)
        self.listar(lista)

    def limpar(self):
        self.inputPedido.setText("")
        self.inputLote.setText("")

    def listar(self, lista):
        row = 0
        self.tableWidget.setRowCount(len(lista))
        for item in lista:
            lote = item['lote']
            pedido = item['pedido']
            completo = item['correto']
            if item['finalizado'] == "0":
                finalizado = "NAO"
            else:
                finalizado = "SIM"
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(lote))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(pedido))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(completo))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(finalizado))
            row += 1

    def selecionar_dados(self):
        linha = self.tableWidget.currentRow()
        lote = self.tableWidget.item(linha, 0).text()
        webbrowser.open(f'http://inaflex.kinghost.net/qualidade_selecao.php?lote={lote}')

    def atualiza_radio(self):
        rbtn = self.sender()

        if rbtn.isChecked() == True:
            if rbtn.text() == "Todos":
                self.finalizado = "2"
            if rbtn.text() == "Aberto":
                self.finalizado = "0"
            if rbtn.text() == "Finalizado":
                self.finalizado = "1"
