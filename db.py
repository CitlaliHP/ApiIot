import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('apiIot.db')

# Crear un cursor
c = conn.cursor()

# Crear tabla
c.execute('''
    CREATE TABLE Iot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dispositivo TEXT NOT NULL,
        valor INTEGER NOT NULL
    )
''')

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()