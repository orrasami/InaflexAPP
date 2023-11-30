from PyQt5.QtWidgets import QApplication
import pymysql.cursors
import sys
import os
import datetime
from banco_de_dados_oracle import BDBohm


class BDArquivos:
    def __init__(self):
        self.conn = pymysql.connect(
            host='mysql.inaflex.kinghost.net',
            user='inaflex03',
            password='zt4cr3',
            db='inaflex03',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    def importar_pedidos_aguardando_acabamento(self):
        respostas = BDBohm().pedidos_no_sistema()
        for resposta in respostas:
            pedido = resposta[0]
            chave_cliente = resposta[1]
            orcamento = resposta[2]
            data = resposta[3]
            data = f'{data.year}/{data.month}/{data.day}'
            respostas_ = BDBohm().pedidos_cliente_cnpj(chave_cliente)
            for resposta_ in respostas_:
                cliente = resposta_[0]
                cnpj = resposta_[1]

            consulta = 'INSERT INTO pedidos (orcamento, pedido, cnpj, cliente, data, liquidado, faturado, faturamento) ' \
                       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            self.cursor.execute(consulta, (orcamento, pedido, cnpj, cliente, data, '1', '0', '0'))
            self.conn.commit()


if __name__ == "__main__":
    qt = QApplication(sys.argv)
    executa = BDArquivos()
    executa.importar_pedidos_aguardando_acabamento()
    qt.exec()
