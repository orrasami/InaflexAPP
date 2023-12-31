# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'janelas\janela_entregas.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Entregas(object):
    def setupUi(self, Entregas):
        Entregas.setObjectName("Entregas")
        Entregas.resize(790, 381)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("janelas\\../static/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Entregas.setWindowIcon(icon)
        self.inputPedido = QtWidgets.QLineEdit(Entregas)
        self.inputPedido.setGeometry(QtCore.QRect(480, 88, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.inputPedido.setFont(font)
        self.inputPedido.setStyleSheet("border-radius: 10px;\n"
"border: 1px solid #CDC99B;")
        self.inputPedido.setAlignment(QtCore.Qt.AlignCenter)
        self.inputPedido.setReadOnly(False)
        self.inputPedido.setClearButtonEnabled(False)
        self.inputPedido.setObjectName("inputPedido")
        self.label_3 = QtWidgets.QLabel(Entregas)
        self.label_3.setGeometry(QtCore.QRect(393, 95, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.btnSelecionarPedido = QtWidgets.QPushButton(Entregas)
        self.btnSelecionarPedido.setEnabled(True)
        self.btnSelecionarPedido.setGeometry(QtCore.QRect(640, 88, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnSelecionarPedido.setFont(font)
        self.btnSelecionarPedido.setStyleSheet("    border-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;")
        self.btnSelecionarPedido.setObjectName("btnSelecionarPedido")
        self.inputCliente = QtWidgets.QLineEdit(Entregas)
        self.inputCliente.setGeometry(QtCore.QRect(480, 126, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.inputCliente.setFont(font)
        self.inputCliente.setStyleSheet("border-radius: 10px;\n"
"border: 1px solid #CDC99B;")
        self.inputCliente.setAlignment(QtCore.Qt.AlignCenter)
        self.inputCliente.setReadOnly(True)
        self.inputCliente.setClearButtonEnabled(False)
        self.inputCliente.setObjectName("inputCliente")
        self.label_8 = QtWidgets.QLabel(Entregas)
        self.label_8.setGeometry(QtCore.QRect(393, 132, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.btnEnviarFaturamento = QtWidgets.QPushButton(Entregas)
        self.btnEnviarFaturamento.setEnabled(True)
        self.btnEnviarFaturamento.setGeometry(QtCore.QRect(390, 320, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnEnviarFaturamento.setFont(font)
        self.btnEnviarFaturamento.setStyleSheet("    border-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: orange;\n"
"    color: white;")
        self.btnEnviarFaturamento.setObjectName("btnEnviarFaturamento")
        self.label_2 = QtWidgets.QLabel(Entregas)
        self.label_2.setGeometry(QtCore.QRect(370, 68, 401, 301))
        self.label_2.setStyleSheet("background: rgb(223, 223, 223); border-radius: 15px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.btnAtualizarInfo = QtWidgets.QPushButton(Entregas)
        self.btnAtualizarInfo.setEnabled(True)
        self.btnAtualizarInfo.setGeometry(QtCore.QRect(480, 205, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnAtualizarInfo.setFont(font)
        self.btnAtualizarInfo.setStyleSheet("    border-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;")
        self.btnAtualizarInfo.setObjectName("btnAtualizarInfo")
        self.tableWidget = QtWidgets.QTableWidget(Entregas)
        self.tableWidget.setGeometry(QtCore.QRect(20, 68, 331, 301))
        self.tableWidget.setStyleSheet("QHeaderView::section\n"
"{\n"
"background-color:black;\n"
"color: white;\n"
"border: 1px solid #CDC99B;\n"
"font-size:12px;\n"
"}")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(190, 190, 190))
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.label_12 = QtWidgets.QLabel(Entregas)
        self.label_12.setGeometry(QtCore.QRect(0, 10, 791, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: white;")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.label_10 = QtWidgets.QLabel(Entregas)
        self.label_10.setGeometry(QtCore.QRect(10, 10, 31, 31))
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap("janelas\\../static/apple-touch-icon.png"))
        self.label_10.setScaledContents(True)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Entregas)
        self.label_11.setGeometry(QtCore.QRect(0, -10, 1071, 61))
        self.label_11.setStyleSheet("background: black;")
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.label_9 = QtWidgets.QLabel(Entregas)
        self.label_9.setGeometry(QtCore.QRect(383, 170, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.inputData = QtWidgets.QDateEdit(Entregas)
        self.inputData.setGeometry(QtCore.QRect(479, 167, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.inputData.setFont(font)
        self.inputData.setStyleSheet("border-radius: 10px;\n"
"border: 1px solid #CDC99B;")
        self.inputData.setFrame(True)
        self.inputData.setAlignment(QtCore.Qt.AlignCenter)
        self.inputData.setReadOnly(False)
        self.inputData.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.inputData.setObjectName("inputData")
        self.btnEnviarFaturado = QtWidgets.QPushButton(Entregas)
        self.btnEnviarFaturado.setEnabled(True)
        self.btnEnviarFaturado.setGeometry(QtCore.QRect(390, 280, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnEnviarFaturado.setFont(font)
        self.btnEnviarFaturado.setStyleSheet("    border-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: rgb(0,200,100);\n"
"    color: white;")
        self.btnEnviarFaturado.setObjectName("btnEnviarFaturado")
        self.checkClienteRetira = QtWidgets.QCheckBox(Entregas)
        self.checkClienteRetira.setGeometry(QtCore.QRect(395, 253, 151, 17))
        self.checkClienteRetira.setObjectName("checkClienteRetira")
        self.label_11.raise_()
        self.label_2.raise_()
        self.inputPedido.raise_()
        self.label_3.raise_()
        self.btnSelecionarPedido.raise_()
        self.inputCliente.raise_()
        self.label_8.raise_()
        self.btnEnviarFaturamento.raise_()
        self.btnAtualizarInfo.raise_()
        self.tableWidget.raise_()
        self.label_12.raise_()
        self.label_10.raise_()
        self.label_9.raise_()
        self.inputData.raise_()
        self.btnEnviarFaturado.raise_()
        self.checkClienteRetira.raise_()

        self.retranslateUi(Entregas)
        QtCore.QMetaObject.connectSlotsByName(Entregas)
        Entregas.setTabOrder(self.inputPedido, self.inputCliente)
        Entregas.setTabOrder(self.inputCliente, self.btnAtualizarInfo)
        Entregas.setTabOrder(self.btnAtualizarInfo, self.btnEnviarFaturamento)
        Entregas.setTabOrder(self.btnEnviarFaturamento, self.tableWidget)
        Entregas.setTabOrder(self.tableWidget, self.btnSelecionarPedido)

    def retranslateUi(self, Entregas):
        _translate = QtCore.QCoreApplication.translate
        Entregas.setWindowTitle(_translate("Entregas", "FATURAMENTO"))
        self.label_3.setText(_translate("Entregas", "Pedido:"))
        self.btnSelecionarPedido.setText(_translate("Entregas", "Buscar"))
        self.label_8.setText(_translate("Entregas", "Cliente:"))
        self.btnEnviarFaturamento.setText(_translate("Entregas", "Voltar para Faturamento"))
        self.btnAtualizarInfo.setText(_translate("Entregas", "Atualizar Informacao"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Entregas", "PEDIDO"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Entregas", "DATA"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Entregas", "CLIENTE"))
        self.label_12.setText(_translate("Entregas", "SISTEMA INTERNO INAFLEX - SII - MODULO ENTREGAS"))
        self.label_9.setText(_translate("Entregas", "Entrega:"))
        self.btnEnviarFaturado.setText(_translate("Entregas", "Finalizar Pedido"))
        self.checkClienteRetira.setText(_translate("Entregas", "Cliente Retira"))
