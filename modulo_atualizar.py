# ATUALIZAR SISTEMA AUTOMATICO. ESTA DESABILITADO
# NAO É CHAMADO PELO APP.PY PRECISA IMPLEMENTAR ISSO PARA FUNCIONAR
from threading import Thread
import os
import subprocess


class Atualizar:
    def __init__(self):
        daemon = Thread(target=self.background_task, args=())
        daemon.daemon = True
        daemon.start()

    @staticmethod
    def background_task():
        subprocess.call(r'c:\Inaflex\atualizar.bat', shell=True)
#        os.system(r'c:\Inaflex\atualizar.bat')
