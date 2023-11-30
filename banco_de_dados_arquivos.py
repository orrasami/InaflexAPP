import pymysql.cursors
import os
import datetime
import tkinter as tk
from tkinter import messagebox
from PyQt5.QtWidgets import QMessageBox
import datetime


class BDArquivos:
    def __init__(self):
        self.conn = pymysql.connect(
            host='mysql.inaflex-app.kinghost.net',
            user='inaflexapp',
            password='zt4cr3',
            db='inaflexapp',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    def inserir_arquivo_db(self, orcamento, indice, atual, titulo, registro):
        consulta = 'INSERT INTO arquivos_pedido (orcamento, indice, atual, titulo, registro) ' \
                   'VALUES (%s, %s, %s, %s, %s)'
        self.cursor.execute(consulta, (orcamento, indice, atual, titulo, registro))
        self.conn.commit()

    def verificar_existe_arquivo_db(self, orcamento, indice, atual, titulo):
        confere = False
        if atual == '1':
            consulta = 'SELECT titulo FROM arquivos_pedido WHERE orcamento LIKE %s AND indice LIKE %s AND atual LIKE %s'
            self.cursor.execute(consulta, (orcamento, indice, '1'))
            self.conn.commit()
            resultado = self.cursor.fetchall()
            if resultado:
                confere = True
        consulta = 'SELECT titulo FROM arquivos_pedido WHERE orcamento LIKE %s AND indice LIKE %s AND ' \
                   'atual LIKE %s AND titulo LIKE %s'
        self.cursor.execute(consulta, (orcamento, indice, atual, titulo))
        self.conn.commit()
        resultado = self.cursor.fetchall()
        if resultado:
            confere = True
        return confere

    def verificar_existe_arquivo_entrega_db(self, pedido, titulo):
        confere = False
        consulta = 'SELECT orcamento FROM pedidos WHERE pedido LIKE %s'
        self.cursor.execute(consulta, (pedido, ))
        self.conn.commit()
        resultado = self.cursor.fetchall()
        orcamento = resultado[0]['orcamento']

        consulta = 'SELECT titulo FROM arquivos_pedido WHERE orcamento LIKE %s AND titulo LIKE %s'
        self.cursor.execute(consulta, (orcamento, titulo))
        self.conn.commit()
        resultado = self.cursor.fetchall()
        if resultado:
            confere = True
        return orcamento, confere

    def atualiza_num_pedido(self, pedido, orcamento):
        consulta = 'UPDATE pedidos SET pedido=%s WHERE orcamento=%s'
        self.cursor.execute(consulta, (pedido, orcamento))
        self.conn.commit()

    def download_arquivo_db(self, orcamento, titulo, indice, atual, apagar):
        if apagar == '2':
            consulta = 'UPDATE arquivos_pedido SET atual=0 WHERE orcamento=%s AND titulo=%s AND indice=%s AND atual=%s'
            self.cursor.execute(consulta, (orcamento, titulo, indice, atual))
            self.conn.commit()
        elif apagar == '1':
            consulta = 'SELECT id, registro FROM arquivos_pedido ' \
                      'WHERE indice LIKE %s AND orcamento LIKE %s AND atual LIKE %s AND titulo LIKE %s'
            self.cursor.execute(consulta, (f'%{indice}%', f'%{orcamento}%', f'%{atual}%', f'%{titulo}%'))
            self.conn.commit()
            resultado = self.cursor.fetchall()
            chave = resultado[0]['id']
            registro = resultado[0]['registro']

            consulta = 'DELETE FROM arquivos_pedido WHERE id=%s'
            self.cursor.execute(consulta, ({chave}))
            self.conn.commit()
            return registro
        else:
            consulta = 'SELECT titulo, registro FROM arquivos_pedido ' \
                      'WHERE indice LIKE %s AND orcamento LIKE %s AND atual LIKE %s AND titulo LIKE %s'
            self.cursor.execute(consulta, (f'%{indice}%', f'%{orcamento}%', f'%{atual}%', f'%{titulo}%'))
            self.conn.commit()
            resultado = self.cursor.fetchall()
            titulo = resultado[0]['titulo']
            registro = resultado[0]['registro']
            return titulo, registro

    def download_arquivo_acabamento_db(self, orcamento, titulo, indice, atual):
        consulta = 'SELECT titulo, registro FROM arquivos_pedido ' \
                  'WHERE indice LIKE %s AND orcamento LIKE %s AND atual LIKE %s AND titulo LIKE %s'
        self.cursor.execute(consulta, (f'%{indice}%', f'%{orcamento}%', f'%{atual}%', f'%{titulo}%'))
        self.conn.commit()
        resultado = self.cursor.fetchall()
        titulo = resultado[0]['titulo']
        registro = resultado[0]['registro']
        return titulo, registro

    def achar_numero_orcamento(self, pedido):
        consulta = 'SELECT orcamento FROM pedidos WHERE pedido=%s'
        self.cursor.execute(consulta, pedido)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def mostrar_orcamentos_db(self, orcamento):
        consulta = 'SELECT orcamento, liquidado FROM pedidos'
        if orcamento != '*':
            consulta += ' WHERE orcamento LIKE %s'
            self.cursor.execute(consulta, f'%{orcamento}%')
        else:
            self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def mostra_arquivos_db(self, orcamento, atual):
        consulta = 'SELECT titulo, indice FROM arquivos_pedido WHERE orcamento LIKE %s AND atual LIKE %s ' \
                   'ORDER BY indice ASC'
        self.cursor.execute(consulta, (f'%{orcamento}%', f'%{atual}%'))
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def mostra_arquivos_acabamento_db(self, orcamento, atual):
        consulta = 'SELECT titulo, indice FROM arquivos_pedido WHERE orcamento LIKE %s AND atual LIKE %s'
        self.cursor.execute(consulta, (f'%{orcamento}%', f'%{atual}%'))
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def mostrar_pedidos_acabamento_db(self, pedido):
        consulta = 'SELECT pedido, orcamento FROM pedidos WHERE liquidado = 1 AND faturamento = 0'
        if pedido != '*':
            if pedido == '' or pedido == False:
                today = datetime.date.today()
                # Calculate the 3 working days ahead (excluding weekends)
                count = 0
                offset = 3
                while count < offset:
                    today += datetime.timedelta(days=1)
                    if today.weekday() < 5:  # Check if it's a weekday (0 - Monday, 4 - Friday)
                        count += 1
                consulta += ' AND data_finalizado <= %s'
                self.cursor.execute(consulta, (today,))
            else:
                consulta += ' AND pedido LIKE %s'
                self.cursor.execute(consulta, f'%{pedido}%')
        else:
            self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def mostrar_pedidos_faturamento_db(self, pedido):
        consulta = 'SELECT pedido, cliente, acao, observacao, obs_faturamento, data_acabamento, faturamento ' \
                   'FROM pedidos WHERE liquidado = 1 AND entregas = 0 AND finalizado = 0 AND faturamento = 1 '
        if pedido != 'NADA':
            consulta += ' AND pedido LIKE %s'
            self.cursor.execute(consulta, f'%{pedido}%')
        else:
            self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def mostrar_pedidos_entregas_db(self, pedido):
        consulta = 'SELECT pedido, cliente, data_entrega ' \
                   'FROM pedidos WHERE entregas = 1 AND finalizado = 0 '
        if pedido != 'NADA':
            consulta += ' AND pedido LIKE %s'
            self.cursor.execute(consulta, f'%{pedido}%')
        else:
            self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    # def listar_pedidos_db(self):
    #     consulta = 'SELECT pedido, cliente, acao, observacao, obs_faturamento, data_acabamento, faturamento ' \
    #                'FROM pedidos WHERE liquidado = 1 AND finalizado = 0 '
    #     self.cursor.execute(consulta)
    #     self.conn.commit()
    #     resultado = self.cursor.fetchall()
    #     return resultado

    def estorna_orcamento(self, orcamento):
        consulta = 'UPDATE pedidos SET liquidado=0, faturamento = 0, entregas = 0 WHERE orcamento=%s'
        self.cursor.execute(consulta, orcamento)
        self.conn.commit()

    def finalizar_db(self, pedido, data):
        consulta = f"UPDATE pedidos SET finalizado = 1, data_finalizado = '{data}' WHERE pedido = {pedido}"
        self.cursor.execute(consulta)
        self.conn.commit()

    # def atualizar_em_aberto(self, pedido):
    #     consulta = 'UPDATE pedidos SET finalizado = 0 WHERE pedido = %s'
    #     self.cursor.execute(consulta, (pedido,))
    #     self.conn.commit()

    def incluir_pedido_bd(self, orcamento):
        resultado = self.analisa_se_pedido(orcamento)
        if not resultado:
            liquidado = '0'
            consulta = 'INSERT INTO pedidos (orcamento, liquidado) VALUES (%s, %s)'
            self.cursor.execute(consulta, (orcamento, liquidado))
            self.conn.commit()
        else:
            return 'Erro'

    def analisa_se_pedido(self, orcamento):
        consulta = 'SELECT orcamento, liquidado FROM pedidos WHERE orcamento LIKE %s'
        self.cursor.execute(consulta, f'%{orcamento}%')
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def excluir_pedido_bd(self, orcamento):
        consulta = 'SELECT orcamento FROM arquivos_pedido WHERE orcamento LIKE %s'
        self.cursor.execute(consulta, orcamento)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        if not resultado:
            consulta = 'DELETE FROM pedidos WHERE orcamento=%s'
            self.cursor.execute(consulta, orcamento)
            self.conn.commit()
            return True
        else:
            return False

    def estornar_liquidar_db(self, orcamento, liquidado, cnpj=None, cliente=None, exigencias=None,
                             obs_acabamento=None, obs_faturamento=None):
        consulta = 'SELECT liquidado FROM pedidos WHERE orcamento=%s'
        self.cursor.execute(consulta, orcamento)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        if resultado[0]['liquidado'] != liquidado:
            consulta = 'UPDATE pedidos SET liquidado=%s, cnpj=%s, cliente=%s, obs_cliente=%s, obs_acabamento=%s, ' \
                       'obs_faturamento=%s WHERE orcamento=%s'
            self.cursor.execute(consulta, (liquidado, cnpj, cliente, exigencias, obs_acabamento,
                                           obs_faturamento, orcamento))
            self.conn.commit()
            return True
        else:
            return False

    def registrar_log(self, usuario, acao, indice=None, titulo='SEM_ARQUIVO'):
        maquina = os.environ['USERNAME']
        data_atual = str(datetime.datetime.now())
        consulta = 'INSERT INTO log_pedidos (data, usuario, maquina, acao, indice, titulo) VALUES ' \
                   '(%s, %s, %s, %s, %s, %s)'
        self.cursor.execute(consulta, (data_atual, usuario, maquina, acao, indice, titulo))
        self.conn.commit()

    @staticmethod
    def verifica_cnpj():
        return True

    def dados_acabamento_db(self, orcamento):
        consulta = 'SELECT cliente, obs_acabamento, obs_faturamento FROM pedidos WHERE pedido LIKE %s'
        self.cursor.execute(consulta, orcamento)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def salva_dados_acabamento(self, pedido, data, local, embalagem):
        consulta = 'UPDATE pedidos SET faturamento=1, data_acabamento=%s, local=%s, embalagem=%s WHERE pedido=%s'
        self.cursor.execute(consulta, (data, local, embalagem, pedido))
        self.conn.commit()

    def volta_para_acabamento_bd(self, pedido):
        consulta = f"UPDATE pedidos SET faturamento=0, data_acabamento='', local='', embalagem='' WHERE pedido={pedido}"
        self.cursor.execute(consulta)
        self.conn.commit()

    def volta_para_faturamento_bd(self, pedido):
        consulta = f"UPDATE pedidos SET entregas =0 WHERE pedido={pedido}"
        self.cursor.execute(consulta)
        self.conn.commit()

    def enviar_para_entregas_bd(self, pedido, data):
        consulta = f"UPDATE pedidos SET entregas = '1', data_entrega = '{data}' WHERE pedido={pedido}"
        self.cursor.execute(consulta)
        self.conn.commit()

    def combobox_faturamento(self):
        consulta = 'SELECT * FROM acao_faturamento'
        self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def salva_dados_faturamento(self, orcamento, responsavel, observacao):
        consulta = 'UPDATE pedidos SET acao=%s, observacao=%s WHERE pedido=%s'
        self.cursor.execute(consulta, (responsavel, observacao, orcamento))
        self.conn.commit()

    def salva_dados_entregas(self, orcamento, data):
        consulta = f"UPDATE pedidos SET data_entrega='{data}' WHERE pedido={orcamento}"
        self.cursor.execute(consulta)
        self.conn.commit()

    def seleciona_orcamentos_liquidados(self):
        consulta = "SELECT orcamento FROM pedidos WHERE liquidado='1' AND finalizado = '0'"
        self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    # def seleciona_pedidos_nao_liquidados(self):
    #     consulta = "SELECT orcamento FROM pedidos WHERE liquidado='0' AND pedido IS NULL"
    #     self.cursor.execute(consulta)
    #     self.conn.commit()
    #     resultado = self.cursor.fetchall()
    #     return resultado

    def atualiza_numero_do_pedido(self, pedido, validade, orcamento):
        consulta = 'UPDATE pedidos SET pedido=%s, data_finalizado=%s WHERE orcamento=%s'
        self.cursor.execute(consulta, (pedido, validade, orcamento))
        self.conn.commit()

    def seleciona_enviados_para_faturamento(self, data_inicial, data_final):
        consulta = "SELECT pedido, orcamento, cnpj, cliente, data_acabamento, local, embalagem FROM pedidos " \
                   "WHERE liquidado='1' AND faturamento='1' AND data_acabamento >= %s AND data_acabamento <= %s"
        self.cursor.execute(consulta, (data_inicial, data_final))
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def seleciona_no_faturamento(self):
        consulta = "SELECT pedido, orcamento, cnpj, cliente, data_acabamento, acao, observacao FROM pedidos " \
                   "WHERE finalizado='0' AND faturamento='1'"
        self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    # def seleciona_finalizados(self, data_inicial, data_final):
    #     consulta = "SELECT pedido, orcamento, cnpj, cliente, data_acabamento, local, embalagem FROM pedidos " \
    #                "WHERE finalizado='1' AND data_finalizado >= %s AND data_finalizado <= %s"
    #     self.cursor.execute(consulta, (data_inicial, data_final))
    #     self.conn.commit()
    #     resultado = self.cursor.fetchall()
    #     return resultado

    def comparar_pedido_liquidado(self, pedido):
        consulta = f"SELECT liquidado FROM pedidos WHERE pedido = {pedido}"
        self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def ver_se_liquidado(self, orcamento):
        try:
            consulta = f"SELECT liquidado FROM pedidos WHERE orcamento = {orcamento}"
            self.cursor.execute(consulta)
            self.conn.commit()
            resultado = self.cursor.fetchall()
            if resultado:
                return resultado
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(f"Liquidar primeiro em Arquivos")
                msg.setWindowTitle("Error")
                msg.exec_()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(f"Não contem numero de orçamento, portanto, evento não pode ser liquidado")
            msg.setWindowTitle("Error")
            msg.exec_()

    def listar_relatorios_inspecao_final(self, pedido, lote, finalizado):
        consulta = f"SELECT lote, pedido, correto, finalizado FROM inspecao_final "
        if pedido != "" or lote != "" or finalizado != "2":
            if pedido != "":
                consulta += f"WHERE pedido = '{pedido}' "
                if lote != "":
                    consulta += f"AND lote = '{lote}' "
                if finalizado != "2":
                    consulta += f"AND finalizado = '{finalizado}' "
            elif lote != "":
                consulta += f"WHERE lote = '{lote}' "
                if finalizado != "2":
                    consulta += f"AND finalizado = '{finalizado}' "
            elif finalizado != "2":
                consulta += f"WHERE finalizado = '{finalizado}' "
        self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def verificar_checklist(self, orcamento):
        consulta = f"SELECT * FROM liberacao_pedidos WHERE orcamento = {orcamento}"
        self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        if resultado:
            return 1
        else:
            return 0

    def fechar(self):
        self.cursor.close()
        self.conn.close()
