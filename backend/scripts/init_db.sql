-- CREAR DB SI NO EXISTE
CREATE DATABASE IF NOT EXISTS cine_db;
USE cine_db;

-- TABLA DE PELÍCULAS
CREATE TABLE IF NOT EXISTS peliculas (
    id_pelicula INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    duracion INT NOT NULL,
    genero VARCHAR(100),
    sinopsis TEXT,
    estado ENUM('en_cartelera', 'proximamente', 'finalizada') DEFAULT 'en_cartelera',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
ALTER TABLE peliculas
ADD COLUMN imagen_url VARCHAR(500) AFTER sinopsis;


-- TABLA DE SALAS
CREATE TABLE IF NOT EXISTS salas (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    capacidad INT NOT NULL,
    tipo_sala ENUM('2D', '3D', 'IMAX') DEFAULT '2D',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- TABLA DE BUTACAS
CREATE TABLE IF NOT EXISTS butacas (
    id_butaca INT AUTO_INCREMENT PRIMARY KEY,
    id_sala INT NOT NULL,
    fila VARCHAR(5) NOT NULL,
    numero INT NOT NULL,
    UNIQUE KEY uk_butaca_sala (id_sala, fila, numero),
    CONSTRAINT fk_butaca_sala 
        FOREIGN KEY (id_sala) REFERENCES salas(id_sala) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- TABLA DE USUARIOS
CREATE TABLE IF NOT EXISTS users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(200),
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- TABLA DE FUNCIONES
CREATE TABLE IF NOT EXISTS funciones (
    id_funcion INT AUTO_INCREMENT PRIMARY KEY,
    id_pelicula INT NOT NULL,
    id_sala INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    precio_base DECIMAL(10,2) NOT NULL,
    UNIQUE KEY uk_funcion_sala_horario (id_sala, fecha_hora),
    KEY idx_funcion_pelicula (id_pelicula),
    CONSTRAINT fk_funcion_pelicula 
        FOREIGN KEY (id_pelicula) REFERENCES peliculas(id_pelicula) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_funcion_sala 
        FOREIGN KEY (id_sala) REFERENCES salas(id_sala) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ====================================================================
-- TABLA PUENTE: disponibilidad de butacas por función
--  - Garantiza que solo existan butacas de la sala de la función
--  - Única por (función, butaca)
--  - Estado: libre/reservada
-- ====================================================================
CREATE TABLE IF NOT EXISTS butacas_funcion (
    id_funcion INT NOT NULL,
    id_butaca INT NOT NULL,
    estado ENUM('libre', 'reservada') DEFAULT 'libre',
    PRIMARY KEY (id_funcion, id_butaca),
    CONSTRAINT fk_bf_funcion 
        FOREIGN KEY (id_funcion) REFERENCES funciones(id_funcion) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_bf_butaca 
        FOREIGN KEY (id_butaca) REFERENCES butacas(id_butaca)
        ON DELETE CASCADE ON UPDATE CASCADE
);


-- ====================================================================
-- Entradas (tickets)
--  - Referencian la combinación exacta (id_funcion, id_butaca)
--  - UNIQUE para no vender dos veces la misma butaca en esa función
-- ====================================================================
CREATE TABLE IF NOT EXISTS entradas(
    id_entrada INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    id_funcion INT NOT NULL,
    id_butaca INT NOT NULL,
    precio_final DECIMAL(10,2) NOT NULL,
    estado ENUM('reservada','pagada','cancelada') DEFAULT 'reservada',
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uk_entrada_funcion_butaca (id_funcion, id_butaca),

    CONSTRAINT fk_entrada_butaca_funcion
        FOREIGN KEY (id_funcion, id_butaca)
        REFERENCES butacas_funcion (id_funcion, id_butaca)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    CONSTRAINT fk_entrada_cliente
        FOREIGN KEY (id_user) REFERENCES users(id_user)
        ON DELETE RESTRICT ON UPDATE CASCADE
);



-- TABLA DE RESERVAS

CREATE TABLE reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_funcion INT NOT NULL,
    id_pelicula INT NOT NULL,
    id_usuario INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE reservas
ADD COLUMN estado ENUM('pendiente', 'pagada') DEFAULT 'pendiente';

-- TABLA PUENTE: butacas asociadas a una reserva
CREATE TABLE reservas_butacas (
    id_reserva INT NOT NULL,
    id_butaca INT NOT NULL,
    PRIMARY KEY (id_reserva, id_butaca),
    FOREIGN KEY (id_reserva) REFERENCES reservas(id_reserva),
    FOREIGN KEY (id_butaca) REFERENCES butacas(id_butaca)
);


-- ====================================================================
-- CARGA DE INFORMACIÓN INICIAL
-- ====================================================================
USE cine_db;

-- Películas
INSERT INTO peliculas (titulo, duracion, genero, sinopsis, estado) VALUES
("Inception", 148, "Ciencia Ficción", "Un ladrón entra en los sueños de las personas.", "en_cartelera"),
("Avatar", 162, "Aventura", "Un humano vive entre una raza alienígena en Pandora.", "en_cartelera"),
("Joker", 122, "Drama", "Origen del odiado villano de DC.", "finalizada");

-- Salas
INSERT INTO salas (nombre, capacidad, tipo_sala) VALUES
("Sala 1", 120, "2D"),
("Sala 2", 80, "3D"),
("Sala IMAX", 200, "IMAX");

-- Funciones
INSERT INTO funciones (id_pelicula, id_sala, fecha_hora, precio_base) VALUES
(1, 1, '2025-11-08 20:00:00', 1500.00),
(2, 3, '2025-11-09 22:00:00', 2200.00);

-- Butacas sala 1 (A1–A10)
INSERT INTO butacas (id_sala, fila, numero) VALUES
(1, 'A', 1),(1, 'A', 2),(1, 'A', 3),(1, 'A', 4),(1, 'A', 5),
(1, 'A', 6),(1, 'A', 7),(1, 'A', 8),(1, 'A', 9),(1, 'A', 10);

-- Disponibilidad de butacas para función 1
INSERT INTO butacas_funcion (id_funcion, id_butaca, estado)
SELECT 1, id_butaca, 'libre' FROM butacas WHERE id_sala = 1;


-- Conexion al contenedor de MySQL para gestion de la base de datos.
-- docker exec -it cine_mysql mysql -u root -p


-- OTRAS QUERYs DE INSERCIÓN DE DATOS

-- Para función 3 (Avatar)
INSERT INTO butacas_funcion (id_funcion, id_butaca, estado)
SELECT 3, id_butaca, 'libre'
FROM butacas
WHERE id_sala = 1;

-- Para función 4 (Interstellar)
INSERT INTO butacas_funcion (id_funcion, id_butaca, estado)
SELECT 4, id_butaca, 'libre'
FROM butacas
WHERE id_sala = 2;

-- Para función 5 (Dori)
INSERT INTO butacas_funcion (id_funcion, id_butaca, estado)
SELECT 5, id_butaca, 'libre'
FROM butacas
WHERE id_sala = 1;

-- Para función 6 (Weapons)
INSERT INTO butacas_funcion (id_funcion, id_butaca, estado)
SELECT 6, id_butaca, 'libre'
FROM butacas
WHERE id_sala = 2;


INSERT INTO funciones (id_pelicula, id_sala, fecha_hora, precio_base) VALUES
(2, 1, '2025-11-10 20:00:00', 1800.00),   -- Avatar
(4, 2, '2025-11-11 21:00:00', 2000.00),   -- Interstellar
(6, 1, '2025-11-12 18:00:00', 1500.00),   -- Dori
(11, 2, '2025-11-13 23:00:00', 2300.00);  -- Weapons


-- BUTACAS: crear 48 butacas en sala 1
INSERT INTO butacas (id_sala, fila, numero)
VALUES
(1, 'A', 1), (1, 'A', 2), (1, 'A', 3), (1, 'A', 4), (1, 'A', 5), (1, 'A', 6), (1, 'A', 7), (1, 'A', 8),
(1, 'B', 1), (1, 'B', 2), (1, 'B', 3), (1, 'B', 4), (1, 'B', 5), (1, 'B', 6), (1, 'B', 7), (1, 'B', 8),
(1, 'C', 1), (1, 'C', 2), (1, 'C', 3), (1, 'C', 4), (1, 'C', 5), (1, 'C', 6), (1, 'C', 7), (1, 'C', 8),
(1, 'D', 1), (1, 'D', 2), (1, 'D', 3), (1, 'D', 4), (1, 'D', 5), (1, 'D', 6), (1, 'D', 7), (1, 'D', 8),
(1, 'E', 1), (1, 'E', 2), (1, 'E', 3), (1, 'E', 4), (1, 'E', 5), (1, 'E', 6), (1, 'E', 7), (1, 'E', 8),
(1, 'F', 1), (1, 'F', 2), (1, 'F', 3), (1, 'F', 4), (1, 'F', 5), (1, 'F', 6), (1, 'F', 7), (1, 'F', 8);

-- BUTACAS: crear 48 butacas en sala 2
INSERT INTO butacas (id_sala, fila, numero)
VALUES
(2, 'A', 1), (2, 'A', 2), (2, 'A', 3), (2, 'A', 4), (2, 'A', 5), (2, 'A', 6), (2, 'A', 7), (2, 'A', 8),
(2, 'B', 1), (2, 'B', 2), (2, 'B', 3), (2, 'B', 4), (2, 'B', 5), (2, 'B', 6), (2, 'B', 7), (2, 'B', 8),
(2, 'C', 1), (2, 'C', 2), (2, 'C', 3), (2, 'C', 4), (2, 'C', 5), (2, 'C', 6), (2, 'C', 7), (2, 'C', 8),
(2, 'D', 1), (2, 'D', 2), (2, 'D', 3), (2, 'D', 4), (2, 'D', 5), (2, 'D', 6), (2, 'D', 7), (2, 'D', 8),
(2, 'E', 1), (2, 'E', 2), (2, 'E', 3), (2, 'E', 4), (2, 'E', 5), (2, 'E', 6), (2, 'E', 7), (2, 'E', 8),
(2, 'F', 1), (2, 'F', 2), (2, 'F', 3), (2, 'F', 4), (2, 'F', 5), (2, 'F', 6), (2, 'F', 7), (2, 'F', 8);



