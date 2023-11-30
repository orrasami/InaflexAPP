# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'janelas/janela_demanda.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_demanda(object):
    def setupUi(self, demanda):
        demanda.setObjectName("demanda")
        demanda.resize(569, 420)
        self.label_16 = QtWidgets.QLabel(demanda)
        self.label_16.setGeometry(QtCore.QRect(-9, -10, 1071, 61))
        self.label_16.setStyleSheet("background: black;")
        self.label_16.setText("")
        self.label_16.setObjectName("label_16")
        self.label_14 = QtWidgets.QLabel(demanda)
        self.label_14.setGeometry(QtCore.QRect(11, 10, 31, 31))
        self.label_14.setText("")
        self.label_14.setPixmap(QtGui.QPixmap("janelas\\../static/apple-touch-icon.png"))
        self.label_14.setScaledContents(True)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(demanda)
        self.label_15.setGeometry(QtCore.QRect(100, 10, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("color: white;")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.inputDataFinal = QtWidgets.QDateEdit(demanda)
        self.inputDataFinal.setGeometry(QtCore.QRect(170, 140, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.inputDataFinal.setFont(font)
        self.inputDataFinal.setStyleSheet("border-radius: 10px;\n"
"border: 1px solid #CDC99B;")
        self.inputDataFinal.setFrame(True)
        self.inputDataFinal.setAlignment(QtCore.Qt.AlignCenter)
        self.inputDataFinal.setReadOnly(False)
        self.inputDataFinal.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.inputDataFinal.setObjectName("inputDataFinal")
        self.label_3 = QtWidgets.QLabel(demanda)
        self.label_3.setGeometry(QtCore.QRect(0, 145, 161, 21))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(demanda)
        self.label_4.setGeometry(QtCore.QRect(0, 105, 161, 31))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.inputDataInicial = QtWidgets.QDateEdit(demanda)
        self.inputDataInicial.setGeometry(QtCore.QRect(170, 105, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.inputDataInicial.setFont(font)
        self.inputDataInicial.setStyleSheet("border-radius: 10px;\n"
"border: 1px solid #CDC99B;")
        self.inputDataInicial.setFrame(True)
        self.inputDataInicial.setAlignment(QtCore.Qt.AlignCenter)
        self.inputDataInicial.setReadOnly(False)
        self.inputDataInicial.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.inputDataInicial.setObjectName("inputDataInicial")
        self.inputCodigo = QtWidgets.QLineEdit(demanda)
        self.inputCodigo.setGeometry(QtCore.QRect(170, 70, 271, 31))
        self.inputCodigo.setStyleSheet("border-radius: 10px;\n"
"border: 1px solid #CDC99B;")
        self.inputCodigo.setAlignment(QtCore.Qt.AlignCenter)
        self.inputCodigo.setObjectName("inputCodigo")
        self.line_4 = QtWidgets.QFrame(demanda)
        self.line_4.setGeometry(QtCore.QRect(10, 180, 551, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.btnPegarDados = QtWidgets.QPushButton(demanda)
        self.btnPegarDados.setEnabled(True)
        self.btnPegarDados.setGeometry(QtCore.QRect(20, 370, 531, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnPegarDados.setFont(font)
        self.btnPegarDados.setStyleSheet("    border-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;")
        self.btnPegarDados.setObjectName("btnPegarDados")
        self.label_5 = QtWidgets.QLabel(demanda)
        self.label_5.setGeometry(QtCore.QRect(0, 75, 161, 21))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(demanda)
        self.label.setGeometry(QtCore.QRect(20, 210, 171, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(demanda)
        self.label_2.setGeometry(QtCore.QRect(20, 230, 171, 16))
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(demanda)
        self.label_6.setGeometry(QtCore.QRect(20, 250, 171, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(demanda)
        self.label_7.setGeometry(QtCore.QRect(20, 270, 171, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(demanda)
        self.label_8.setGeometry(QtCore.QRect(20, 290, 171, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(demanda)
        self.label_9.setGeometry(QtCore.QRect(20, 310, 171, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(demanda)
        self.label_10.setGeometry(QtCore.QRect(20, 330, 171, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(demanda)
        self.label_11.setGeometry(QtCore.QRect(300, 210, 171, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(demanda)
        self.label_12.setGeometry(QtCore.QRect(300, 230, 171, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(demanda)
        self.label_13.setGeometry(QtCore.QRect(300, 330, 171, 16))
        self.label_13.setObjectName("label_13")
        self.line = QtWidgets.QFrame(demanda)
        self.line.setGeometry(QtCore.QRect(263, 190, 20, 161))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.labelOrcamentos = QtWidgets.QLabel(demanda)
        self.labelOrcamentos.setGeometry(QtCore.QRect(160, 208, 101, 20))
        self.labelOrcamentos.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelOrcamentos.setObjectName("labelOrcamentos")
        self.labelPedidos = QtWidgets.QLabel(demanda)
        self.labelPedidos.setGeometry(QtCore.QRect(160, 228, 101, 20))
        self.labelPedidos.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelPedidos.setObjectName("labelPedidos")
        self.labelComprado = QtWidgets.QLabel(demanda)
        self.labelComprado.setGeometry(QtCore.QRect(160, 248, 101, 20))
        self.labelComprado.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelComprado.setObjectName("labelComprado")
        self.labelImportado = QtWidgets.QLabel(demanda)
        self.labelImportado.setGeometry(QtCore.QRect(160, 268, 101, 20))
        self.labelImportado.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelImportado.setObjectName("labelImportado")
        self.labelFabricado = QtWidgets.QLabel(demanda)
        self.labelFabricado.setGeometry(QtCore.QRect(160, 288, 101, 20))
        self.labelFabricado.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelFabricado.setObjectName("labelFabricado")
        self.labelEInicial = QtWidgets.QLabel(demanda)
        self.labelEInicial.setGeometry(QtCore.QRect(160, 308, 101, 20))
        self.labelEInicial.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelEInicial.setObjectName("labelEInicial")
        self.labelEFinal = QtWidgets.QLabel(demanda)
        self.labelEFinal.setGeometry(QtCore.QRect(160, 328, 101, 20))
        self.labelEFinal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelEFinal.setObjectName("labelEFinal")
        self.labelOrcado = QtWidgets.QLabel(demanda)
        self.labelOrcado.setGeometry(QtCore.QRect(430, 208, 121, 20))
        self.labelOrcado.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelOrcado.setObjectName("labelOrcado")
        self.labelVendido = QtWidgets.QLabel(demanda)
        self.labelVendido.setGeometry(QtCore.QRect(430, 228, 121, 20))
        self.labelVendido.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelVendido.setObjectName("labelVendido")
        self.labelMovimentado = QtWidgets.QLabel(demanda)
        self.labelMovimentado.setGeometry(QtCore.QRect(430, 328, 121, 20))
        self.labelMovimentado.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelMovimentado.setObjectName("labelMovimentado")
        self.labelCalculando = QtWidgets.QLabel(demanda)
        self.labelCalculando.setGeometry(QtCore.QRect(-10, 50, 591, 371))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.labelCalculando.setFont(font)
        self.labelCalculando.setStyleSheet("background: rgb(188, 188, 188, 210)")
        self.labelCalculando.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCalculando.setObjectName("labelCalculando")

        self.retranslateUi(demanda)
        QtCore.QMetaObject.connectSlotsByName(demanda)
        demanda.setTabOrder(self.inputCodigo, self.inputDataInicial)
        demanda.setTabOrder(self.inputDataInicial, self.inputDataFinal)
        demanda.setTabOrder(self.inputDataFinal, self.btnPegarDados)

    def retranslateUi(self, demanda):
        _translate = QtCore.QCoreApplication.translate
        demanda.setWindowTitle(_translate("demanda", "ANALISE DEMANDA"))
        self.label_15.setText(_translate("demanda", "SII - VER DEMANDA DO PRODUTO"))
        self.label_3.setText(_translate("demanda", "Data Final:"))
        self.label_4.setText(_translate("demanda", "Data inicial:"))
        self.btnPegarDados.setText(_translate("demanda", "Analisar"))
        self.label_5.setText(_translate("demanda", "Item:"))
        self.label.setText(_translate("demanda", "Quantidade de Orçamentos:"))
        self.label_2.setText(_translate("demanda", "Quantidade de Pedidos:"))
        self.label_6.setText(_translate("demanda", "Comprado:"))
        self.label_7.setText(_translate("demanda", "Importado:"))
        self.label_8.setText(_translate("demanda", "Fabricado:"))
        self.label_9.setText(_translate("demanda", "Estoque Inicial:"))
        self.label_10.setText(_translate("demanda", "Estoque Final:"))
        self.label_11.setText(_translate("demanda", "Quantidade Orçado:"))
        self.label_12.setText(_translate("demanda", "Quantidade Vendido:"))
        self.label_13.setText(_translate("demanda", "Quantidade Movimentado:"))
        self.labelOrcamentos.setText(_translate("demanda", "n/a"))
        self.labelPedidos.setText(_translate("demanda", "n/a"))
        self.labelComprado.setText(_translate("demanda", "n/a"))
        self.labelImportado.setText(_translate("demanda", "n/a"))
        self.labelFabricado.setText(_translate("demanda", "n/a"))
        self.labelEInicial.setText(_translate("demanda", "n/a"))
        self.labelEFinal.setText(_translate("demanda", "n/a"))
        self.labelOrcado.setText(_translate("demanda", "n/a"))
        self.labelVendido.setText(_translate("demanda", "n/a"))
        self.labelMovimentado.setText(_translate("demanda", "n/a"))
        self.labelCalculando.setText(_translate("demanda", "Calculando...       Favor aguardar!!"))
