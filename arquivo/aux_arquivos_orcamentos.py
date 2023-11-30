from PyQt5.QtWidgets import QMainWindow, QMessageBox
from tkinter import *


class JanelaInsereArquivo(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.indice = None
        self.atual = None
        self.cadeado = False
        self.titulo = ''

        def fecha():
            self.indice = pegar.get()
            if atual_valor.get():
                self.atual = '0'
            else:
                self.atual = '1'
            janela.destroy()

        # Pastas.atualiza_arvore(pedido)
        janela = Tk()
        janela.title("Inserir indice")
        janela.focus_set()

        app_width = 300
        app_height = 120
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x_pos = (screen_width / 2) - (app_width / 2) - 205
        y_pos = (screen_height / 2) - (app_height / 2) - 50
        janela.geometry(f'{app_width}x{app_height}+{int(x_pos)}+{int(y_pos)}')

        texto = Label(janela, text="Qual Indice?")
        texto.grid(column=0, row=0, padx=10, pady=0)
        texto.place(relx=0.5, y=15, anchor=CENTER)
        pegar = Entry(janela, justify=CENTER)
        pegar.grid(column=0, row=1, padx=10, pady=0)
        pegar.place(relx=0.5, y=40, anchor=CENTER)
        pegar.focus_set()
        atual_valor = IntVar()
        check = Checkbutton(janela, text='Arquivo', variable=atual_valor, onvalue=1, offvalue=0)
        check.grid(column=0, row=2, padx=10, pady=5)
        check.place(relx=0.5, y=70, anchor=CENTER)
        botao = Button(janela, text="      OK      ", command=fecha)
        botao.grid(column=0, row=3, padx=0, pady=5)
        botao.place(relx=0.5, y=100, anchor=CENTER)
        janela.bind("<Return>", (lambda event: fecha()))
        janela.mainloop()
