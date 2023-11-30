# 1.5 FATURAMENTO
from janelas.janela_entregas import *
from banco_de_dados_arquivos import BDArquivos
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QWidget, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore, QtWidgets
from datetime import datetime, date
from azure.storage.blob import ContainerClient
from time import gmtime, strftime
import os
import json


global atual
global pedido
global titulo
global indice


path_download = ''
with open('setup.json', 'r') as file:
    d1_json = file.read()
    d1_json = json.loads(d1_json)

for x, y in d1_json.items():
    path_download = y['download']

class Entregas(QMainWindow, Ui_Entregas):
    def __init__(self, bd_oracle_ok, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.checkClienteRetira.setChecked(False)
        self.btnSelecionarPedido.clicked.connect(self.buscar_pedido)
        self.btnAtualizarInfo.clicked.connect(self.atualizar_status)
        self.btnEnviarFaturado.clicked.connect(self.finalizar_pedido)
        self.btnEnviarFaturamento.clicked.connect(self.volta_para_faturamento)
        delegate = AlignDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0, delegate)
        self.tableWidget.setItemDelegateForColumn(1, delegate)
        self.tableWidget.clicked.connect(self.selecionar_dados)
        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setColumnWidth(2, 170)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.itemSelectionChanged.connect(self.selecionar_dados)
        self.inputPedido.textChanged.connect(self.apaga_valores)
        self.shortcut_procura = QShortcut(QKeySequence('return'), self)
        self.shortcut_procura.activated.connect(self.buscar_pedido)
        self.lista_entregas(valor='NADA')
        if bd_oracle_ok == 'Falha':
            self.bd_oracle_ok = True
        else:
            self.bd_oracle_ok = False

    def lista_entregas(self, valor):
        resultados = BDArquivos().mostrar_pedidos_entregas_db(valor)
        self.mostrar_dados(resultados, valor)

    def finalizar_pedido(self):
        global mensagem
        pedido = self.inputPedido.text()
        if pedido != '':
            if self.checkClienteRetira.isChecked():
                resposta = True
            else:
                resposta, mensagem = self.inserir_comprovante_de_entrega(pedido)
            self.checkClienteRetira.setChecked(False)
            if resposta:
                try:
                    data = date.today()
                    data = str(data.year) + "/" + str(data.month) + "/" + str(data.day)
                    BDArquivos().finalizar_db(pedido, data)
                    self.inputPedido.setText('')
                    self.inputCliente.setText('')
                    self.inputData.setDate(QtCore.QDate.currentDate())
                    self.lista_entregas('NADA')
                except:
                    mensagem = "Erro no Banco de dados"
            else:
                QMessageBox.about(self, "Erro", mensagem)
        else:
            QMessageBox.about(self, "Erro", "Pedido não selecionado")

    def volta_para_faturamento(self):
        pedido = self.inputPedido.text()
        if pedido != '':
            BDArquivos().volta_para_faturamento_bd(pedido)
            self.inputPedido.setText('')
            self.inputCliente.setText('')
            self.inputData.setDate(QtCore.QDate.currentDate())
            self.lista_entregas('NADA')
        else:
            QMessageBox.about(self, "Erro", "Pedido não selecionado")

    def mostrar_dados(self, resultados, valor):
        row = 0
        if resultados == ():
            self.tableWidget.setRowCount(0)
        else:
            self.tableWidget.setRowCount(len(resultados))
            for resultado in resultados:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(resultado['pedido']))
                data = resultado['data_entrega']
                data_entrega = str(data.day) + '/' + str(data.month) + '/' + str(data.year)
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(data_entrega))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(resultado['cliente']))
                row += 1
                if valor != 'NADA':
                    self.inputCliente.setText(resultado['cliente'])

    def selecionar_dados(self):
        global pedido
        row = self.tableWidget.currentRow()
        if row != -1:
            pedido = self.tableWidget.item(row, 0).text()
            data = self.tableWidget.item(row, 1).text()
            data = data + ' 0:0:0'
            data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            cliente = self.tableWidget.item(row, 2).text()
            self.inputPedido.setText(pedido)
            self.inputCliente.setText(cliente)
            self.inputData.setDate(data)

    def buscar_pedido(self, pedido_=None):
        global pedido
        pedido = self.inputPedido.text()
        if not pedido:
            pedido = pedido_
        if not pedido:
            pedido = 'NADA'
        self.lista_entregas(pedido)

    def atualizar_status(self):
        global pedido
        pedido = self.inputPedido.text()
        data = self.inputData.date().toPyDate()
        data = str(data.year) + "/" + str(data.month) + "/" + str(data.day)
        if pedido and data:
            BDArquivos().salva_dados_entregas(pedido, data)
            self.lista_entregas('NADA')
        else:
            QMessageBox.about(self, "Erro", "Preencher todos os campos")

    def apaga_valores(self):
        self.inputCliente.setText('')
        self.inputData.setDate(QtCore.QDate.currentDate())

    def inserir_comprovante_de_entrega(self, pedido):
        try:
            pdf = QFileDialog.getOpenFileName(
                self.centralWidget(),
                'Escolher Arquivos',
                path_download,
            )
            nome_arquivo, extensao_arquivo = os.path.splitext(pdf[0])
            extensao_arquivo = extensao_arquivo.upper()
            if extensao_arquivo == '.PDF':
                # titulo = os.path.basename(pdf[0])
                titulo = "00 - COMPROVANTE DE ENTREGA.pdf"
                orcamento, confere = BDArquivos().verificar_existe_arquivo_entrega_db(pedido, titulo)
                if confere:
                    QMessageBox.about(self, "Erro", "Arquivo ja existe!")
                    resposta = False
                    return resposta
                else:
                    acao = 'INSERIR_ARQUIVO'
                    registro = orcamento + '-' + strftime("%Y%m%d%H%M%S", gmtime())
                    registro_hd = registro + '-' + titulo
                    atual = '1'
                    indice = '0'
                    BDArquivos().inserir_arquivo_db(orcamento, indice, atual, titulo, registro)

                    connection_string = 'DefaultEndpointsProtocol=https;AccountName=inaflex;AccountK' \
                                        'ey=FCF8566/TzEdl2hHvp+2owWDZPVxfyX+MYTFX0ToDe1Nkxvg4TO1eHLp' \
                                        '2DU1EcBirNrrW4TOxl3v+AStHXst8w==;EndpointSuffix=core.windows' \
                                        '.net'
                    container_name = 'pedidos'
                    container_client = ContainerClient.from_connection_string(connection_string,
                                                                              container_name)
                    blob_client = container_client.get_blob_client(registro_hd)

                    with open(pdf[0], "rb") as data:
                        blob_client.upload_blob(data)
                    resposta = True
                    mensagem = ""
                    return resposta, mensagem
            else:
                resposta = False
                mensagem = "Arquivo não é PDF"
                return resposta, mensagem
        except:
            resposta = False
            mensagem = "Faltou algum dado!"
            return resposta, mensagem


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
