# 2.3 SELECT
from janelas.janela_select import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from banco_de_dados_oracle import BDBohm
from banco_de_dados_workflow import BDWorkflow
import xlsxwriter
import json
import re
from os.path import exists

path_download = ''
with open('setup.json', 'r') as file:
    d1_json = file.read()
    d1_json = json.loads(d1_json)

for x, y in d1_json.items():
    path_download = y['relatorio']


class Select(QMainWindow, Ui_Select):
    def __init__(self, widget_select, bd_oracle_ok, nome_usuario, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnGerar.clicked.connect(self.gerar_relatorio)
        self.btnSalvar.clicked.connect(self.salvar)
        self.btnApagar.clicked.connect(self.apagar)
        self.dropdownNome.currentIndexChanged.connect(self.selecionar_select)
        self.nome_usuario = nome_usuario
        self.dropdownNome.setEditable(True)
        self.dropdownNome.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.dropdownNome.setCurrentIndex(0)
        self.criar_dropdown_nome()

        if bd_oracle_ok == 'Falha':
            self.bd_oracle_ok = False
        else:
            self.bd_oracle_ok = True

    def apagar(self):
        rm = QMessageBox.question(self, '', "Tem certeza que deseja EXCLUIR esse SELECT?",
                                  QMessageBox.Yes | QMessageBox.No)
        if rm == 16384:
            nome = self.dropdownNome.currentText()
            self. inputNome.setText('')
            self.textEdit.setText('')
            self.dropdownNome.setCurrentIndex(0)
            msg, mensagem = BDWorkflow().apagar_select(nome, self.nome_usuario)
            if msg:
                QMessageBox.about(self, "Info", mensagem)
            self.dropdownNome.clear()
            self.criar_dropdown_nome()

    def criar_dropdown_nome(self):
        resultados = BDWorkflow().combobox_select(self.nome_usuario)
        self.dropdownNome.addItem('Selecionar Select')
        if resultados:
            for resultado in resultados:
                self.dropdownNome.addItem(resultado['nome'])

    def selecionar_select(self):
        self. inputNome.setText('')
        self.textEdit.setText('')
        nome = self.dropdownNome.currentText()
        if nome != 'Selecionar Select' and nome != '':
            select, msg, mensagem = BDWorkflow().selecionar_select(nome, self.nome_usuario)
            if msg:
                QMessageBox.about(self, "Info", mensagem)
            else:
                if select:
                    self.textEdit.setText(select)
                else:
                    self.textEdit.setText('')

    def salvar(self):
        select = self.textEdit.toPlainText()
        nome = self.inputNome.text()
        if select and nome:
            msg, mensagem = BDWorkflow().salva_select(nome, select, self.nome_usuario)
            self.dropdownNome.clear()
            self.criar_dropdown_nome()
            QMessageBox.about(self, "Info", mensagem)
            if msg:
                self.dropdownNome.setCurrentText(nome)
                self.selecionar_select()
            else:
                self.dropdownNome.setCurrentIndex(0)

    def gerar_relatorio(self):
        if self.bd_oracle_ok:
            consulta = self.textEdit.toPlainText()
            consulta = re.sub(r'\n', r' ', consulta)
            res = consulta.split()
            colunas = []
            for item in res:
                item = re.sub(r',', r'', item)
                item = re.sub(r'INAFLEX.', r'', item)
                item = item.upper()
                if item == 'FROM':
                    break
                elif item == 'AS':
                    colunas.pop()
                    pass
                elif item == 'SELECT':
                    pass
                else:
                    colunas.append(item)

            try:
                resultados = BDBohm().select(consulta)
                if resultados:
                    nome = ''
                    num = 1
                    nome_check = True
                    while nome_check == True:
                        nome = f'\select{num}'
                        nome_check = exists(path_download + nome + '.xlsx')
                        num += 1
                    i = 0
                    workbook = xlsxwriter.Workbook(f'{path_download}{nome}.xlsx')
                    worksheet = workbook.add_worksheet('Relatorio')
                    while i < len(colunas):
                        worksheet.write(0, i, colunas[i])
                        i += 1
                    row = 1
                    for resultado in resultados:
                        i = 0
                        while i < len(colunas):
                            worksheet.write(row, i, resultado[i])
                            i += 1
                        row += 1
                    workbook.close()
                    QMessageBox.about(self, "Sucesso", f"Relatório {nome}.xlsx criado")
                else:
                    QMessageBox.about(self, "Erro", "Sem dados até o momento")
            except:
                QMessageBox.about(self, "Erro", "Erro no select")
