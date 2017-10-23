import pymysql

conn = pymysql.connect(host='srvhomolog.cipec.net', port=3306, user='root',
passwd='beleza', db='homocipec')
cur = conn.cursor()

sql = "select descricao from pecas where sr_deleted != 'T' and descricao is not null and codigo = '023632'"
cur.execute(sql)
peca = cur.fetchone()

descricao = peca[0]
palavras = peca[0].split()
nova = descricao

# TROCAS OBRIGATORIAS
nova = nova.replace("O'RING","O-RING")
nova = nova.replace('"','POL ')
nova = nova.replace("'","")

for origem in palavras:

    if len(origem) > 2:
        sql = "select destino from palavras where palavras.origem = %s and destino is not null and palavras.sr_deleted != 'T'"
        cur.execute(sql, origem)
        troca = cur.fetchone()

        if troca != None:
            destino = troca[0]
            print(origem,"-",destino)
            nova = nova.replace(origem,destino)

print("ANTIGO[",descricao,"]","NOVO[",nova,"]")
