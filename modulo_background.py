# BACKGROUND
# ATUALMENTE FAZ APENAS A ATUALIZAÇÃO DA LISTA DOS PEDIDOS EM ACABAMENTO E NO FATURAMENTO
import schedule
import time
from threading import Thread
from modulo_faturamento import Faturamento
from modulo_acabamento import Acabamento


class Background:
    def __init__(self, bd_oracle_ok):
        self.bd_oracle_ok = bd_oracle_ok
        daemon = Thread(target=self.background_task, args=())
        daemon.daemon = True
        daemon.start()

    def background_task(self):
        schedule.every().day.at("19:00").do(self.tarefas)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def tarefas(self):
        Acabamento(self.bd_oracle_ok).atualizar_dados()
        Faturamento(self.bd_oracle_ok).atualizar_faturados()


'''
here for another time u can use following:
schedule.every(10).minutes.do(RunMyCode)
schedule.every().hour.do(RunMyCode)
schedule.every().day.at(“10:30”).do(RunMyCode)
schedule.every(5).to(10).minutes.do(RunMyCode)
schedule.every().monday.do(RunMyCode)
schedule.every(4).seconds.do(RunMyCode)
schedule.every().wednesday.at(“13:15”)do(RunMyCode)
schedule.every().minutes.at(":17").do(RunMyCode)
'''