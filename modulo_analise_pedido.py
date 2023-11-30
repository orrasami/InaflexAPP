# NADA - FOI UM ESTUDO ANTERIOR QUE EU MANTIVE PARA HISTORICO
from janelas.janela_analise_pedido import Ui_analisePedido
from PyQt5.QtWidgets import QMainWindow, QShortcut
from PyQt5.QtGui import QKeySequence
from banco_de_dados_oracle import BDBohm
from PyQt5 import QtWidgets
import ast
import re


class AnalisePedido(QMainWindow, Ui_analisePedido):
    def __init__(self, widget_analise_pedido, bd_oracle_ok, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.shortcut_procura = QShortcut(QKeySequence('return'), self)
        self.shortcut_procura.activated.connect(self.atualizar_dados)
        self.shortcut_procura_num = QShortcut(QKeySequence('enter'), self)
        self.shortcut_procura_num.activated.connect(self.atualizar_dados)
        self.tableWidget.setColumnWidth(0, 210)     # Item
        self.tableWidget.setColumnWidth(1, 40)      # Item - Quantidade
        self.tableWidget.setColumnWidth(2, 0)       # Item - Indice
        self.tableWidget.setColumnWidth(3, 0)       # Item - Posicao
        self.tableWidget.setColumnWidth(4, 0)       # OP/OC - É OP ou é OC
        self.tableWidget.setColumnWidth(5, 0)       # Vinc. - SIM ou ''
        self.tableWidget.setColumnWidth(6, 0)       # Vinc. - Lista de Valores
        self.tableWidget.setColumnWidth(7, 70)      # Vinc. - Quantidade de Itens
        self.tableWidget.setColumnWidth(8, 70)      # OP/OC - Quantidade de Itens
        self.tableWidget.setColumnWidth(9, 0)       # OP/OC - Lista de Valores
        self.tableWidget.setColumnWidth(10, 0)       # OP/OC - Lista de Valores
        self.tableWidget.setColumnWidth(11, 70)       # OP/OC - Valor
        self.tableWidget.setColumnWidth(12, 70)       # Item - Preco Venda
        self.tableWidget.setColumnWidth(13, 70)       # Item - Data Entrega
        self.tableWidget.setColumnWidth(14, 0)       # Item - IPI
        self.tableWidget.setColumnWidth(15, 0)       # Item - ICMS
        self.tableWidget.setColumnWidth(16, 0)       # Item - Pis
        self.tableWidget.setColumnWidth(17, 0)       # Item - Cofins
        self.tableWidget.setColumnWidth(18, 70)       # Item - Estoque
        self.tableWidget.setColumnWidth(19, 70)       # Item - Saldo
        self.tableWidget.setColumnWidth(20, 70)       # Item - Demanda
        self.tableWidget.setColumnWidth(21, 0)       # Item - Demanda - Ops Ocs
        self.tableWidget_2.setColumnWidth(0, 70)
        self.tableWidget_2.setColumnWidth(1, 50)
        self.tableWidget_2.setColumnWidth(2, 94)
        self.tableWidget_3.setColumnWidth(0, 70)
        self.tableWidget_3.setColumnWidth(1, 50)
        self.tableWidget_3.setColumnWidth(2, 94)
        self.tableWidget_4.setColumnWidth(0, 70)
        self.tableWidget_4.setColumnWidth(1, 50)
        self.tableWidget_4.setColumnWidth(2, 94)
        self.tableWidget_5.setColumnWidth(0, 70)
        self.tableWidget_5.setColumnWidth(1, 50)
        self.tableWidget_5.setColumnWidth(2, 94)
        self.tableWidget_6.setColumnWidth(0, 70)
        self.tableWidget_6.setColumnWidth(1, 50)
        self.tableWidget_6.setColumnWidth(2, 94)
        self.tableWidget.clicked.connect(self.selecionar_dados)
        self.tableWidget.itemSelectionChanged.connect(self.selecionar_dados)
        self.tableWidget.setHorizontalHeaderLabels(['ITEM', 'QTD', '', '', '', '', '', 'QTD', 'QTD', '', '',
                                                    'CUSTO', 'PRECO', 'ENTREGA', '', '', '', '',
                                                    'SALDO', 'ESTOQUE', 'DEMANDA', ''])
        self.checkRentabilidade.clicked.connect(self.selecionar_dados)
        self.btnAnalisar.clicked.connect(self.atualizar_dados)
        self.checkFormula.setChecked(True)
        self.checkOpOc.setChecked(True)
        self.checkOpOcPedido.setChecked(True)
        self.checkCustos.setChecked(True)
        self.inputPedido.setText('22751')
        self.limpa_tela()
        if bd_oracle_ok == 'Falha':
            self.bd_oracle_ok = True
        else:
            self.bd_oracle_ok = False

    def atualizar_dados(self):
        pedido = self.inputPedido.text()
        if not self.bd_oracle_ok:
            if self.checkFormula.isChecked():
                self.atualizar_formula(pedido, True)
            else:
                self.atualizar_formula(pedido, False)
            if self.checkOpOc.isChecked():
                self.atualizar_op_oc(pedido)
            if self.checkOpOcPedido.isChecked():
                self.atualizar_dedicadas(pedido)
            if self.checkCustos.isChecked():
                self.atualizar_custos(pedido)
                self.atualizar_estoque(pedido)
                self.demanda(pedido)
                self.rentabilidade()

    def atualizar_tabela(self, lista):
        row = 0
        self.tableWidget.setRowCount(len(lista))
        if lista:
            for resultado in lista:
                espaco = '_'
                indice = str(resultado['indice'])
                n = 3 * int(indice)
                item = espaco * n + resultado['item']
                quantidade = str(resultado['quantidade'])
                posicao = str(resultado['posicao'])
                preco_venda = str(resultado['preco_venda'])
                data_entrega = str(resultado['data_entrega'])
                ipi = str(resultado['ipi'])
                icms = str(resultado['icms'])
                pis = str(resultado['pis'])
                cofins = str(resultado['cofins'])
                try:
                    qtdd_oc_op = str(resultado['qtdd_oc_op'])
                except:
                    qtdd_oc_op = ''
                try:
                    qtdd_item_oc_op = str(resultado['qtdd_item_oc_op'])
                except:
                    qtdd_item_oc_op = ''
                if qtdd_item_oc_op == '':
                    qtdd_item_oc_op_saldo = 0
                else:
                    qtdd_item_oc_op_saldo = int(resultado['qtdd_item_oc_op'])
                try:
                    oc_op = str(resultado['oc_op'])
                except:
                    oc_op = ''
                try:
                    conteudo_oc_op = str(resultado['conteudo_oc_op'])
                except:
                    conteudo_oc_op = ''
                try:
                    dedicada = str(resultado['dedicada'])
                except:
                    dedicada = ''
                try:
                    dedicada_oc_op = str(resultado['dedicada_oc_op'])
                except:
                    dedicada_oc_op = ''
                try:
                    dedicada_qtd = str(resultado['dedicada_qtd'])
                except:
                    dedicada_qtd = ''
                try:
                    valor = str(resultado['valor'])
                except:
                    valor = ''
                try:
                    estoque = str(resultado['estoque'])
                except:
                    estoque = ''
                if estoque == '':
                    estoque_saldo = 0
                else:
                    estoque_saldo = int(resultado['estoque'])
                try:
                    demanda = str(resultado['demanda'])
                except:
                    demanda = ''
                if demanda == '':
                    demanda_saldo = 0
                else:
                    demanda_saldo = int(resultado['demanda'])
                try:
                    demanda_oc_op = str(resultado['demanda_oc_op'])
                except:
                    demanda_oc_op = ''
                try:
                    saldo = str(estoque_saldo + qtdd_item_oc_op_saldo - demanda_saldo)
                except:
                    saldo = ''
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(item))              # Item
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(quantidade))        # Item - Quantidade
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(indice))            # Item - Indice
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(posicao))           # Item - Posicao
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(oc_op))             # OP/OC - É OP ou é OC
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(dedicada))          # Vinc. - SIM ou ''
                self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(dedicada_oc_op))    # Vinc. - Lista de Valores
                self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(dedicada_qtd))      # Vinc. - Quantidade de Itens
                self.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(qtdd_item_oc_op))   # OP/OC - Quantidade de Itens
                self.tableWidget.setItem(row, 9, QtWidgets.QTableWidgetItem(qtdd_oc_op))        # OP/OC - Quantidade OPs e OCs
                self.tableWidget.setItem(row, 10, QtWidgets.QTableWidgetItem(conteudo_oc_op))   # OP/OC - Lista de Valores
                self.tableWidget.setItem(row, 11, QtWidgets.QTableWidgetItem(valor))            # OP/OC - Valor
                self.tableWidget.setItem(row, 12, QtWidgets.QTableWidgetItem(preco_venda))      # Item - Preco Venda
                self.tableWidget.setItem(row, 13, QtWidgets.QTableWidgetItem(data_entrega))     # Item - data de Entrega
                self.tableWidget.setItem(row, 14, QtWidgets.QTableWidgetItem(ipi))              # Item - Ipi
                self.tableWidget.setItem(row, 15, QtWidgets.QTableWidgetItem(icms))             # Item - Icms
                self.tableWidget.setItem(row, 16, QtWidgets.QTableWidgetItem(pis))              # Item - Pis
                self.tableWidget.setItem(row, 17, QtWidgets.QTableWidgetItem(cofins))           # Item - Cofins
                self.tableWidget.setItem(row, 18, QtWidgets.QTableWidgetItem(saldo))            # Item - Saldo
                self.tableWidget.setItem(row, 19, QtWidgets.QTableWidgetItem(estoque))          # Item - Estoque
                self.tableWidget.setItem(row, 20, QtWidgets.QTableWidgetItem(demanda))          # Item - Demanda
                self.tableWidget.setItem(row, 21, QtWidgets.QTableWidgetItem(demanda_oc_op))    # Item - Demanda - Oc Op
                row += 1

    def cria_lista_pela_tabela(self):
        lista = []
        tamanho = self.tableWidget.rowCount()
        for i in range(tamanho):
            dic = {}
            item = self.tableWidget.item(i, 0).text()
            dic['item'] = re.sub('_', '', item)
            dic['quantidade'] = self.tableWidget.item(i, 1).text()
            dic['indice'] = self.tableWidget.item(i, 2).text()
            dic['posicao'] = self.tableWidget.item(i, 3).text()
            dic['oc_op'] = self.tableWidget.item(i, 4).text()
            dic['dedicada'] = self.tableWidget.item(i, 5).text()
            dic['dedicada_oc_op'] = self.tableWidget.item(i, 6).text()
            dic['dedicada_qtd'] = self.tableWidget.item(i, 7).text()
            dic['qtdd_item_oc_op'] = self.tableWidget.item(i, 8).text()
            dic['qtdd_oc_op'] = self.tableWidget.item(i, 9).text()
            dic['conteudo_oc_op'] = self.tableWidget.item(i, 10).text()
            dic['valor'] = self.tableWidget.item(i, 11).text()
            dic['preco_venda'] = self.tableWidget.item(i, 12).text()
            dic['data_entrega'] = self.tableWidget.item(i, 13).text()
            dic['ipi'] = self.tableWidget.item(i, 14).text()
            dic['icms'] = self.tableWidget.item(i, 15).text()
            dic['pis'] = self.tableWidget.item(i, 16).text()
            dic['cofins'] = self.tableWidget.item(i, 17).text()
            dic['estoque'] = self.tableWidget.item(i, 18).text()
            dic['saldo'] = self.tableWidget.item(i, 19).text()
            dic['demanda'] = self.tableWidget.item(i, 20).text()
            dic['demanda_oc_op'] = self.tableWidget.item(i, 21).text()
            lista.append(dic)
        return lista

    def atualizar_formula(self, pedido, formula):
        if pedido != '':
            lista = BDBohm().itens_do_pedido(pedido, formula)
            self.atualizar_tabela(lista)

    def atualizar_op_oc(self, pedido):
        if pedido != '':
            lista = self.cria_lista_pela_tabela()
            lista = BDBohm().itens_oc_op(lista)
            self.atualizar_tabela(lista)

    def atualizar_dedicadas(self, pedido):
        if pedido != '':
            lista = self.cria_lista_pela_tabela()
            lista = BDBohm().oc_op_dedicadas(lista, pedido)
            self.atualizar_tabela(lista)

    def atualizar_custos(self, pedido):
        if pedido != '':
            lista = self.cria_lista_pela_tabela()
            lista = BDBohm().itens_custo(lista)
            self.atualizar_tabela(lista)

    def atualizar_estoque(self, pedido):
        if pedido != '':
            lista = self.cria_lista_pela_tabela()
            lista = BDBohm().estoque_final_codigo(lista)
            self.atualizar_tabela(lista)

    def demanda(self, pedido):
        if pedido != '':
            lista = self.cria_lista_pela_tabela()
            lista = BDBohm().demanda(lista)
            self.atualizar_tabela(lista)

    def selecionar_dados(self):
        if self.tableWidget.currentRow() >= 0:
            self.limpa_tela()
            row = self.tableWidget.currentRow()
            op_oc = self.tableWidget.item(row, 4).text()
            dedicada = self.tableWidget.item(row, 5).text()
            dedicada_op_oc = self.tableWidget.item(row, 6).text()
            conteudo_op_oc = self.tableWidget.item(row, 10).text()
            demanda_op_oc = self.tableWidget.item(row, 21).text()
            try:
                dedicada_op_oc = ast.literal_eval(dedicada_op_oc)
            except:
                dedicada_op_oc = []
            try:
                conteudo_op_oc = ast.literal_eval(conteudo_op_oc)
            except:
                conteudo_op_oc = []
            try:
                demanda_op_oc = ast.literal_eval(demanda_op_oc)
            except:
                demanda_op_oc = []
            if op_oc == 'OC':
                self.labelOc.show()
                self.tableWidget_4.show()
                self.atualizar_tabela_oc(conteudo_op_oc)
                if dedicada == 'SIM':
                    self.labelOcPedido.show()
                    self.tableWidget_2.show()
                    self.atualizar_tabela_oc_dedicada(dedicada_op_oc)
            if op_oc == 'OP':
                self.labelOp.show()
                self.tableWidget_5.show()
                self.atualizar_tabela_op(conteudo_op_oc)
                if dedicada == 'SIM':
                    self.labelOpPedido.show()
                    self.tableWidget_3.show()
                    self.atualizar_tabela_op_dedicada(dedicada_op_oc)
            if demanda_op_oc:
                self.labelDemanda.show()
                self.tableWidget_6.show()
                self.atualizar_tabela_demanda(demanda_op_oc)
        self.rentabilidade()

    def atualizar_tabela_demanda(self, lista):
        row = 0
        self.tableWidget_6.setHorizontalHeaderLabels(['DOC', 'QTD', 'STATUS'])
        self.tableWidget_6.setRowCount(len(lista))
        if lista:
            for resultado in lista:
                self.tableWidget_6.setItem(row, 0, QtWidgets.QTableWidgetItem(str(resultado['op'])))
                self.tableWidget_6.setItem(row, 1, QtWidgets.QTableWidgetItem(str(resultado['qtd'])))
                self.tableWidget_6.setItem(row, 2, QtWidgets.QTableWidgetItem(resultado['status']))
                row += 1

    def atualizar_tabela_oc_dedicada(self, lista):
        row = 0
        self.tableWidget_2.setHorizontalHeaderLabels(['OC', 'QTD', 'DATA'])
        self.tableWidget_2.setRowCount(len(lista))
        if lista:
            for resultado in lista:
                self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(resultado['oc'])))
                self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(resultado['qtd'])))
                self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(resultado['data']))
                row += 1

    def atualizar_tabela_op_dedicada(self, lista):
        row = 0
        self.tableWidget_3.setHorizontalHeaderLabels(['OP', 'QTD', 'STATUS'])
        self.tableWidget_3.setRowCount(len(lista))
        if lista:
            for resultado in lista:
                self.tableWidget_3.setItem(row, 0, QtWidgets.QTableWidgetItem(str(resultado['op'])))
                self.tableWidget_3.setItem(row, 1, QtWidgets.QTableWidgetItem(str(resultado['qtd'])))
                self.tableWidget_3.setItem(row, 2, QtWidgets.QTableWidgetItem(resultado['status']))
                row += 1

    def atualizar_tabela_oc(self, lista):
        row = 0
        self.tableWidget_4.setHorizontalHeaderLabels(['OC', 'QTD', 'DATA'])
        self.tableWidget_4.setRowCount(len(lista))
        if lista:
            for resultado in lista:
                self.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(resultado['oc'])))
                self.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(resultado['quantidade'])))
                self.tableWidget_4.setItem(row, 2, QtWidgets.QTableWidgetItem(str(resultado['data_entrega'])))
                row += 1

    def atualizar_tabela_op(self, lista):
        row = 0
        self.tableWidget_5.setHorizontalHeaderLabels(['OP', 'QTD', 'STATUS'])
        self.tableWidget_5.setRowCount(len(lista))
        if lista:
            for resultado in lista:
                self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(resultado['op'])))
                self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(resultado['quantidade'])))
                self.tableWidget_5.setItem(row, 2, QtWidgets.QTableWidgetItem(resultado['status']))
                row += 1

    def limpa_tela(self):
        self.labelOc.hide()
        self.labelOp.hide()
        self.labelDemanda.hide()
        self.labelOcPedido.hide()
        self.labelOpPedido.hide()
        self.tableWidget_2.hide()
        self.tableWidget_3.hide()
        self.tableWidget_4.hide()
        self.tableWidget_5.hide()
        self.tableWidget_6.hide()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_2.clear()
        self.tableWidget_3.clear()
        self.tableWidget_4.clear()
        self.tableWidget_5.clear()
        self.tableWidget_6.clear()

    def rentabilidade(self):
        preco = 0
        custo = 0
        ipi = 0
        icms = 0
        pis = 0
        cofins = 0
        if not self.checkRentabilidade.isChecked():
            lista = self.cria_lista_pela_tabela()
            for item in lista:
                try:
                    preco = preco + float(item['preco_venda'])
                    custo = custo + float(item['valor'])
                    ipi = ipi + float(item['ipi'])
                    icms = icms + float(item['icms'])
                    pis = pis + float(item['pis'])
                    cofins = cofins + float(item['cofins'])
                except:
                    pass
        else:
            i = self.tableWidget.currentRow()
            try:
                preco = float(self.tableWidget.item(i, 12).text())
                custo = float(self.tableWidget.item(i, 11).text())
                ipi = float(self.tableWidget.item(i, 14).text())
                icms = float(self.tableWidget.item(i, 15).text())
                pis = float(self.tableWidget.item(i, 16).text())
                cofins = float(self.tableWidget.item(i, 17).text())
            except:
                pass
        if preco == 0:
            self.labelValorComIpi.setText(str("%.2f" % 0))
            self.labelIPI.setText(str("%.2f" % 0))
            self.labelIPI_2.setText(str("%.2f" % 0))
            self.labelValorSemIpi.setText(str("%.2f" % 0))
            self.labelCusto.setText(str("%.2f" % 0))
            self.labelIcms.setText(str("%.2f" % 0))
            self.labelIcms_2.setText(str("%.2f" % 0))
            self.labelCofins.setText(str("%.2f" % 0))
            self.labelCofins_2.setText(str("%.2f" % 0))
            self.labelPis.setText(str("%.2f" % 0))
            self.labelPis_2.setText(str("%.2f" % 0))
            self.inputDespesasAdm.setText('21')
            self.labelDespesasAdm.setText(str("%.2f" % 0))
            self.inputDespesasCom.setText('17')
            self.labelDespesasCom.setText(str("%.2f" % 0))
            self.inputComissao.setText('6')
            self.labelComissao.setText(str("%.2f" % 0))
            self.labelLucroLiquido.setText(str("%.2f" % 0))
            self.labelLucroLiquido_2.setText(str("%.2f" % 0))
        else:
            self.labelValorComIpi.setText(str("%.2f" % (preco + ipi)))
            self.labelIPI.setText(str("%.2f" % ipi))
            self.labelIPI_2.setText(str("%.2f" % ((((preco + ipi)/preco)-1)*100)))
            self.labelValorSemIpi.setText(str("%.2f" % preco))
            self.labelCusto.setText(str("%.2f" % custo))
            self.labelIcms.setText(str("%.2f" % icms))
            self.labelIcms_2.setText(str("%.2f" % ((icms/preco)*100)))
            self.labelCofins.setText(str("%.2f" % cofins))
            self.labelCofins_2.setText(str("%.2f" % ((cofins/preco)*100)))
            self.labelPis.setText(str("%.2f" % pis))
            self.labelPis_2.setText(str("%.2f" % ((pis/preco)*100)))
            self.inputDespesasAdm.setText('21')
            despesas_adm = (float(self.inputDespesasAdm.text())/100) * preco
            self.labelDespesasAdm.setText(str("%.2f" % despesas_adm))
            self.inputDespesasCom.setText('17')
            despesas_com = (float(self.inputDespesasCom.text())/100) * preco
            self.labelDespesasCom.setText(str("%.2f" % despesas_com))
            self.inputComissao.setText('6')
            comissao = (float(self.inputComissao.text())/100) * preco
            self.labelComissao.setText(str("%.2f" % comissao))
            self.labelLucroLiquido.setText(str("%.2f" % (preco - custo - icms - pis - cofins - despesas_adm -
                                                         despesas_com - comissao)))
            self.labelLucroLiquido_2.setText(str("%.2f" % (((preco - custo - icms - pis - cofins - despesas_adm -
                                                             despesas_com - comissao)/preco)*100)))
