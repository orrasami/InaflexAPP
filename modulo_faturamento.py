# 1.5 FATURAMENTO
from janelas.janela_faturamento import *
from banco_de_dados_arquivos import BDArquivos
from banco_de_dados_oracle import BDBohm
from PyQt5.QtWidgets import QMainWindow, QShortcut, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore, QtWidgets
from datetime import datetime, date
from threading import Thread


global atual
global pedido
global titulo
global indice


class Faturamento(QMainWindow, Ui_Faturamento):
    def __init__(self, bd_oracle_ok, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.criar_dropdowm()
        self.dropdownAcao.setEditable(True)
        self.dropdownAcao.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.btnSelecionarPedido.clicked.connect(self.buscar_pedido)
        self.btnAtualizarInfo.clicked.connect(self.atualizar_status)
        self.btnEnviarFaturamento.clicked.connect(self.volta_para_acabamento)
        self.btnEnviarEntregas.clicked.connect(self.enviar_para_entregas)
        delegate = AlignDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0, delegate)
        self.tableWidget.setItemDelegateForColumn(1, delegate)
        self.tableWidget.clicked.connect(self.selecionar_dados)
        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setColumnWidth(2, 170)
        self.tableWidget.setColumnWidth(3, 0)
        self.tableWidget.setColumnWidth(4, 0)
        self.tableWidget.setColumnWidth(5, 0)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.itemSelectionChanged.connect(self.selecionar_dados)
        self.inputPedido.textChanged.connect(self.apaga_valores)
        self.shortcut_procura = QShortcut(QKeySequence('return'), self)
        self.shortcut_procura.activated.connect(self.buscar_pedido)
        self.lista_faturamento(valor='NADA')
        self.labelAtualizando.hide()
        if bd_oracle_ok == 'Falha':
            self.bd_oracle_ok = True
        else:
            self.bd_oracle_ok = False
            self.atualizar_pedidos()

    def criar_dropdowm(self):
        resultados = BDArquivos().combobox_faturamento()
        self.dropdownAcao.addItem('--SELECIONAR--')
        for resultado in resultados:
            self.dropdownAcao.addItem(resultado['acao'])

    def lista_faturamento(self, valor):
        resultados = BDArquivos().mostrar_pedidos_faturamento_db(valor)
        if resultados == ():
            valor = 'NADA'
            resultados = BDArquivos().mostrar_pedidos_faturamento_db(valor)
        self.mostrar_dados(resultados, valor)

    def volta_para_acabamento(self):
        pedido = self.inputPedido.text()
        BDArquivos().volta_para_acabamento_bd(pedido)
        self.inputPedido.setText('')
        self.inputCliente.setText('')
        self.dropdownAcao.setCurrentIndex(0)
        self.textObservacao.setText('')
        self.lista_faturamento('NADA')

    def enviar_para_entregas(self):
        pedido = self.inputPedido.text()
        self.inputData.setDate(QtCore.QDate.currentDate())
        data = date.today()
        data = str(data.year) + '/' + str(data.month) + '/' + str(data.day)
        BDArquivos().enviar_para_entregas_bd(pedido, data)
        self.inputPedido.setText('')
        self.inputCliente.setText('')
        self.dropdownAcao.setCurrentIndex(0)
        self.textObservacao.setText('')
        self.lista_faturamento('NADA')

    def mostrar_dados(self, resultados, valor):
        row = 0
        self.tableWidget.setRowCount(len(resultados))
        for resultado in resultados:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(resultado['pedido']))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(resultado['acao']))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(resultado['observacao']))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(resultado['obs_faturamento']))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(resultado['cliente']))
            data = resultado['data_acabamento']
            data_acabamento = str(data.day) + '/' + str(data.month) + '/' + str(data.year)
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(data_acabamento))
            row += 1
            if valor != 'NADA':
                self.inputCliente.setText(resultado['cliente'])
                self.dropdownAcao.setCurrentText(resultado['acao'])
                self.textObservacao.setText(resultado['observacao'])

    def selecionar_dados(self):
        global pedido
        row = self.tableWidget.currentRow()
        pedido = self.tableWidget.item(row, 0).text()
        acao = self.tableWidget.item(row, 1).text()
        observacao = self.tableWidget.item(row, 2).text()
        observacao_faturamento = self.tableWidget.item(row, 3).text()
        cliente = self.tableWidget.item(row, 4).text()
        data = self.tableWidget.item(row, 5).text()
        data = data + ' 0:0:0'
        data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')

        self.inputPedido.setText(pedido)
        self.dropdownAcao.setCurrentText(acao)
        self.textObservacao.setText(observacao)
        self.textObsFaturamento.setText(observacao_faturamento)
        self.inputCliente.setText(cliente)
        self.inputData.setDate(data)

    def buscar_pedido(self, pedido_=None):
        global pedido
        pedido = self.inputPedido.text()
        if not pedido:
            pedido = pedido_
        if not pedido:
            pedido = 'NADA'
        self.lista_faturamento(pedido)

    def atualizar_status(self):
        global pedido
        pedido = self.inputPedido.text()
        responsavel = self.dropdownAcao.currentText()
        observacao = self.textObservacao.toPlainText().upper()
        if pedido and responsavel and observacao:
            BDArquivos().salva_dados_faturamento(pedido, responsavel, observacao)
            self.inputPedido.setText('')
            self.inputCliente.setText('')
            self.dropdownAcao.setCurrentIndex(0)
            self.textObservacao.setText('')
            self.textObsFaturamento.setText('')
            self.inputData.setDate(QtCore.QDate.currentDate())
            self.lista_faturamento('NADA')
        else:
            QMessageBox.about(self, "Erro", "Preencher todos os campos")

    def apaga_valores(self):
        self.inputCliente.setText('')
        self.dropdownAcao.setCurrentIndex(0)
        self.textObservacao.setText('')
        self.textObsFaturamento.setText('')
        self.inputData.setDate(QtCore.QDate.currentDate())

    def atualizar_pedidos(self):
        daemon = Thread(target=self.atualizar_dados, args=())
        daemon.daemon = True
        daemon.start()

    def atualizar_dados(self):
        self.labelAtualizando.show()
        self.atualizar_faturados()
        self.labelAtualizando.hide()

    def atualizar_faturados(self):
        # PEGA TODOS ORÇAMENTOS LIQUIDADO = 1 AND FATURADO = 0
        orcamentos = BDArquivos().seleciona_orcamentos_liquidados()
        for orcamento in orcamentos:
            # PEGA DA ORACLE O NUMERO DO PEDIDO E A VALIDADE DO ORÇAMENTO SELECIONADO
            num_pedido = BDBohm().atualiza_lista_pedidos(orcamento['orcamento'])
            validade = BDBohm().ver_validade_pedido(num_pedido)
            # SE TIVER NUMERO DE PEDIDO, ATUALIZA NUMERO DE PEDIDO E VALIDADE
            # SE NAO TIVER NUMERO DE PEDIDO, ESTORNA O PEDIDO NO APP
            if num_pedido:
                BDArquivos().atualiza_numero_do_pedido(num_pedido, validade, orcamento['orcamento'])
            else:
                BDArquivos().estorna_orcamento(orcamento['orcamento'])
        self.buscar_pedido('')


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
