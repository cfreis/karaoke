def removeFila(con):
    cur = con.cursor()
    cur.execute('DELETE FROM fila')
    con.commit()
    cur.close()
    
def removeFilaFirst(con, codigo):
    cur = con.cursor()
    sql = 'DELETE FROM fila WHERE codigo = "'+codigo+'";'
    cur.execute(sql)
    con.commit()
    cur.close()

def insertFila(con,nome,titulo, codigo):
    cur = con.cursor()
    sql='INSERT INTO fila VALUES("'+nome+'","'+titulo+'","'+codigo+'")'
    print(sql)
    cur.execute(sql)
    con.commit()
    cur.close
    
def selectFila(con):
    cur = con.cursor()
    cur.execute('SELECT * FROM fila')
    data=cur.fetchall()
    return(data)

def select1Fila(con):
    cur = con.cursor()
    cur.execute('SELECT * FROM fila limit 1')
    data=cur.fetchall()
    return(data)

def countFila(con):
    cur = con.cursor()
    cur.execute('SELECT count(*) FROM fila')
    data=cur.fetchall()
    return(data)

def getNextCodigo(con):
    cur = con.cursor()
    sql = 'SELECT MAX(CAST(codigo as INTEGER)) FROM musicas'
    cur.execute(sql)
    data=cur.fetchall()[0][0]+1 
    return(data)
     
def insertMusica(con, cantor, codigo, titulo, letra, idioma):
    cur = con.cursor()
    sql='INSERT INTO musicas VALUES ("'+cantor+'","'+str(codigo)+'","'+titulo+'","'+letra+'","'+idioma+'")'
    print(sql)
    #return(0)
    erro = 0
    try:
        cur.execute(sql)
        con.commit()
        cur.close
    except:
        erro = 1
    return(erro)

def deleteMusica(con, codigo):
    cur = con.cursor()
    sql='DELETE FROM musicas WHERE CODIGO = "'+str(codigo)+'"'
    cur.execute(sql)
    con.commit()
    cur.close
    

def select(con, titulo, cantor):
    cur = con.cursor()
    if titulo == '' and cantor == '':
        sql="SELECT * FROM musicas ORDER BY titulo"
    if titulo != '' and cantor == '':
        sql='SELECT * FROM musicas WHERE titulo like "%'+titulo+'%" ORDER BY titulo'
    if titulo == '' and cantor != '':
        sql='SELECT * FROM musicas WHERE cantor like "%'+cantor+'%" ORDER BY titulo'
    if titulo != '' and cantor != '':
        sql='SELECT * FROM musicas WHERE cantor like "%'+cantor+'%" and titulo like "%'+titulo+'%" ORDER BY titulo'
    #print(sql)
    cur.execute(sql)
    data=cur.fetchall()
    return(data)

def atuRanking(con, codigo):
    cur = con.cursor()
    sql = 'select count(*) from ranking where codigo = "'+str(codigo)+'"'
    cur.execute(sql)
    contagem = cur.fetchall()[0][0]
    print(contagem)
    if contagem == 0:
        sql = 'insert into ranking values ("'+str(codigo)+'", 1)'
        cur.execute(sql)
    else:
        sql = 'select contagem from ranking where codigo = "'+str(codigo)+'"'
        cur.execute(sql)
        contagem = cur.fetchall()[0][0]
        print(contagem)
        sql = 'update ranking set contagem = '+ str(contagem +1)+ ' WHERE codigo = "'+str(codigo)+'"'
        cur.execute(sql)
    con.commit()
    cur.close
