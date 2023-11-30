# 1.2 ACABAMENTO
from banco_de_dados_oracle import BDBohm
from janelas.janela_acabamento import *
from banco_de_dados_arquivos import BDArquivos
from PyQt5.QtWidgets import QMainWindow, QShortcut, QMessageBox
from PyQt5.QtGui import QKeySequence
from azure.storage.blob import ContainerClient
from threading import Thread
import os

global atual
global pedido
global titulo
global indice


class Acabamento(QMainWindow, Ui_Acabamento):
    def __init__(self, bd_oracle_ok, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.treeWidget.doubleClicked.connect(self.download_arquivo)
        self.treeWidget.clicked.connect(self.selecionar_dados)
        self.btnSelecionarPedido.clicked.connect(self.buscar_pedido)
        self.btnEnviarFaturamento.clicked.connect(self.enviar_para_faturamento)
        self.btnAtualizarPedidos.clicked.connect(self.atualizar_dados)
        self.btnAtualizarPedidos.setVisible(False)
        self.inputPedido.textChanged.connect(self.apaga_valores)
        self.inputData.setDate(QtCore.QDate.currentDate())
        self.shortcut_procura = QShortcut(QKeySequence('return'), self)
        self.shortcut_procura.activated.connect(self.buscar_pedido)
        self.shortcut_procura_alt = QShortcut(QKeySequence('enter'), self)
        self.shortcut_procura_alt.activated.connect(self.buscar_pedido)
        self.labelAtualizando.hide()
        self.mostrar_dados(valor='')
        if bd_oracle_ok == 'Falha':
            self.bd_oracle_ok = True
        else:
            self.bd_oracle_ok = False
            self.atualizar_pedidos()

    def download_arquivo(self):
        global atual
        global pedido
        global titulo
        global indice
        apagar = '0'
        pedido = self.inputPedido.text()
        orcamento = BDArquivos().achar_numero_orcamento(pedido)
        orcamento = orcamento[0]['orcamento']
        if titulo != 'Arquivo' and titulo != '':
            titulo, registro = BDArquivos().download_arquivo_acabamento_db(orcamento, titulo, indice, atual)
            raiz = r'C:\Download'
            caminho_completo = os.path.join(raiz, titulo)
            nome_arquivo = registro + '-' + titulo

            connection_string = 'DefaultEndpointsProtocol=https;AccountName=inaflex;AccountKey=FCF8566/TzEdl2hHvp+2ow' \
                                'WDZPVxfyX+MYTFX0ToDe1Nkxvg4TO1eHLp2DU1EcBirNrrW4TOxl3v+AStHXst8w==;EndpointSuffix=co' \
                                're.windows.net'
            container_name = 'pedidos'
            container_client = ContainerClient.from_connection_string(connection_string, container_name)
            blob_client = container_client.get_blob_client(nome_arquivo)

            arquivo_storage = blob_client.download_blob()
            arquivo_bite = arquivo_storage.readall()
            with open(caminho_completo, 'wb') as data:
                data.write(arquivo_bite)

    def mostrar_dados(self, valor):
        global atual
        global pedido
        global titulo
        tw = self.treeWidget
        tw.setHeaderLabels(['Pedidos:'])
        tw.setAlternatingRowColors(True)
        pedidos = BDArquivos().mostrar_pedidos_acabamento_db(valor)
        for pedido_ in pedidos:
            num_pedido = pedido_['pedido']
            num_orcamento = pedido_['orcamento']
            cg = QtWidgets.QTreeWidgetItem(tw, [num_pedido])
            cg.setCheckState(0, QtCore.Qt.CheckState.Checked)
            atual = 1
            titulos = BDArquivos().mostra_arquivos_acabamento_db(num_orcamento, atual)
            for titulo in titulos:
                nome_titulo = f"{titulo['indice']} - {titulo['titulo']}"
                QtWidgets.QTreeWidgetItem(cg, [nome_titulo])

    def selecionar_dados(self):
        global atual
        global pedido
        global titulo
        global indice
        atual, index = self.achar_indice()
        try:
            pedido = self.treeWidget.topLevelItem(index).text(0)
            self.inputPedido.setText(pedido)
            titulo = self.treeWidget.selectedItems()[0].text(0)
            if titulo[1:2] == ' ':
                indice = titulo[:1]
                titulo = self.treeWidget.selectedItems()[0].text(0)[4:]
            elif titulo[1:2] == 'r':
                indice = ''
                atual = ''
            else:
                indice = titulo[:2]
                titulo = self.treeWidget.selectedItems()[0].text(0)[5:]
            resposta = BDArquivos().dados_acabamento_db(pedido)
            self.inputCliente.setText(resposta[0]['cliente'])
            self.textObsAcabamento.setText(resposta[0]['obs_acabamento'])
            self.inputLocal.setText('')
            self.inputEmbalagem.setText('')
        except:
            pedido = self.treeWidget.selectedItems()[0].text(0)
            self.inputPedido.setText(pedido)
            resposta = BDArquivos().dados_acabamento_db(pedido)
            self.inputCliente.setText(resposta[0]['cliente'])
            self.textObsAcabamento.setText(resposta[0]['obs_acabamento'])
            self.inputLocal.setText('')
            self.inputEmbalagem.setText('')

    def atualiza_arvore(self, pedido_tree=''):
        self.treeWidget.clear()
        self.mostrar_dados(pedido_tree)
        if pedido_tree == '*':
            self.treeWidget.collapseAll()
        else:
            self.treeWidget.expandAll()

    def achar_indice(self):
        global atual
        atual = '0'
        index = self.treeWidget.currentIndex().parent().parent().parent().row()
        if index == -1:
            index = self.treeWidget.currentIndex().parent().parent().row()
            atual = '0'
            if index == -1:
                index = self.treeWidget.currentIndex().parent().row()
                atual = '1'
        return atual, index

    def buscar_pedido(self, pedido_=''):
        global pedido
        fg = True
        pedido = self.inputPedido.text()
        if not pedido:
            pedido = pedido_
        if pedido == '' or pedido == False or pedido == '*':
            fg = False
        self.treeWidget.clear()
        self.mostrar_dados(pedido)
        if fg:
            self.treeWidget.expandAll()

    def enviar_para_faturamento(self):
        global pedido
        pedido = self.inputPedido.text()
        self.inputData.setDate(QtCore.QDate.currentDate())
        data = self.inputData.date().toString('yyyy/MM/dd')
        local = self.inputLocal.text().upper()
        embalagem = self.inputEmbalagem.text().upper()
        if pedido and data and local and embalagem:
            BDArquivos().salva_dados_acabamento(pedido, data, local, embalagem)
            self.inputPedido.setText('')
            self.inputCliente.setText('')
            self.inputLocal.setText('')
            self.inputEmbalagem.setText('')
            self.textObsAcabamento.setText('')
            self.atualiza_arvore('')
        else:
            QMessageBox.about(self, "Erro", "Preencher todos os campos")

    def apaga_valores(self):
        self.inputEmbalagem.setText('')
        self.inputLocal.setText('')
        self.inputCliente.setText('')

    def atualizar_pedidos(self):
        daemon = Thread(target=self.atualizar_dados, args=())
        daemon.daemon = True
        daemon.start()

    def atualizar_dados(self):
        self.labelAtualizando.show()
        self.atualizar_faturados()
        self.treeWidget.clear()
        self.mostrar_dados('')
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
