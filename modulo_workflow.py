# 1.4 WORKFLOW
from janelas.janela_workflow import *
from banco_de_dados_workflow import BDWorkflow
from banco_de_dados_arquivos import BDArquivos
from PyQt5.QtWidgets import QMainWindow, QShortcut, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore, QtWidgets
from datetime import datetime
from unidecode import unidecode

global atual
global pedido
global titulo
global indice


class Workflow(QMainWindow, Ui_workflow):
    def __init__(self, widget_workflow, resultado_login, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.tabWidget.setCurrentIndex(4)
        self.inputData.setDate(QtCore.QDate.currentDate())
        self.shortcut_procura = QShortcut(QKeySequence('return'), self)
        self.shortcut_procura.activated.connect(self.mostrar_dados)
        self.shortcut_procura_num = QShortcut(QKeySequence('enter'), self)
        self.shortcut_procura_num.activated.connect(self.mostrar_dados)
        self.tableWidgetHistorico.setColumnWidth(0, 268)
        self.tableWidgetHistorico.setColumnWidth(1, 80)
        self.tableWidgetEventos.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        delegate = AlignDelegate(self.tableWidgetEventos)
        self.tableWidgetHistorico.setItemDelegateForColumn(1, delegate)
        self.tableWidgetHistorico.setItemDelegateForColumn(2, delegate)
        self.tableWidgetEventos.clicked.connect(self.selecionar_dados)
        self.tableWidgetEventos.itemSelectionChanged.connect(self.selecionar_dados)
        self.tableWidgetEventos.setColumnWidth(0, 50)
        self.tableWidgetEventos.setColumnWidth(1, 50)
        self.tableWidgetEventos.setColumnWidth(2, 50)
        self.tableWidgetEventos.setColumnWidth(3, 100)
        self.tableWidgetEventos.setColumnWidth(4, 180)
        self.tableWidgetEventos.setColumnWidth(5, 50)
        self.tableWidgetEventos.setColumnWidth(6, 30)
        self.tableWidgetEventos.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        delegate = AlignDelegate(self.tableWidgetEventos)
        self.tableWidgetEventos.setItemDelegateForColumn(0, delegate)
        self.tableWidgetEventos.setItemDelegateForColumn(1, delegate)
        self.tableWidgetEventos.setItemDelegateForColumn(2, delegate)
        self.tableWidgetEventos.setItemDelegateForColumn(3, delegate)
        self.tableWidgetEventos.setItemDelegateForColumn(4, delegate)
        self.tableWidgetEventos.setItemDelegateForColumn(5, delegate)
        self.tableWidgetEventos.setItemDelegateForColumn(6, delegate)
        self.btnBuscar.clicked.connect(self.mostrar_dados)
        self.btnLimpar.clicked.connect(self.limpa_pesquisa)
        self.btnCriarEvento.clicked.connect(self.criar_evento)
        self.btnConcluirEtapa.clicked.connect(self.concluir_etapa)
        self.btnRetornarEtapa.clicked.connect(self.retornar_etapa)
        self.btnAdotar.clicked.connect(self.adotar_evento)
        self.btnAlterar.clicked.connect(self.alterar_evento)
        self.btnAtualizaExtra.clicked.connect(self.atualiza_extra)
        self.inputOrcamento.setPlaceholderText('Orçamento')
        self.inputOrcamentoEtapa.setPlaceholderText('Orcamento')
        self.inputOrcamentoNovo.setPlaceholderText('Orcamento')
        self.inputPedido.setPlaceholderText('Pedido')
        self.inputPedidoEtapa.setPlaceholderText('Pedido')
        self.inputPedidoNovo.setPlaceholderText('Pedido')
        self.inputEvento.setPlaceholderText('Evento')
        self.usuario_logado = resultado_login['nomeUsuario']
        self.dropdownUsuarios.setEditable(True)
        self.dropdownUsuarios.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.dropdownUsuarios.setCurrentIndex(0)
        self.criar_dropdown_usuarios()
        self.dropdownTipoEvento.setEditable(True)
        self.dropdownTipoEvento.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.dropdownTipoEvento.setCurrentIndex(0)
        self.dropdownTipoEventoNovo.setEditable(True)
        self.dropdownTipoEventoNovo.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.dropdownTipoEventoNovo.setCurrentIndex(0)
        self.dropdownTipoEventoAlterar.setEditable(True)
        self.dropdownTipoEventoAlterar.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.dropdownTipoEventoAlterar.setCurrentIndex(0)
        self.criar_dropdown_tipo_de_evento()
        self.mostrar_dados()

    def atualiza_extra(self):
        evento = self.labelEventoExtra.text()
        comentario = self.textComentarioExtra.toPlainText()
        orcamento = self.inputOrcamentoExtra.text()
        if self.checkEsperaExtra.isChecked():
            espera = 1
        else:
            espera = 0
        msg, mensagem = BDWorkflow().atualiza_extra_bd(evento, comentario, orcamento,
                                                       espera, self.usuario_logado)
        if msg:
            QMessageBox.about(self, "Erro", mensagem)
        self.textComentarioExtra.setText('')
        self.inputOrcamentoExtra.setText('')
        self.checkEsperaExtra.setChecked(False)
        self.mostrar_dados(evento)

    def alterar_evento(self):
        evento = self.labelEventoAlterar.text()
        estagio = self.labelEstagioAlterar.text()
        tipo_evento = self.labelTipoEventoAlterar.text()
        novo_tipo_evento = self.dropdownTipoEventoAlterar.currentText()
        if novo_tipo_evento != 'Selecionar Tipo de Evento' and evento and estagio and tipo_evento:
            if estagio == '0':
                BDWorkflow().alterar_evento(evento, novo_tipo_evento)
                self.dropdownTipoEventoAlterar.setCurrentIndex(0)
                self.mostrar_dados(evento)
            else:
                QMessageBox.about(self, "Erro", "Permitido alteração apenas para eventos no estagio ZERO")
        else:
            QMessageBox.about(self, "Erro", "Esta faltando informações")

    def adotar_evento(self):
        evento = self.labelEventoAdotar.text()
        tipo_evento = self.labelTipoEventoAdotar.text()
        estagio = self.labelEstagioAdotar.text()
        if evento and tipo_evento and estagio:
            msg, mensagem = BDWorkflow().adotar_evento(evento, tipo_evento, estagio, self.usuario_logado)
            if msg:
                QMessageBox.about(self, "Erro", mensagem)
        else:
            QMessageBox.about(self, "Erro", 'Selecionar EVENTO')
        self.mostrar_dados(evento)

    def concluir_etapa(self):
        evento = self.labelEventoEtapa.text()
        orcamento = self.inputOrcamentoEtapa.text()
        pedido_ = self.inputPedidoEtapa.text()
        comentario = unidecode(self.textComentario.toPlainText())
        etapa = self.labelEstagioEtapa.text()
        tipo_evento = self.labelTipoEventoEtapa.text()
        data_atual = datetime.now()
        if evento and comentario and tipo_evento and data_atual and etapa:
            # VERIFICA SE PEDIDO ESTA LIQUIDADO PELO APP
            if etapa == '3' and tipo_evento == 'GERAR PEDIDO':
                liquidado = BDArquivos().ver_se_liquidado(orcamento)
                if liquidado:
                    # RETORNA O VALOR DE LIQUIDADO NO BANCO DE DADOS
                    # SE FOR ZERO, NÃO PASSA PARA A PROXIMA ETAPA
                    # SE FOR 1, PASSA
                    liquidado = liquidado[0]['liquidado']
                else:
                    # LIQUIDADO = 0 NAO PASSA PARA A PROXIMA ETAPA
                    liquidado = '0'
            else:
                liquidado = '1'
            # SE LIQUIDADO = 1, CHAMA A PROXIMA FUNÇÃO
            if liquidado == '1':
                msg, mensagem = BDWorkflow().proxima_etapa(evento, orcamento, pedido_, comentario, self.usuario_logado,
                                                           etapa, tipo_evento)
                if msg:
                    QMessageBox.about(self, "Erro", mensagem)
            else:
                pass
        else:
            QMessageBox.about(self, "Erro", "falta Informações")
        self.labelEventoEtapa.setText('')
        self.inputOrcamentoEtapa.setText('')
        self.inputPedidoEtapa.setText('')
        self.textComentario.setText('')
        self.labelEstagioEtapa.setText('')
        self.labelTipoEventoEtapa.setText('')
        self.mostrar_dados(evento)

    def retornar_etapa(self):
        evento = self.labelEventoEtapa.text()
        comentario = unidecode(self.textComentario.toPlainText())
        etapa = self.labelEstagioEtapa.text()
        if evento and comentario and etapa:
            msg, mensagem = BDWorkflow().volta_etapa(evento, comentario, self.usuario_logado, etapa)
            if msg:
                QMessageBox.about(self, "Erro", mensagem)
        else:
            QMessageBox.about(self, "Erro", "falta Informações")
        self.labelEventoEtapa.setText('')
        self.textComentario.setText('')
        self.labelEstagioEtapa.setText('')
        self.mostrar_dados(evento)

    def criar_evento(self):
        tipo_evento = self.dropdownTipoEventoNovo.currentText()
        pedido_ = self.inputPedidoNovo.text()
        orcamento = self.inputOrcamentoNovo.text()
        if tipo_evento != 'Selecionar Tipo de Evento':
            msg, mensagem = BDWorkflow().criar_evento(tipo_evento, self.usuario_logado, pedido_, orcamento)
            if msg:
                QMessageBox.about(self, "Erro", mensagem)
            else:
                self.dropdownTipoEventoNovo.setCurrentIndex(0)
                self.inputOrcamentoNovo.setText('')
                self.inputPedidoNovo.setText('')
                self.inputPedido.setText(pedido_)
                self.inputOrcamento.setText(orcamento)
                self.dropdownUsuarios.setCurrentText(self.usuario_logado)
                self.dropdownTipoEvento.setCurrentText(tipo_evento)
                self.mostrar_dados()

    def limpa_pesquisa(self):
        self.inputOrcamento.setText('')
        self.inputPedido.setText('')
        self.inputEvento.setText('')
        self.dropdownUsuarios.setCurrentIndex(0)
        self.dropdownTipoEvento.setCurrentIndex(0)
        self.checkMinhasPendencias.setChecked(False)
        self.checkMeuEvento.setChecked(False)
        self.checkFinalizados.setChecked(False)
        self.inputData.setDate(QtCore.QDate.currentDate())
        self.checkEspera.setChecked(False)

    def criar_dropdown_usuarios(self):
        resultados = BDWorkflow().combobox_usuarios()
        self.dropdownUsuarios.addItem('Selecionar Usuarios')
        for resultado in resultados:
            self.dropdownUsuarios.addItem(resultado['nomeUsuario'])

    def criar_dropdown_tipo_de_evento(self):
        resultados = BDWorkflow().combobox_tipo_de_evento()
        self.dropdownTipoEvento.addItem('Selecionar Tipo de Evento')
        self.dropdownTipoEventoNovo.addItem('Selecionar Tipo de Evento')
        self.dropdownTipoEventoAlterar.addItem('Selecionar Tipo de Evento')
        for resultado in resultados:
            self.dropdownTipoEvento.addItem(resultado['tipoEvento'])
            self.dropdownTipoEventoNovo.addItem(resultado['tipoEvento'])
            self.dropdownTipoEventoAlterar.addItem(resultado['tipoEvento'])

    def mostrar_dados(self, evento=None):
        global pedido
        self.tableWidgetHistorico.setRowCount(0)
        self.tableWidgetHistorico.clear()
        data = self.inputData.date().toString('yyyy-MM-dd 23:23:00')
        m_pendencias = False
        m_eventos = False
        eu = self.usuario_logado
        if not evento:
            evento = self.inputEvento.text()
        tipodeevento = self.dropdownTipoEvento.currentText()
        if tipodeevento == 'Selecionar Tipo de Evento':
            tipodeevento = ''
        usuario = self.dropdownUsuarios.currentText()
        if usuario == 'Selecionar Usuarios':
            usuario = ''
        orcamento = self.inputOrcamento.text()
        pedido = self.inputPedido.text()
        if self.checkMinhasPendencias.isChecked():
            m_pendencias = True
        if self.checkMeuEvento.isChecked():
            m_eventos = True
        if self.checkFinalizados.isChecked():
            finalizados = 0
        else:
            finalizados = 1
        if self.checkEspera.isChecked():
            espera = 1
        else:
            espera = 0
        resultados = BDWorkflow().mostrar_eventos_db(finalizados, data, eu, evento, tipodeevento, usuario, orcamento,
                                                     pedido, m_pendencias, m_eventos, espera)
        row = 0
        self.tableWidgetEventos.setRowCount(len(resultados))
        for resultado in resultados:
            self.tableWidgetEventos.setItem(row, 0, QtWidgets.QTableWidgetItem(str(resultado['id'])))
            self.tableWidgetEventos.setItem(row, 1, QtWidgets.QTableWidgetItem(str(resultado['numOrc'])))
            self.tableWidgetEventos.setItem(row, 2, QtWidgets.QTableWidgetItem(str(resultado['numPed'])))
            self.tableWidgetEventos.setItem(row, 3, QtWidgets.QTableWidgetItem(resultado['usuario']))
            self.tableWidgetEventos.setItem(row, 4, QtWidgets.QTableWidgetItem(resultado['tipoEvento']))
            self.tableWidgetEventos.setItem(row, 5, QtWidgets.QTableWidgetItem(str(resultado['estagio'])))
            self.tableWidgetEventos.setItem(row, 6, QtWidgets.QTableWidgetItem(str(resultado['espera'])))
            row += 1
        self.tableWidgetHistorico.setHorizontalHeaderLabels(['COMENTARIOS', 'USUARIO', 'DATA'])

    def selecionar_dados(self):
        global pedido
        row = self.tableWidgetEventos.currentRow()
        if row >= 0:
            evento = self.tableWidgetEventos.item(row, 0).text()
            orcamento = self.tableWidgetEventos.item(row, 1).text()
            pedido = self.tableWidgetEventos.item(row, 2).text()
            tipo_evento = self.tableWidgetEventos.item(row, 4).text()
            estagio = self.tableWidgetEventos.item(row, 5).text()
            espera = self.tableWidgetEventos.item(row, 6).text()
            if orcamento == '0':
                orcamento = ''
            if pedido == '0':
                pedido = ''
            self.labelEventoEtapa.setText(evento)
            self.labelEventoAdotar.setText(evento)
            self.labelEventoAlterar.setText(evento)
            self.labelEventoExtra.setText(evento)
            self.labelTipoEventoEtapa.setText(tipo_evento)
            self.labelTipoEventoAdotar.setText(tipo_evento)
            self.labelTipoEventoAlterar.setText(tipo_evento)
            self.labelTipoEventoExtra.setText(tipo_evento)
            self.labelEstagioEtapa.setText(estagio)
            self.labelEstagioAdotar.setText(estagio)
            self.labelEstagioAlterar.setText(estagio)
            self.labelEstagioExtra.setText(estagio)
            self.inputOrcamentoEtapa.setText(orcamento)
            self.inputOrcamentoExtra.setText(orcamento)
            self.inputPedidoEtapa.setText(pedido)
            if espera == '1':
                self.checkEsperaExtra.setChecked(True)
            else:
                self.checkEsperaExtra.setChecked(False)
            resultados = BDWorkflow().seleciona_comentarios(evento)
            row = 0
            self.tableWidgetHistorico.setRowCount(len(resultados))
            for resultado in resultados:
                comentario_corrigido = resultado['comentario']
                try:
                    comentario_corrigido = comentario_corrigido
                except:
                    pass
                self.tableWidgetHistorico.setWordWrap(True)
                self.tableWidgetHistorico.setItem(row, 0, QtWidgets.QTableWidgetItem(comentario_corrigido))
                self.tableWidgetHistorico.setItem(row, 1, QtWidgets.QTableWidgetItem(str(resultado['logUsuario'])))
                self.tableWidgetHistorico.setItem(row, 2, QtWidgets.QTableWidgetItem(str(resultado['logData'])))
                self.tableWidgetHistorico.resizeRowsToContents()
                row += 1


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
