-- Datos de ejemplo (ficticios) para pruebas locales
INSERT INTO usuarios (
    tipo_documento, numero_documento, primer_nombre, segundo_nombre,
    primer_apellido, segundo_apellido, fecha_nacimiento, genero,
    correo_electronico, telefono, direccion, ciudad, departamento, pais,
    eps, alergias, password_hash, estado
) VALUES
    ('CC', '1010123456', 'Mariana', NULL, 'Gomez', 'Restrepo', '1994-03-12', 'femenino',
     'mariana.gomez@example.com', '3011234567', 'Calle 45 # 12-30', 'Bogota', 'Cundinamarca', 'Colombia',
     'Sura EPS', 'Penicilina', '$2b$12$fakehash.seed.user.one.0000000000000000', 'activo'),

    ('CC', '1020654321', 'Andres', 'Felipe', 'Martinez', 'Lopez', '1988-07-21', 'masculino',
     'andres.martinez@example.com', '3129876543', 'Carrera 7 # 80-15', 'Medellin', 'Antioquia', 'Colombia',
     'Nueva EPS', NULL, '$2b$12$fakehash.seed.user.two.0000000000000000', 'activo'),

    ('TI', '10203040', 'Valentina', NULL, 'Ramirez', NULL, '2007-11-05', 'femenino',
     'valentina.ramirez@example.com', '3005551234', 'Avenida 6N # 23-11', 'Cali', 'Valle del Cauca', 'Colombia',
     'Compensar', 'Ibuprofeno', '$2b$12$fakehash.seed.user.three.00000000000000', 'activo'),

    ('CE', 'CE778899', 'Carlos', 'Eduardo', 'Fernandez', 'Diaz', '1979-01-30', 'masculino',
     'carlos.fernandez@example.com', '3187654321', 'Calle 100 # 15-20', 'Barranquilla', 'Atlantico', 'Colombia',
     'Sanitas', NULL, '$2b$12$fakehash.seed.user.four.000000000000000', 'inactivo'),

    ('PA', 'PA5566778', 'Laura', NULL, 'Suarez', 'Ortiz', '1996-09-17', 'otro',
     'laura.suarez@example.com', '3143332211', 'Transversal 8 # 45-67', 'Bucaramanga', 'Santander', 'Colombia',
     NULL, 'Sulfamidas', '$2b$12$fakehash.seed.user.five.000000000000000', 'activo');
