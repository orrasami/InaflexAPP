# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'janelas\janela_analise_pedido.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_analisePedido(object):
    def setupUi(self, analisePedido):
        analisePedido.setObjectName("analisePedido")
        analisePedido.resize(1126, 627)
        self.btnAnalisar = QtWidgets.QPushButton(analisePedido)
        self.btnAnalisar.setEnabled(True)
        self.btnAnalisar.setGeometry(QtCore.QRect(240, 10, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnAnalisar.setFont(font)
        self.btnAnalisar.setStyleSheet("    border-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;")
        self.btnAnalisar.setObjectName("btnAnalisar")
        self.label_5 = QtWidgets.QLabel(analisePedido)
        self.label_5.setGeometry(QtCore.QRect(-7, 17, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.inputPedido = QtWidgets.QLineEdit(analisePedido)
        self.inputPedido.setGeometry(QtCore.QRect(80, 10, 151, 31))
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
        self.tableWidget = QtWidgets.QTableWidget(analisePedido)
        self.tableWidget.setGeometry(QtCore.QRect(10, 90, 811, 211))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(22)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(21, item)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget_2 = QtWidgets.QTableWidget(analisePedido)
        self.tableWidget_2.setGeometry(QtCore.QRect(590, 340, 231, 271))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        self.tableWidget_3 = QtWidgets.QTableWidget(analisePedido)
        self.tableWidget_3.setGeometry(QtCore.QRect(590, 340, 231, 271))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(3)
        self.tableWidget_3.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        self.tableWidget_4 = QtWidgets.QTableWidget(analisePedido)
        self.tableWidget_4.setGeometry(QtCore.QRect(300, 340, 231, 271))
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(3)
        self.tableWidget_4.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(2, item)
        self.tableWidget_5 = QtWidgets.QTableWidget(analisePedido)
        self.tableWidget_5.setGeometry(QtCore.QRect(300, 340, 231, 271))
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(3)
        self.tableWidget_5.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(2, item)
        self.labelOpPedido = QtWidgets.QLabel(analisePedido)
        self.labelOpPedido.setGeometry(QtCore.QRect(590, 310, 231, 21))
        self.labelOpPedido.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOpPedido.setObjectName("labelOpPedido")
        self.labelOcPedido = QtWidgets.QLabel(analisePedido)
        self.labelOcPedido.setGeometry(QtCore.QRect(590, 310, 231, 21))
        self.labelOcPedido.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOcPedido.setObjectName("labelOcPedido")
        self.labelOp = QtWidgets.QLabel(analisePedido)
        self.labelOp.setGeometry(QtCore.QRect(300, 310, 231, 21))
        self.labelOp.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOp.setObjectName("labelOp")
        self.labelOc = QtWidgets.QLabel(analisePedido)
        self.labelOc.setGeometry(QtCore.QRect(300, 310, 231, 21))
        self.labelOc.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOc.setObjectName("labelOc")
        self.checkOpOc = QtWidgets.QCheckBox(analisePedido)
        self.checkOpOc.setGeometry(QtCore.QRect(440, 16, 70, 21))
        self.checkOpOc.setObjectName("checkOpOc")
        self.checkOpOcPedido = QtWidgets.QCheckBox(analisePedido)
        self.checkOpOcPedido.setGeometry(QtCore.QRect(500, 16, 121, 21))
        self.checkOpOcPedido.setObjectName("checkOpOcPedido")
        self.checkFormula = QtWidgets.QCheckBox(analisePedido)
        self.checkFormula.setGeometry(QtCore.QRect(370, 16, 70, 21))
        self.checkFormula.setObjectName("checkFormula")
        self.checkCustos = QtWidgets.QCheckBox(analisePedido)
        self.checkCustos.setGeometry(QtCore.QRect(624, 16, 121, 21))
        self.checkCustos.setObjectName("checkCustos")
        self.label = QtWidgets.QLabel(analisePedido)
        self.label.setGeometry(QtCore.QRect(10, 59, 251, 31))
        self.label.setStyleSheet("    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(analisePedido)
        self.label_2.setGeometry(QtCore.QRect(260, 59, 71, 31))
        self.label_2.setStyleSheet("    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(analisePedido)
        self.label_3.setGeometry(QtCore.QRect(330, 59, 71, 31))
        self.label_3.setStyleSheet("    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(analisePedido)
        self.label_4.setGeometry(QtCore.QRect(400, 59, 141, 31))
        self.label_4.setStyleSheet("    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.inputDespesasAdm = QtWidgets.QLineEdit(analisePedido)
        self.inputDespesasAdm.setGeometry(QtCore.QRect(1030, 421, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.inputDespesasAdm.setFont(font)
        self.inputDespesasAdm.setStyleSheet("border-radius: 10px;\n"
"border: 1px solid #CDC99B;")
        self.inputDespesasAdm.setAlignment(QtCore.Qt.AlignCenter)
        self.inputDespesasAdm.setReadOnly(False)
        self.inputDespesasAdm.setClearButtonEnabled(False)
        self.inputDespesasAdm.setObjectName("inputDespesasAdm")
        self.label_6 = QtWidgets.QLabel(analisePedido)
        self.label_6.setGeometry(QtCore.QRect(850, 421, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.inputDespesasCom = QtWidgets.QLineEdit(analisePedido)
        self.inputDespesasCom.setGeometry(QtCore.QRect(1030, 450, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.inputDespesasCom.setFont(font)
        self.inputDespesasCom.setStyleSheet("border-radius: 10px;\n"
"border: 1px solid #CDC99B;")
        self.inputDespesasCom.setAlignment(QtCore.Qt.AlignCenter)
        self.inputDespesasCom.setReadOnly(False)
        self.inputDespesasCom.setClearButtonEnabled(False)
        self.inputDespesasCom.setObjectName("inputDespesasCom")
        self.label_7 = QtWidgets.QLabel(analisePedido)
        self.label_7.setGeometry(QtCore.QRect(850, 450, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.inputComissao = QtWidgets.QLineEdit(analisePedido)
        self.inputComissao.setGeometry(QtCore.QRect(1030, 480, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.inputComissao.setFont(font)
        self.inputComissao.setStyleSheet("border-radius: 10px;\n"
"border: 1px solid #CDC99B;")
        self.inputComissao.setAlignment(QtCore.Qt.AlignCenter)
        self.inputComissao.setReadOnly(False)
        self.inputComissao.setClearButtonEnabled(False)
        self.inputComissao.setObjectName("inputComissao")
        self.label_8 = QtWidgets.QLabel(analisePedido)
        self.label_8.setGeometry(QtCore.QRect(850, 480, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(analisePedido)
        self.label_9.setGeometry(QtCore.QRect(850, 390, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(analisePedido)
        self.label_10.setGeometry(QtCore.QRect(850, 360, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(analisePedido)
        self.label_11.setGeometry(QtCore.QRect(850, 330, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.labelIcms = QtWidgets.QLabel(analisePedido)
        self.labelIcms.setGeometry(QtCore.QRect(960, 330, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelIcms.setFont(font)
        self.labelIcms.setText("")
        self.labelIcms.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelIcms.setObjectName("labelIcms")
        self.labelCofins = QtWidgets.QLabel(analisePedido)
        self.labelCofins.setGeometry(QtCore.QRect(960, 360, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelCofins.setFont(font)
        self.labelCofins.setText("")
        self.labelCofins.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelCofins.setObjectName("labelCofins")
        self.labelPis = QtWidgets.QLabel(analisePedido)
        self.labelPis.setGeometry(QtCore.QRect(960, 390, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelPis.setFont(font)
        self.labelPis.setText("")
        self.labelPis.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelPis.setObjectName("labelPis")
        self.label_15 = QtWidgets.QLabel(analisePedido)
        self.label_15.setGeometry(QtCore.QRect(850, 270, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.labelValorSemIpi = QtWidgets.QLabel(analisePedido)
        self.labelValorSemIpi.setGeometry(QtCore.QRect(960, 270, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelValorSemIpi.setFont(font)
        self.labelValorSemIpi.setText("")
        self.labelValorSemIpi.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelValorSemIpi.setObjectName("labelValorSemIpi")
        self.label_17 = QtWidgets.QLabel(analisePedido)
        self.label_17.setGeometry(QtCore.QRect(850, 240, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.labelIPI = QtWidgets.QLabel(analisePedido)
        self.labelIPI.setGeometry(QtCore.QRect(960, 240, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelIPI.setFont(font)
        self.labelIPI.setText("")
        self.labelIPI.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelIPI.setObjectName("labelIPI")
        self.label_19 = QtWidgets.QLabel(analisePedido)
        self.label_19.setGeometry(QtCore.QRect(960, 210, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_19.setFont(font)
        self.label_19.setText("")
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(analisePedido)
        self.label_20.setGeometry(QtCore.QRect(850, 210, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_20.setFont(font)
        self.label_20.setText("")
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(analisePedido)
        self.label_21.setGeometry(QtCore.QRect(850, 210, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.labelValorComIpi = QtWidgets.QLabel(analisePedido)
        self.labelValorComIpi.setGeometry(QtCore.QRect(960, 210, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelValorComIpi.setFont(font)
        self.labelValorComIpi.setText("")
        self.labelValorComIpi.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelValorComIpi.setObjectName("labelValorComIpi")
        self.label_23 = QtWidgets.QLabel(analisePedido)
        self.label_23.setGeometry(QtCore.QRect(840, 110, 271, 451))
        self.label_23.setStyleSheet("    border-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: rgb(216,216,216);\n"
"    color: white;")
        self.label_23.setText("")
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(analisePedido)
        self.label_24.setGeometry(QtCore.QRect(850, 510, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.labelLucroLiquido = QtWidgets.QLabel(analisePedido)
        self.labelLucroLiquido.setGeometry(QtCore.QRect(960, 510, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelLucroLiquido.setFont(font)
        self.labelLucroLiquido.setText("")
        self.labelLucroLiquido.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelLucroLiquido.setObjectName("labelLucroLiquido")
        self.label_26 = QtWidgets.QLabel(analisePedido)
        self.label_26.setGeometry(QtCore.QRect(1040, 180, 20, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_26.setFont(font)
        self.label_26.setAlignment(QtCore.Qt.AlignCenter)
        self.label_26.setObjectName("label_26")
        self.labelLucroLiquido_2 = QtWidgets.QLabel(analisePedido)
        self.labelLucroLiquido_2.setGeometry(QtCore.QRect(1020, 510, 51, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelLucroLiquido_2.setFont(font)
        self.labelLucroLiquido_2.setText("")
        self.labelLucroLiquido_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelLucroLiquido_2.setObjectName("labelLucroLiquido_2")
        self.label_28 = QtWidgets.QLabel(analisePedido)
        self.label_28.setGeometry(QtCore.QRect(840, 120, 271, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setAlignment(QtCore.Qt.AlignCenter)
        self.label_28.setObjectName("label_28")
        self.checkRentabilidade = QtWidgets.QCheckBox(analisePedido)
        self.checkRentabilidade.setGeometry(QtCore.QRect(938, 150, 101, 21))
        self.checkRentabilidade.setObjectName("checkRentabilidade")
        self.labelPis_2 = QtWidgets.QLabel(analisePedido)
        self.labelPis_2.setGeometry(QtCore.QRect(1020, 390, 51, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelPis_2.setFont(font)
        self.labelPis_2.setText("")
        self.labelPis_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelPis_2.setObjectName("labelPis_2")
        self.labelCofins_2 = QtWidgets.QLabel(analisePedido)
        self.labelCofins_2.setGeometry(QtCore.QRect(1020, 360, 51, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelCofins_2.setFont(font)
        self.labelCofins_2.setText("")
        self.labelCofins_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelCofins_2.setObjectName("labelCofins_2")
        self.labelIcms_2 = QtWidgets.QLabel(analisePedido)
        self.labelIcms_2.setGeometry(QtCore.QRect(1020, 330, 51, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelIcms_2.setFont(font)
        self.labelIcms_2.setText("")
        self.labelIcms_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelIcms_2.setObjectName("labelIcms_2")
        self.labelIPI_2 = QtWidgets.QLabel(analisePedido)
        self.labelIPI_2.setGeometry(QtCore.QRect(1020, 240, 51, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelIPI_2.setFont(font)
        self.labelIPI_2.setText("")
        self.labelIPI_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelIPI_2.setObjectName("labelIPI_2")
        self.labelDespesasAdm = QtWidgets.QLabel(analisePedido)
        self.labelDespesasAdm.setGeometry(QtCore.QRect(960, 420, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelDespesasAdm.setFont(font)
        self.labelDespesasAdm.setText("")
        self.labelDespesasAdm.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelDespesasAdm.setObjectName("labelDespesasAdm")
        self.labelDespesasCom = QtWidgets.QLabel(analisePedido)
        self.labelDespesasCom.setGeometry(QtCore.QRect(960, 450, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelDespesasCom.setFont(font)
        self.labelDespesasCom.setText("")
        self.labelDespesasCom.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelDespesasCom.setObjectName("labelDespesasCom")
        self.labelComissao = QtWidgets.QLabel(analisePedido)
        self.labelComissao.setGeometry(QtCore.QRect(960, 480, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelComissao.setFont(font)
        self.labelComissao.setText("")
        self.labelComissao.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelComissao.setObjectName("labelComissao")
        self.label_27 = QtWidgets.QLabel(analisePedido)
        self.label_27.setGeometry(QtCore.QRect(960, 180, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_27.setFont(font)
        self.label_27.setAlignment(QtCore.Qt.AlignCenter)
        self.label_27.setObjectName("label_27")
        self.label_16 = QtWidgets.QLabel(analisePedido)
        self.label_16.setGeometry(QtCore.QRect(850, 300, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.labelCusto = QtWidgets.QLabel(analisePedido)
        self.labelCusto.setGeometry(QtCore.QRect(960, 300, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.labelCusto.setFont(font)
        self.labelCusto.setText("")
        self.labelCusto.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelCusto.setObjectName("labelCusto")
        self.label_12 = QtWidgets.QLabel(analisePedido)
        self.label_12.setGeometry(QtCore.QRect(610, 59, 211, 31))
        self.label_12.setStyleSheet("    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(analisePedido)
        self.label_13.setGeometry(QtCore.QRect(540, 59, 71, 31))
        self.label_13.setStyleSheet("    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"    border: 1px solid rgb(0,0,0);\n"
"    background-color: #CDC99B;\n"
"    color: white;")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.tableWidget_6 = QtWidgets.QTableWidget(analisePedido)
        self.tableWidget_6.setGeometry(QtCore.QRect(10, 340, 231, 271))
        self.tableWidget_6.setObjectName("tableWidget_6")
        self.tableWidget_6.setColumnCount(3)
        self.tableWidget_6.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_6.setHorizontalHeaderItem(2, item)
        self.labelDemanda = QtWidgets.QLabel(analisePedido)
        self.labelDemanda.setGeometry(QtCore.QRect(10, 310, 231, 21))
        self.labelDemanda.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDemanda.setObjectName("labelDemanda")
        self.label_23.raise_()
        self.btnAnalisar.raise_()
        self.label_5.raise_()
        self.inputPedido.raise_()
        self.tableWidget.raise_()
        self.tableWidget_2.raise_()
        self.tableWidget_3.raise_()
        self.tableWidget_4.raise_()
        self.tableWidget_5.raise_()
        self.labelOpPedido.raise_()
        self.labelOcPedido.raise_()
        self.labelOp.raise_()
        self.labelOc.raise_()
        self.checkOpOc.raise_()
        self.checkOpOcPedido.raise_()
        self.checkFormula.raise_()
        self.checkCustos.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.inputDespesasAdm.raise_()
        self.label_6.raise_()
        self.inputDespesasCom.raise_()
        self.label_7.raise_()
        self.inputComissao.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.labelIcms.raise_()
        self.labelCofins.raise_()
        self.labelPis.raise_()
        self.label_15.raise_()
        self.labelValorSemIpi.raise_()
        self.label_17.raise_()
        self.labelIPI.raise_()
        self.label_19.raise_()
        self.label_20.raise_()
        self.label_21.raise_()
        self.labelValorComIpi.raise_()
        self.label_24.raise_()
        self.labelLucroLiquido.raise_()
        self.label_26.raise_()
        self.labelLucroLiquido_2.raise_()
        self.label_28.raise_()
        self.checkRentabilidade.raise_()
        self.labelPis_2.raise_()
        self.labelCofins_2.raise_()
        self.labelIcms_2.raise_()
        self.labelIPI_2.raise_()
        self.labelDespesasAdm.raise_()
        self.labelDespesasCom.raise_()
        self.labelComissao.raise_()
        self.label_27.raise_()
        self.label_16.raise_()
        self.labelCusto.raise_()
        self.label_12.raise_()
        self.label_13.raise_()
        self.tableWidget_6.raise_()
        self.labelDemanda.raise_()

        self.retranslateUi(analisePedido)
        QtCore.QMetaObject.connectSlotsByName(analisePedido)

    def retranslateUi(self, analisePedido):
        _translate = QtCore.QCoreApplication.translate
        analisePedido.setWindowTitle(_translate("analisePedido", "ANALISE DE PEDIDO"))
        self.btnAnalisar.setText(_translate("analisePedido", "Sub-Itens"))
        self.label_5.setText(_translate("analisePedido", "Pedido:"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(12)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(13)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(14)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(15)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(16)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(17)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(18)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(19)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(20)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(21)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("analisePedido", "OC"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("analisePedido", "QTD"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("analisePedido", "DATA"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("analisePedido", "OP"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("analisePedido", "QTD"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("analisePedido", "STATUS"))
        item = self.tableWidget_4.horizontalHeaderItem(0)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget_4.horizontalHeaderItem(1)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget_4.horizontalHeaderItem(2)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget_5.horizontalHeaderItem(0)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget_5.horizontalHeaderItem(1)
        item.setText(_translate("analisePedido", "New Column"))
        item = self.tableWidget_5.horizontalHeaderItem(2)
        item.setText(_translate("analisePedido", "New Column"))
        self.labelOpPedido.setText(_translate("analisePedido", "OPs para o Pedido"))
        self.labelOcPedido.setText(_translate("analisePedido", "OCs para o Pedido"))
        self.labelOp.setText(_translate("analisePedido", "OPs"))
        self.labelOc.setText(_translate("analisePedido", "OCs"))
        self.checkOpOc.setText(_translate("analisePedido", "OP/OC"))
        self.checkOpOcPedido.setText(_translate("analisePedido", "OP/OC para Pedidos"))
        self.checkFormula.setText(_translate("analisePedido", "Formula"))
        self.checkCustos.setText(_translate("analisePedido", "Custos"))
        self.label.setText(_translate("analisePedido", "FORMULA"))
        self.label_2.setText(_translate("analisePedido", "VINCULADAS"))
        self.label_3.setText(_translate("analisePedido", "GERAL"))
        self.label_4.setText(_translate("analisePedido", "PRECO"))
        self.label_6.setText(_translate("analisePedido", "Despesas Adm:"))
        self.label_7.setText(_translate("analisePedido", "Despesas Com:"))
        self.label_8.setText(_translate("analisePedido", "Comissao:"))
        self.label_9.setText(_translate("analisePedido", "Pis:"))
        self.label_10.setText(_translate("analisePedido", "Cofins:"))
        self.label_11.setText(_translate("analisePedido", "ICMS:"))
        self.label_15.setText(_translate("analisePedido", "Valor Sem IPI:"))
        self.label_17.setText(_translate("analisePedido", "IPI:"))
        self.label_21.setText(_translate("analisePedido", "Valor Com IPI:"))
        self.label_24.setText(_translate("analisePedido", "Lucro Liquido:"))
        self.label_26.setText(_translate("analisePedido", "%"))
        self.label_28.setText(_translate("analisePedido", "Rentabilidade"))
        self.checkRentabilidade.setText(_translate("analisePedido", "    Item"))
        self.label_27.setText(_translate("analisePedido", "Valor"))
        self.label_16.setText(_translate("analisePedido", "Custo Produto:"))
        self.label_12.setText(_translate("analisePedido", "ESTOQUE"))
        self.label_13.setText(_translate("analisePedido", "ESTREGA"))
        item = self.tableWidget_6.horizontalHeaderItem(0)
        item.setText(_translate("analisePedido", "OP"))
        item = self.tableWidget_6.horizontalHeaderItem(1)
        item.setText(_translate("analisePedido", "QTD"))
        item = self.tableWidget_6.horizontalHeaderItem(2)
        item.setText(_translate("analisePedido", "STATUS"))
        self.labelDemanda.setText(_translate("analisePedido", "Demanda (Pedidos/OPs)"))
