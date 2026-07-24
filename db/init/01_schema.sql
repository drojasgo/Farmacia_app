-- Esquema de ejemplo: usuarios registrados de la farmacia
CREATE TYPE tipo_documento AS ENUM ('CC', 'TI', 'CE', 'PA');
CREATE TYPE genero AS ENUM ('femenino', 'masculino', 'otro', 'prefiere_no_decir');
CREATE TYPE estado_usuario AS ENUM ('activo', 'inactivo', 'suspendido');

CREATE TABLE usuarios (
    id                  SERIAL PRIMARY KEY,
    tipo_documento      tipo_documento NOT NULL,
    numero_documento    VARCHAR(20)  NOT NULL,
    primer_nombre       VARCHAR(50)  NOT NULL,
    segundo_nombre      VARCHAR(50),
    primer_apellido     VARCHAR(50)  NOT NULL,
    segundo_apellido    VARCHAR(50),
    fecha_nacimiento    DATE         NOT NULL,
    genero              genero       NOT NULL DEFAULT 'prefiere_no_decir',
    correo_electronico  VARCHAR(120) NOT NULL,
    telefono            VARCHAR(20),
    direccion           VARCHAR(150),
    ciudad              VARCHAR(60),
    departamento        VARCHAR(60),
    pais                VARCHAR(60)  NOT NULL DEFAULT 'Colombia',
    eps                 VARCHAR(80),
    alergias            TEXT,
    password_hash       VARCHAR(255) NOT NULL,
    estado              estado_usuario NOT NULL DEFAULT 'activo',
    fecha_registro      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    actualizado_en      TIMESTAMPTZ  NOT NULL DEFAULT now(),

    CONSTRAINT uq_usuarios_documento UNIQUE (tipo_documento, numero_documento),
    CONSTRAINT uq_usuarios_correo UNIQUE (correo_electronico)
);

CREATE INDEX idx_usuarios_correo ON usuarios (correo_electronico);
CREATE INDEX idx_usuarios_documento ON usuarios (numero_documento);

CREATE OR REPLACE FUNCTION set_actualizado_en()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_usuarios_actualizado
    BEFORE UPDATE ON usuarios
    FOR EACH ROW
    EXECUTE FUNCTION set_actualizado_en();
