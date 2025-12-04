CREATE DATABASE finanzas;

USE finanzas;

SHOW TABLES;

CREATE OR REPLACE VIEW activos_completos_mensual AS
SELECT 
    DATE_FORMAT(btc.open_time, '%Y-%m-01') AS mes,
    MAX(btc.high) AS precio_btc,
    MAX(oro.high_oz) AS precio_oro,
    MAX(sp500.high) AS precio_sp500,
    MAX(letras_del_tesoro.interes_medio) AS interes_letras
FROM btc
LEFT JOIN oro ON DATE_FORMAT(oro.open_time, '%Y-%m-01') = DATE_FORMAT(btc.open_time, '%Y-%m-01')
LEFT JOIN sp500 ON DATE_FORMAT(sp500.open_time, '%Y-%m-01') = DATE_FORMAT(btc.open_time, '%Y-%m-01')
LEFT JOIN letras_del_tesoro ON DATE_FORMAT(letras_del_tesoro.fecha, '%Y-%m-01') = DATE_FORMAT(btc.open_time, '%Y-%m-01')
GROUP BY mes
ORDER BY mes;

#En esta tabla coinciden las fechas de todos los activos
SELECT * FROM finanzas.activos_completos_mensual;



CREATE OR REPLACE VIEW activos_mensuales AS
SELECT 
    DATE_FORMAT(sp500.open_time, '%Y-%m-01') AS mes,
    MAX(btc.high) AS btc_high,
    MAX(sp500.high) AS sp500_high,
    MAX(oro.high_oz) AS oro_high,
    MAX(letras_del_tesoro.interes_medio) AS letras_interes
FROM sp500
LEFT JOIN btc 
    ON YEAR(btc.open_time) = YEAR(sp500.open_time)
    AND MONTH(btc.open_time) = MONTH(sp500.open_time)
LEFT JOIN oro
    ON YEAR(oro.open_time) = YEAR(sp500.open_time)
    AND MONTH(oro.open_time) = MONTH(sp500.open_time)
LEFT JOIN letras_del_tesoro
    ON YEAR(letras_del_tesoro.fecha) = YEAR(sp500.open_time)
    AND MONTH(letras_del_tesoro.fecha) = MONTH(sp500.open_time)
GROUP BY mes
ORDER BY mes;

#En esta tabla aparecen todos los meses desde el 2000 y se van añadiendo activos
SELECT * from activos_mensuales;


-- 1. Crear la tabla fechas
CREATE TABLE IF NOT EXISTS fechas (
    fecha_id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 2. Insertar todas las fechas únicas de las tablas existentes
INSERT INTO fechas (fecha)
SELECT DISTINCT open_time FROM btc
UNION
SELECT DISTINCT open_time FROM sp500
UNION
SELECT DISTINCT open_time FROM oro
UNION
SELECT DISTINCT fecha FROM letras_del_tesoro;

-- 3. Añadir columna de referencia (foreign key) en cada tabla
ALTER TABLE btc ADD COLUMN fecha_id INT;
ALTER TABLE sp500 ADD COLUMN fecha_id INT;
ALTER TABLE oro ADD COLUMN fecha_id INT;
ALTER TABLE letras_del_tesoro ADD COLUMN fecha_id INT;

-- 4. Actualizar la columna fecha_id con la referencia de la tabla fechas
SET SQL_SAFE_UPDATES = 0;

UPDATE btc b
JOIN fechas f ON b.open_time = f.fecha
SET b.fecha_id = f.fecha_id;

UPDATE sp500 s
JOIN fechas f ON s.open_time = f.fecha
SET s.fecha_id = f.fecha_id;

UPDATE oro o
JOIN fechas f ON o.open_time = f.fecha
SET o.fecha_id = f.fecha_id;

UPDATE letras_del_tesoro l
JOIN fechas f ON l.fecha = f.fecha
SET l.fecha_id = f.fecha_id;

-- 5. Crear las claves foráneas para mantener integridad
ALTER TABLE btc ADD CONSTRAINT fk_btc_fecha FOREIGN KEY (fecha_id) REFERENCES fechas(fecha_id);
ALTER TABLE sp500 ADD CONSTRAINT fk_sp500_fecha FOREIGN KEY (fecha_id) REFERENCES fechas(fecha_id);
ALTER TABLE oro ADD CONSTRAINT fk_oro_fecha FOREIGN KEY (fecha_id) REFERENCES fechas(fecha_id);
ALTER TABLE letras_del_tesoro ADD CONSTRAINT fk_letras_fecha FOREIGN KEY (fecha_id) REFERENCES fechas(fecha_id);


SELECT f.fecha,
       sp500.high AS precio_actual,
       sp500.high / LAG(sp500.high) OVER (ORDER BY f.fecha) - 1 AS retorno_mensual
FROM fechas f
LEFT JOIN sp500 ON f.fecha = sp500.open_time
ORDER BY f.fecha;



SELECT fecha_id;


