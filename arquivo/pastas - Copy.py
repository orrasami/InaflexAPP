from banco_de_dados_arquivos import *
from janelas.design import *
from janelas.incluir_pedido import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
import sys
from PyQt5 import QtWidgets, QtCore
import base64
import os


class TelaPedidos(QMainWindow, Ui_telaIncluirPedido):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnIncluirPedidoTela.clicked.connect(self.inserir_arquivo)

    def inserir_arquivo(self):
        pedido = self.inputIncluirPedido.text()
        indice = self.inputIncluirIndice.text()
        atual = self.checkIncluirAtual.checkState()
        if atual:
            atual = '0'
        else:
            atual = '1'
        try:
            pdf = QFileDialog.getOpenFileName(
                self.labelErro,
                'Escolher Arquivos',
                r'C:\Users\Sami\Desktop',
                # r'C:\Users\sami.INAFLEXSERVER\Desktop',
            )
            with open(pdf[0], "rb") as pdf_file:
                arquivo = base64.b64encode(pdf_file.read())
            titulo = os.path.basename(pdf[0])
            agenda = BDArquivos('agenda.db')
            confere = agenda.verificar_existe_arquivo_db(pedido, indice, atual, titulo)
            if confere:
                QMessageBox.about(self, "Erro", "Arquivo ja existe!")
            else:
                agenda.inserir_arquivo_db(pedido, indice, atual, titulo, arquivo)
                self.close()
        except:
            return


class Pastas(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.janela_inserir_pedido = TelaPedidos(self)
        self.btnAbrirArquivo.clicked.connect(self.mostra_incluir_arquivo)
        self.btnApagar.clicked.connect(self.apagar_arquivo)
        self.btnSelecionarPedido.clicked.connect(self.buscar_pedido)
        self.btnLiquidar.clicked.connect(self.liquidar)
        self.btnEstornar.clicked.connect(self.estornar)
        self.btnIncluirPedido.clicked.connect(self.incluir_pedido)
        self.btnExcluirPedido.clicked.connect(self.excluir_pedido)
        self.btnArquivar.clicked.connect(self.arquivar)
        self.mostrar_dados(valor='NADA')
        self.treeWidget.clicked.connect(self.selecionar_dados)
        self.treeWidget.doubleClicked.connect(self.recuperar_arquivo)

    def incluir_pedido(self):
        pedido = self.inputPedido.text()
        if not pedido:
            QMessageBox.about(self, "Erro", "Sem numero de PEDIDO!")
            return
        agenda = BDArquivos('agenda.db')
        erro = agenda.incluir_pedido_bd(pedido)
        if erro == 'Erro':
            QMessageBox.about(self, "Erro", "PEDIDO ja existe!")
        self.atualiza_arvore(pedido)

    def excluir_pedido(self):
        pedido = self.inputPedido.text()
        if not pedido:
            QMessageBox.about(self, "Erro", "Selecionar PEDIDO!")
            return
        rm = QMessageBox.question(self, '', "Tem certeza que deseja EXCLUIR esse PEDIDO?",
                                  QMessageBox.Yes | QMessageBox.No)
        if rm == 16384:
            agenda = BDArquivos('agenda.db')
            agenda.excluir_pedido_bd(pedido)
            self.atualiza_arvore('NADA')
            self.treeWidget.collapseAll()

    def mostra_incluir_arquivo(self):
        pedido = self.inputPedido.text()
        self.janela_inserir_pedido.inputIncluirPedido.setText(pedido)
        self.janela_inserir_pedido.show()
        # self.inserir_arquivo = QtWidgets.QMainWindow()
        # self.ui = Ui_telaIncluirPedido()
        # self.ui.setupUi(self.inserir_arquivo)
        # self.window

    def mostrar_dados(self, valor):
        # if not valor:
        #     pedido = 'NADA'
        tw = self.treeWidget
        tw.setHeaderLabels(['Pedidos'])
        tw.setAlternatingRowColors(True)
        agenda = BDArquivos('agenda.db')
        pedidos = agenda.mostrar_orcamentos_db(valor)
        for pedido in pedidos:
            num_pedido = pedido['pedido']
            cg = QtWidgets.QTreeWidgetItem(tw, [num_pedido])
            if pedido['liquidado'] == '1':
                cg.setCheckState(0, QtCore.Qt.CheckState.Checked)
            else:
                cg.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
            agenda = BDArquivos('agenda.db')
            atual = 1
            titulos = agenda.mostra_arquivos_db(num_pedido, atual)
            for titulo in titulos:
                nome_titulo = f"{titulo['indice']} - {titulo['titulo']}"
                QtWidgets.QTreeWidgetItem(cg, [nome_titulo])
            ch = QtWidgets.QTreeWidgetItem(cg, ['Arquivo'])
            agenda = BDArquivos('agenda.db')
            atual = 0
            titulos = agenda.mostra_arquivos_db(num_pedido, atual)
            for titulo in titulos:
                nome_titulo = f"{titulo['indice']} - {titulo['titulo']}"
                QtWidgets.QTreeWidgetItem(ch, [nome_titulo])

    def selecionar_dados(self):
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
            self.inputAtual.setText(atual)
        except:
            pedido = self.treeWidget.selectedItems()[0].text(0)
            self.inputPedido.setText(pedido)
            self.inputArquivo.setText('')
            self.inputIndice.setText('')
            self.inputAtual.setText('')

    def atualiza_arvore(self, pedido):
        self.treeWidget.clear()
        self.mostrar_dados(pedido)
        self.treeWidget.expandAll()

    def apagar_arquivo(self):
        apagar = '1'
        pedido = self.inputPedido.text()
        titulo = self.inputArquivo.text()
        if titulo and titulo != 'Arquivo':
            rm = QMessageBox.question(self, '', "Tem certeza que deseja EXCLUIR esse ITEM?",
                                      QMessageBox.Yes | QMessageBox.No)
            if rm == 16384:
                if titulo[1:2] == ' ':
                    titulo = self.treeWidget.selectedItems()[0].text(0)[4:]
                else:
                    titulo = self.treeWidget.selectedItems()[0].text(0)[5:]
                indice = self.inputIndice.text()
                atual = self.inputAtual.text()
                agenda = BDArquivos('agenda.db')
                agenda.download_arquivo_db(pedido, titulo, indice, atual, apagar)
                self.atualiza_arvore(pedido)
        else:
            QMessageBox.about(self, "Erro", "Selecionar ARQUIVO!")

    def recuperar_arquivo(self):
        apagar = '0'
        pedido = self.inputPedido.text()
        titulo = self.inputArquivo.text()
        indice = self.inputIndice.text()
        atual = self.inputAtual.text()
        if titulo != 'Arquivo' and titulo != '':
            agenda = BDArquivos('agenda.db')
            titulo, arquivo = agenda.download_arquivo_db(pedido, titulo, indice, atual, apagar)
            raiz = r'C:\Users\sami.INAFLEXSERVER\Desktop\Download'
            # raiz = r'C:\Users\sami\Desktop\Download'
            caminho_completo = os.path.join(raiz, titulo)
            bytes = base64.b64decode(arquivo)
            with open(caminho_completo, 'wb') as f:
                f.write(bytes)

    def achar_indice(self):
        atual = '0'
        index = self.treeWidget.currentIndex().parent().parent().parent().row()
        if index == -1:
            index = self.treeWidget.currentIndex().parent().parent().row()
            atual = '0'
            if index == -1:
                index = self.treeWidget.currentIndex().parent().row()
                atual = '1'
        return atual, index

    def buscar_pedido(self):
        pedido = self.inputPedido.text()
        if not pedido:
            pedido = 'NADA'
        self.treeWidget.clear()
        self.mostrar_dados(pedido)
        if pedido != 'NADA':
            self.treeWidget.expandAll()

    def liquidar(self):
        pedido = self.inputPedido.text()
        liquidado = '1'
        if not pedido:
            QMessageBox.about(self, "Erro", "Selecionar PEDIDO!")
        self.estorno_liquida(pedido, liquidado)

    def estornar(self):
        pedido = self.inputPedido.text()
        liquidado = '0'
        self.estorno_liquida(pedido, liquidado)

    def estorno_liquida(self, pedido, liquidado):
        if pedido:
            agenda = BDArquivos('agenda.db')
            agenda.estornar_liquidar_db(pedido, liquidado)
            self.atualiza_arvore('NADA')
            self.treeWidget.collapseAll()

    def arquivar(self):
        titulo = self.inputArquivo.text()
        if titulo and titulo != 'Arquivo':
            rm = QMessageBox.question(self, '', "Tem certeza que voce quer ARQUIVAR esse ITEM?",
                                      QMessageBox.Yes | QMessageBox.No)
            if rm == 16384:
                apagar = '2'
                pedido = self.inputPedido.text()
                indice = self.inputIndice.text()
                atual = self.inputAtual.text()
                agenda = BDArquivos('agenda.db')
                agenda.download_arquivo_db(pedido, titulo, indice, atual, apagar)
                self.atualiza_arvore(pedido)
        else:
            QMessageBox.about(self, "Erro", "Selecionar ARQUIVO!")


if __name__ == "__main__":
    qt = QApplication(sys.argv)
    pastas = Pastas()
    pastas.show()
    qt.exec()
