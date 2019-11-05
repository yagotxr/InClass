from database import conexao


class QueryService:

    def __init__(self, db_env, db):
        self._db_env = db_env
        self._db = db
        self._conn = conexao(self._db_env, self._db).conn

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

    def getDisciplinas(self):
        cursor = self._conn.cursor(buffered=True)
        query = "SELECT id FROM `tbdisciplina` WHERE id_escola = 2"
        cursor.execute(query)
        rs = cursor.fetchone()
        if not rs:
            return None

        return {}

    def getSalas(self):
        cursor = self._conn.cursor(buffered=True)
        query = "SELECT id FROM `tbsalas` WHERE id_escola = 2"
        cursor.execute(query)
        rs = cursor.fetchone()
        if not rs:
            return None

        return {}