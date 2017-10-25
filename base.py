import pymysql
import enchant

def conecta_banco()
    return pymysql.connect(host='srvhomolog.cipec.net', port=3306, user='root', passwd='beleza', db='homocipec')


def gera_base_dados()
    conn = conecta_banco()
    conn.show_warnings()
    cur = conn.cursor()

    cur.execute(
        "select pecas.descricao, pecas.codigo from pecas where pecas.sr_deleted != 'T' and codigo > 023600")
    pecas = cur.fetchall()

    for peca in pecas:
        if peca[0] == None:
            continue  # volta para o for

        palavras = peca[0].split()
        # print(peca[1])

        for palavra in palavras:
            palavra = palavra.replace('"', '')
            palavra = palavra.replace("'", "")

            # print('\t',palavra)

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
            print(peca[1], palavra, sql % (incidencia, palavra))
            cur.execute(sql % (incidencia, palavra))
            conn.commit()


def trocar_palavra(descricao)
    conn = conecta_banco()
    cur = conn.cursor()

    palavras = descricao.split()
    nova = descricao

    # TROCAS OBRIGATORIAS
    nova = nova.replace("O'RING", "O-RING")
    nova = nova.replace('"', 'POL ')
    nova = nova.replace("'", "")

    for origem in palavras:

        if len(origem) > 2:
            sql = "select destino from palavras where palavras.origem = %s and destino is not null and palavras.sr_deleted != 'T'"
            cur.execute(sql, origem)
            troca = cur.fetchone()

            if troca != None:
                destino = troca[0]
                print(origem, "-", destino)
                nova = nova.replace(origem, destino)

    #print("ANTIGO[", descricao, "]", "NOVO[", nova, "]")

    return (nova)


def verifica_ortografia(descricao)
    d = enchant.Dict("pt_BR")

    for palavra in descricao.split():
        if d.check(palavra):
            if d.check(palavra)

            
    return (descricao_corrigida)