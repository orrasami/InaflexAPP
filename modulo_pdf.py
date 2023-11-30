# 2.1 PDF
import PyPDF2
from janelas.janela_pdf import Ui_pdfMerger
from PyQt5.QtWidgets import QMainWindow, QListWidget, QAbstractItemView, QShortcut, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QPixmap
from pdf2image import convert_from_path
import os
from PIL import Image
# IMPORTS APENAS PARA STAND-ALONE
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import sys


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(60, 60)
        self.setGeometry(20, 70, 500, 410)
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
        self.shortcut_procura = QShortcut(QKeySequence('delete'), self)
        self.shortcut_procura.activated.connect(self.deletar)
        self.listview.itemSelectionChanged.connect(self.visualizar)
        self.checkVisualizar.clicked.connect(self.visualizar)
        self.btnAntiHorario.clicked.connect(self.antihorario)
        self.btnHorario.clicked.connect(self.horario)
        self.btnDesproteger.clicked.connect(self.desproteger)
        self.btnSeparar.clicked.connect(self.split)
        self.checkProteger.clicked.connect(self.proteger_check)

    def split(self):
        try:
            itematual = self.listview.currentItem().text()
            with open(itematual, 'rb') as infile:
                reader = PyPDF2.PdfFileReader(infile)
                writer = PyPDF2.PdfFileWriter()
                i = self.inputPagInicial.text()
                f = self.inputPagFinal.text()
                try:
                    i = int(i) - 1
                    f = int(f) - 1
                    if f > len(reader.pages):
                        QMessageBox.about(self, "Erro", f"Pagina final deve ser menor que {len(reader.pages)}!")
                        return
                    if i > len(reader.pages):
                        QMessageBox.about(self, "Erro", f"Pagina inicial deve ser menor que {len(reader.pages)}!")
                        return
                    if i < 0:
                        QMessageBox.about(self, "Erro", f"Pagina inicial deve ser maior que 0")
                        return
                    while i <= f:
                        writer.addPage(reader.getPage(i))
                        i += 1
                    with open(itematual[:len(itematual)-4] + '_split.pdf', 'wb') as outfile:
                        writer.write(outfile)
                        QMessageBox.about(self, "Sucesso", "Arquivo gerado!")
                except:
                    QMessageBox.about(self, "Erro", "Numero da pagina deve ser inteiro!")
        except:
            QMessageBox.about(self, "Erro", "Selecionar arquivo!")

    def desproteger(self):
        try:
            itematual = self.listview.currentItem().text()
            password = self.inputSenha.text()
            with open(itematual, 'rb') as input_file, open(itematual[:len(itematual)-4] + '_temp', 'wb') as output_file:
                reader = PyPDF2.PdfFileReader(input_file)
                reader.decrypt(password)
                writer = PyPDF2.PdfFileWriter()
                for i in range(reader.getNumPages()):
                    writer.addPage(reader.getPage(i))
                writer.write(output_file)
                input_file.close()
                output_file.close()
                os.remove(itematual)
                os.rename(itematual[:len(itematual) - 4] + '_temp', itematual)
                QMessageBox.about(self, "Sucesso", "Senha removida!")
        except:
            QMessageBox.about(self, "Erro", "Senha errada!")

    def proteger_check(self):
        if self.inputSenha.text():
            pass
        else:
            QMessageBox.about(self, "Senha", "Senha em Branco")
            self.checkProteger.setChecked(False)

    def proteger(self, path):
        password = self.inputSenha.text()
        itematual = path + '/novo.pdf'
        pdf_in_file = open(itematual, 'rb')

        inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
        pages_no = inputpdf.numPages
        output = PyPDF2.PdfFileWriter()

        for i in range(pages_no):
            inputpdf = PyPDF2.PdfFileReader(pdf_in_file)

            output.addPage(inputpdf.getPage(i))
            output.encrypt(password)

            with open(itematual[:len(itematual)-4] + '_temp', "wb") as outputStream:
                output.write(outputStream)

        pdf_in_file.close()

        os.remove(itematual)
        os.rename(itematual[:len(itematual) - 4] + '_temp', itematual)

    def antihorario(self):
        angulo = 270
        self.rotacionar(angulo)

    def horario(self):
        angulo = 90
        self.rotacionar(angulo)

    def rotacionar(self, angulo):
        itematual = self.listview.currentItem().text()

        pdf_in = open(itematual, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_in)
        pdf_writer = PyPDF2.PdfFileWriter()

        for pagenum in range(pdf_reader.numPages):
            page = pdf_reader.getPage(pagenum)
            page.rotateClockwise(angulo)
            pdf_writer.addPage(page)

        pdf_out = open(itematual[:len(itematual)-4] + '_temp', 'wb')
        pdf_writer.write(pdf_out)
        pdf_out.close()
        pdf_in.close()

        os.remove(itematual)
        os.rename(itematual[:len(itematual)-4] + '_temp', itematual)

        self.checkVisualizar.setChecked(True)
        self.visualizar()

    def visualizar(self):
        if self.checkVisualizar.isChecked():
            try:
                itematual = self.listview.currentItem().text()
                images = convert_from_path(itematual, 20)
                images[0].save(itematual + '_thumbnail' + '.jpg', 'JPEG')
                image_path = itematual + '_thumbnail' + '.jpg'
                image = QPixmap(image_path)
                thumb = image.scaledToWidth(191)
                self.labelView.setPixmap(thumb)
                os.remove(image_path)
            except:
                self.labelView.setText('Não é possivel Visualizar')

    def deletar(self):
        list_items = self.listview.selectedItems()
        if not list_items:
            return
        for item in list_items:
            self.listview.takeItem(self.listview.row(item))

    def deletar_todos(self):
        self.listview.clear()

    def move_baixo(self):
        self.checkVisualizar.setChecked(False)
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
        self.checkVisualizar.setChecked(False)
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
        path = ''
        novo_pdf = PyPDF2.PdfFileMerger()
        lista = self.cria_lista()
        for item in lista:
            arquivo_pdf = open(item, 'rb')
            novo_pdf.append(arquivo_pdf)
            path = os.path.dirname(item)
        with open(path + '/novo.pdf', 'wb') as meu_novo_pdf:
            novo_pdf.write(meu_novo_pdf)
        if self.checkSuperProteger.isChecked():
            self.super_proteger(path)
        if self.checkProteger.isChecked():
            self.proteger(path)
        QMessageBox.about(self, "Sucesso", "Arquivo gerado")

    def super_proteger(self, path):
        novo_pdf = PyPDF2.PdfFileMerger()
        itematual = path + '/novo.pdf'
        images = convert_from_path(itematual)
        for i in range(len(images)):
            images[i].save(itematual[:len(itematual)-4] + '_pagina' + str(i) + '.jpg', 'JPEG')

        for i in range(len(images)):
            image = Image.open(itematual[:len(itematual)-4] + '_pagina' + str(i) + '.jpg')
            im = image.convert('RGB')
            im.save(itematual[:len(itematual)-4] + '_pagina' + str(i) + '.pdf')

        os.remove(path + '/novo.pdf')
        lista = []
        for i in range(len(images)):
            path_file = itematual[:len(itematual)-4] + '_pagina' + str(i) + '.pdf'
            lista.append(path_file)

        for item in lista:
            arquivo_pdf = open(item, 'rb')
            novo_pdf.append(arquivo_pdf)
            path = os.path.dirname(item)
            arquivo_pdf.close()

        with open(path + '/novo.pdf', 'wb') as meu_novo_pdf:
            novo_pdf.write(meu_novo_pdf)

        for i in range(len(images)):
            os.remove(itematual[:len(itematual)-4] + '_pagina' + str(i) + '.pdf')
            os.remove(itematual[:len(itematual)-4] + '_pagina' + str(i) + '.jpg')


if __name__ == "__main__":
    qt = QApplication(sys.argv)

    # Janela PDF
    widget_pdf = QtWidgets.QStackedWidget()
    janela_pdf = PdfMerger(widget_pdf)
    widget_pdf.addWidget(janela_pdf)
    widget_pdf.setFixedSize(748, 555)
    widget_pdf.show()

    qt.exec()
