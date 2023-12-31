# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'incluir_pedido.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_telaIncluirPedido(object):
    def setupUi(self, telaIncluirPedido):
        telaIncluirPedido.setObjectName("telaIncluirPedido")
        telaIncluirPedido.resize(749, 281)
        self.labelErro = QtWidgets.QLabel(telaIncluirPedido)
        self.labelErro.setGeometry(QtCore.QRect(0, 0, 751, 51))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.labelErro.setFont(font)
        self.labelErro.setStyleSheet("QLabel {\n"
"    color: white;\n"
"}")
        self.labelErro.setAlignment(QtCore.Qt.AlignCenter)
        self.labelErro.setObjectName("labelErro")
        self.btnIncluirPedidoTela = QtWidgets.QPushButton(telaIncluirPedido)
        self.btnIncluirPedidoTela.setGeometry(QtCore.QRect(40, 210, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnIncluirPedidoTela.setFont(font)
        self.btnIncluirPedidoTela.setStyleSheet("QPushButton {\n"
"    border-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;\n"
"}")
        self.btnIncluirPedidoTela.setObjectName("btnIncluirPedidoTela")
        self.inputIncluirPedido = QtWidgets.QLineEdit(telaIncluirPedido)
        self.inputIncluirPedido.setGeometry(QtCore.QRect(40, 89, 113, 31))
        self.inputIncluirPedido.setStyleSheet("QLineEdit {\n"
"    border-top-right-radius: 10px;\n"
"    border-top-left-radius: 10px;\n"
"    border: 1px solid #CDC99B;\n"
"}")
        self.inputIncluirPedido.setAlignment(QtCore.Qt.AlignCenter)
        self.inputIncluirPedido.setObjectName("inputIncluirPedido")
        self.inputIncluirIndice = QtWidgets.QLineEdit(telaIncluirPedido)
        self.inputIncluirIndice.setGeometry(QtCore.QRect(40, 119, 113, 31))
        self.inputIncluirIndice.setStyleSheet("QLineEdit {\n"
"    border-bottom-right-radius: 10px;\n"
"    border-bottom-left-radius: 10px;\n"
"    border: 1px solid #CDC99B;\n"
"}")
        self.inputIncluirIndice.setAlignment(QtCore.Qt.AlignCenter)
        self.inputIncluirIndice.setObjectName("inputIncluirIndice")
        self.checkIncluirAtual = QtWidgets.QCheckBox(telaIncluirPedido)
        self.checkIncluirAtual.setGeometry(QtCore.QRect(140, 170, 91, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkIncluirAtual.setFont(font)
        self.checkIncluirAtual.setStyleSheet("QLineEdit {\n"
"    border-top-right-radius: 10px;\n"
"    border-top-left-radius: 10px;\n"
"    border: 1px solid #CDC99B;\n"
"}")
        self.checkIncluirAtual.setObjectName("checkIncluirAtual")
        self.label = QtWidgets.QLabel(telaIncluirPedido)
        self.label.setGeometry(QtCore.QRect(160, 100, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(telaIncluirPedido)
        self.label_2.setGeometry(QtCore.QRect(160, 130, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(telaIncluirPedido)
        self.label_3.setGeometry(QtCore.QRect(280, 70, 451, 191))
        self.label_3.setStyleSheet("QLabel {\n"
"    background-color: rgb(188, 188, 188);\n"
"    border-radius: 15px;\n"
"}")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(telaIncluirPedido)
        self.label_4.setGeometry(QtCore.QRect(-4, -8, 761, 61))
        self.label_4.setStyleSheet("QLabel {\n"
"    background-color: #CDC99B;\n"
"}")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(telaIncluirPedido)
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit.setGeometry(QtCore.QRect(290, 130, 211, 121))
        self.plainTextEdit.setStyleSheet("QPlainTextEdit {\n"
"    background-color: rgb(0, 0, 0, 0);\n"
"    border: 0px;\n"
"}")
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setBackgroundVisible(False)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(telaIncluirPedido)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(510, 130, 211, 121))
        self.plainTextEdit_2.setStyleSheet("QPlainTextEdit {\n"
"    border-top-right-radius: 10px;\n"
"    border-bottom-right-radius: 10px;\n"
"}")
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.label_5 = QtWidgets.QLabel(telaIncluirPedido)
        self.label_5.setGeometry(QtCore.QRect(280, 70, 451, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("QLabel {\n"
"    border: 1px solid #CDC99B;\n"
"    border-top-right-radius: 15px;\n"
"    border-top-left-radius: 15px;\n"
"}\n"
"")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_4.raise_()
        self.labelErro.raise_()
        self.btnIncluirPedidoTela.raise_()
        self.inputIncluirPedido.raise_()
        self.inputIncluirIndice.raise_()
        self.checkIncluirAtual.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.plainTextEdit.raise_()
        self.plainTextEdit_2.raise_()
        self.label_5.raise_()

        self.retranslateUi(telaIncluirPedido)
        QtCore.QMetaObject.connectSlotsByName(telaIncluirPedido)

    def retranslateUi(self, telaIncluirPedido):
        _translate = QtCore.QCoreApplication.translate
        telaIncluirPedido.setWindowTitle(_translate("telaIncluirPedido", "INCLUIR PEDIDO"))
        self.labelErro.setText(_translate("telaIncluirPedido", "Incluir Pedido"))
        self.btnIncluirPedidoTela.setText(_translate("telaIncluirPedido", "Incluir"))
        self.checkIncluirAtual.setText(_translate("telaIncluirPedido", "Arquivo"))
        self.label.setText(_translate("telaIncluirPedido", "Pedido"))
        self.label_2.setText(_translate("telaIncluirPedido", "Indice"))
        self.plainTextEdit.setPlainText(_translate("telaIncluirPedido", "1 - ONONON\n"
"2 - PEDIDO DO CLIENTE\n"
"3 - NONONON\n"
"4 - SDLSKDJFSLDJ\n"
"5 - ODMSD DKSLDFKSD\n"
"6 - DESENHO, CORQUIS, PIT\n"
"7 - REQUISICAO DO CLIENTE\n"
"8 - ORCAMENTO INAFLEX"))
        self.plainTextEdit_2.setPlainText(_translate("telaIncluirPedido", "1 - ONONON\n"
"2 - PEDIDO DO CLIENTE\n"
"3 - NONONON\n"
"4 - SDLSKDJFSLDJ\n"
"5 - ODMSD DKSLDFKSD\n"
"6 - DESENHO, CORQUIS, PIT\n"
"7 - REQUISICAO DO CLIENTE\n"
"8 - ORCAMENTO INAFLEX"))
        self.label_5.setText(_translate("telaIncluirPedido", "LEGENDA"))
