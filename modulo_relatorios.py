# 1.3 RELATORIOS
from janelas.janela_relatorio import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from banco_de_dados_oracle import BDBohm
from banco_de_dados_arquivos import BDArquivos
import xlsxwriter
import json

path_download = ''
with open('setup.json', 'r') as file:
    d1_json = file.read()
    d1_json = json.loads(d1_json)

for x, y in d1_json.items():
    path_download = y['relatorio']


class Relatorios(QMainWindow, Ui_Relatorios):
    def __init__(self, widget_relatorios, bd_oracle_ok, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.inputDataInicial.setDate(QtCore.QDate.currentDate())
        self.inputDataFinal.setDate(QtCore.QDate.currentDate())
        self.btnGerarRelatorios.clicked.connect(self.gerar_relatorio)
        self.dropdownRepresentantes.hide()
        if bd_oracle_ok == 'Falha':
            self.bd_oracle_ok = True
        else:
            self.bd_oracle_ok = False

    # Enviados para faturamento no periodo
    def gerar_relatorio(self):
        checkenviadosfaturamento = self.checkEnviadosFaturamento.checkState()
        if checkenviadosfaturamento:
            data_inicial = self.inputDataInicial.date().toString('yyyy/MM/dd')
            data_final = self.inputDataFinal.date().toString('yyyy/MM/dd')
            resultados = BDArquivos().seleciona_enviados_para_faturamento(data_inicial, data_final)
            if resultados:
                workbook = xlsxwriter.Workbook(f'{path_download}\Enviado_para_faturamento.xlsx')
                worksheet = workbook.add_worksheet('Relatorio')
                worksheet.write(0, 0, 'pedido')
                worksheet.write(0, 1, 'orcamento')
                worksheet.write(0, 2, 'cnpj')
                worksheet.write(0, 3, 'cliente')
                worksheet.write(0, 4, 'data_acabamento')
                worksheet.write(0, 5, 'local')
                worksheet.write(0, 6, 'embalagem')
                row = 1
                for resultado in resultados:
                    worksheet.write(row, 0, resultado['pedido'])
                    worksheet.write(row, 1, resultado['orcamento'])
                    worksheet.write(row, 2, resultado['cnpj'])
                    worksheet.write(row, 3, resultado['cliente'])
                    worksheet.write(row, 4, f"{resultado['data_acabamento'].day}/{resultado['data_acabamento'].month}/"
                                            f"{resultado['data_acabamento'].year}")
                    worksheet.write(row, 5, resultado['local'])
                    worksheet.write(row, 6, resultado['embalagem'])
                    row += 1
                workbook.close()
            else:
                QMessageBox.about(self, "Erro", "Sem dados até o momento")
        # Faturados no periodo
        checkfaturados = self.checkFaturados.checkState()
        if checkfaturados:
            data_inicial = self.inputDataInicial.date().toString('dd/MM/yyyy')
            data_final = self.inputDataFinal.date().toString('dd/MM/yyyy')
            data_inicial = f"TO_DATE('{data_inicial}','DD-MM-YY')"
            data_final = f"TO_DATE('{data_final}','DD-MM-YY')"
            if not self.bd_oracle_ok:
                resultados = BDBohm().relatorio_faturados(data_inicial, data_final)
                if resultados:
                    workbook = xlsxwriter.Workbook(r'C:\Download\Faturados_no_periodo.xlsx')
                    worksheet = workbook.add_worksheet('Relatorio')
                    worksheet.write(0, 0, 'pedido')
                    worksheet.write(0, 1, 'orcamento')
                    worksheet.write(0, 2, 'data')
                    row = 1
                    for resultado in resultados:
                        pedido = resultado[0]
                        orcamento = resultado[1]
                        data = resultado[2]
                        data_str = f'{data.day}/{data.month}/{data.year}'
                        worksheet.write(row, 0, pedido)
                        worksheet.write(row, 1, orcamento)
                        worksheet.write(row, 2, data_str)
                        row += 1
                    workbook.close()
                else:
                    QMessageBox.about(self, "Erro", "Sem dados até o momento")
            else:
                QMessageBox.about(self, 'Erro',
                                  'Sem acesso à base de dados Oracle para fazer o relatório "Faturados no Periodo"')
        # Aguardando faturamento
        checknofaturamento = self.checkNoFaturamento.checkState()
        if checknofaturamento:
            resultados = BDArquivos().seleciona_no_faturamento()
            if resultados:
                workbook = xlsxwriter.Workbook(r'C:\Download\Aguardando_faturamento.xlsx')
                worksheet = workbook.add_worksheet('Relatorio')
                worksheet.write(0, 0, 'pedido')
                worksheet.write(0, 1, 'orcamento')
                worksheet.write(0, 2, 'cnpj')
                worksheet.write(0, 3, 'cliente')
                worksheet.write(0, 4, 'data_acabamento')
                worksheet.write(0, 5, 'quem?')
                worksheet.write(0, 6, 'motivo')
                row = 1
                for resultado in resultados:
                    worksheet.write(row, 0, resultado['pedido'])
                    worksheet.write(row, 1, resultado['orcamento'])
                    worksheet.write(row, 2, resultado['cnpj'])
                    worksheet.write(row, 3, resultado['cliente'])
                    worksheet.write(row, 4, f"{resultado['data_acabamento'].day}/{resultado['data_acabamento'].month}/"
                                            f"{resultado['data_acabamento'].year}")
                    worksheet.write(row, 5, resultado['acao'])
                    worksheet.write(row, 6, resultado['observacao'])
                    row += 1
                workbook.close()
            else:
                QMessageBox.about(self, "Erro", "Sem dados até o momento")

        # Faturados mas nao atualizados no APP
        check_liquidados = self.checkLiquidados.checkState()
        if check_liquidados:
            if not self.bd_oracle_ok:
                resultados = BDBohm().analisar_lista_liquidados()
                workbook = xlsxwriter.Workbook(r'C:\Download\Pedidos_liquidados.xlsx')
                worksheet = workbook.add_worksheet('Relatorio')
                worksheet.write(0, 0, 'PEDIDO')
                worksheet.write(0, 1, 'STATUS')
                row = 1
                for resultado in resultados:
                    pedido = resultado[0]
                    resultado_ = BDArquivos().comparar_pedido_liquidado(pedido)
                    if resultado_ and resultado_[0]['liquidado'] == '0':
                        worksheet.write(row, 0, pedido)
                        worksheet.write(row, 1, 'LIQUIDAR NO APP')
                        row += 1
                    if not resultado_:
                        worksheet.write(row, 0, pedido)
                        worksheet.write(row, 1, 'INSERIR NO APP')
                        row += 1
                workbook.close()
            else:
                QMessageBox.about(self, 'Erro',
                                  'Sem acesso à base de dados Oracle para fazer o relatório "Liquidados"')
