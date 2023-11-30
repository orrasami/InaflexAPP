# 1.1 ARQUIVOS
from banco_de_dados_oracle import BDBohm
from janelas.janela_arquivos_orcamentos import *
from janelas.janela_arquivos_cliente import *
from janelas.janela_arquivos_arquivo import *
from banco_de_dados_arquivos import *
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QWidget, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtWidgets, QtCore
import os
from azure.storage.blob import ContainerClient
from time import gmtime, strftime
import json

usuario = ''
pedido = ''
indice = ''
titulo = ''
atual = ''
cadeado = False

path_download = ''
with open('setup.json', 'r') as file:
    d1_json = file.read()
    d1_json = json.loads(d1_json)

for x, y in d1_json.items():
    path_download = y['download']


class Pedidos(QMainWindow, Ui_mainWindow):
    def __init__(self, widget_pedidos, janela_cliente, janela_arquivo, direito, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.btnAbrirArquivo.clicked.connect(self.ver_arquivos)
        self.btnApagar.clicked.connect(self.apagar_arquivo)
        self.btnSelecionarPedido.clicked.connect(self.buscar_pedido)
        self.btnLiquidar.clicked.connect(self.ver_cliente)
        self.btnEstornar.clicked.connect(self.estornar)
        self.btnIncluirPedido.clicked.connect(self.incluir_pedido)
        self.btnExcluirPedido.clicked.connect(self.excluir_pedido)
        self.btnArquivar.clicked.connect(self.arquivar)
        self.btnAtualizarNumPedido.clicked.connect(self.atualiza_num_pedido)
        self.treeWidget.clicked.connect(self.selecionar_dados)
        self.treeWidget.doubleClicked.connect(self.download_arquivo)
        self.shortcut_procura = QShortcut(QKeySequence('return'), self)
        self.shortcut_procura.activated.connect(self.buscar_pedido)
        self.shortcut_procura_alt = QShortcut(QKeySequence('enter'), self)
        self.shortcut_procura_alt.activated.connect(self.buscar_pedido)
        self.janela_cliente = janela_cliente
        self.janela_arquivo = janela_arquivo
        self.widget_pedidos = widget_pedidos
        self.direito = direito
        self.widget_pedidos.currentChanged.connect(self.ao_mudar)
        self.mostrar_dados(valor='')

    def atualiza_num_pedido(self):
        orcamento = self.inputPedido.text()
        if orcamento:
            pedido = BDBohm().atualiza_num_pedido(orcamento)
            if pedido:
                BDArquivos().atualiza_num_pedido(pedido, orcamento)
                QMessageBox.about(self, "Sucesso", f"ORÇAMENTO: {orcamento} GEROU O PEDIDO: {pedido}")
            else:
                QMessageBox.about(self, "Erro", "ESSE ORÇAMENTO NÃO É UM PEDIDO AINDA")
        else:
            QMessageBox.about(self, "Erro", "SELECIONAR ORÇAMENTO")

    def apagar_arquivo(self):
        global atual
        global pedido
        global titulo
        global indice
        apagar = '1'
        pedido = self.inputPedido.text()
        titulo = self.inputArquivo.text()

        if pedido:
            resposta = BDArquivos().analisa_se_pedido(pedido)
            liquidado = resposta[0]['liquidado']
            if liquidado == '1':
                QMessageBox.about(self, "Erro", "Negado - Pedido LIQUIDADO!")
            else:
                if titulo and titulo != 'Arquivo':
                    rm = QMessageBox.question(self, '', "Tem certeza que deseja EXCLUIR esse ITEM?",
                                              QMessageBox.Yes | QMessageBox.No)
                    if rm == 16384:
                        acao = 'EXCLUIR_ARQUIVO'
                        BDArquivos().registrar_log(usuario, acao, indice, titulo)
                        indice = self.inputIndice.text()
                        registro = BDArquivos().download_arquivo_db(pedido, titulo, indice, atual, apagar)
                        nome_arquivo = registro + '-' + titulo

                        connection_string = 'DefaultEndpointsProtocol=https;AccountName=inaflex;AccountKey=FCF8566/Tz' \
                                            'Edl2hHvp+2owWDZPVxfyX+MYTFX0ToDe1Nkxvg4TO1eHLp2DU1EcBirNrrW4TOxl3v+AStHX' \
                                            'st8w==;EndpointSuffix=core.windows.net'
                        container_name = 'pedidos'
                        container_client = ContainerClient.from_connection_string(connection_string, container_name)
                        blob_client = container_client.get_blob_client(nome_arquivo)
                        blob_client.delete_blob()

                        self.atualiza_arvore(pedido)
                else:
                    QMessageBox.about(self, "Erro", "Selecionar ARQUIVO!")
        else:
            QMessageBox.about(self, "Erro", "Selecionar PEDIDO")

    def download_arquivo(self):
        global atual
        global pedido
        global titulo
        global indice
        global path_download
        apagar = '0'
        pedido = self.inputPedido.text()
        titulo = self.inputArquivo.text()
        indice = self.inputIndice.text()
        if titulo != 'Arquivo' and titulo != '' and indice and atual and pedido:
            titulo, registro = BDArquivos().download_arquivo_db(pedido, titulo, indice, atual, apagar)
            raiz = path_download
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

    def arquivar(self):
        global atual
        global titulo
        global pedido
        global indice
        titulo = self.inputArquivo.text()
        pedido = self.inputPedido.text()
        indice = self.inputIndice.text()
        if titulo and pedido:
            resposta = BDArquivos().analisa_se_pedido(pedido)
            liquidado = resposta[0]['liquidado']
            if liquidado == '1':
                QMessageBox.about(self, "Erro", "Negado - Pedido LIQUIDADO!")
            else:
                if titulo and titulo != 'Arquivo' and indice and pedido:
                    rm = QMessageBox.question(self, '', "Tem certeza que voce quer ARQUIVAR esse ITEM?",
                                              QMessageBox.Yes | QMessageBox.No)
                    if rm == 16384:
                        apagar = '2'
                        acao = 'ARQUIVAR_ARQUIVO'
                        BDArquivos().registrar_log(usuario, acao, indice, titulo)
                        BDArquivos().download_arquivo_db(pedido, titulo, indice, atual, apagar)
                        self.atualiza_arvore(pedido)
                else:
                    QMessageBox.about(self, "Erro", "Selecionar ARQUIVO!")
        else:
            QMessageBox.about(self, "Erro", "Selecionar ARQUIVO")

    def mostrar_dados(self, valor):
        global atual
        global pedido
        global titulo
        tw = self.treeWidget
        tw.setHeaderLabels(['Orçamentos:'])
        tw.setAlternatingRowColors(True)
        if valor != '':
            pedidos = BDArquivos().mostrar_orcamentos_db(valor)
            for pedido_ in pedidos:
                num_pedido = pedido_['orcamento']
                cg = QtWidgets.QTreeWidgetItem(tw, [num_pedido])
                if pedido_['liquidado'] == '1':
                    cg.setCheckState(0, QtCore.Qt.CheckState.Checked)
                else:
                    cg.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
                atual = 1
                titulos = BDArquivos().mostra_arquivos_db(num_pedido, atual)
                for titulo in titulos:
                    nome_titulo = f"{titulo['indice']} - {titulo['titulo']}"
                    QtWidgets.QTreeWidgetItem(cg, [nome_titulo])
                ch = QtWidgets.QTreeWidgetItem(cg, ['Arquivo'])
                atual = 0
                titulos = BDArquivos().mostra_arquivos_db(num_pedido, atual)
                for titulo in titulos:
                    nome_titulo = f"{titulo['indice']} - {titulo['titulo']}"
                    QtWidgets.QTreeWidgetItem(ch, [nome_titulo])

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
            self.inputArquivo.setText(titulo)
            self.inputIndice.setText(indice)
        except:
            pedido = self.treeWidget.selectedItems()[0].text(0)
            self.inputPedido.setText(pedido)
            self.inputArquivo.setText('')
            self.inputIndice.setText('')

    def atualiza_arvore(self, pedido_tree='NADA'):
        self.treeWidget.clear()
        self.mostrar_dados(pedido_tree)
        if pedido_tree == 'NADA':
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

    def buscar_pedido(self, pedido_=None):
        global pedido
        fg = True
        pedido = self.inputPedido.text()
        if not pedido:
            pedido = pedido_
        if pedido == '*':
            fg = False
        self.treeWidget.clear()
        self.mostrar_dados(pedido)
        if fg:
            self.treeWidget.expandAll()

    def estornar(self):
        global pedido
        if self.direito == '1':
            pedido = self.inputPedido.text()
            liquidado = '0'
            self.estornar_liquidar(pedido, liquidado)
            self.atualiza_arvore(pedido)
            self.treeWidget.expandAll()
        else:
            QMessageBox.about(self, "Erro", "Voce não tem direitos suficientes")

    def estornar_liquidar(self, pedido_input, liquidado):
        acao = 'ESTORNAR_ARQUIVO'
        if pedido_input:
            feito = BDArquivos().estornar_liquidar_db(pedido_input, liquidado)
            if feito:
                BDArquivos().registrar_log(usuario, acao)
            else:
                QMessageBox.about(self, "Erro", "Orçamento ja está ESTORNADO")

    def incluir_pedido(self):
        global pedido
        pedido = self.inputPedido.text()
        if not pedido:
            QMessageBox.about(self, "Erro", "Sem numero de PEDIDO!")
            return
        erro = BDArquivos().incluir_pedido_bd(pedido)
        if erro != 'Erro':
            acao = 'INCLUIR_ORCAMENTO'
            BDArquivos().registrar_log(usuario, acao)
        if erro == 'Erro':
            QMessageBox.about(self, "Erro", "PEDIDO ja existe!")
        self.atualiza_arvore(pedido)

    def excluir_pedido(self):
        global pedido
        pedido = self.inputPedido.text()
        if not pedido:
            QMessageBox.about(self, "Erro", "Selecionar PEDIDO!")
        else:
            rm = QMessageBox.question(self, '', "Tem certeza que deseja EXCLUIR esse PEDIDO?",
                                      QMessageBox.Yes | QMessageBox.No)
            if rm == 16384:
                resultado = BDArquivos().excluir_pedido_bd(pedido)
                if resultado:
                    acao = 'EXCLUIR_ORCAMENTO'
                    BDArquivos().registrar_log(usuario, acao)
                    self.atualiza_arvore('NADA')
                    self.treeWidget.collapseAll()
                else:
                    QMessageBox.about(self, "Erro", "EXCLUIR arquivos antes de apagar o PEDIDO")

    def ver_cliente(self):
        status = BDArquivos().verificar_checklist(pedido)
        if status == 0:
            QMessageBox.about(self, "Erro", "Falta fazer o checklist para o orçamento")
        else:
            self.widget_pedidos.setCurrentIndex(1)
            self.widget_pedidos.setFixedSize(742, 399)
            self.janela_cliente.labelPedido.setText(f'N°:{pedido}')

    def ver_arquivos(self):
        self.widget_pedidos.setCurrentIndex(2)
        self.widget_pedidos.setFixedSize(749, 281)
        self.janela_arquivo.labelPedido.setText(f'N°:{pedido}')

    def ao_mudar(self, i):
        print('Mudou o widget para %d' % i)
        if i == 0:
            if pedido == '':
                self.atualiza_arvore('NADA')
            else:
                self.atualiza_arvore(pedido)


class JanelaCliente(QWidget, Ui_janelaMensagemCliente):
    def __init__(self, widget_pedidos, direito, bd_oracle_ok, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.textObsAcabamento.setReadOnly(False)
        self.textObsFaturamento.setReadOnly(False)
        self.shortcut_procura = QShortcut(QKeySequence('return'), self)
        self.shortcut_procura.activated.connect(self.seleciona_cliente)
        self.shortcut_procura_alt = QShortcut(QKeySequence('enter'), self)
        self.shortcut_procura_alt.activated.connect(self.seleciona_cliente)
        self.inputCnpj.setPlaceholderText('CNPJ (COM PONTUAÇÃO)')
        self.btnCNPJ.clicked.connect(self.seleciona_cliente)
        self.btnLiquidar.clicked.connect(self.liquidar)
        self.btnCancelar.clicked.connect(self.ver_pedidos)
        self.btnInfoAdicional.clicked.connect(self.mostra_info_adicional)
        self.textExigencias.setReadOnly(True)
        self.widget_pedidos = widget_pedidos
        self.direito = direito
        if bd_oracle_ok == 'Falha':
            self.bd_oracle_ok = True
        else:
            self.bd_oracle_ok = False
        self.tela_liquidar()

    def tela_liquidar(self):
        self.textObsAcabamento.setText('')
        self.textObsFaturamento.setText('')
        self.textExigencias.setReadOnly(True)
        self.labelPedido.show()
        self.labelNomeCliente.show()
        self.checkDeclaracao.show()
        self.btnCNPJ.show()
        self.btnLiquidar.show()
        self.btnInfoAdicional.show()
        self.btnCancelar.show()

    def mostra_info_adicional(self):
        largura = self.widget_pedidos.width()
        if largura < 700:
            self.widget_pedidos.setFixedSize(742, 399)
        else:
            self.widget_pedidos.setFixedSize(400, 399)

    def seleciona_cliente(self):
        if not self.bd_oracle_ok:
            cnpj = self.inputCnpj.text()
            if cnpj:
                try:
                    resposta = BDBohm().pegar_nome_cliente(cnpj)
                except:
                    QMessageBox.about(self, "Erro", "Erro ao passar para o BDBohm")
                if not resposta:
                    QMessageBox.about(self, "Erro", "Infomações erradas, ou cliente não cadastrado no Analysis")
                else:
                    try:
                        cliente = resposta[0]
                        exigencias = resposta[1]
                    except:
                        QMessageBox.about(self, "Erro", "Erro para pegar os valores de resposta")
                    try:
                        self.labelNomeCliente.setText(cliente)
                        self.textExigencias.setText(exigencias)
                    except:
                        QMessageBox.about(self, "Erro", "Erro para colocar os valores nos inputs")
            else:
                QMessageBox.about(self, "Erro", "Erro conexão Oracle")

    def liquidar(self):
        global pedido
        if self.direito == '1':
            if self.labelNomeCliente.text() != 'Selecionar cliente':
                if self.checkDeclaracao.isChecked():
                    cnpj = self.inputCnpj.text()
                    pedido = self.labelPedido.text()[3:]
                    cliente = self.labelNomeCliente.text()
                    exigencias = self.textExigencias.toPlainText().upper()
                    obs_acabamento = self.textObsAcabamento.toPlainText().upper()
                    obs_faturamento = self.textObsFaturamento.toPlainText().upper()
                    liquidado = '1'
                    if not pedido:
                        QMessageBox.about(self, "Erro", "Selecionar PEDIDO!")
                    self.estornar_liquidar(pedido, liquidado, cnpj, cliente, exigencias, obs_acabamento, obs_faturamento)
                else:
                    QMessageBox.about(self, "Erro", "E obrigatorio ler e conferir os dados acima. Se nao conferiu "
                                                    "ainda, favor cancelar, conferir e depois liquidar")
            else:
                QMessageBox.about(self, "Erro", "Selecionar o cliente primeiro")
        else:
            QMessageBox.about(self, "Erro", "Voce não tem direitos suficientes")

    def estornar_liquidar(self, pedido_input, liquidado, cnpj, cliente, exigencias, obs_acabamento, obs_faturamento):
        global pedido
        pedido = pedido_input
        acao = 'LIQUIDAR_ARQUIVO'
        if pedido:
            feito = BDArquivos().estornar_liquidar_db(pedido, liquidado, cnpj, cliente, exigencias, obs_acabamento, obs_faturamento)
            self.ver_pedidos()
            if feito:
                BDArquivos().registrar_log(usuario, acao)
            else:
                QMessageBox.about(self, "Erro", "Orçamento ja está LIQUIDADO")

    def ver_pedidos(self):
        self.tela_liquidar()
        self.inputCnpj.setText('')
        self.textExigencias.setText('')
        self.labelNomeCliente.setText('')
        self.checkDeclaracao.setChecked(False)
        self.widget_pedidos.setFixedSize(722, 479)
        index_ = self.widget_pedidos.currentIndex()
        if index_ != 0:
            self.widget_pedidos.setCurrentIndex(0)


class JanelaArquivos(QMainWindow, Ui_telaIncluirArquivos):
    def __init__(self, widget_pedidos, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.widget_pedidos = widget_pedidos
        self.btnCancela.clicked.connect(self.ver_pedidos)
        self.btnIncluirPedidoTela.clicked.connect(self.inserir_arquivo)

    def ver_pedidos(self):
        self.inputIncluirIndice.setText('')
        self.checkIncluirAtual.setChecked(False)
        self.labelPedido.setText('Selecionar Pedido')
        self.widget_pedidos.setFixedSize(722, 479)
        index_ = self.widget_pedidos.currentIndex()
        if index_ != 0:
            self.widget_pedidos.setCurrentIndex(0)

    def inserir_arquivo(self):
        global indice
        global atual
        global pedido
        global titulo
        global cadeado
        global path_download

        if not cadeado:
            cadeado = True
            pedido = self.labelPedido.text()[3:]
            if pedido:
                resposta = BDArquivos().analisa_se_pedido(pedido)
                if resposta:
                    liquidado = resposta[0]['liquidado']
                    if liquidado == '1':
                        QMessageBox.about(self, "Erro", "Negado - Pedido LIQUIDADO!")
                        cadeado = False
                    else:
                        indice = self.inputIncluirIndice.text()
                        if self.checkIncluirAtual.isChecked():
                            atual = '0'
                        else:
                            atual = '1'
                        try:
                            pdf = QFileDialog.getOpenFileName(
                                self.centralWidget(),
                                'Escolher Arquivos',
                                path_download,
                            )
                            nome_arquivo, extensao_arquivo = os.path.splitext(pdf[0])
                            extensao_arquivo = extensao_arquivo.upper()
                            if extensao_arquivo == '.PDF':
                                titulo = os.path.basename(pdf[0])
                                confere = BDArquivos().verificar_existe_arquivo_db(pedido, indice, atual, titulo)
                                if confere:
                                    QMessageBox.about(self, "Erro", "Arquivo ja existe!")
                                else:
                                    acao = 'INSERIR_ARQUIVO'
                                    registro = pedido + '-' + strftime("%Y%m%d%H%M%S", gmtime())
                                    registro_hd = registro + '-' + titulo
                                    BDArquivos().registrar_log(usuario, acao, indice, titulo)
                                    BDArquivos().inserir_arquivo_db(pedido, indice, atual, titulo, registro)

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

                                    cadeado = False
                                    self.ver_pedidos()
                            else:
                                QMessageBox.about(self, "Erro", "Arquivo não é PDF")
                                cadeado = False
                                return
                        except:
                            QMessageBox.about(self, "Erro", "Faltou algum dado!")
                            cadeado = False
                            return
                else:
                    QMessageBox.about(self, "Erro", "Pedido Inválido")
            else:
                QMessageBox.about(self, "Erro", "Selecionar PEDIDO")
                cadeado = False
        cadeado = False


