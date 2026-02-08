import sqlite3

DB = "equipos.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Tabla de equipos
cur.execute("""
CREATE TABLE IF NOT EXISTS equipos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    puertos INTEGER NOT NULL
)
""")

# Tabla de puertos
cur.execute("""
CREATE TABLE IF NOT EXISTS puertos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipo_id INTEGER,
    puerto INTEGER,
    estado TEXT DEFAULT 'Sin asignar',
    comentario TEXT DEFAULT '',
    FOREIGN KEY (equipo_id) REFERENCES equipos(id)
)
""")

conn.commit()

# --- CARGA INICIAL ---
equipos_base = [
    ("Aruba 2930F", 48),
    ("Aruba 2530", 24),
    ("Cisco Catalyst 2960", 24),
    ("Cisco Catalyst 9200", 48),
    ("HP ProCurve 1810", 24),
]

for nombre, cantidad in equipos_base:
    cur.execute(
        "INSERT INTO equipos (nombre, puertos) VALUES (?, ?)",
        (nombre, cantidad)
    )
    equipo_id = cur.lastrowid

    for p in range(1, cantidad + 1):
        cur.execute(
            "INSERT INTO puertos (equipo_id, puerto) VALUES (?, ?)",
            (equipo_id, p)
        )

conn.commit()
conn.close()

print("✅ Base de datos creada correctamente")

