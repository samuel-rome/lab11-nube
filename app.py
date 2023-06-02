from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configurar la conexión a la base de datos
db_config = {
    'host': 'aws.connect.psdb.cloud',
    'user': 'wsr0pevpkl4971qwxnf1',
    'password': 'pscale_pw_D6khSwMyUmJXE1GJr73ZbrXse8j0P6Je3DGR1bYsedt',
    'database': 'lab11'
}

# Ruta principal
@app.route('/', methods=['GET'])
def index():
    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Obtener los registros de la tabla 'books'
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    # Renderizar el template 'index.html' con los registros obtenidos
    return render_template('index.html', rows=rows)

# Ruta para agregar un libro
@app.route('/add', methods=['POST'])
def add():
    # Obtener los datos del formulario
    title = request.form['title']
    author = request.form['author']

    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insertar el libro en la tabla 'books'
    cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
    conn.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    # Redirigir a la página principal
    return redirect(url_for('index'))

# Ruta para eliminar un libro
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Eliminar el libro de la tabla 'books'
    cursor.execute("DELETE FROM books WHERE id = %s", (id,))
    conn.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    # Redirigir a la página principal
    return redirect(url_for('index'))

# Ruta para editar un libro
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Obtener los datos del formulario de edición
        title = request.form['title']
        author = request.form['author']

        # Actualizar el libro en la tabla 'books'
        cursor.execute("UPDATE books SET title = %s, author = %s WHERE id = %s", (title, author, id))
        conn.commit()

        # Redirigir a la página principal
        return redirect(url_for('index'))
    else:
        # Obtener el libro a editar
        cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
        book = cursor.fetchone()

        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()

        # Renderizar el template 'edit.html' con los datos del libro
        return render_template('edit.html', book=book)

if __name__ == '__main__':
    app.run()