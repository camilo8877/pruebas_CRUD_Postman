# app.py (API REST con JSON)
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Conexión DB
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicializar DB
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 🔹 GET - Obtener todos los usuarios
@app.route('/usuarios', methods=['GET', 'OPTIONS'])
def get_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()

    return jsonify([dict(u) for u in usuarios])

# 🔹 GET - Obtener un usuario
@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()
    conn.close()

    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify(dict(usuario))

# 🔹 POST - Crear usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()

    nombre = data.get('nombre')
    correo = data.get('correo')

    conn = get_db_connection()
    conn.execute('INSERT INTO usuarios (nombre, correo) VALUES (?, ?)', (nombre, correo))
    conn.commit()
    conn.close()

    return jsonify({'mensaje': 'Usuario creado'}), 201

# 🔹 PUT - Actualizar usuario completo
@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.get_json()

    nombre = data.get('nombre')
    correo = data.get('correo')

    conn = get_db_connection()
    conn.execute('UPDATE usuarios SET nombre = ?, correo = ? WHERE id = ?',
                 (nombre, correo, id))
    conn.commit()
    conn.close()

    return jsonify({'mensaje': 'Usuario actualizado'})

# 🔹 PATCH - Actualización parcial
@app.route('/usuarios/<int:id>', methods=['PATCH'])
def patch_usuario(id):
    data = request.get_json()

    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()

    if usuario is None:
        conn.close()
        return jsonify({'error': 'Usuario no encontrado'}), 404

    nombre = data.get('nombre', usuario['nombre'])
    correo = data.get('correo', usuario['correo'])

    conn.execute('UPDATE usuarios SET nombre = ?, correo = ? WHERE id = ?',
                 (nombre, correo, id))
    conn.commit()
    conn.close()

    return jsonify({'mensaje': 'Usuario actualizado parcialmente'})

# 🔹 DELETE - Eliminar usuario
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'mensaje': 'Usuario eliminado'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
