from modulo_atualizar import Atualizar
import time
from banco_de_dados_workflow import BDWorkflow
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from tkinter import *
import sys


class JanelaLogin(QMainWindow):
    def __init__(self, bd_worflow_ok, bd_arquivos_ok, bd_oracle_ok, desenvolvimento, parent=None):
        super().__init__(parent)
        self.logado = False
        self.resultado = ''

        def fecha():
            usuario_ = pegar_usuario.get().upper()
            senha = pegar_senha.get()
            if not atualizar:
                if not desenvolvimento:
                    if senha:
                        resultado = BDWorkflow().verificar_login_db(usuario_, senha)
                        if resultado:
                            self.resultado = resultado[0]
                            self.logado = True
                            janela.destroy()
                        else:
                            QMessageBox.about(self, "Login", "Informações erradas")
                    else:
                        QMessageBox.about(self, "Login", "Informações erradas")
                else:
                    self.resultado = {'direito':1, 'id':1, 'nomeUsuario':usuario_}
                    self.logado = True
                    janela.destroy()
            else:
                QMessageBox.about(self, "Login", "Favor Atualizar APP")

        atualizar = True
        versao_atual = '1.014'
        versao = BDWorkflow().verificar_versao()
        versao = versao[0]['versao']
        if versao == versao_atual:
            mensagem = f'Versao {versao_atual}'
            atualizar = False
        else:
            QMessageBox.about(self, "Login", "Programa será atualizado, apertar ok e reiniciar o APP após a tela de "
                                             "atualização fechar")
            # Atualizar()
            # time.sleep(10)
            sys.exit()

        janela = Tk()
        janela.title("inserir Indice")

        app_width = 250
        app_height = 260
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x_pos = (screen_width / 2) - (app_width / 2)
        y_pos = (screen_height / 2) - (app_height / 2)
        janela.geometry(f'{app_width}x{app_height}+{int(x_pos)}+{int(y_pos)}')

        texto_usuario = Label(janela, text="Usuario:")
        texto_usuario.grid(column=0, row=0, padx=10, pady=10)
        pegar_usuario = Entry(janela, justify=CENTER)
        pegar_usuario.grid(column=1, row=0, padx=5, pady=10)
        pegar_usuario.focus_set()

        texto_senha = Label(janela, text="Senha:")
        texto_senha.grid(column=0, row=1, padx=10, pady=5)
        pegar_senha = Entry(janela, justify=CENTER, show='*')
        pegar_senha.grid(column=1, row=1, padx=5, pady=10)

        botao = Button(janela, text="      Login      ", command=fecha)
        botao.grid(column=1, row=2, padx=0, pady=5)
        janela.bind("<Return>", (lambda event: fecha()))

        texto_versao_label = Label(janela, text="Versão:")
        texto_versao_label.grid(column=0, row=4, padx=10, pady=5)
        texto_versao = Label(janela, text=mensagem)
        texto_versao.grid(column=1, row=4, padx=10, pady=5)

        texto_bd_workflow_label = Label(janela, text="BD-Workflow:")
        texto_bd_workflow_label.grid(column=0, row=5, padx=10, pady=5)
        texto_bd_workflow = Label(janela, text=bd_worflow_ok)
        texto_bd_workflow.grid(column=1, row=5, padx=10, pady=5)

        texto_bd_arquivos_label = Label(janela, text="BD-Arquivos:")
        texto_bd_arquivos_label.grid(column=0, row=6, padx=10, pady=5)
        texto_bd_arquivos = Label(janela, text=bd_arquivos_ok)
        texto_bd_arquivos.grid(column=1, row=6, padx=10, pady=5)

        texto_bd_oracle_label = Label(janela, text="BD-Oracle:")
        texto_bd_oracle_label.grid(column=0, row=7, padx=10, pady=5)
        texto_bd_oracle = Label(janela, text=bd_oracle_ok)
        texto_bd_oracle.grid(column=1, row=7, padx=10, pady=5)

        janela.mainloop()


def log_in(bd_worflow_ok, bd_arquivos_ok, bd_oracle_ok, desenvolvimento):
    janela_login = JanelaLogin(bd_worflow_ok, bd_arquivos_ok, bd_oracle_ok, desenvolvimento)
    resultado = janela_login.resultado
    logado = janela_login.logado
    return resultado, logado
