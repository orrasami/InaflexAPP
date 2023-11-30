# 2.4 ANALISE OPS/OCS
from threading import Thread
from janelas.janela_analise_necessidade import Ui_analiseNecessidade
from PyQt5.QtWidgets import QMainWindow, QShortcut
from banco_de_dados_oracle import BDBohm
from PyQt5 import QtWidgets


class AnaliseNecessidade(QMainWindow, Ui_analiseNecessidade):
    def __init__(self, widget_analise_necessidade, bd_oracle_ok, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnAnalisar.clicked.connect(self.gerar_plano_de_fundo)
        self.tableOC.clicked.connect(self.selecionar_dados_oc)
        self.tableOC.itemSelectionChanged.connect(self.selecionar_dados_oc)
        self.tableOP.clicked.connect(self.selecionar_dados_op)
        self.tableOP.itemSelectionChanged.connect(self.selecionar_dados_op)
        if bd_oracle_ok == 'Falha':
            self.bd_oracle_ok = True
        else:
            self.bd_oracle_ok = False
        self.lista_itens_pedidos = []
        self.lista_itens_ops_materiais = []
        self.lista_itens_estoque_minimo = []
        self.lista_itens_ops_produtos = []
        self.lista_itens_oc = []
        self.lista_itens_estoque = []
        self.lista_oc = []
        self.lista_op = []
        self.labelCalculando.hide()
        self.refresh()

    def gerar_plano_de_fundo(self):
        daemon = Thread(target=self.atualizar, args=())
        daemon.daemon = True
        daemon.start()

    def refresh(self):
        self.tableOC.clear()
        self.tableOC.setColumnWidth(0, 170)
        self.tableOC.setColumnWidth(1, 100)
        self.tableOC.setHorizontalHeaderLabels(['ITEM', 'QTD'])
        self.tableOP.clear()
        self.tableOP.setColumnWidth(0, 170)
        self.tableOP.setColumnWidth(1, 100)
        self.tableOP.setHorizontalHeaderLabels(['ITEM', 'QTD'])
        self.tablePedido.clear()
        self.tablePedido.setColumnWidth(0, 170)
        self.tablePedido.setColumnWidth(1, 100)
        self.tablePedido.setHorizontalHeaderLabels(['PEDIDO', 'QTD'])
        self.tableOPmat.clear()
        self.tableOPmat.setColumnWidth(0, 170)
        self.tableOPmat.setColumnWidth(1, 100)
        self.tableOPmat.setHorizontalHeaderLabels(['OP', 'QTD'])
        self.tableEM.clear()
        self.tableEM.setColumnWidth(0, 270)
        self.tableEM.setHorizontalHeaderLabels(['ESTOQUE MINIMO'])
        self.tableCompra.clear()
        self.tableCompra.setColumnWidth(0, 170)
        self.tableCompra.setColumnWidth(1, 100)
        self.tableCompra.setHorizontalHeaderLabels(['OC', 'QTD'])
        self.tableOPprod.clear()
        self.tableOPprod.setColumnWidth(0, 170)
        self.tableOPprod.setColumnWidth(1, 100)
        self.tableOPprod.setHorizontalHeaderLabels(['OP', 'QTD'])
        self.tableEstoque.clear()
        self.tableEstoque.setColumnWidth(0, 270)
        self.tableEstoque.setHorizontalHeaderLabels(['ESTOQUE ATUAL'])

    def atualizar(self):
        self.labelCalculando.show()
        self.refresh()
        codigo = self.inputItem.text()
        self.lista_itens_pedidos, self.lista_itens_ops_materiais, self.lista_itens_estoque_minimo, \
        self.lista_itens_ops_produtos, self.lista_itens_oc, self.lista_itens_estoque, \
        self.lista_oc, self.lista_op = BDBohm().analisar_itens_pedidos(codigo)
        self.atualizar_tabela_oc(self.lista_oc)
        self.atualizar_tabela_op(self.lista_op)
        self.labelCalculando.hide()

    def atualizar_tabela_oc(self, lista):
        self.tableOC.clear()
        self.tableOC.setRowCount(0)
        row = 0
        self.tableOC.setRowCount(len(lista))
        if lista:
            for resultado in lista:
                item = resultado['item']
                quantidade = str("%.3f" % resultado['qtd'])
                self.tableOC.setItem(row, 0, QtWidgets.QTableWidgetItem(item))              # Item
                self.tableOC.setItem(row, 1, QtWidgets.QTableWidgetItem(quantidade))        # Item - Quantidade
                row += 1
        self.tableOC.setHorizontalHeaderLabels(['ITEM', 'QTD'])

    def atualizar_tabela_op(self, lista):
        self.tableOP.clear()
        self.tableOP.setRowCount(0)
        row = 0
        self.tableOP.setRowCount(len(lista))
        if lista:
            for resultado in lista:
                item = resultado['item']
                quantidade = str("%.3f" % resultado['qtd'])
                self.tableOP.setItem(row, 0, QtWidgets.QTableWidgetItem(item))              # Item
                self.tableOP.setItem(row, 1, QtWidgets.QTableWidgetItem(quantidade))        # Item - Quantidade
                row += 1
        self.tableOP.setHorizontalHeaderLabels(['ITEM', 'QTD'])

    def selecionar_dados_oc(self):
        if self.tableOC.currentRow() >= 0:
            row = self.tableOC.currentRow()
            item = self.tableOC.item(row, 0).text()
            self.preencher_pedido(item)
            self.preencher_op_material(item)
            self.preencher_estoque_minimo(item)
            self.preencher_compras(item)
            self.preencher_op_produto(item)
            self.preencher_estoque(item)

    def selecionar_dados_op(self):
        if self.tableOP.currentRow() >= 0:
            row = self.tableOP.currentRow()
            item = self.tableOP.item(row, 0).text()
            self.preencher_pedido(item)
            self.preencher_op_material(item)
            self.preencher_estoque_minimo(item)
            self.preencher_compras(item)
            self.preencher_op_produto(item)
            self.preencher_estoque(item)

    def preencher_pedido(self, item_pai):
        self.tablePedido.clear()
        self.tablePedido.setHorizontalHeaderLabels(['PEDIDO', 'QTD'])
        self.tablePedido.setRowCount(0)
        row = 0
        self.tablePedido.setRowCount(len(self.lista_itens_pedidos))
        if self.lista_itens_pedidos:
            for resultado in self.lista_itens_pedidos:
                pedido = str(resultado['pedido'])
                item = resultado['item']
                quantidade = str("%.3f" % resultado['qtd'])
                if item == item_pai:
                    self.tablePedido.setItem(row, 0, QtWidgets.QTableWidgetItem(pedido))            # Pedido
                    self.tablePedido.setItem(row, 1, QtWidgets.QTableWidgetItem(quantidade))        # Item - Quantidade
                    row += 1
        self.tablePedido.setRowCount(row)

    def preencher_op_material(self, item_pai):
        self.tableOPmat.clear()
        self.tableOPmat.setHorizontalHeaderLabels(['OP', 'QTD'])
        self.tableOPmat.setRowCount(0)
        row = 0
        self.tableOPmat.setRowCount(len(self.lista_itens_ops_materiais))
        if self.lista_itens_ops_materiais:
            for resultado in self.lista_itens_ops_materiais:
                pedido = str(resultado['op_material'])
                item = resultado['item']
                quantidade = str("%.3f" % resultado['qtd'])
                if item == item_pai:
                    self.tableOPmat.setItem(row, 0, QtWidgets.QTableWidgetItem(pedido))            # Pedido
                    self.tableOPmat.setItem(row, 1, QtWidgets.QTableWidgetItem(quantidade))        # Item - Quantidade
                    row += 1
        self.tableOPmat.setRowCount(row)

    def preencher_estoque_minimo(self, item_pai):
        self.tableEM.clear()
        self.tableEM.setHorizontalHeaderLabels(['ESTOQUE MINIMO'])
        self.tableEM.setRowCount(0)
        row = 0
        self.tableEM.setRowCount(len(self.lista_itens_estoque_minimo))
        if self.lista_itens_estoque_minimo:
            for resultado in self.lista_itens_estoque_minimo:
                item = resultado['item']
                quantidade = str("%.3f" % resultado['qtd'])
                if item == item_pai:
                    self.tableEM.setItem(row, 0, QtWidgets.QTableWidgetItem(quantidade))        # Item - Quantidade
                    row += 1
        self.tableEM.setRowCount(row)

    def preencher_compras(self, item_pai):
        self.tableCompra.clear()
        self.tableCompra.setHorizontalHeaderLabels(['OC', 'QTD'])
        self.tableCompra.setRowCount(0)
        row = 0
        self.tableCompra.setRowCount(len(self.lista_itens_oc))
        if self.lista_itens_oc:
            for resultado in self.lista_itens_oc:
                pedido = str(resultado['oc'])
                item = resultado['item']
                quantidade = str("%.3f" % resultado['qtd'])
                if item == item_pai:
                    self.tableCompra.setItem(row, 0, QtWidgets.QTableWidgetItem(pedido))            # Pedido
                    self.tableCompra.setItem(row, 1, QtWidgets.QTableWidgetItem(quantidade))        # Item - Quantidade
                    row += 1
        self.tableCompra.setRowCount(row)

    def preencher_op_produto(self, item_pai):
        self.tableOPprod.clear()
        self.tableOPprod.setHorizontalHeaderLabels(['OP', 'QTD'])
        self.tableOPprod.setRowCount(0)
        row = 0
        self.tableOPprod.setRowCount(len(self.lista_itens_ops_produtos))
        if self.lista_itens_ops_produtos:
            for resultado in self.lista_itens_ops_produtos:
                pedido = str(resultado['op_produto'])
                item = resultado['item']
                quantidade = str("%.3f" % resultado['qtd'])
                if item == item_pai:
                    self.tableOPprod.setItem(row, 0, QtWidgets.QTableWidgetItem(pedido))            # Pedido
                    self.tableOPprod.setItem(row, 1, QtWidgets.QTableWidgetItem(quantidade))        # Item - Quantidade
                    row += 1
        self.tableOPprod.setRowCount(row)

    def preencher_estoque(self, item_pai):
        self.tableEstoque.clear()
        self.tableEstoque.setHorizontalHeaderLabels(['ESTOQUE ATUAL'])
        self.tableEstoque.setRowCount(0)
        row = 0
        self.tableEstoque.setRowCount(len(self.lista_itens_estoque))
        if self.lista_itens_estoque:
            for resultado in self.lista_itens_estoque:
                item = resultado['item']
                quantidade = str("%.3f" % resultado['qtd'])
                if item == item_pai:
                    self.tableEstoque.setItem(row, 0, QtWidgets.QTableWidgetItem(quantidade))        # Item - Quantidade
                    row += 1
        self.tableEstoque.setRowCount(row)
