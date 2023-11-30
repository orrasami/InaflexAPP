# 2.2 DEMANDA POR ITEM
from threading import Thread
from janelas.janela_demanda import Ui_demanda
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from banco_de_dados_oracle import BDBohm


class Demanda(QMainWindow, Ui_demanda):
    def __init__(self, widget_relatorios, bd_oracle_ok, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnPegarDados.clicked.connect(self.gerar_plano_de_fundo)
        self.inputDataInicial.setDate(QDate(2021, 1, 1))
        self.inputDataFinal.setDate(QDate(2022, 12, 31))
        self.inputCodigo.setText('')
        self.labelCalculando.hide()
        if bd_oracle_ok == 'Falha':
            self.bd_oracle_ok = True
        else:
            self.bd_oracle_ok = False

    def gerar_plano_de_fundo(self):
        daemon = Thread(target=self.atualizar_dados, args=())
        daemon.daemon = True
        daemon.start()

    def atualizar_dados(self):
        if not self.bd_oracle_ok:
            self.labelCalculando.show()
            lista_itens = []
            lista = []
            item = self.inputCodigo.text()
            data_inicial = self.inputDataInicial.date().toString("dd/MM/yyyy")
            data_final = self.inputDataFinal.date().toString("dd/MM/yyyy")
            lista_itens.append(item)
            lista_itens, lista_completa = BDBohm().calcular_demanda(lista_itens, lista)
            lista_orcamento_unico = lista_completa.copy()
            lista_orcamento_ics = lista_completa.copy()
            lista_pedido = lista_completa.copy()
            lista_estoque = lista_completa[0].copy()
            orcamentos_unico, quantidade_orcamentos_unico = \
                BDBohm().demanda_oracamento_unico(lista_orcamento_unico, data_inicial, data_final)
            orcamentos_ics, quantidade_orcamentos_ics = \
                BDBohm().demanda_oracamento_ics(lista_orcamento_ics, data_inicial, data_final)
            quantidade_orcamentos_item = quantidade_orcamentos_ics + quantidade_orcamentos_unico
            quantidade_orcamentos = orcamentos_ics + orcamentos_unico
            quantidade_pedidos, quantidade_pedidos_item = \
                BDBohm().demanda_pedido(lista_pedido, data_inicial, data_final)
            total_comprado, total_importado, total_fabricado = BDBohm().demanda_estoque(lista_estoque, data_inicial, data_final)
            estoque_inicial = BDBohm().estoque_inicial(lista_estoque, data_inicial, data_final)
            estoque_final = BDBohm().estoque_final(lista_estoque)
            movimentado = (estoque_final - estoque_inicial) + (total_comprado + total_importado + total_fabricado)
            self.labelOrcamentos.setText(str(quantidade_orcamentos))
            self.labelPedidos.setText(str(quantidade_pedidos))
            self.labelComprado.setText(str(total_comprado))
            self.labelImportado.setText(str(total_importado))
            self.labelFabricado.setText(str(total_fabricado))
            self.labelEInicial.setText(str(estoque_inicial))
            self.labelEFinal.setText(str(estoque_final))
            self.labelOrcado.setText(str(quantidade_orcamentos_item))
            self.labelVendido.setText(str(quantidade_pedidos_item))
            self.labelMovimentado.setText(str(movimentado))
            self.labelCalculando.hide()
        else:
            QMessageBox.about(self, "Erro", "Erro conexão Oracle")
