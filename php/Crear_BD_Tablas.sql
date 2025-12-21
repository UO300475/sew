DROP DATABASE IF EXISTS UO300475_DB;
CREATE DATABASE IF NOT EXISTS UO300475_DB;

USE UO300475_DB;

CREATE TABLE Profesion (
    id_profesion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Genero (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL
);

CREATE TABLE PericiaInformatica (
    id_pericia INT AUTO_INCREMENT PRIMARY KEY,
    nivel INT NOT NULL CHECK (nivel BETWEEN 0 AND 10)
);

CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_profesion INT NOT NULL,
    edad INT NOT NULL,
    id_genero INT NOT NULL,
    id_pericia INT NOT NULL,

    FOREIGN KEY (id_profesion) REFERENCES Profesion(id_profesion),
    FOREIGN KEY (id_genero) REFERENCES Genero(id_genero),
    FOREIGN KEY (id_pericia) REFERENCES PericiaInformatica(id_pericia)
);

CREATE TABLE Dispositivo (
    id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL 
);

CREATE TABLE ResultadoUsabilidad (
    id_resultado INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_dispositivo INT NOT NULL,
    tiempo_completado TIME NOT NULL DEFAULT '00:00:00',
    tarea_completada BOOLEAN NOT NULL,
    comentarios TEXT,
    propuestas_mejora TEXT,
    valoracion INT NOT NULL CHECK (valoracion BETWEEN 0 AND 10),

    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_dispositivo) REFERENCES Dispositivo(id_dispositivo)
);

CREATE TABLE ObservacionFacilitador (
    id_observacion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    comentario TEXT NOT NULL,

    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);