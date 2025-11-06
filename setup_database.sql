-- =============================================
-- Script Completo para Configuración de Base de Datos
-- =============================================

-- Borrar tablas si ya existen para una nueva instalación limpia (opcional)
DROP TABLE IF EXISTS tprofesores;
DROP TABLE IF EXISTS tcursos;
DROP TABLE IF EXISTS tchistes;
DROP TABLE IF EXISTS tasistencia;
DROP TABLE IF EXISTS tcharla;
DROP TABLE IF EXISTS tobjetivos;

-- =============================================
-- Tabla de Profesores
-- =============================================
CREATE TABLE tprofesores (
    idprofesor INT IDENTITY(1,1) PRIMARY KEY,
    codprofesor INT NOT NULL,
    nombresprofesor NVARCHAR(255)
);

INSERT INTO tprofesores (codprofesor, nombresprofesor) VALUES
(1601, N'WILBERT VILCAHUAMAN MAMANI'),
(2056, N'RICHARD TAPIA PAJUELO');

-- =============================================
-- Tabla de Cursos
-- =============================================
CREATE TABLE tcursos (
    idcurso INT IDENTITY(1,1) PRIMARY KEY,
    codcurso INT NOT NULL,
    nombrecurso NVARCHAR(255),
    codprofesor INT
);

INSERT INTO tcursos (codcurso, nombrecurso, codprofesor) VALUES
(10526, N'INFORMATICA APLICADA I', 1601),
(10527, N'SAP', 1601),
(10530, N'PROCESO DE COMPRAS', 2056);

-- =============================================
-- Tabla de Chistes
-- =============================================
CREATE TABLE tchistes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    chiste NVARCHAR(MAX)
);

INSERT INTO tchistes (chiste) VALUES
(N'Abuelo, por que estas delante del ordenador con ...'),
(N'Por que Windows esta resfriado, Por abrir tantas ...'),
(N'Mi sistema operativo es multitarea, Acaba con mi ...');

-- =============================================
-- Tabla de Asistencia
-- =============================================
CREATE TABLE tasistencia (
    idalumno INT PRIMARY KEY,
    codalumno INT,
    nombres NVARCHAR(255),
    sexo INT,
    codcurso INT,
    fecha DATE,
    situacion NVARCHAR(50),
    foto VARBINARY(MAX)
);

INSERT INTO tasistencia (idalumno, codalumno, nombres, sexo, codcurso, fecha, situacion, foto) VALUES
(1, 415278, N'MIGUEL SALAZAR TORRES', 1, 10526, '2022-02-10', N'presente', 0x307832463339364132463332373734323434313431363230323230323130),
(7, 417845, N'JUAN TORRES HUAMANI', 1, 10526, '2022-02-10', N'faltó', 0x307832463339364132463332373734323434313431363230323230323130),
(4, 528954, N'SILVIA CASAS FUENTES', 0, 10526, '2022-02-10', N'presente', 0x307832463339364132463332373734323434313431363230323230323130),
(6, 6312789, N'CARLOS MONTES SOSA', 1, 10526, '2022-02-10', N'presente', 0x307832463339364132463332373734323434313431363230323230323130),
(5, 634578, N'DIANA PUMA ZAPATA', 0, 10526, '2022-02-10', N'faltó', 0x307832463339364132463332373734323434313431363230323230323130);

-- =============================================
-- Tabla de Charlas
-- =============================================
CREATE TABLE tcharla (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titulo NVARCHAR(255),
    contenido NVARCHAR(MAX)
);

INSERT INTO tcharla (titulo, contenido) VALUES (
    'Cuidado de los ojos',
    'El uso de unos buenos consejos de higiene visual puede evitar a contribuir al desarrollo de la fatiga visual, ya que se evita usar de modo ineficiente o sobreutilizar el sistema de enfoque del ojo, así como el de alineamiento ocular.

En este sentido, recuerda que existen ejercicios de terapia visual, cientificamente validados, que permiten mejorar algunas capacidades visuales, pero solo deben de indicarse en caso de que exista una alteracion que requiera la recuperacion de la eficiencia del sistema visual.

Algunos consejos.

Evita de frotarte el ojo
Evita el consumo de tabaco
Dejar de fumar
Evita el consumo de alcohol'
);

-- =============================================
-- Tabla de Objetivos
-- =============================================
CREATE TABLE tobjetivos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titulo NVARCHAR(255),
    contenido NVARCHAR(MAX)
);

INSERT INTO tobjetivos (titulo, contenido) VALUES (
    'Objetivo Principal',
    'Conocer y aplicar los conceptos del paradigma de la programación orientada a objetos, para la correcta identificación estructural de la codificación del programa por medio del lenguaje de programación de Java y utilizando el ide de Anaconda Navigator.'
);

PRINT 'Base de datos configurada exitosamente con todas las tablas y datos.';