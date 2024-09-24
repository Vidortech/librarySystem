from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'mysecretkey')

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'biblioteca'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/livros')
def livros():
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM livros")
            livros = cursor.fetchall()
        except Error as e:
            print(f"Erro ao recuperar livros: {e}")
            livros = []
        finally:
            cursor.close()
            conn.close()
        return render_template('list_livros.html', livros=livros)
    flash("Não foi possível conectar ao banco de dados.", "error")
    return redirect(url_for('index'))

@app.route('/add_livro', methods=['GET', 'POST'])
def add_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        codigo_barras = request.form['codigo_barras']

        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO livros (titulo, autor, codigo_barras) VALUES (%s, %s, %s)",
                    (titulo, autor, codigo_barras)
                )
                conn.commit()
                flash("Livro adicionado com sucesso!", "success")
            except Error as e:
                print(f"Erro ao adicionar livro: {e}")
                flash("Erro ao adicionar livro.", "error")
            finally:
                cursor.close()
                conn.close()
        return redirect(url_for('livros'))
    return render_template('add_livro.html')

@app.route('/edit_livro/<int:id>', methods=['GET', 'POST'])
def edit_livro(id):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            if request.method == 'POST':
                titulo = request.form['titulo']
                autor = request.form['autor']
                codigo_barras = request.form['codigo_barras']
                cursor.execute(
                    "UPDATE livros SET titulo = %s, autor = %s, codigo_barras = %s WHERE idLivro = %s",
                    (titulo, autor, codigo_barras, id)
                )
                conn.commit()
                flash("Livro atualizado com sucesso!", "success")
                return redirect(url_for('livros'))

            cursor.execute("SELECT * FROM livros WHERE idLivro = %s", (id,))
            livro = cursor.fetchone()
        except Error as e:
            print(f"Erro ao editar livro: {e}")
            livro = None
        finally:
            cursor.close()
            conn.close()
        return render_template('edit_livro.html', livro=livro)
    flash("Não foi possível conectar ao banco de dados.", "error")
    return redirect(url_for('livros'))

@app.route('/delete_livro/<int:id>', methods=['POST'])
def delete_livro(id):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM livros WHERE idLivro = %s", (id,))
            conn.commit()
            flash("Livro removido com sucesso!", "success")
        except Error as e:
            print(f"Erro ao remover livro: {e}")
            flash("Erro ao remover livro.", "error")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Não foi possível conectar ao banco de dados.", "error")
    return redirect(url_for('livros'))

@app.route('/socios')
def socios():
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM socios")
            socios = cursor.fetchall()
        except Error as e:
            print(f"Erro ao recuperar sócios: {e}")
            socios = []
        finally:
            cursor.close()
            conn.close()
        return render_template('list_socios.html', socios=socios)
    flash("Não foi possível conectar ao banco de dados.", "error")
    return redirect(url_for('index'))

@app.route('/add_socio', methods=['GET', 'POST'])
def add_socio():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO socios (nome, email, telefone) VALUES (%s, %s, %s)",
                    (nome, email, telefone)
                )
                conn.commit()
                flash("Sócio adicionado com sucesso!", "success")
            except Error as e:
                print(f"Erro ao adicionar sócio: {e}")
                flash("Erro ao adicionar sócio.", "error")
            finally:
                cursor.close()
                conn.close()
        return redirect(url_for('socios'))
    return render_template('add_socio.html')

@app.route('/edit_socio/<int:id>', methods=['GET', 'POST'])
def edit_socio(id):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            if request.method == 'POST':
                nome = request.form['nome']
                email = request.form['email']
                telefone = request.form['telefone']
                cursor.execute(
                    "UPDATE socios SET nome = %s, email = %s, telefone = %s WHERE id = %s",
                    (nome, email, telefone, id)
                )
                conn.commit()
                flash("Sócio atualizado com sucesso!", "success")
                return redirect(url_for('socios'))

            cursor.execute("SELECT * FROM socios WHERE id = %s", (id,))
            socio = cursor.fetchone()
        except Error as e:
            print(f"Erro ao editar sócio: {e}")
            socio = None
        finally:
            cursor.close()
            conn.close()
        return render_template('edit_socio.html', socio=socio)
    flash("Não foi possível conectar ao banco de dados.", "error")
    return redirect(url_for('socios'))

@app.route('/delete_socio/<int:id>', methods=['POST'])
def delete_socio(id):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE socios SET status = 'Inativo' WHERE id = %s", (id,))
            conn.commit()
            flash("Sócio removido com sucesso!", "success")
        except Error as e:
            print(f"Erro ao remover sócio: {e}")
            flash("Erro ao remover sócio.", "error")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Não foi possível conectar ao banco de dados.", "error")
    return redirect(url_for('socios'))

@app.route('/movimentacoes')
def movimentacoes():
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(""" 
                SELECT s.nome AS socio, l.titulo AS livro, m.codigo_barras, 
                       m.data_emprestimo, m.data_devolucao, m.prazo_devolucao, m.id
                FROM movimentacoes m
                JOIN socios s ON m.id_socio = s.id
                JOIN livros l ON m.id_livro = l.idLivro
            """)
            movimentacoes = cursor.fetchall()
        except Error as e:
            print(f"Erro ao recuperar movimentações: {e}")
            movimentacoes = []
        finally:
            cursor.close()
            conn.close()
        return render_template('movimentacoes.html', movimentacoes=movimentacoes)
    flash("Não foi possível conectar ao banco de dados.", "error")
    return redirect(url_for('index'))


@app.route('/add_movimentacao', methods=['GET', 'POST'])
def add_movimentacao():
    conn = connect_to_database()
    if conn:
        if request.method == 'POST':
            codigo_barras = request.form.get('codigo_barras')
            id_socio = request.form.get('id_socio')
            id_livro = request.form.get('id_livro')
            data_emprestimo = request.form.get('data_emprestimo')
            prazo_devolucao = request.form.get('prazo_devolucao')

            if not all([codigo_barras, id_socio, id_livro, data_emprestimo, prazo_devolucao]):
                flash("Todos os campos devem ser preenchidos.", "warning")
                return redirect(url_for('add_movimentacao'))

            try:
                cursor = conn.cursor()
                data_emprestimo = datetime.strptime(data_emprestimo, '%Y-%m-%d')
                prazo_devolucao = int(prazo_devolucao)
                data_devolucao = data_emprestimo + timedelta(days=prazo_devolucao)

                # Inserir a movimentação
                cursor.execute(
                    "INSERT INTO movimentacoes (codigo_barras, id_socio, id_livro, data_emprestimo, data_devolucao, prazo_devolucao) VALUES (%s, %s, %s, %s, %s, %s)",
                    (codigo_barras, id_socio, id_livro, data_emprestimo, data_devolucao, prazo_devolucao)
                )

                # Atualizar o status do livro
                cursor.execute(
                    "UPDATE livros SET status = 'Emprestado' WHERE idLivro = %s",
                    (id_livro,)
                )

                conn.commit()
                flash("Movimentação adicionada com sucesso!", "success")
                return redirect(url_for('movimentacoes'))
            except Error as e:
                print(f"Erro ao adicionar movimentação: {e}")
                flash("Erro ao adicionar movimentação.", "error")
            finally:
                cursor.close()
                conn.close()
        else:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT id, nome FROM socios")
                socios = cursor.fetchall()
                cursor.execute("SELECT idLivro, titulo FROM livros")
                livros = cursor.fetchall()
            except Error as e:
                print(f"Erro ao recuperar sócios ou livros: {e}")
                socios = []
                livros = []
            finally:
                cursor.close()
                conn.close()
            return render_template('add_movimentacao.html', socios=socios, livros=livros)
    flash("Não foi possível conectar ao banco de dados.", "error")
    return redirect(url_for('index'))



@app.route('/delete_movimentacao/<int:id>', methods=['POST'])
def delete_movimentacao(id):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()

            # Primeiro, recuperar o id_livro associado à movimentação que será deletada
            cursor.execute("SELECT id_livro FROM movimentacoes WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            
            if resultado:
                id_livro = resultado[0]

                # Remover a movimentação
                cursor.execute("DELETE FROM movimentacoes WHERE id = %s", (id,))
                
                # Atualizar o status do livro para 'Disponível'
                cursor.execute(
                    "UPDATE livros SET status = 'Disponível' WHERE idLivro = %s",
                    (id_livro,)  # Passando como tupla
                )

            conn.commit()
            flash("Movimentação removida com sucesso!", "success")
        except Error as e:
            print(f"Erro ao remover movimentação: {e}")
            flash("Erro ao remover movimentação.", "error")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Não foi possível conectar ao banco de dados.", "error")
    return redirect(url_for('movimentacoes'))




@app.route('/search_livros', methods=['GET'])
def search_livros():
    query = request.args.get('query', '')
    conn = connect_to_database()
    results = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT titulo, autor, codigo_barras 
                FROM livros 
                WHERE titulo LIKE %s OR autor LIKE %s OR codigo_barras LIKE %s
            """, ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
            results = cursor.fetchall()
        except Error as e:
            print(f"Erro ao pesquisar livros: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('search_results_livros.html', results=results, query=query)



@app.route('/search_socios', methods=['GET'])
def search_socios():
    query = request.args.get('query', '')
    conn = connect_to_database()
    results = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT nome, telefone, email 
                FROM socios 
                WHERE nome LIKE %s OR telefone LIKE %s OR email LIKE %s
            """, ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
            results = cursor.fetchall()
        except Error as e:
            print(f"Erro ao pesquisar sócios: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('search_results_socios.html', results=results, query=query)

@app.route('/search_livro', methods=['GET'])
def search_livro():
    codigo_barras = request.args.get('codigo_barras')
    conn = connect_to_database()
    livro = None
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT idLivro, titulo, codigo_barras FROM livros WHERE codigo_barras = %s", (codigo_barras,))
            livro = cursor.fetchone()
        except Error as e:
            print(f"Erro ao buscar livro: {e}")
        finally:
            cursor.close()
            conn.close()
    return jsonify(livro)




if __name__ == '__main__':
    app.run(debug=True)
