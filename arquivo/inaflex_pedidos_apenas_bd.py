# pyinstaller --onefile --noconsole --icon="static\favicon.ico modulo_arquivos_orcamentos.py
from arquivo.aux_arquivos_orcamentos import *
from janelas.design import *
from janelas.mensagem_cliente import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QWidget, QDesktopWidget, QShortcut
from PyQt5.QtGui import QKeySequence
import sys
from PyQt5 import QtWidgets, QtCore
import base64
from banco_de_dados_arquivos import *
import os

logado = False
usuario = ''
direito = '0'
pedido = ''
indice = ''
titulo = ''
atual = ''
cadeado = False


class Pedidos(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.btnAbrirArquivo.clicked.connect(self.inserir_arquivo)
        self.btnApagar.clicked.connect(self.apagar_arquivo)
        self.btnSelecionarPedido.clicked.connect(self.buscar_pedido)
        self.btnLiquidar.clicked.connect(self.ver_cliente)
        self.btnEstornar.clicked.connect(self.estornar)
        self.btnIncluirPedido.clicked.connect(self.incluir_pedido)
        self.btnExcluirPedido.clicked.connect(self.excluir_pedido)
        self.btnArquivar.clicked.connect(self.arquivar)
        self.mostrar_dados(valor='NADA')
        self.treeWidget.clicked.connect(self.selecionar_dados)
        self.treeWidget.doubleClicked.connect(self.download_arquivo)
        self.shortcut_procura = QShortcut(QKeySequence('return'), self)
        self.shortcut_procura.activated.connect(self.buscar_pedido)
        widget.currentChanged.connect(self.ao_mudar)

    """
    ############################################################
    ###################-----ARQUIVO-----########################
    ############################################################
    """
    def inserir_arquivo(self):
        global indice
        global atual
        global pedido
        global titulo
        global cadeado
        if not cadeado:
            cadeado = True
            pedido = self.inputPedido.text()
            if pedido:
                resposta = BDArquivos().analisa_se_pedido(pedido)
                if resposta:
                    liquidado = resposta[0]['liquidado']
                    if liquidado == '1':
                        QMessageBox.about(self, "Erro", "Negado - Pedido LIQUIDADO!")
                        cadeado = False
                    else:
                        janela_inserir_arquivo = JanelaInsereArquivo()
                        indice = janela_inserir_arquivo.indice
                        atual = janela_inserir_arquivo.atual
                        try:
                            pdf = QFileDialog.getOpenFileName(
                                self.centralwidget,
                                'Escolher Arquivos',
                                r'C:\Download',
                            )
                            with open(pdf[0], "rb") as pdf_file:
                                arquivo = base64.b64encode(pdf_file.read())
                            nome_arquivo, extensao_arquivo = os.path.splitext(pdf[0])
                            if extensao_arquivo == '.pdf':
                                titulo = os.path.basename(pdf[0])
                                confere = BDArquivos().verificar_existe_arquivo_db(pedido, indice, atual, titulo)
                                if confere:
                                    QMessageBox.about(self, "Erro", "Arquivo ja existe!")
                                else:
                                    acao = 'INSERIR_ARQUIVO'
                                    BDArquivos().registrar_log(usuario, acao, indice, titulo)
                                    BDArquivos().inserir_arquivo_db(pedido, indice, atual, titulo, arquivo)
                                    self.atualiza_arvore(pedido)
                                    cadeado = False
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
                        if titulo[1:2] == ' ':
                            titulo = self.treeWidget.selectedItems()[0].text(0)[4:]
                        else:
                            titulo = self.treeWidget.selectedItems()[0].text(0)[5:]
                        indice = self.inputIndice.text()
                        BDArquivos().download_arquivo_db(pedido, titulo, indice, atual, apagar)
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
        apagar = '0'
        pedido = self.inputPedido.text()
        titulo = self.inputArquivo.text()
        indice = self.inputIndice.text()
        if titulo != 'Arquivo' and titulo != '':
            titulo, arquivo = BDArquivos().download_arquivo_db(pedido, titulo, indice, atual, apagar)
            raiz = r'C:\Download'
            caminho_completo = os.path.join(raiz, titulo)
            arquivo_bytes = base64.b64decode(arquivo)
            with open(caminho_completo, 'wb') as f:
                f.write(arquivo_bytes)

    def arquivar(self):
        global atual
        global titulo
        global pedido
        global indice
        titulo = self.inputArquivo.text()
        pedido = self.inputPedido.text()
        indice = self.inputIndice.text()
        if titulo:
            resposta = BDArquivos().analisa_se_pedido(pedido)
            liquidado = resposta[0]['liquidado']
            if liquidado == '1':
                QMessageBox.about(self, "Erro", "Negado - Pedido LIQUIDADO!")
            else:
                if titulo and titulo != 'Arquivo':
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

    """
    ############################################################
    ###################-----ARVORE-----#########################
    ############################################################
    """
    def mostrar_dados(self, valor):
        global atual
        global pedido
        global titulo
        tw = self.treeWidget
        tw.setHeaderLabels(['Orçamentos:'])
        tw.setAlternatingRowColors(True)
        pedidos = BDArquivos().mostrar_orcamentos_db(valor)
        for pedido_ in pedidos:
            num_pedido = pedido_['pedido']
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
            #####AQUI#####################################
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
            ###AQUI##################
            pedido = self.treeWidget.selectedItems()[0].text(0)
            self.inputPedido.setText(pedido)
            self.inputArquivo.setText('')
            self.inputIndice.setText('')

    def atualiza_arvore(self, pedido_tree='NADA', reduz=None):
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

    """
    ############################################################
    ##################-----PEDIDOS-----#########################
    ############################################################
    """
    def buscar_pedido(self, pedido_=None):
        global pedido
        fg = True
        pedido = self.inputPedido.text()
        if not pedido:
            pedido = pedido_
        if not pedido:
            pedido = 'NADA'
            fg = False
        self.treeWidget.clear()
        self.mostrar_dados(pedido)
        if fg:
            self.treeWidget.expandAll()

    def estornar(self):
        global pedido
        global direito
        if direito == '1':
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
        widget.setCurrentIndex(1)
        widget.resize(400, 399)
        janela_cliente.labelPedido.setText(f'N°:{pedido}')

    def ao_mudar(self, i):
        print('Mudou o widget para %d' % i)
        if i == 0:
            if pedido == '':
                self.atualiza_arvore('NADA')
            else:
                self.atualiza_arvore(pedido)


class JanelaCliente(QWidget, Ui_janelaMensagemCliente):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.shortcut_procura = QShortcut(QKeySequence('return'), self)
        self.shortcut_procura.activated.connect(self.seleciona_cliente)
        self.inputCnpj.setPlaceholderText('CNPJ (só numeros)')
        self.btnCNPJ.clicked.connect(self.seleciona_cliente)
        self.btnCadastrar.clicked.connect(self.cadastra_cliente)
        self.btnLiquidar.clicked.connect(self.liquidar)
        self.textExigencias.setReadOnly(True)
        self.btnCancelar.clicked.connect(self.ver_pedidos)
        self.btnEditar.clicked.connect(self.tela_editar)
        self.btnAtualizar.clicked.connect(self.atualizar_cadastro)
        self.tela_liquidar()

    def tela_cadastrar(self):
        self.textExigencias.setReadOnly(False)
        self.inputNomeCliente.show()
        self.btnCadastrar.show()
        self.labelPedido.hide()
        # self.labelPedido.setText(f'N°:{pedido}')
        self.btnCNPJ.hide()
        self.btnLiquidar.hide()
        self.labelNomeCliente.hide()
        self.checkDeclaracao.hide()
        self.btnEditar.hide()
        self.btnAtualizar.hide()

    def tela_editar(self):
        self.textExigencias.setReadOnly(False)
        self.inputNomeCliente.hide()
        self.btnCadastrar.hide()
        self.labelPedido.hide()
        self.btnCNPJ.hide()
        self.btnLiquidar.hide()
        self.labelNomeCliente.show()
        self.checkDeclaracao.hide()
        self.btnEditar.hide()
        self.btnAtualizar.show()

    def tela_liquidar(self):
        self.textExigencias.setReadOnly(True)
        self.inputNomeCliente.hide()
        self.btnCadastrar.hide()
        self.labelPedido.show()
        # self.labelPedido.setText(f'N°:{pedido}')
        self.btnCNPJ.show()
        self.btnLiquidar.show()
        self.labelNomeCliente.show()
        self.checkDeclaracao.show()
        self.btnEditar.show()
        self.btnAtualizar.hide()

    def ver_pedidos(self):
        self.tela_liquidar()
        self.inputCnpj.setText('')
        self.textExigencias.setText('')
        self.inputNomeCliente.setText('')
        self.labelNomeCliente.setText('')
        # self.labelPedido.setText('')
        self.checkDeclaracao.setChecked(False)
        widget.resize(722, 414)
        index_ = widget.currentIndex()
        if index_ != 0:
            widget.setCurrentIndex(0)

    def atualizar_cadastro(self):
        cnpj = self.inputCnpj.text()
        exigencias = self.textExigencias.toPlainText()
        if len(cnpj) == 14:
            resposta = BDArquivos().atualiza_informacoes(cnpj, exigencias)
            self.tela_liquidar()
            if not resposta:
                rm = QMessageBox.question(self, '', "Gostaria de Cadastrar esse CNPJ?",
                                          QMessageBox.Yes | QMessageBox.No)
                if rm == 16384:
                    self.tela_cadastrar()
                    self.seleciona_cliente()
        else:
            QMessageBox.about(self, "Erro", "CNPJ Inválido")

    def seleciona_cliente(self):
        cnpj = self.inputCnpj.text()
        retorno = BDArquivos().verifica_cnpj()
        if retorno:
            retorno = BDArquivos().busca_cliente(cnpj)
            if retorno:
                self.labelNomeCliente.setText(retorno[0]['nome'])
                self.textExigencias.setText(retorno[0]['exigencias'])
            else:
                rm = QMessageBox.question(self, '', "Gostaria de Cadastrar esse CNPJ?",
                                          QMessageBox.Yes | QMessageBox.No)
                if rm == 16384:
                    self.tela_cadastrar()
                else:
                    self.tela_liquidar()
        else:
            QMessageBox.about(self, "Erro", "CNPJ Inválido")

    def cadastra_cliente(self):
        cnpj = self.inputCnpj.text()
        cliente = self.inputNomeCliente.text()
        exigencias = self.textExigencias.toPlainText()

        if len(cnpj) == 14 or len(cliente) >= 5:
            BDArquivos().cadastra_cliente_db(cnpj, cliente, exigencias)
            self.tela_liquidar()
            self.seleciona_cliente()
        else:
            QMessageBox.about(self, "Erro", "Infomações incompletas")

    def liquidar(self):
        global direito
        global pedido
        if direito == '1':
            if self.checkDeclaracao.isChecked():
                cnpj = self.inputCnpj.text()
                pedido = self.labelPedido.text()[3:]
                liquidado = '1'
                if not pedido:
                    QMessageBox.about(self, "Erro", "Selecionar PEDIDO!")
                self.estornar_liquidar(pedido, liquidado, cnpj)
            else:
                QMessageBox.about(self, "Erro", "E obrigatorio ler e conferir os dados acima. Se nao conferiu ainda, "
                                                "favor cancelar, conferir e depois liquidar")
        else:
            QMessageBox.about(self, "Erro", "Voce não tem direitos suficientes")

    def estornar_liquidar(self, pedido_input, liquidado, cnpj):
        global pedido
        pedido = pedido_input
        acao = 'LIQUIDAR_ARQUIVO'
        if pedido:
            feito = BDArquivos().estornar_liquidar_db(pedido, liquidado, cnpj)
            self.ver_pedidos()
            if feito:
                BDArquivos().registrar_log(usuario, acao)
            else:
                QMessageBox.about(self, "Erro", "Orçamento ja está LIQUIDADO")


"""
############################################################
####################-----LOGIN-----#########################
############################################################
"""


def log_in():
    global logado
    global direito
    janela_login = JanelaLogin()
    direito = janela_login.direito
    logado = janela_login.logado
    if not logado:
        exit()


if __name__ == "__main__":
    qt = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    janela_pedidos = Pedidos()
    janela_cliente = JanelaCliente()
    widget.addWidget(janela_pedidos)
    widget.addWidget(janela_cliente)

    qtRectangle = janela_pedidos.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    janela_pedidos.move(qtRectangle.topLeft())

    log_in()

    widget.resize(722, 414)
    widget.show()
    qt.exec()
