import datetime

import cx_Oracle
import json
from PyQt5.QtWidgets import QMessageBox
import ast

path_oracle_client = ''
with open('setup.json', 'r') as file:
    d1_json = file.read()
    d1_json = json.loads(d1_json)

for x, y in d1_json.items():
    path_oracle_client = y['oracle_client']


class BDBohm:
    def __init__(self):
        try:
            self.conn = cx_Oracle.connect('CONSULTA/INAFLEX@INAFLEX')
        except:
            pass
        try:
            self.conexao = self.conn.cursor()
        except:
            pass

    def fechar(self):
        self.conn.close()

    def select(self, consulta):
            respostas = self.conexao.execute(consulta)
            return respostas

    def pegar_nome_cliente(self, cnpj):
        try:
            consulta = f"select nome, observacoes_gerais from inaflex.clientes where cgc='{cnpj}'"
            respostas = self.conexao.execute(consulta)
        except:
            QMessageBox.about(self, "Erro", "Sem resposta")
        for resposta in respostas:
            try:
                return resposta
            except:
                QMessageBox.about(self, "Erro", f"Resposta errada {resposta}")

    def atualiza_lista_pedidos(self, orcamento):
        consulta = f"select numped from inaflex.pedidos where chave_orcamento='{orcamento}'"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            return resposta[0]

    def ver_validade_pedido(self, pedido):
        if pedido:
            consulta = f"select min(data_entrega) from inaflex.pedidos_itens where chave_pedido='{pedido}' and saldo_remessa>0"
            respostas = self.conexao.execute(consulta)
            for resposta in respostas:
                return resposta[0]
        else:
            resposta = ''
            return resposta

    def relatorio_faturados(self, data_inicial, data_final):
        respostas_dicionario = []
        consulta = f"select valida_chave_pedido, chave_orcamento, data_emissao from inaflex.notas " \
                   f"where nfe_status='AUTORIZADA' and data_emissao >= {data_inicial} " \
                   f"and data_emissao <= {data_final}"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            respostas_dicionario.append(resposta)
        return respostas_dicionario

    # def atualizar_faturados(self, pedido):
    #     consulta = f"select status from inaflex.pedidos where numped='{pedido}'"
    #     respostas = self.conexao.execute(consulta)
    #     for resposta in respostas:
    #         return resposta

    # def dropdown_representantes(self):
    #     consulta = f"select codvendedor, nomered from inaflex.vendedores where inativo='NAO'"
    #     respostas = self.conexao.execute(consulta)
    #     return respostas

    def pedidos_no_sistema(self):
        consulta = f"select numped, chave_cliente, chave_orcamento, data_pedido from inaflex.pedidos " \
                   f"where status='EM ABERTO'"
        respostas = self.conexao.execute(consulta)
        return respostas

    def pedidos_cliente_cnpj(self, valor):
        consulta = f"select nome, cgc from inaflex.clientes where codcli={valor}"
        respostas_ = self.conexao.execute(consulta)
        return respostas_

    def analisar_lista_liquidados(self):
        consulta = f"select numped from inaflex.pedidos where status = 'EM ABERTO'"
        respostas_ = self.conexao.execute(consulta)
        return respostas_

    def calcular_demanda(self, lista_itens, lista):
        lista_pai = []
        codigo = lista_itens[0]
        lista_itens.pop()
        consulta = f"select cprod from inaflex.produtos where codigo = '{codigo}'"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            item = resposta[0]
        dicionario = {}
        dicionario['item'] = item
        dicionario['quantidade'] = 1
        lista.append(dicionario)
        lista_pai.append(item)
        lista_itens.append(dicionario)
        i = len(lista_itens)
        while i > 0:
            lista_processos = []
            item = lista_itens[len(lista_itens)-1]['item']
            quantidade_item = lista_itens[len(lista_itens)-1]['quantidade']
            lista_itens.pop()
            consulta = f"select chave_processo, quantidade from inaflex.processos_materiais where chave_material = {item}"
            respostas_ = self.conexao.execute(consulta)
            for resposta_ in respostas_:
                dicionario_processo = {}
                dicionario_processo['chave_processo'] = resposta_[0]
                dicionario_processo['quantidade'] = resposta_[1]
                lista_processos.append(dicionario_processo)
            for processo in lista_processos:
                chave_processo = processo['chave_processo']
                quantidade = processo['quantidade']
                consulta = f"select chave_produto from inaflex.processos where chave = {chave_processo}"
                respostas__ = self.conexao.execute(consulta)
                for resposta__ in respostas__:
                    chave_produto_pai = resposta__[0]
                dicionario = {}
                dicionario['item'] = chave_produto_pai
                dicionario['quantidade'] = quantidade * quantidade_item
                lista.append(dicionario)
                lista_pai.append(chave_produto_pai)
                lista_itens.append(dicionario)
            i = len(lista_itens)
        return lista_pai, lista

    def demanda_oracamento_unico(self, lista_orcamento_unico, data_inicial, data_final):
        total = 0
        total_orcamentos = 0
        while len(lista_orcamento_unico) > 0:
            item = lista_orcamento_unico[len(lista_orcamento_unico) - 1]['item']
            quantidade_original = lista_orcamento_unico[len(lista_orcamento_unico) - 1]['quantidade']
            consulta = f"select inaflex.orcamentos_itens.quantidade " \
                       f"from inaflex.orcamentos_itens, inaflex.orcamentos " \
                       f"where (inaflex.orcamentos_itens.chave_produto = {item}) " \
                       f"and (inaflex.orcamentos_itens.chave_pedido = inaflex.orcamentos.chave) " \
                       f"and (inaflex.orcamentos.data_pedido >= TO_DATE('{data_inicial}','DD-MM-YYYY')) " \
                       f"and (inaflex.orcamentos.data_pedido <= TO_DATE('{data_final}','DD-MM-YYYY'))"
            respostas = self.conexao.execute(consulta)
            for resposta in respostas:
                quantidade = resposta[0]
                total += quantidade * quantidade_original
                total_orcamentos += 1
            lista_orcamento_unico.pop()
        return total_orcamentos, total

    def demanda_oracamento_ics(self, lista_orcamento_ics, data_inicial, data_final):
        total = 0
        total_orcamentos = 0
        while len(lista_orcamento_ics) > 0:
            item = lista_orcamento_ics[len(lista_orcamento_ics) - 1]['item']
            quantidade_original = lista_orcamento_ics[len(lista_orcamento_ics) - 1]['quantidade']
            consulta = f"select inaflex.orcamentos_itens_c.quantidade " \
                       f"from inaflex.orcamentos_itens_c, inaflex.orcamentos " \
                       f"where (inaflex.orcamentos_itens_c.chave_produto = {item}) " \
                       f"and (inaflex.orcamentos_itens_c.chave_pedido = inaflex.orcamentos.chave) " \
                       f"and (inaflex.orcamentos.data_pedido >= TO_DATE('{data_inicial}','DD-MM-YYYY')) " \
                       f"and (inaflex.orcamentos.data_pedido <= TO_DATE('{data_final}','DD-MM-YYYY'))"
            respostas = self.conexao.execute(consulta)
            for resposta in respostas:
                quantidade = resposta[0]
                total += quantidade * quantidade_original
                total_orcamentos += 1
            lista_orcamento_ics.pop()
        return total_orcamentos, total

    def demanda_pedido(self, lista_pedidos, data_inicial, data_final):
        total = 0
        total_pedidos = 0
        while len(lista_pedidos) > 0:
            item = lista_pedidos[len(lista_pedidos)-1]['item']
            quantidade_original = lista_pedidos[len(lista_pedidos)-1]['quantidade']
            consulta = f"select inaflex.pedidos_itens.quantidade " \
                       f"from inaflex.pedidos_itens, inaflex.pedidos " \
                       f"where (inaflex.pedidos_itens.chave_produto = {item}) " \
                       f"and (inaflex.pedidos_itens.chave_pedido = inaflex.pedidos.chave) " \
                       f"and (inaflex.pedidos.data_pedido >= TO_DATE('{data_inicial}','DD-MM-YYYY')) " \
                       f"and (inaflex.pedidos.data_pedido <= TO_DATE('{data_final}','DD-MM-YYYY'))"
            respostas = self.conexao.execute(consulta)
            for resposta in respostas:
                quantidade = resposta[0]
                total += quantidade * quantidade_original
                total_pedidos += 1
            lista_pedidos.pop()
        return total_pedidos, total

    def demanda_estoque(self, lista_estoque, data_inicial, data_final):
        total_comprado = 0
        total_importado = 0
        total_fabricado = 0
        item = lista_estoque['item']
        consulta = f"SELECT INAFLEX.ENTRADAS_ITENS.QUANTIDADE " \
                   f"FROM INAFLEX.ENTRADAS_ITENS, INAFLEX.ENTRADAS, INAFLEX.PRODUTOS " \
                   f"WHERE (INAFLEX.ENTRADAS_ITENS.CHAVE_ENTRADA = INAFLEX.ENTRADAS.CHAVE) " \
                   f"AND (INAFLEX.PRODUTOS.CPROD = INAFLEX.ENTRADAS_ITENS.CHAVE_PRODUTO) " \
                   f"AND (INAFLEX.ENTRADAS.DATA_EMISSAO >= TO_DATE('{data_inicial}','DD-MM-YYYY')) " \
                   f"AND (INAFLEX.ENTRADAS.DATA_EMISSAO <= TO_DATE('{data_final}','DD-MM-YYYY')) " \
                   f"AND (INAFLEX.PRODUTOS.CPROD = {item})"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            quantidade = resposta[0]
            total_comprado += quantidade
        consulta = f"SELECT INAFLEX.IMPORTACOES_ITENS.QUANTIDADE " \
                   f"FROM INAFLEX.IMPORTACOES_ITENS, INAFLEX.IMPORTACOES " \
                   f"WHERE (INAFLEX.IMPORTACOES_ITENS.CHAVE_IMPORTACAO = INAFLEX.IMPORTACOES.CHAVE) " \
                   f"AND (INAFLEX.IMPORTACOES.DATA_EMISSAO >= TO_DATE('{data_inicial}','DD-MM-YYYY')) " \
                   f"AND (INAFLEX.IMPORTACOES.DATA_EMISSAO <= TO_DATE('{data_final}','DD-MM-YYYY')) " \
                   f"AND (INAFLEX.IMPORTACOES_ITENS.CHAVE_PRODUTO = {item}) "
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            quantidade = resposta[0]
            total_importado += quantidade
        consulta = f"SELECT INAFLEX.ORDENS.QUANTIDADE_PRODUZIDA " \
                   f"FROM INAFLEX.ORDENS, INAFLEX.PRODUTOS " \
                   f"WHERE (INAFLEX.PRODUTOS.CPROD = INAFLEX.ORDENS.CHAVE_PRODUTO) " \
                   f"AND (INAFLEX.ORDENS.DATA_EMISSAO >= TO_DATE('{data_inicial}','DD-MM-YYYY')) " \
                   f"AND (INAFLEX.ORDENS.DATA_EMISSAO <= TO_DATE('{data_final}','DD-MM-YYYY')) " \
                   f"AND (INAFLEX.PRODUTOS.CPROD = {item})"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            quantidade = resposta[0]
            total_fabricado += quantidade
        return total_comprado, total_importado, total_fabricado

    def estoque_inicial(self, lista_estoque, data_inicial, data_final):
        estoque_inicial = 0
        item = lista_estoque['item']
        consulta = f"SELECT A.QUANTIDADE, A.SALDO_ESTOQUE, A.TIPO " \
                   f"FROM INAFLEX.MOVESTOQUE A, INAFLEX.PRODUTOS D " \
                   f"WHERE (A.CHAVE_PRODUTO = D.CPROD) " \
                   f"AND (D.CPROD = {item}) " \
                   f"AND (A.DATA_MOV >= TO_DATE('{data_inicial}','DD-MM-YYYY')) " \
                   f"AND (A.DATA_MOV <= TO_DATE('{data_final}','DD-MM-YYYY')) " \
                   f"AND A.DATA_MOV = (SELECT MIN(B.DATA_MOV) " \
                   f"FROM INAFLEX.MOVESTOQUE B " \
                   f"WHERE (B.CHAVE_PRODUTO = A.CHAVE_PRODUTO) " \
                   f"AND (B.DATA_MOV >= TO_DATE('{data_inicial}','DD-MM-YYYY')) " \
                   f"AND (B.DATA_MOV <= TO_DATE('{data_final}','DD-MM-YYYY')) " \
                   f"GROUP BY B.CHAVE_PRODUTO) " \
                   f"AND A.CHAVE= (SELECT MIN(C.CHAVE) " \
                   f"FROM INAFLEX.MOVESTOQUE C " \
                   f"WHERE (C.CHAVE_PRODUTO = A.CHAVE_PRODUTO) " \
                   f"AND (C.DATA_MOV > TO_DATE('{data_inicial}','DD-MM-YYYY')) " \
                   f"AND (C.DATA_MOV <= TO_DATE('{data_final}','DD-MM-YYYY')) " \
                   f"GROUP BY C.CHAVE_PRODUTO)"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            quantidade = resposta[0]
            saldo = resposta[1]
            tipo = resposta[2]
            if tipo == 'CREDITO':
                estoque_inicial = saldo - quantidade
            else:
                estoque_inicial = saldo - quantidade
        return estoque_inicial

    def estoque_final(self, lista_estoque):
        estoque_final = 0
        item = lista_estoque['item']
        consulta = f"SELECT INAFLEX.MOVJOBS.ESTOQUE_DISPONIVEL " \
                   f"FROM INAFLEX.PRODUTOS, INAFLEX.MOVJOBS " \
                   f"WHERE (INAFLEX.PRODUTOS.CPROD = INAFLEX.MOVJOBS.CHAVE_PRODUTO)" \
                   f"AND (INAFLEX.PRODUTOS.CPROD = {item})"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            estoque_final = resposta[0]
        return estoque_final

    def atualiza_num_pedido(self, orcamento):
        consulta = f"select chave_pedido from inaflex.orcamentos where chave='{orcamento}'"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            pedido = resposta[0]
        return pedido

    def analisar_itens_pedidos(self, codigo):
        lista_itens = []
        lista_itens_pedidos = []
        lista_itens_ops_materiais = []
        lista_itens_estoque_minimo = []
        lista_itens_ops_produtos = []
        lista_itens_oc = []
        lista_itens_estoque = []
        lista_oc = []
        lista_op = []
        #################### (+) DEMANDA ####################
        # LISTA ITENS DE PEDIDOS COM SALDO A ENTREGAR
        consulta = f"SELECT P.CHAVE_PEDIDO, I.CODIGO, P.SALDO FROM INAFLEX.PEDIDOS_ITENS P, INAFLEX.PRODUTOS I " \
                   f"WHERE (P.SALDO > 0) AND (I.CPROD = P.CHAVE_PRODUTO) "
        if codigo != "":
            consulta += f"AND(I.CODIGO = '{codigo}')"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            item = {}
            item['pedido'] = resposta[0]
            item['item'] = resposta[1]
            item['qtd'] = -resposta[2]
            lista_itens_pedidos.append(item)
            lista_itens.append(item)

        # LISTA ITENS DE OPS COM SALDO A REQUISITAR
        consulta = f"SELECT I.CHAVE_ORDEM, P.CODIGO, I.REQUISITAR " \
                   f"FROM INAFLEX.ORDENS_MATERIAIS I, INAFLEX.ORDENS O, INAFLEX.PRODUTOS P " \
                   f"WHERE(I.CHAVE_MATERIAL = P.CPROD) AND(I.CHAVE_ORDEM = O.CHAVE) " \
                   f"AND(O.STATUS <> 'FECHADA') AND(O.STATUS <> 'CONTABILIZADA') " \
                   f"AND(O.STATUS <> 'CANCELADA') AND(I.REQUISITAR > 0) " \
                   f"AND(O.LIBERADO_NECESSIDADE = 'SIM') "
        if codigo != "":
            consulta += f"AND(P.CODIGO = '{codigo}')"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            item = {}
            item['op_material'] = resposta[0]
            item['item'] = resposta[1]
            item['qtd'] = -resposta[2]
            lista_itens_ops_materiais.append(item)
            lista_itens.append(item)

        # LISTA ITENS COM ESTOQUE MINIMO
        consulta = f"SELECT P.CODIGO, J.ESTOQUE_MINIMO " \
                   f"FROM INAFLEX.PRODUTOS P, INAFLEX.PRODUTOS_JOB J " \
                   f"WHERE (J.CHAVE_PRODUTO = P.CPROD) AND (J.ESTOQUE_MINIMO > 0) "
        if codigo != "":
            consulta += f"AND(P.CODIGO = '{codigo}')"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            item = {}
            item['estoque_minimo'] = "estoque_minimo"
            item['item'] = resposta[0]
            item['qtd'] = -resposta[1]
            lista_itens_estoque_minimo.append(item)
            lista_itens.append(item)

        #################### (-) DEMANDA ####################
        # LISTA DE PRODUTOS COM OPS
        consulta = f"SELECT O.CHAVE, P.CODIGO, O.QUANTIDADE_PRODUZIR " \
                   f"FROM INAFLEX.ORDENS O, INAFLEX.PRODUTOS P " \
                   f"WHERE (O.QUANTIDADE_PRODUZIR > 0) AND (O.CHAVE_PRODUTO = P.CPROD) " \
                   f"AND(O.STATUS <> 'FECHADA') AND(O.STATUS <> 'CONTABILIZADA') " \
                   f"AND(O.STATUS <> 'CANCELADA') " \
                   f"AND(O.LIBERADO_NECESSIDADE = 'SIM') "
        if codigo != "":
            consulta += f"AND(P.CODIGO = '{codigo}')"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            item = {}
            item['op_produto'] = resposta[0]
            item['item'] = resposta[1]
            item['qtd'] = resposta[2]
            lista_itens_ops_produtos.append(item)
            lista_itens.append(item)

        # LISTA DE PRODUTOS EM OCS A RECEBER
        consulta = f"SELECT I.CHAVE_OC, P.CODIGO, I.SALDO " \
                   f"FROM INAFLEX.OC_MP_ITENS I, INAFLEX.OC_MP O, INAFLEX.PRODUTOS P " \
                   f"WHERE I.SALDO > 0 AND (I.CHAVE_OC = O.CHAVE) AND (I.CHAVE_MATERIAL = P.CPROD) " \
                   f"AND (O.STATUS = 'EM ABERTO') " \
                   f"AND (O.DESCONSIDERAR_SEMANA = 'SIM')"  #ISSO DESCONSIDERA A OC DA ANALISE DE NECESSIDADE
        if codigo != "":
            consulta += f"AND(P.CODIGO = '{codigo}')"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            item = {}
            item['oc'] = resposta[0]
            item['item'] = resposta[1]
            item['qtd'] = resposta[2]
            lista_itens_oc.append(item)
            lista_itens.append(item)

        # SALDO EM ESTOQUE
        consulta = f"SELECT P.CODIGO, M.ESTOQUE_ATUAL " \
                   f"FROM INAFLEX.MOVJOBS M, INAFLEX.PRODUTOS P " \
                   f"WHERE (M.CHAVE_PRODUTO = P.CPROD) AND M.ESTOQUE_ATUAL > 0 "
        if codigo != "":
            consulta += f"AND(P.CODIGO = '{codigo}')"
        respostas = self.conexao.execute(consulta)
        for resposta in respostas:
            item = {}
            item['estoque'] = "estoque"
            item['item'] = resposta[0]
            item['qtd'] = resposta[1]
            lista_itens_estoque.append(item)
            lista_itens.append(item)


        # AGRUPA ITENS IGUAIS SOMANDO A QUANTIDADE
        lista_acumulada = []
        i = 0
        while i < len(lista_itens):
            item_acumulado = {}
            codigo1 = lista_itens[i]['item']
            qtd1 = lista_itens[i]['qtd']
            j = i + 1
            while j < len(lista_itens):
                codigo2 = lista_itens[j]['item']
                qtd2 = lista_itens[j]['qtd']
                if codigo2 == codigo1:
                    qtd1 = qtd1 + qtd2
                    del lista_itens[j]
                else:
                    j += 1
            item_acumulado['item'] = codigo1
            item_acumulado['qtd'] = qtd1
            lista_acumulada.append(item_acumulado)
            i += 1

        # VERIFICA SE ITEM TEM PROCESSO DE PRODUÇÃO
        for item in lista_acumulada:
            codigo_ = item['item']
            qtd = item['qtd']
            if codigo != "" or qtd < -0.000001:
                consulta = f"SELECT P.ANALISA_COMPRA, P.SERVICO FROM INAFLEX.PRODUTOS P WHERE P.CODIGO = '{codigo_}'"
                respostas = self.conexao.execute(consulta)
                for resposta in respostas:
                    if resposta[1] == 'NAO':
                        if resposta[0] == 'SIM':
                            lista_oc.append(item)
                        else:
                            lista_op.append(item)
        return lista_itens_pedidos, lista_itens_ops_materiais, lista_itens_estoque_minimo, lista_itens_ops_produtos, \
               lista_itens_oc, lista_itens_estoque, lista_oc, lista_op

    def pegar_valores_demanda(self, item, data):
        qtd_orcados = 0
        qtd_orcamentos = 0
        qtd_vendidos = 0
        qtd_pedidos = 0
        estoque_atual = 0
        estoque_minimo = 0
        demanda = 0
        custo = 0
        estoque_data_inicial = 0
        entrada_compras = 0
        entrada_importacao = 0
        entrada_ops = 0

        item = str(item)
        if item != "None" and item != "item" and item[0:2] != "__" and item!="":
            consulta = (f"SELECT SUM(C.QUANTIDADE), COUNT(P.CODIGO) "
                        f"FROM INAFLEX.ORCAMENTOS_ITENS_C C, INAFLEX.ORCAMENTOS_ITENS I, "
                        f"INAFLEX.ORCAMENTOS O, INAFLEX.PRODUTOS P "
                        f"WHERE (I.CHAVE = C.CHAVE_ORCAMENTO_ITEM) AND (I.CHAVE_PEDIDO = O.NUMPED) "
                        f"AND (C.CHAVE_PRODUTO = P.CPROD) AND (O.DATA_PEDIDO >= TO_DATE('{data}','DD-MM-YYYY')) "
                        f"AND (P.CODIGO = '{item}')")
            respostas = self.conexao.execute(consulta)

            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    qtd_orcados = qtd_orcados + resposta[0]
                    qtd_orcamentos = qtd_orcamentos + resposta[1]

            consulta = (f"SELECT SUM(I.QUANTIDADE), COUNT(P.CODIGO) "
                        f"FROM INAFLEX.ORCAMENTOS_ITENS I, INAFLEX.ORCAMENTOS O, INAFLEX.PRODUTOS P "
                        f"WHERE (P.CPROD = I.CHAVE_PRODUTO) AND (O.NUMPED = I.CHAVE_PEDIDO) "
                        f"AND (P.CODIGO <> 'ICSRV000000') AND (P.CODIGO <> 'IC800000000') "
                        f"AND (P.CODIGO <> 'IC810000000') AND (P.CODIGO <> 'IC820000000') "
                        f"AND (P.CODIGO <> 'IC840000000') AND (P.CODIGO <> 'IC84T000000') "
                        f"AND (P.CODIGO <> 'IC870000000') AND (P.CODIGO <> 'IC440000000') "
                        f"AND (P.CODIGO <> 'IC460000000') AND (P.CODIGO <> 'VAN00000001') "
                        f"AND (P.CODIGO <> 'TESTE-INAFLEX') AND (P.CODIGO <> 'TESTE000000') "
                        f"AND (O.DATA_PEDIDO >= TO_DATE('{data}','DD-MM-YYYY')) "
                        f"AND (P.CODIGO = '{item}')")
            respostas = self.conexao.execute(consulta)

            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    qtd_orcados = qtd_orcados + resposta[0]
                    qtd_orcamentos = qtd_orcamentos + resposta[1]

            consulta = (f"SELECT SUM(C.QUANTIDADE), COUNT(P.CODIGO) "
                        f"FROM INAFLEX.PEDIDOS_ITENS_C C, INAFLEX.PEDIDOS_ITENS I, "
                        f"INAFLEX.PEDIDOS O, INAFLEX.PRODUTOS P "
                        f"WHERE (I.CHAVE = C.CHAVE_PEDIDO_ITEM) AND (I.CHAVE_PEDIDO = O.NUMPED) "
                        f"AND (C.CHAVE_PRODUTO = P.CPROD) AND (O.DATA_PEDIDO >= TO_DATE('{data}','DD-MM-YYYY')) "
                        f"AND (P.CODIGO = '{item}')")
            respostas = self.conexao.execute(consulta)

            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    qtd_vendidos = qtd_vendidos + resposta[0]
                    qtd_pedidos = qtd_pedidos + resposta[1]

            consulta = (f"SELECT SUM(I.QUANTIDADE), COUNT(P.CODIGO) "
                        f"FROM INAFLEX.PEDIDOS_ITENS I, INAFLEX.PEDIDOS O, INAFLEX.PRODUTOS P "
                        f"WHERE (P.CPROD = I.CHAVE_PRODUTO) AND (O.NUMPED = I.CHAVE_PEDIDO) "
                        f"AND (O.DATA_PEDIDO >= TO_DATE('{data}','DD-MM-YYYY')) "
                        f"AND (P.CODIGO <> 'ICSRV000000') AND (P.CODIGO <> 'IC800000000') "
                        f"AND (P.CODIGO <> 'IC810000000') AND (P.CODIGO <> 'IC820000000') "
                        f"AND (P.CODIGO <> 'IC840000000') AND (P.CODIGO <> 'IC84T000000') "
                        f"AND (P.CODIGO <> 'IC870000000') AND (P.CODIGO <> 'IC440000000') "
                        f"AND (P.CODIGO <> 'IC460000000') AND (P.CODIGO <> 'VAN00000001') "
                        f"AND (P.CODIGO <> 'TESTE-INAFLEX') AND (P.CODIGO <> 'TESTE000000') "
                        f"AND (P.CODIGO = '{item}')")
            respostas = self.conexao.execute(consulta)

            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    qtd_vendidos = qtd_vendidos + resposta[0]
                    qtd_pedidos = qtd_pedidos + resposta[1]

            consulta = (f"SELECT M.ESTOQUE_DISPONIVEL "
                        f"FROM INAFLEX.PRODUTOS P, INAFLEX.MOVJOBS M "
                        f"WHERE (P.CPROD = M.CHAVE_PRODUTO) "
                        f"AND (P.CODIGO = '{item}')")
            respostas = self.conexao.execute(consulta)

            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    estoque_atual = resposta[0]

            consulta = (f"SELECT J.ESTOQUE_MINIMO "
                        f"FROM INAFLEX.PRODUTOS P, INAFLEX.PRODUTOS_JOB J "
                        f"WHERE (J.CHAVE_PRODUTO = P.CPROD) AND (J.ESTOQUE_MINIMO > 0) "
                        f"AND (P.CODIGO = '{item}')")
            respostas = self.conexao.execute(consulta)

            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    estoque_minimo = resposta[0]

            consulta = (f"SELECT D.CODIGO, A.QUANTIDADE, A.SALDO_ESTOQUE, A.TIPO, A.DATA_MOV "
                        f"FROM INAFLEX.MOVESTOQUE A, INAFLEX.PRODUTOS D "
                        f"WHERE (A.CHAVE_PRODUTO = D.CPROD) AND (A.DATA_MOV > TO_DATE('{data}','DD-MM-YYYY')) "
                        f"AND A.DATA_MOV = (SELECT MIN(B.DATA_MOV) "
                        f"FROM INAFLEX.MOVESTOQUE B WHERE (B.CHAVE_PRODUTO = A.CHAVE_PRODUTO) "
                        f"AND (B.DATA_MOV > TO_DATE('{data}','DD-MM-YYYY')) GROUP BY B.CHAVE_PRODUTO) "
                        f"AND A.CHAVE=(SELECT MIN(C.CHAVE) "
                        f"FROM INAFLEX.MOVESTOQUE C "
                        f"WHERE (C.CHAVE_PRODUTO = A.CHAVE_PRODUTO) "
                        f"AND (C.DATA_MOV > TO_DATE('{data}','DD-MM-YYYY')) GROUP BY C.CHAVE_PRODUTO) "
                        f"AND (D.CODIGO = '{item}')")
            respostas = self.conexao.execute(consulta)

            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    tipo = resposta[3]
                    qtd = resposta[1]
                    saldo = resposta[2]
                    if tipo == "CREDITO":
                        quantidade = saldo - qtd
                    else:
                        quantidade = saldo + qtd

                    demanda = demanda + quantidade
                    estoque_data_inicial = quantidade

            consulta = (f"SELECT SUM(I.QUANTIDADE) "
                        f"FROM INAFLEX.ENTRADAS_ITENS I, INAFLEX.ENTRADAS E, INAFLEX.PRODUTOS P "
                        f"WHERE (I.CHAVE_ENTRADA = E.CHAVE) AND (P.CPROD = I.CHAVE_PRODUTO) "
                        f"AND (E.DATA_EMISSAO >= TO_DATE('{data}','DD-MM-YYYY')) "
                        f"AND (P.CODIGO = '{item}')")
            respostas = self.conexao.execute(consulta)

            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    demanda = demanda + resposta[0]
                    entrada_compras = resposta[0]

            consulta = (f"SELECT SUM(P.QUANTIDADE) "
                        f"FROM INAFLEX.IMPORTACOES_ITENS P, INAFLEX.IMPORTACOES I "
                        f"WHERE (P.CHAVE_IMPORTACAO = I.CHAVE) "
                        f"AND (I.DATA_EMISSAO >= TO_DATE('{data}','DD-MM-YYYY')) "
                        f"AND (P.CODIGO = '{item}')")
            respostas = self.conexao.execute(consulta)

            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    demanda = demanda + resposta[0]
                    entrada_importacao = resposta[0]

            consulta = (f"SELECT SUM(O.QUANTIDADE_PRODUZIDA) "
                        f"FROM INAFLEX.ORDENS O, INAFLEX.PRODUTOS P "
                        f"WHERE (P.CPROD = O.CHAVE_PRODUTO) "
                        f"AND (O.DATA_EMISSAO >= TO_DATE('{data}','DD-MM-YYYY')) "
                        f"AND (P.CODIGO = '{item}')")
            respostas = self.conexao.execute(consulta)

            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    demanda = demanda + resposta[0]
                    entrada_ops = resposta[0]

            demanda = demanda - estoque_atual

            consulta = f"SELECT P.DESCRICAO, P.CUSTO_TOTAL FROM INAFLEX.PRODUTOS P WHERE (P.CODIGO = '{item}')"
            respostas = self.conexao.execute(consulta)

            descricao = "Item não cadastrado"
            for resposta in respostas:
                if resposta[0] and resposta[0] is not None:
                    descricao = resposta[0]
                    custo = resposta[1]

        else:
            qtd_orcados = ""
            qtd_orcamentos = ""
            qtd_vendidos = ""
            qtd_pedidos = ""
            estoque_atual = ""
            estoque_minimo = ""
            demanda = ""
            descricao = ""
            custo = ""

        return (estoque_data_inicial, entrada_compras, entrada_importacao, entrada_ops, qtd_orcados, qtd_orcamentos,
                qtd_vendidos, qtd_pedidos, estoque_atual, estoque_minimo, demanda, descricao, custo)