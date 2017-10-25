import pymysql
import enchant

def conecta_banco():
    return pymysql.connect(host='srvhomolog.cipec.net', port=3306, user='root', passwd='beleza', db='homocipec')


def pegar_descricao(codigo=''):
    conn = conecta_banco()
    conn.show_warnings()
    cur = conn.cursor()

    if codigo is None:
        sql = "select pecas.descricao, pecas.codigo from pecas where pecas.sr_deleted != 'T'"
    else:
        sql = "select pecas.descricao, pecas.codigo from pecas where pecas.sr_deleted != 'T' and codigo = '"+codigo+"' "

    cur.execute(sql)
    return cur.fetchall()


def gerar_base_dados(codigo=''):
    conn = conecta_banco()
    conn.show_warnings()
    cur = conn.cursor()

    pecas = pegar_descricao(codigo)
    for peca in pecas:
        if peca[0] == None:
            continue  # volta para o for

        palavras = peca[0].split()
        for palavra in palavras:
            palavra = palavra.replace('"', '')
            palavra = palavra.replace("'", "")

            sql = "select incidencia from palavras where palavras.origem=%s"
            cur.execute(sql, palavra)
            result = cur.fetchone()

            if result == None:
                incidencia = 0
                sql = "INSERT INTO palavras (`incidencia`, `origem`, `sr_deleted`) VALUES (%s, '%s', '')"
            else:
                incidencia = int(result[0])
                sql = "UPDATE palavras SET `incidencia` = %s WHERE `origem` = '%s'"

            incidencia = incidencia + 1
            print(peca[1], palavra, sql % (incidencia, palavra))
            cur.execute(sql % (incidencia, palavra))
            conn.commit()


def verifica_descricao(descricao):
    conn = conecta_banco()
    cur = conn.cursor()

    palavras = descricao.split()
    descricao_corrigida = descricao

    # TROCAS OBRIGATORIAS
    descricao_corrigida = descricao_corrigida.replace("O'RING", "O-RING")
    descricao_corrigida = descricao_corrigida.replace('"', 'POL ')
    descricao_corrigida = descricao_corrigida.replace("'", "")

    for origem in palavras:
        if len(origem) > 2:
            sql = "select destino from palavras where palavras.origem = %s and destino is not null and palavras.sr_deleted != 'T'"
            cur.execute(sql, origem)
            troca = cur.fetchone()

            if troca != None:
                destino = troca[0]
                descricao_corrigida = descricao_corrigida.replace(origem, destino)

    return (descricao_corrigida)


def verifica_ortografia(descricao):
    d = enchant.Dict("pt_BR")
    descricao_ortografia_corrigida = ''

    for palavra in descricao.split():
        if d.check(palavra):
           descricao_ortografia_corrigida = descricao_ortografia_corrigida + ' ' + palavra
        else:
           #selecionar qual a palavra mais correta
           #print(d.suggest(palavra))
           t = d.suggest(palavra)
           descricao_ortografia_corrigida = descricao_ortografia_corrigida + ' ' + t[0]

    return (descricao_ortografia_corrigida.strip())