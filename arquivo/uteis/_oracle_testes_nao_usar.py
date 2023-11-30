import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"C:\app\client\sami\product\12.1.0\client_1")
conn = cx_Oracle.connect('CONSULTA/INAFLEX@INAFLEX')
conexao = conn.cursor()
valor = '07.471.932/0001-61'
consulta = f"select codvendedor, nomered from inaflex.vendedores where inativo='NAO'"
respostas = conexao.execute(consulta)
for resposta in respostas:
    resposta1 = resposta[0]
    resposta2 = resposta[1]
    print(resposta1)
    print(resposta2)
conn.close()

