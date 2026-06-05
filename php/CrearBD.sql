DROP DATABASE IF EXISTS UO300475_DB;
CREATE DATABASE IF NOT EXISTS UO300475_DB;

USE UO300475_DB;

CREATE TABLE TipoRecurso (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE RecursoTuristico (
    id_recurso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    plazas INT NOT NULL CHECK (plazas > 0),
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    id_tipo INT NOT NULL,
    FOREIGN KEY (id_tipo) REFERENCES TipoRecurso(id_tipo)
);

CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    telefono VARCHAR(20)
);

CREATE TABLE EstadoReserva (
    id_estado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL
);

CREATE TABLE Reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_recurso INT NOT NULL,
    id_estado INT NOT NULL,
    fecha_reserva DATETIME NOT NULL,
    num_personas INT NOT NULL CHECK (num_personas > 0),
    precio_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_recurso) REFERENCES RecursoTuristico(id_recurso),
    FOREIGN KEY (id_estado) REFERENCES EstadoReserva(id_estado)
);

-- Datos iniciales de TipoRecurso
INSERT INTO TipoRecurso (nombre) VALUES
    ('Museo'),
    ('Ruta'),
    ('Restaurante'),
    ('Hotel');

-- Datos iniciales de EstadoReserva
INSERT INTO EstadoReserva (nombre) VALUES
    ('Pendiente'),
    ('Confirmada'),
    ('Anulada');

-- Datos iniciales de RecursoTuristico
INSERT INTO RecursoTuristico (nombre, descripcion, precio, plazas, fecha_inicio, fecha_fin, id_tipo) VALUES
    ('Museo de Leon', 'Visita guiada al Museo de Leon con exposiciones permanentes y temporales', 8.00, 20, '2025-07-01 10:00:00', '2025-07-01 12:00:00', 1),
    ('Ruta de las Medulas', 'Ruta guiada por Las Medulas, Patrimonio de la Humanidad', 15.00, 15, '2025-07-02 09:00:00', '2025-07-02 14:00:00', 2),
    ('Ruta Catedral de Leon', 'Recorrido por el casco historico de Leon con visita a la Catedral', 12.00, 20, '2025-07-03 10:00:00', '2025-07-03 13:00:00', 2),
    ('Restaurante El Forno', 'Cena con menu degustacion de cocina leonesa tradicional', 35.00, 30, '2025-07-04 21:00:00', '2025-07-04 23:00:00', 3),
    ('Hotel NH Leon', 'Alojamiento en hotel 4 estrellas en el centro de Leon', 95.00, 50, '2025-07-05 14:00:00', '2025-07-06 12:00:00', 4);
