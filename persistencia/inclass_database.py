import mysql.connector


conexao = mysql.connector.connect(
    host='localhost',
    database='inclass',
    user='root',
    password='root',
    port=8889
)

cursor = conexao.cursor(buffered=True)


def exemplo_query(self):
    cursor = self._conn.cursor(buffered=True)
    query = """ 
    select  
    ... 
    """
    cursor.execute(query)
    rs = cursor.fetchone()

    if not rs:
        return None

    return {}


def get_disciplinas():
    query = "SELECT nome FROM tbdisciplina WHERE id_escola = 2 LIMIT 6"

    return _executa_query(query)


def get_salas():
    query = "SELECT id , capacidade FROM tbsala LIMIT 4"

    return _executa_query(query)


def _executa_query(query: str):
    cursor.execute(query)
    retorno_query = cursor.fetchall()

    return retorno_query

retorno_disciplinas = get_disciplinas()

disciplinas = []

for i in retorno_disciplinas:
    disciplinas.append(str(i[0]))

print(disciplinas)