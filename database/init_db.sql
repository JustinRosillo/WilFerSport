-- database/init_db.sql
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('admin', 'vendedor'))
);
