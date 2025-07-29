            -- Estructura de base de datos para Sistema de Inventario Raywal
-- Base de datos: raywal_inventory

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `MateriasPrimas`
--

CREATE TABLE `MateriasPrimas` (
  `CodMP` int(11) NOT NULL AUTO_INCREMENT,
  `DscNegocio` varchar(100) NOT NULL COMMENT 'Descripción del producto',
  `UdeM` varchar(20) NOT NULL COMMENT 'Unidad de medida',
  `TpoInventario` int(1) NOT NULL DEFAULT 1 COMMENT 'Tipo de inventario: 1=Paquetes, 2=Unidades',
  `MinxCompra` decimal(10,2) DEFAULT 1.00 COMMENT 'Mínimo por compra',
  `Estado` int(1) NOT NULL DEFAULT 0 COMMENT '0=Activo, 1=Inactivo',
  `FechaCreacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`CodMP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `MateriasPrimasxBodega`
--

CREATE TABLE `MateriasPrimasxBodega` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `CodMP` int(11) NOT NULL,
  `CodBod` int(11) NOT NULL COMMENT 'Código de bodega',
  `Stock_xSemana` decimal(10,2) DEFAULT 0.00 COMMENT 'Stock requerido por semana',
  `OrderIngreso` int(11) DEFAULT 0 COMMENT 'Orden de ingreso para mostrar productos',
  `Estado` int(1) NOT NULL DEFAULT 0 COMMENT '0=Activo, 1=Inactivo',
  PRIMARY KEY (`Id`),
  KEY `idx_codmp` (`CodMP`),
  KEY `idx_codbod` (`CodBod`),
  FOREIGN KEY (`CodMP`) REFERENCES `MateriasPrimas`(`CodMP`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `EncInventario`
--

CREATE TABLE `EncInventario` (
  `IdFoto` int(11) NOT NULL AUTO_INCREMENT,
  `CodBod` int(11) NOT NULL COMMENT 'Código de bodega',
  `IdFotoPapa` int(11) DEFAULT 0 COMMENT 'ID foto padre',
  `Estado` int(1) NOT NULL DEFAULT 0 COMMENT '0=Pendiente, 1=Procesado',
  `FechaRegistro` date NOT NULL,
  `UsuarioRegistro` varchar(50) NOT NULL,
  `FechaCreacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`IdFoto`),
  KEY `idx_codbod` (`CodBod`),
  KEY `idx_fecha` (`FechaRegistro`),
  KEY `idx_estado` (`Estado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `DtlleInventario`
--

CREATE TABLE `DtlleInventario` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `IdFoto` int(11) NOT NULL,
  `CodMP` int(11) NOT NULL,
  `Pquetes` decimal(10,2) DEFAULT 0.00 COMMENT 'Cantidad en paquetes',
  `Uds` decimal(10,2) DEFAULT 0.00 COMMENT 'Cantidad en unidades',
  `Condicion` varchar(20) DEFAULT 'bueno' COMMENT 'Condición del producto: bueno, malo, vencido',
  PRIMARY KEY (`Id`),
  KEY `idx_idfoto` (`IdFoto`),
  KEY `idx_codmp` (`CodMP`),
  FOREIGN KEY (`IdFoto`) REFERENCES `EncInventario`(`IdFoto`) ON DELETE CASCADE,
  FOREIGN KEY (`CodMP`) REFERENCES `MateriasPrimas`(`CodMP`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Datos de ejemplo para la tabla `MateriasPrimas`
--

INSERT INTO `MateriasPrimas` (`CodMP`, `DscNegocio`, `UdeM`, `TpoInventario`, `MinxCompra`, `Estado`) VALUES
(1, 'Arroz Blanco Premium', 'Kg', 1, 25.00, 0),
(2, 'Aceite Vegetal', 'Litros', 1, 12.00, 0),
(3, 'Azúcar Refinada', 'Kg', 1, 50.00, 0),
(4, 'Sal Marina', 'Kg', 1, 20.00, 0),
(5, 'Pasta Espagueti', 'Paquetes', 2, 1.00, 0),
(6, 'Leche Entera', 'Litros', 1, 6.00, 0),
(7, 'Pan Integral', 'Unidades', 2, 1.00, 0),
(8, 'Huevos Frescos', 'Docenas', 1, 30.00, 0),
(9, 'Pollo Entero', 'Kg', 1, 2.00, 0),
(10, 'Carne de Res', 'Kg', 1, 1.00, 0);

-- --------------------------------------------------------

--
-- Datos de ejemplo para la tabla `MateriasPrimasxBodega`
--

INSERT INTO `MateriasPrimasxBodega` (`CodMP`, `CodBod`, `Stock_xSemana`, `OrderIngreso`) VALUES
(1, 1, 100.00, 1),
(2, 1, 50.00, 2),
(3, 1, 75.00, 3),
(4, 1, 40.00, 4),
(5, 1, 200.00, 5),
(6, 1, 80.00, 6),
(7, 1, 150.00, 7),
(8, 1, 60.00, 8),
(9, 1, 30.00, 9),
(10, 1, 25.00, 10),
(1, 2, 120.00, 1),
(2, 2, 60.00, 2),
(3, 2, 90.00, 3),
(4, 2, 50.00, 4),
(5, 2, 250.00, 5);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;