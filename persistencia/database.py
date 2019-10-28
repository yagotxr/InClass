# Módulo de conexão com o MySql
import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    database='mysql',
    user='root',
    password=''
)
