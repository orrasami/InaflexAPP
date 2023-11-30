import PyPDF2
from janelas.janela_pdf import Ui_pdfMerger
from PyQt5.QtWidgets import QMainWindow, QListWidget, QAbstractItemView, QShortcut, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(60, 60)
        self.setGeometry(20, 70, 500, 330)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            link = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    link.append(str(url.toLocalFile()))
                else:
                    link.append(str(url.toString()))
            self.addItems(link)
        else:
            event.ignore()


class PdfMerger(QMainWindow, Ui_pdfMerger):
    def __init__(self, widget_pdf, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.listview = ListBoxWidget(self)
        self.listview.setUpdatesEnabled(True)
        self.btnJuntar.clicked.connect(lambda: self.junta_pdf())
        self.btnSobe.clicked.connect(lambda: self.move_cima())
        self.btnDesce.clicked.connect(lambda: self.move_baixo())
        self.btnApagar.clicked.connect(lambda: self.deletar())
        self.btnApagarTodos.clicked.connect(lambda: self.deletar_todos())
        self.shortcut_procura = QShortcut(QKeySequence('up'), self)
        self.shortcut_procura.activated.connect(self.move_cima)
        self.shortcut_procura = QShortcut(QKeySequence('down'), self)
        self.shortcut_procura.activated.connect(self.move_baixo)
        self.shortcut_procura = QShortcut(QKeySequence('delete'), self)
        self.shortcut_procura.activated.connect(self.deletar)

    def deletar(self):
        list_items = self.listview.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.listview.takeItem(self.listview.row(item))

    def deletar_todos(self):
        self.listview.clear()

    def move_baixo(self):
        itens_texto = []
        linhaatual = 0
        itens = self.listview.selectedItems()
        lista = self.cria_lista()
        qtdd_itens = len(itens)
        qtdd_lista = len(lista)
        for i in range(qtdd_itens):
            item = itens[i].text()
            for n in range(qtdd_lista):
                if item == lista[n]:
                    if linhaatual < n:
                        linhaatual = n
        for m in range(qtdd_itens):
            if linhaatual == qtdd_lista - 1:
                pass
            else:
                self.listview.setCurrentRow(linhaatual)
                itematual = self.listview.currentItem().text()
                itens_texto.append(itematual)
                del lista[linhaatual]
                lista.insert(linhaatual + 1, itematual)
                linhaatual -= 1
        self.listview.clear()
        self.mostrar_lista(lista)
        for i in itens_texto:
            matching_items = self.listview.findItems(i, Qt.MatchExactly)
            for item in matching_items:
                item.setSelected(True)

    def move_cima(self):
        itens_texto = []
        linhaatual = 10000000
        itens = self.listview.selectedItems()
        lista = self.cria_lista()
        qtdd_itens = len(itens)
        qtdd_lista = len(lista)
        for i in range(qtdd_itens):
            item = itens[i].text()
            for n in range(qtdd_lista):
                if item == lista[n]:
                    if linhaatual > n:
                        linhaatual = n
        for m in range(qtdd_itens):
            if linhaatual != 0:
                self.listview.setCurrentRow(linhaatual)
                itematual = self.listview.currentItem().text()
                itens_texto.append(itematual)
                del lista[linhaatual]
                lista.insert(linhaatual - 1, itematual)
                linhaatual += 1
        self.listview.clear()
        self.mostrar_lista(lista)
        for i in itens_texto:
            matching_items = self.listview.findItems(i, Qt.MatchExactly)
            for item in matching_items:
                item.setSelected(True)

    def mostrar_lista(self, lista):
        self.listview.addItems(lista)

    def cria_lista(self):
        lista = []
        row = 0
        item = 'inicio'
        while item:
            self.listview.setCurrentRow(row)
            if self.listview.currentItem():
                item = self.listview.currentItem().text()
            else:
                item = ''
            if item:
                lista.append(item)
            row += 1
        return lista

    def junta_pdf(self):
        novo_pdf = PyPDF2.PdfFileMerger()
        lista = self.cria_lista()
        for item in lista:
            arquivo_pdf = open(item, 'rb')
            novo_pdf.append(arquivo_pdf)
        with open(r'c:\Download\novo.pdf', 'wb') as meu_novo_pdf:
            novo_pdf.write(meu_novo_pdf)
        QMessageBox.about(self, "Sucesso", "Arquivo gerado")
