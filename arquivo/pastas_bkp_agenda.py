from banco_de_dados_arquivos import *
from janelas.design import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QDesktopWidget
import sys
from PyQt5 import QtWidgets, QtCore
import base64
import os
from tkinter import *

logado = False
usuario = ''
direito = '0'
pedido = ''
indice = ''
titulo = ''
atual = ''
cadeado = False


class Pastas(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.btnAbrirArquivo.clicked.connect(self.inserir_arquivo)
        self.btnApagar.clicked.connect(self.apagar_arquivo)
        self.btnSelecionarPedido.clicked.connect(self.buscar_pedido)
        self.btnLiquidar.clicked.connect(self.liquidar)
        self.btnEstornar.clicked.connect(self.estornar)
        self.btnIncluirPedido.clicked.connect(self.incluir_pedido)
        self.btnExcluirPedido.clicked.connect(self.excluir_pedido)
        self.btnArquivar.clicked.connect(self.arquivar)
        self.mostrar_dados(valor='NADA')
        self.treeWidget.clicked.connect(self.selecionar_dados)
        self.treeWidget.doubleClicked.connect(self.download_arquivo)
        self.log_in()

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
                liquidado = resposta[0]['liquidado']
                if liquidado == '1':
                    QMessageBox.about(self, "Erro", "Negado - Pedido LIQUIDADO!")
                    cadeado = False
                else:
                    def fecha():
                        global indice
                        global atual
                        indice = pegar.get()
                        if atual_valor.get():
                            atual = '0'
                        else:
                            atual = '1'
                        janela.destroy()

                    self.atualiza_arvore(pedido)
                    janela = Tk()
                    janela.title("Inserir indice")
                    janela.focus_set()

                    app_width = 300
                    app_height = 120
                    screen_width = janela.winfo_screenwidth()
                    screen_height = janela.winfo_screenheight()
                    x_pos = (screen_width / 2) - (app_width / 2) - 205
                    y_pos = (screen_height / 2) - (app_height / 2) - 50
                    janela.geometry(f'{app_width}x{app_height}+{int(x_pos)}+{int(y_pos)}')

                    texto = Label(janela, text="Qual Indice?")
                    texto.grid(column=0, row=0, padx=10, pady=0)
                    texto.place(relx=0.5, y=15, anchor=CENTER)
                    pegar = Entry(janela, justify=CENTER)
                    pegar.grid(column=0, row=1, padx=10, pady=0)
                    pegar.place(relx=0.5, y=40, anchor=CENTER)
                    pegar.focus_set()
                    atual_valor = IntVar()
                    check = Checkbutton(janela, text='Arquivo', variable=atual_valor, onvalue=1, offvalue=0)
                    check.grid(column=0, row=2, padx=10, pady=5)
                    check.place(relx=0.5, y=70, anchor=CENTER)
                    botao = Button(janela, text="      OK      ", command=fecha)
                    botao.grid(column=0, row=3, padx=0, pady=5)
                    botao.place(relx=0.5, y=100, anchor=CENTER)
                    janela.bind("<Return>", (lambda event: fecha()))
                    janela.mainloop()

                    try:
                        pdf = QFileDialog.getOpenFileName(
                            self.centralwidget,
                            'Escolher Arquivos',
                            # r'C:\Users\Sami\Desktop',
                            r'C:\Users\sami.INAFLEXSERVER\Desktop',
                        )
                        with open(pdf[0], "rb") as pdf_file:
                            arquivo = base64.b64encode(pdf_file.read())
                        nome_arquivo, extensao_arquivo = os.path.splitext(pdf[0])
                        print(extensao_arquivo)
                        print(nome_arquivo)
                        if extensao_arquivo == '.pdf':
                            titulo = os.path.basename(pdf[0])
                            pedido = pedido['pedido']
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
            raiz = r'C:\Users\sami.INAFLEXSERVER\Desktop\Download'
            # raiz = r'C:\Users\sami\Desktop\Download'
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
        for pedido in pedidos:
            num_pedido = pedido['pedido']
            cg = QtWidgets.QTreeWidgetItem(tw, [num_pedido])
            if pedido['liquidado'] == '1':
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

    def atualiza_arvore(self, pedido_tree):
        self.treeWidget.clear()
        self.mostrar_dados(pedido_tree)
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
    def buscar_pedido(self):
        global pedido
        fg = True
        pedido = self.inputPedido.text()
        if not pedido:
            pedido = 'NADA'
            fg = False
        self.treeWidget.clear()
        self.mostrar_dados(pedido)
        if fg:
            self.treeWidget.expandAll()

    def liquidar(self):
        global direito
        global pedido
        if direito == '1':
            pedido = self.inputPedido.text()
            liquidado = '1'
            if not pedido:
                QMessageBox.about(self, "Erro", "Selecionar PEDIDO!")
            self.estornar_liquidar(pedido, liquidado)
        else:
            QMessageBox.about(self, "Erro", "Voce não tem direitos suficientes")

    def estornar(self):
        global pedido
        global direito
        if direito == '1':
            pedido = self.inputPedido.text()
            liquidado = '0'
            self.estornar_liquidar(pedido, liquidado)
        else:
            QMessageBox.about(self, "Erro", "Voce não tem direitos suficientes")

    def estornar_liquidar(self, pedido_input, liquidado):
        if liquidado == '1':
            acao = 'LIQUIDAR_ARQUIVO'
        else:
            acao = 'ESTORNAR_ARQUIVO'
        if pedido_input:
            feito = BDArquivos().estornar_liquidar_db(pedido_input, liquidado)
            if feito:
                BDArquivos().registrar_log(usuario, acao)
                self.atualiza_arvore(pedido_input)
                self.treeWidget.expandAll()
            else:
                if liquidado == '1':
                    QMessageBox.about(self, "Erro", "Orçamento ja está LIQUIDADO")
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

    """
    ############################################################
    ####################-----LOGIN-----#########################
    ############################################################
    """
    def log_in(self):
        global logado

        def fecha():
            global indice
            global atual
            global logado
            global direito
            global usuario
            usuario = pegar_usuario.get().upper()
            senha = pegar_senha.get()
            dominio = dominio_get
            if senha:
                resultado = BDArquivos().verificar_login_db(usuario, senha, dominio)
                if resultado:
                    direito = resultado[0]['direito']
                    logado = True
                    janela.destroy()
                else:
                    QMessageBox.about(self, "Login", "Informações erradas")
            else:
                QMessageBox.about(self, "Login", "Informações erradas")

        dominio_get = os.environ['USERDOMAIN']
        print(dominio_get)
        janela = Tk()
        janela.title("inserir Indice")

        app_width = 230
        app_height = 150
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x_pos = (screen_width / 2) - (app_width / 2)
        y_pos = (screen_height / 2) - (app_height / 2)
        janela.geometry(f'{app_width}x{app_height}+{int(x_pos)}+{int(y_pos)}')

        texto_usuario = Label(janela, text="Usuario:")
        texto_usuario.grid(column=0, row=0, padx=10, pady=10)
        pegar_usuario = Entry(janela, justify=CENTER)
        pegar_usuario.grid(column=1, row=0, padx=5, pady=10)
        pegar_usuario.focus_set()

        texto_senha = Label(janela, text="Senha:")
        texto_senha.grid(column=0, row=1, padx=10, pady=5)
        pegar_senha = Entry(janela, justify=CENTER, show='*')
        pegar_senha.grid(column=1, row=1, padx=5, pady=10)

        texto_computador_label = Label(janela, text="Dominio:")
        texto_computador_label.grid(column=0, row=2, padx=10, pady=5)
        texto_computador = Label(janela, text=dominio_get)
        texto_computador.grid(column=1, row=2, padx=10, pady=5)

        botao = Button(janela, text="      Login      ", command=fecha)
        botao.grid(column=1, row=3, padx=0, pady=5)
        janela.bind("<Return>", (lambda event: fecha()))

        janela.mainloop()
        if not logado:
            exit()


if __name__ == "__main__":
    qt = QApplication(sys.argv)
    pastas = Pastas()

    qtRectangle = pastas.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    pastas.move(qtRectangle.topLeft())

    pastas.show()
    qt.exec()
