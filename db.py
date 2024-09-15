# db.py
import mysql.connector 
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='biblioteca',
            user='root',
            password=''
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def adicionar_livro(titulo, autor, codigo_barras):
    conexao = conectar()
    if conexao is None:
        return

    cursor = conexao.cursor()
    sql = "INSERT INTO livros (titulo, autor, codigo_barras) VALUES (%s, %s, %s)"
    valores = (titulo, autor, codigo_barras)
    try:
        cursor.execute(sql, valores)
        conexao.commit()
        print("Livro adicionado com sucesso!")
    except Error as e:
        print(f"Erro ao adicionar livro: {e}")
    finally:
        cursor.close()
        conexao.close()

def listar_livros():
    conexao = conectar()
    if conexao is None:
        return []

    cursor = conexao.cursor()
    sql = "SELECT * FROM livros"
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao listar livros: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()
