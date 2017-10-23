import pymysql

conn = pymysql.connect(host='srvhomolog.cipec.net', port=3306, user='root',
passwd='beleza', db='homocipec')
conn.show_warnings()
cur = conn.cursor()

cur.execute("select pecas.descricao, pecas.codigo from pecas where pecas.sr_deleted != 'T' and codigo > 023600")
pecas = cur.fetchall()

for peca in pecas:
    if peca[0] == None:
       continue

    palavras = peca[0].split()
    #print(peca[1])

    for palavra in palavras:
        palavra = palavra.replace('"','')
        palavra = palavra.replace("'","")

        #print('\t',palavra)

        sql = "select incidencia from palavras where palavras.origem=%s"
        cur.execute(sql, palavra)
        result = cur.fetchone()

        if result == None:
            incidencia = 0
        else:
            incidencia = int(result[0])

        if incidencia == 0:
            sql = "INSERT INTO palavras (`incidencia`, `origem`, `sr_deleted`) VALUES (%s, '%s', '')"
        else:
            sql = "UPDATE palavras SET `incidencia` = %s WHERE `origem` = '%s'"

        incidencia = incidencia + 1
        print(peca[1],palavra,sql%(incidencia,palavra))
        cur.execute(sql%(incidencia,palavra))
        conn.commit()

