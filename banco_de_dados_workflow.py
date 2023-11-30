import pymysql.cursors
import re


class BDWorkflow:
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

    def combobox_select(self, usuario):
        consulta = f"SELECT nome FROM selecao WHERE usuario = '{usuario}' ORDER BY nome"
        self.cursor.execute(consulta)
        self.conn.commit()
        resultados = self.cursor.fetchall()
        return resultados

    def selecionar_select(self, nome, usuario):
        try:
            consulta = f"SELECT selecao FROM selecao WHERE nome = '{nome}' AND usuario = '{usuario}'"
            self.cursor.execute(consulta)
            self.conn.commit()
            resultado = self.cursor.fetchall()
            resultado = resultado[0]['selecao']
            resultado = re.sub(r"&!", r"'", resultado)
            msg = False
            mensagem = f''
            return resultado, msg, mensagem
        except:
            resultado = ''
            msg = True
            mensagem = f'SELECT não encontrado'
            return resultado, msg, mensagem

    def apagar_select(self, nome, usuario):
        try:
            consulta = f"DELETE FROM selecao WHERE nome = '{nome}' AND usuario = '{usuario}'"
            self.cursor.execute(consulta)
            self.conn.commit()
            msg = True
            mensagem = f'SELECT {nome} removido'
            return msg, mensagem
        except:
            msg = True
            mensagem = f'Erro ao tentar remover {nome}'
            return msg, mensagem

    def salva_select(self, nome, select, usuario):
        try:
            select = re.sub(r"'", r"&!", select)
            consulta = f"INSERT INTO selecao (nome, selecao, usuario) VALUES ('{nome}', '{select}', '{usuario}')"
            self.cursor.execute(consulta)
            self.conn.commit()
            msg = True
            mensagem = f'SELECT {nome} Salvo'
            return msg, mensagem
        except:
            msg = False
            mensagem = f'Erro ao salvar SELECT'
            return msg, mensagem

    def mostrar_eventos_db(self, finalizados, data, eu=None, evento=None, tipodeevento=None, usuario=None,
                           orcamento=None, pedido=None, m_pendencias=None, m_eventos=None, espera=None):
        data = f'"{data}"'
        if m_eventos:
            log_usuario = f'"{eu}"'
        else:
            log_usuario = 'logUsuario'
        if not evento:
            evento = 'id'
        if not tipodeevento:
            tipodeevento = 'tipoEvento'
        else:
            tipodeevento = f'"{tipodeevento}"'
        if m_pendencias:
            usuario = f'"{eu}"'
        else:
            if not usuario:
                usuario = 'usuario'
            else:
                usuario = f'"{usuario}"'
        if orcamento == '':
            orcamento = 0
        if pedido == '':
            pedido = 0
        if not orcamento:
            orcamento = 'numOrc'
        if not pedido:
            pedido = 'numPed'
        if espera != 1:
            espera = 'espera'
        consulta = f'SELECT id, numOrc, numPed, usuario, tipoEvento, estagio, espera FROM eventos ' \
                   f'WHERE id={evento} AND tipoEvento={tipodeevento} AND usuario={usuario} AND ' \
                   f'numOrc={orcamento} AND numPed ={pedido} AND ativo={finalizados} AND logUsuario={log_usuario} ' \
                   f'AND espera = {espera} AND logData<={data} ORDER BY id ASC;'
        self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def combobox_usuarios(self):
        consulta = "SELECT nomeUsuario FROM usuarios WHERE ativo = '1' ORDER BY nomeUsuario"
        self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def combobox_tipo_de_evento(self):
        consulta = 'SELECT tipoEvento FROM tipoeventos ORDER BY tipoEvento'
        self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def seleciona_comentarios(self, pedido):
        consulta = 'SELECT comentario, logUsuario, logData FROM comentario WHERE eventoID=%s ORDER BY id DESC'
        self.cursor.execute(consulta, pedido)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def criar_evento(self, tipo, usuario_logado, pedido=None, orcamento=None):
        if pedido == '':
            pedido = 0
        if orcamento == '':
            orcamento = 0
        try:
            pedido = int(pedido)
            orcamento = int(orcamento)
        except:
            mensagem = "Formato errado de Pedido ou Orcamento"
            msg = True
            return msg, mensagem
        consulta = 'INSERT INTO eventos ' \
                   '(tipoEvento, numPed, numOrc, usuario, estagio, logUsuario, logData, diretoria, pendencia, ' \
                   'checklist, ativo) VALUES (%s, %s, %s, %s, 0, %s, CURRENT_TIMESTAMP(), 0, 0, "N/A", 1)'
        self.cursor.execute(consulta, (tipo, pedido, orcamento, usuario_logado, usuario_logado))
        self.conn.commit()
        msg = False
        mensagem = ''
        return msg, mensagem

    def proxima_etapa(self, evento, orcamento, pedido, comentario, usuario_logado, etapa, tipo_evento):
        direito = False
        passo_prox = 0
        usuario_prox = ''
        if pedido == '':
            pedido = 0
        if orcamento == '':
            orcamento = 0
        try:
            pedido = int(pedido)
            orcamento = int(orcamento)
        except:
            mensagem = "Formato errado de Pedido ou Orcamento"
            msg = True
            return msg, mensagem
        # CHECA SE O USUARIO QUE APERTOU O BOTÃO É O "DONO" DO EVENTO
        consulta = "SELECT usuario FROM eventos " \
                   "WHERE id=%s"
        self.cursor.execute(consulta, evento)
        self.conn.commit()
        resultados = self.cursor.fetchall()
        for resultado_ in resultados:
            usuario_prox = resultado_['usuario']
            if usuario_prox == usuario_logado:
                direito = True
        # SE O USUARIO PASSOU NO TESTE ACIMA, INICIA A PRÓXIMA FUNÇÃO
        if direito:
            # PEGA VALORES DA PROXIMA ETAPA E DO PROXIMO USUARIO E VE SE USUARIO ATUAL ESTA PREENCHIDO
            consulta = "SELECT usuarioProx, passoProx FROM workflow " \
                       "WHERE tipoEvento=%s AND passoAtual=%s AND usuarioAtual=%s"
            self.cursor.execute(consulta, (tipo_evento, etapa, usuario_logado))
            self.conn.commit()
            resultados = self.cursor.fetchall()
            # SE NÃO TIVER UMA REGRA ESPECIFICA NESSA ETAPA PARA ESSE USUARIO ELE VALORES DA PROXIMA ETAPA E DO PROXIMO
            # USUARIO DE USUARIO ATUAL EM BRANCO (GENERICO)
            if not resultados:
                consulta = "SELECT usuarioProx, passoProx FROM workflow " \
                           "WHERE tipoEvento=%s AND passoAtual=%s AND usuarioAtual=''"
                self.cursor.execute(consulta, (tipo_evento, etapa))
                self.conn.commit()
                resultados = self.cursor.fetchall()
                for resultado_ in resultados:
                    usuario_prox = resultado_['usuarioProx']
                    passo_prox = resultado_['passoProx']
            else:
                for resultado_ in resultados:
                    usuario_prox = resultado_['usuarioProx']
                    passo_prox = resultado_['passoProx']
            # A SEQUENCIA ABAIXO if passo_prox == ?: É PARA DEFINIR QUAL CAMPO PEGAR PARA logEstagio? SE TIVER RETORNO,
            # SUBSTITUI O PROXIMO USUARIO PARA ESSE USUARIO. ISSO É´FEITO PARA GARANTIR QUE O EVENTO VAI PARA QUEM
            # RETORNOU E NÃO PARA UMA PESSOA NOVA
            if passo_prox == 1:
                consulta = f"SELECT logEstagio2 FROM eventos WHERE id = {evento}"
                self.cursor.execute(consulta)
                self.conn.commit()
                resultados = self.cursor.fetchall()
                if resultados[0]['logEstagio2']:
                    usuario_prox = resultados[0]['logEstagio2']
            if passo_prox == 2:
                consulta = f"SELECT logEstagio3 FROM eventos WHERE id = {evento}"
                self.cursor.execute(consulta)
                self.conn.commit()
                resultados = self.cursor.fetchall()
                if resultados[0]['logEstagio3']:
                    usuario_prox = resultados[0]['logEstagio3']
            if passo_prox == 3:
                consulta = f"SELECT logEstagio4 FROM eventos WHERE id = {evento}"
                self.cursor.execute(consulta)
                self.conn.commit()
                resultados = self.cursor.fetchall()
                if resultados[0]['logEstagio4']:
                    usuario_prox = resultados[0]['logEstagio4']
            if passo_prox == 4:
                consulta = f"SELECT logEstagio5 FROM eventos WHERE id = {evento}"
                self.cursor.execute(consulta)
                self.conn.commit()
                resultados = self.cursor.fetchall()
                if resultados[0]['logEstagio5']:
                    usuario_prox = resultados[0]['logEstagio5']
            if passo_prox == 5:
                consulta = f"SELECT logEstagio6 FROM eventos WHERE id = {evento}"
                self.cursor.execute(consulta)
                self.conn.commit()
                resultados = self.cursor.fetchall()
                if resultados:
                    if resultados[0]['logEstagio6'] != None:
                        usuario_prox = resultados[0]['logEstagio6']
            # DEFINE VALOR DE ATIVO PARA SALVAR NA HORA DO UPDATE
            if passo_prox == 99:
                ativo = 0
            else:
                ativo = 1
            # PEGA VALOR DE logUsuario E estagio. logUsuario É O USUARIO QUE CRIOU O EVENTO
            consulta = 'SELECT logUsuario, estagio FROM eventos ' \
                       'WHERE id=%s'
            self.cursor.execute(consulta, evento)
            self.conn.commit()
            resultado__ = self.cursor.fetchall()
            estagio = resultado__[0]['estagio']
            usuario_temp = usuario_prox
            # TODA VEZ QUE usuario_prox ESTIVER EM BRANCO NO WORKFLOW,
            # ELE PASSA O EVENTO PARA O CRIADOR DO EVENTO (logUsuario)
            if usuario_prox == '':
                usuario_prox = resultado__[0]['logUsuario']
            # ESSA PARTE PEGA EVENTOS NO ESTAGIO 0 E IMPLEMENTA O PROCESSO RANDOMICO EM CRIAR ORCAMENTOS
            if usuario_temp == '' and estagio == 0:
                consulta = f"SELECT logEstagio2 FROM eventos " \
                           f"WHERE id = {evento}"
                self.cursor.execute(consulta)
                self.conn.commit()
                resultados = self.cursor.fetchall()
                resultado = resultados[0]['logEstagio2']
                if resultado:
                    usuario_prox = resultado
                else:
                    consulta = f"SELECT nomeUsuario FROM usuarios " \
                               f"WHERE orcamentista = 1"
                    self.cursor.execute(consulta)
                    self.conn.commit()
                    resultados = self.cursor.fetchall()
                    lista_orcamentistas = []
                    for usuario in resultados:
                        usuario_pesquisa = usuario['nomeUsuario']
                        consulta = f"SELECT COUNT(CASE WHEN usuario = '{usuario_pesquisa}' " \
                                   f"AND estagio = 1 AND espera <> '1' " \
                                   f"AND tipoEvento = 'FAZER ORCAMENTO' THEN 1 END) FROM eventos"
                        self.cursor.execute(consulta)
                        self.conn.commit()
                        resultados = self.cursor.fetchall()
                        usuario['qtd'] = resultados[0][f"COUNT(CASE WHEN usuario = '{usuario_pesquisa}' " \
                                                       f"AND estagio = 1 AND espera <> '1' " \
                                                       f"AND tipoEvento = 'FAZER ORCAMENTO' THEN 1 END)"]
                        lista_orcamentistas.append(usuario)
                    qtd = 1000
                    for i in range(len(lista_orcamentistas)):
                        qtd_nova = lista_orcamentistas[i]['qtd']
                        if qtd_nova < qtd:
                            usuario_prox = lista_orcamentistas[i]['nomeUsuario']
                            qtd = qtd_nova
            consulta = f"UPDATE eventos SET usuario='{usuario_prox}', ativo={ativo}, estagio={passo_prox}, " \
                       f"numOrc={orcamento}, numPed={pedido}, logUltimo=CURRENT_TIMESTAMP(), espera = '0', "
            if estagio == 0:
                consulta += f"logEstagio1='{usuario_logado}'"
            if estagio == 1:
                consulta += f"logEstagio2='{usuario_logado}'"
            if estagio == 2:
                consulta += f"logEstagio3='{usuario_logado}'"
            if estagio == 3:
                consulta += f"logEstagio4='{usuario_logado}'"
            if estagio == 4:
                consulta += f"logEstagio5='{usuario_logado}'"
            if estagio == 5:
                consulta += f"logEstagio6='{usuario_logado}'"
            if passo_prox == 99:
                consulta += f", logFinal=CURRENT_TIMESTAMP()"
            consulta += f" WHERE id={evento} "
            self.cursor.execute(consulta)
            self.conn.commit()
            consulta = f"INSERT INTO comentario (eventoID, comentario, logUsuario, logData) " \
                       f"VALUES ({evento}, '{comentario}', '{usuario_logado}', CURRENT_TIMESTAMP())"
            self.cursor.execute(consulta)
            self.conn.commit()

            #FINALIZACAO EVENTO DE MANUTENCAO
            if tipo_evento == "MANUTENCAO - P1" or evento == "MANUTENCAO - P2":
                if passo_prox == 99:
                    consulta = f"UPDATE relatorio_parada_maquinas SET fim=CURRENT_TIMESTAMP() " \
                               f"WHERE id={evento}"
                    self.cursor.execute(consulta)
                    self.conn.commit()
            #################################

            mensagem = f''
            msg = False
            return msg, mensagem
        else:
            mensagem = f'Voce não pode alterar esse evento'
            msg = True
            return msg, mensagem

    def volta_etapa(self, evento, comentario, usuario_logado, etapa):
        usuario_prox = ''
        if etapa == '0':
            mensagem = f'Não tem como returnar eventos no Estágio 0 (Zero)'
            msg = True
            return msg, mensagem
        if etapa == '99' or etapa == '90':
            mensagem = f'Evento ja está finalizado'
            msg = True
            return msg, mensagem
        else:
            consulta = f"SELECT usuario FROM eventos WHERE id = {evento}"
            self.cursor.execute(consulta)
            self.conn.commit()
            resultados = self.cursor.fetchall()
            usuario = resultados[0]['usuario']
            if usuario == usuario_logado:
                if etapa == '5':
                    consulta = f"SELECT logEstagio5 FROM eventos WHERE id = {evento}"
                    self.cursor.execute(consulta)
                    self.conn.commit()
                    resultados = self.cursor.fetchall()
                    usuario_prox = resultados[0]['logEstagio5']
                elif etapa == '4':
                    consulta = f"SELECT logEstagio4 FROM eventos WHERE id = {evento}"
                    self.cursor.execute(consulta)
                    self.conn.commit()
                    resultados = self.cursor.fetchall()
                    usuario_prox = resultados[0]['logEstagio4']
                elif etapa == '3':
                    consulta = f"SELECT logEstagio3 FROM eventos WHERE id = {evento}"
                    self.cursor.execute(consulta)
                    self.conn.commit()
                    resultados = self.cursor.fetchall()
                    usuario_prox = resultados[0]['logEstagio3']
                elif etapa == '2':
                    consulta = f"SELECT logEstagio2 FROM eventos WHERE id = {evento}"
                    self.cursor.execute(consulta)
                    self.conn.commit()
                    resultados = self.cursor.fetchall()
                    usuario_prox = resultados[0]['logEstagio2']
                elif etapa == '1':
                    consulta = f"SELECT logEstagio1 FROM eventos WHERE id = {evento}"
                    self.cursor.execute(consulta)
                    self.conn.commit()
                    resultados = self.cursor.fetchall()
                    usuario_prox = resultados[0]['logEstagio1']
                else:
                    pass
            else:
                mensagem = f'Voce não pode alterar esse evento'
                msg = True
                return msg, mensagem
            passo_prox = int(etapa) - 1
            if etapa == '1':
                consulta = f"UPDATE eventos SET usuario='{usuario_prox}', pendencia=1, " \
                           f"estagio={passo_prox}, logEstagio2='{usuario_logado}', " \
                           f"logUltimo=CURRENT_TIMESTAMP() WHERE id={evento}"
            if etapa == '2':
                consulta = f"UPDATE eventos SET usuario='{usuario_prox}', pendencia=1, " \
                           f"estagio={passo_prox}, logEstagio3='{usuario_logado}', " \
                           f"logUltimo=CURRENT_TIMESTAMP() WHERE id={evento}"
            if etapa == '3':
                consulta = f"UPDATE eventos SET usuario='{usuario_prox}', pendencia=1, " \
                           f"estagio={passo_prox}, logEstagio4='{usuario_logado}', " \
                           f"logUltimo=CURRENT_TIMESTAMP() WHERE id={evento}"
            if etapa == '4':
                consulta = f"UPDATE eventos SET usuario='{usuario_prox}', pendencia=1, " \
                           f"estagio={passo_prox}, logEstagio5='{usuario_logado}', " \
                           f"logUltimo=CURRENT_TIMESTAMP() WHERE id={evento}"
            if etapa == '5':
                consulta = f"UPDATE eventos SET usuario='{usuario_prox}', pendencia=1, " \
                           f"estagio={passo_prox}, logEstagio6='{usuario_logado}', " \
                           f"logUltimo=CURRENT_TIMESTAMP() WHERE id={evento}"
            self.cursor.execute(consulta)
            self.conn.commit()
            consulta = f"INSERT INTO comentario (eventoID, comentario, logUsuario, logData) " \
                       f"VALUES ({evento}, '{comentario}', '{usuario_logado}', CURRENT_TIMESTAMP())"
            self.cursor.execute(consulta)
            self.conn.commit()
            mensagem = f''
            msg = False
            return msg, mensagem

    def adotar_evento(self, evento, tipo_evento, estagio, usuario_logado):
        consulta = f"SELECT usuario FROM direitos " \
                   f"WHERE direito1 = '{tipo_evento}' AND direito2 = {estagio} AND usuario = '{usuario_logado}'"
        self.cursor.execute(consulta)
        self.conn.commit()
        resultados = self.cursor.fetchall()
        if resultados:
            consulta = f"UPDATE eventos SET usuario='{usuario_logado}' WHERE id = {evento}"
            self.cursor.execute(consulta)
            self.conn.commit()
            mensagem = f''
            msg = False
            return msg, mensagem
        else:
            mensagem = f'Você não tem direito para adotar esse evento nesse estágio'
            msg = True
            return msg, mensagem

    def verificar_login_db(self, usuario, senha):
        consulta = 'SELECT * FROM usuarios WHERE nomeUsuario=%s AND senhaUsuario=%s'
        self.cursor.execute(consulta, (usuario, senha))
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def verificar_versao(self):
        consulta = 'SELECT versao FROM versao'
        self.cursor.execute(consulta)
        self.conn.commit()
        resultado = self.cursor.fetchall()
        return resultado

    def alterar_evento(self, evento, novo_tipo_evento):
        consulta = f"UPDATE eventos SET tipoEvento='{novo_tipo_evento}' WHERE id = {evento}"
        self.cursor.execute(consulta)
        self.conn.commit()

    def atualiza_extra_bd(self, evento, comentario, orcamento, espera, usuario_logado):
        direito = False
        if orcamento == '':
            orcamento = 0
        consulta = "SELECT usuario FROM eventos " \
                   "WHERE id=%s"
        self.cursor.execute(consulta, evento)
        self.conn.commit()
        resultados = self.cursor.fetchall()
        for resultado_ in resultados:
            usuario_prox = resultado_['usuario']
            if usuario_prox == usuario_logado:
                direito = True
            else:
                msg = True
                mensagem = 'So é permitido alterar seus proprios eventos'
                return msg, mensagem
        if direito:
            if orcamento != 0:
                consulta = f"UPDATE eventos SET numOrc = {orcamento}, espera = '{espera}' WHERE id = {evento}"
                self.cursor.execute(consulta)
                self.conn.commit()
            else:
                consulta = f"UPDATE eventos SET espera = '{espera}' WHERE id = {evento}"
                self.cursor.execute(consulta)
                self.conn.commit()
            if len(comentario) >= 5:
                consulta = f"INSERT INTO comentario (eventoID, comentario, logUsuario, logData) " \
                           f"VALUES ({evento}, '{comentario}', '{usuario_logado}', CURRENT_TIMESTAMP())"
                self.cursor.execute(consulta)
                self.conn.commit()
        msg = False
        mensagem = ''
        return msg, mensagem
