import mysql.connector

# Conexión a la base de datos en Railway
conexion = mysql.connector.connect(
          #host ="autorack.proxy.rlwy.net",
        #user ="root",
       # passwd ="gFtPlGDqnVuPzOovONvIsBKUCjnsdCOe",
       # database = "railway",
       # port=41106 


           host ="gondola.proxy.rlwy.net",
        user ="root",
        passwd ="vpHvlRYKRWqoUSZWULYplLTymXzoBspd",
        database = "railway",
        port=10708  
)

cursor = conexion.cursor()

""" Crear tabla
DROP TABLE `MateriasPrimasxBodega`

DELETE FROM MateriasPrimasxBodega;

DROP TABLE `BodegasxFranquicia` 
DROP TABLE `DtllInventario`  
DROP TABLE `EncInventario` 


CREATE TABLE `BodegasxFranquicia` (
  `CodFca` INT NOT NULL,
  `CodBod` INT NOT NULL,
  `Nombre` VARCHAR(60) NOT NULL

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `BodegasxFranquicia`
  ADD PRIMARY KEY (`CodFca`,`CodBod`);


CREATE TABLE `MateriasPrimas` (
  `CodMP` INT NOT NULL,
  `DscNegocio` VARCHAR(100) NOT NULL,
  `DscProveedor` VARCHAR(100) NOT NULL,
  `UdeM` VARCHAR(20) NOT NULL,
  `SeFabrica` INT NOT NULL,
  `TpoInventario` INT NOT NULL,
  `Estado` INT NOT NULL,
  `CtrlInventario` INT NOT NULL, 
  `MinxCompra` DECIMAL(7,2) NOT NULL,
  `MinxConsumo` DECIMAL(7,2) NOT NULL,
  `CodMPSys` INT NOT NULL,
  `DscSys` VARCHAR(100) NOT NULL, 
  `MinxInventario` DECIMAL(7,2) NOT NULL

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `MateriasPrimas`
  ADD PRIMARY KEY (`CodMP`);
  


CREATE TABLE `MateriasPrimasxBodega` (
  `CodBod` INT NOT NULL,
  `CodMP` INT NOT NULL,
  `StockMin` DECIMAL(7,2) NOT NULL,
  `Stock_xSemana` DECIMAL(7,2) NOT NULL,
  `StockMax_xDiaNmal` DECIMAL(7,2) NOT NULL,
  `StockMax_xDiaFtvo` DECIMAL(7,2) NOT NULL,
  `OrderIngreso` INT NOT NULL,
  `Estado` INT NOT NULL

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `MateriasPrimasxBodega`
  ADD PRIMARY KEY (`CodBod`,`CodMP`);

  

  
CREATE TABLE `EncInventario` (
  `IdFoto` INT AUTO_INCREMENT PRIMARY KEY,
  `CodBod` INT NOT NULL,
  `IdFotoPapa` INT NOT NULL,
  `Estado` INT NOT NULL,
  `FechaRegistro` DATETIME NOT NULL,
  `UsuarioRegistro` VARCHAR(20) NOT NULL

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `DtlleInventario` (
    `IdFoto` INT NOT NULL,
    `CodMP` INT NOT NULL,
    `Pquetes` INT NOT NULL,
    `Uds` DECIMAL(7,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `DtlleInventario`
  ADD PRIMARY KEY (`IdFoto`,`CodMP`);


  CREATE TABLE `Kardex` (
  `IdMov` INT AUTO_INCREMENT PRIMARY KEY,
  `TipoMov` VARCHAR(10) NOT NULL,
  `CodBod` INT NOT NULL,
  `CodMP` INT NOT NULL,
  `Uds` DECIMAL(7,2) NOT NULL,
  `IdFotoRef` INT  NULL,
  `FechaRegistro` DATETIME NOT NULL,
  `UsuarioRegistro` VARCHAR(20) NOT NULL

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Saldos` (
  `IdSaldo` INT AUTO_INCREMENT PRIMARY KEY,
  `CodMP` INT NOT NULL,
  `Nombre` VARCHAR(100) NOT NULL,
  `Saldo` DECIMAL(7,2) NOT NULL,
  `FechaRegistro` DATETIME NOT NULL

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `InformeSaldosInventario` 
(
  `Id` INT AUTO_INCREMENT PRIMARY KEY,
  `CodMP` INT NOT NULL,
  `CodMPSys` INT NOT NULL,
  `Nombre` VARCHAR(100) NOT NULL,
  `InvPreparacion` DECIMAL(7,2) NOT NULL,
  `InvBodega` DECIMAL(7,2) NOT NULL,
  `SaldoActual` DECIMAL(7,2) NOT NULL

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





_-------------------------------------------------

 CREATE TABLE `InformeDeInventarioxDia` 
 (
  `CodMP` INT NOT NULL,
  `InventarioFinal_DiaAnt` DECIMAL(7,2) NOT NULL,
  `Consumos_Dia` DECIMAL(7,2) NOT NULL,
  `InventarioInicial_Dia` DECIMAL(7,2) NOT NULL,
  `InventarioFinal_Dia` DECIMAL(7,2) NOT NULL

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




INSERT INTO BodegasxFranquicia (CodFca,CodBod,Nombre)
VALUES 
(1,2,'Preparación'),
(1,4,'Bodega')


INSERT INTO MateriasPrimas (CodMP,DscNegocio,DscProveedor,UdeM,SeFabrica,TpoInventario,Estado, CtrlInventario,MinxCompra,MinxConsumo,CodMPSys,DscSys,MinxInventario)
VALUES 
(1,'Palillos(x180)','','Caja',0,2,0,0,1,1,311100023,'PALILLOS(X180)',180),
(2,'Pitillos','','Paquete',0,2,0,0,1,0.25,0,'N/A',1),
(3,'Ripio(x1000)','','Paquete',0,2,0,0,1,1,311100002,'RIPIO(X1000)',1000),
(4,'Queso tajado(x5/18)','','Bloque',0,2,0,0,1,1,118100027,'AD. DOBLE QUESO TAJADO',90),
(5,'Papel Chicle Hamb.(x300)','','Rollo',0,2,0,0,1,1,311100013,'PAPEL CRISTAFLEX(X300)',300),
(70,'Papel Chicle Papas.(x300)','','Rollo',0,2,0,0,1,1,311100013,'PAPEL CRISTAFLEX(X300)',300),
(6,'Rllo. Caja','','Rollo',0,2,0,0,1,1,0,'N/A',1),
(7,'T15(x100)','','Paquete',0,2,0,0,1,1,311100014,'BOLSA T15 (X100)',100),
(8,'T20(x100)','','Paquete',0,2,0,0,1,1,311100015,'BOLSA T20 (X100)',100),
(9,'T25(x100)','','Paquete',0,2,0,0,1,1,311100016,'BOLSA T25(X100)',100),
(10,'T30(x100)','','Paquete',0,2,0,0,1,1,311100029,'BOLSA T30(X100)',100),
(11,'Opaca(x100)','','Paquete',0,2,0,0,1,1,311100017,'BOLSA OPACA 8*12 (X100)',100),
(12,'Aluminio(x100)','','Paquete',0,2,0,0,1,1,311100018,'BOLSA ALUMINIO 6*6 ABIERTA (X100)',100),
(13,'Servilleta Nuve(x300)','','Paquete',0,2,0,0,1,1,311100019,'SERVILLETA EMPAQUE(X300)',300),
(14,'Servilleta Plus(x100)','','Paquete',0,2,0,0,1,1,311100020,'SERVILLETA MESA(X100)',100),
(15,'Papel Higienico','','Rollo',0,2,0,0,1,1,118100012,'PAPEL HIGIENICO',1),
(16,'Citronela','','Unidad',0,2,0,0,1,1,118100013,'LIMPIAPISOS',1),
(17,'jabon Liquido','','Unidad',0,2,0,0,1,0.25,118100014,'JABON LIQUIDO',1),
(18,'Limpido','','Unidad',0,2,0,0,1,0.25,118100015,'LIMPIDO',1),
(19,'Axion','','Unidad',0,2,0,0,1,1,0,'N/A',1),
(20,'Jabon Rey','','Unidad',0,2,0,0,1,0.5,118100017,'JABON EN BARRA',1),
(21,'Jabon Fab','','Unidad',0,2,0,0,1,0.25,0,'N/A',1),
(22,'Tenedores(x100)','','Paquete',0,2,0,0,1,1,311100022,'TENEDORES PEQUEÑOS(X100)',100),
(28,'Chorizo.Coctelero(x1250)','','Gramos',0,0,0,0,1250,1250,311100005,'CHORIZO COCTELEROS(X103)',1),

(23,'Pan Hamburguesa(x12)','','Paquete',0,1,0,1,12,12,311100030,'PAN HAMBURGUESA (X12)',12),
(24,'Pan Perro(x10)','','Paquete',0,1,0,1,10,10,311100003,'PAN PERRO GRANDE(X10)',10),
(25,'Carne Hamb 700(x10)','','Paquete',0,1,0,1,10,10,118100008,'CARNE HAMBURGUESA 700 GR (X10)',10),
(26,'Tocineta Premiun(x32)','','Paquete',0,1,0,1,32,32,118100023,'TOCINETA PREMIUN(X 32)',32),
(27,'Salchicha Perro(x25)','','Paquete',0,1,0,1,25,25,118100007,'SALCHICHA PERRO(X25)',25),
(29,'Huevo Codorniz(x24)','','Cajas',0,1,0,1,24,24,118100002,'HUEVOS CODORNIZ(X24)',24),

(30,'S. Mayonesa(x3650)','','Gramos',1,3,0,0,3650,3650,311100031,'SS. MAYONESA',1),
(31,'S. Rosada(x3650)','','Gramos',1,3,0,0,3650,3650,311100038,'SS. ROSADA',1),
(32,'S. Ajo(x3650)','','Gramos',1,3,0,0,3650,3650,311100040,'SS. AJO',1),
(33,'S. Tartara(x3650)','','Gramos',1,3,0,0,3650,3650,311100039,'SS. TARTARA',1),
(34,'S. Roja(x4000)','','Gramos',0,3,0,0,4000,4000,311100009,'SS. ROJA',1),
(35,'S. Mostaza(x4000)','','Gramos',0,3,0,0,4000,4000,311100010,'SS. MOSTAZA',1),
(36,'S. Piña(x4000)','','Gramos',0,3,0,0,4000,4000,311100011,'SS. PINA',1),
(37,'S. BBQ(x4000)','','Gramos',0,3,0,0,4000,4000,311100012,'SS. BBQ',1),
(72,'Lecherita(x4000)','','Gramos',0,3,0,0,4000,4000,311100048,'SS. LECHERITA',1),

(38,'Gaseosas 1/5','','Unidad',0,0,0,1,6,1,122100004,'GASEOSA 1/5ML',1),
(39,'Coca-Cola 1/5','','Unidad',0,0,0,1,6,1,122100003,'COCACOLA 1/5ML',1),
(40,'Hit 1L','','Unidad',0,0,0,1,12,1,122100005,'HIT 1 LT',1),
(71,'Hit 500 ml','','Unidad',0,0,0,1,12,1,122100013,'HIT 500 ML',1),
(41,'Econolitro','','Unidad',0,0,0,1,12,1,122100007,'ECONOLITRO',1),
(42,'Malta','','Unidad',0,0,0,1,15,1,122100006,'MALTA 1LT',1),
(43,'Coca-Cola 400 ml','','Unidad',0,0,0,1,12,1,122100012,'COCACOLA 400ML',1),
(44,'Gaseosa 250 ml','','Unidad',0,0,0,1,12,1,122100001,'GASEOSA 250ML',1),
(45,'Mr tea 300 ml','','Unidad',0,0,0,1,15,1,	122100011,'MR. TEA 300ML',1),
(46,'Agua Normal','','Unidad',0,0,0,1,20,1,122100010,'AGUA CRISTAL 300ML',1),
(47,'Del valle','','Unidad',0,0,0,1,12,1,122100008,'DEL VALLE 400ML',1),
(48,'Vasos Plasticos(x50)','','Unidad',0,0,0,0,50,50,311100001,'VASOS PLASTICOS 7 ONZ TRAN(X50)',1),
(49,'Papas','','Gramos',0,0,0,1,50,1,311100004,'PAPAS PREPARADAS',1),
(50,'Longaniza(x20)','','Unidad',0,0,0,1,20,1,118100011,'LONGANIZA MIXTA (X12)',1),
(51,'Manguera(x500)','','Gramos',0,0,0,0,500,500,311100006,'SALCHICHA MANGUERA(X500/230)',1),
(52,'Porta Perro(x50)','','Unidad',0,0,0,0,50,50,311100007,'PORTA PERRO',1),
(53,'Porta Hamburguesa(x50)','','Unidad',0,0,0,0,50,50,311100008,'PORTA HAMBURGUESA',1),
(54,'Azucar','','Gramos',0,0,0,0,500,500,311100033,'AZUCAR',1),
(55,'Zanahoria','','Gramos',0,0,0,0,100,100,311100034,'ZANAHORIA',1),
(56,'Repollo','','Gramos',0,0,0,0,100,100,311100037,'REPOLLO',1),
(57,'Aceite(x18)','','Gramos',0,0,0,0,18,1,115200001,'ACEITE(X18000)',1),
(58,'Bolsa Basura','','Unidad',0,0,0,0,10,1,311100021,'BOLSA BASURA 66X100 CM (X10)',1),
(59,'Paprica','','Gramos',0,0,0,0,1000,10,311100024,'PAPRICA(X1000)',1),
(60,'Plato Hondo','','Unidad',0,0,0,1,20,1,311100025,'PLATO HONDO',1),
(61,'Bandeja 17','','Unidad',0,0,0,1,20,1,311100026,'BANDEJA 17*20',1),
(62,'Bandeja 4','','Unidad',0,0,0,1,20,1,311100047,'BANDEJA 4',1),
(63,'Bandeja Ovalada','','Unidad',0,0,0,1,20,1,311100028,'PLATO HONDO OVALADO',1),
(64,'Chuzos Cerdo','','Unidad',0,0,0,1,1,1,112600001,'AD. CHUZO DE CERDO',1),
(65,'Chuzos Pollo','','Unidad',0,0,0,1,1,1,112600002,'AD. CHUZO DE POLLO',1),
(66,'Cocas Ensalada','','Unidad',0,0,0,1,0,1,0,'N/A',1),
(67,'Chorizo Cerdo','','Unidad',0,0,0,1,1,1,118100010,'CHORIZO DE CERDO CAMPESINO',1),
(68,'Arepas','','Unidad',0,0,0,0,50,1,118100009,'AREPA FRITA',1),
(69,'Chorizos Grandes','','Unidad',0,0,0,1,1,1,0,'N/A',1),
(73,'Chorizos Ternera','','Unidad',0,0,0,1,25,1,118100026,'CHORIZO TERNERA FRICAR (X25)',1)
#


INSERT INTO MateriasPrimasxBodega (CodBod,CodMP,StockMin,Stock_xSemana,StockMax_xDiaNmal,StockMax_xDiaFtvo,OrderIngreso,Estado)
VALUES 

# Bebidas
(4,38,5,12,5,5,1,0),                #(38,'Gaseosas 1/5','','un',0,0,0,1,6,1),
(4,39,10,24,10,10,2,0),              #(39,'Coca-Cola 1/5','','un',0,0,0,1,6,1),
(4,40,10,12,10,10,3,0),              #(40,'Hit 1L','','un',0,0,0,1,12,1),
(4,41,5,18,5,5,4,0),                #(41,'Econolitro','','un',0,0,0,1,12,1),
(4,42,5,12,5,5,5,0),                #(42,'Malta','','un',0,0,0,1,15,1),
(4,43,14,36,12,12,6,0),              #(43,'Coca-Cola 400','','un',0,0,0,1,12,1),
(4,44,40,66,35,35,7,0),              #(44,'Gaseosa 250','','un',0,0,0,1,12,1),
(4,45,6,12,12,12,8,0),                #(45,'Mr tea 300','','un',0,0,0,1,15,1),
(4,46,6,6,6,6,9,0),                 #(46,'Agua Normal','','un',0,0,0,1,20,1),
(4,47,6,12,6,6,10,0),               #(47,'Del valle','','un',0,0,0,1,12,1),

# Villa
(4,48,10,100,10,10,11,0),            #(48,'Vasos Plasticos(x50)','','un',0,0,0,0,50,50),
(4,3,8,20,8,8,12,0),                #(3,'Ripio(x1000)','','gr',0,2,0,0,1,1),
(4,23,144,600,144,240,13,0),          #(23,'Pan Hamburguesa(x12)','','un',0,1,0,1,12,12),
(4,24,60,130,60,60,14,0),            #(24,'Pan Perro(x10)','','un',0,1,0,1,10,10),
(4,25,150,700,150,250,15,0),          #(25,'Carne Hamb 700(x10)','','un',0,1,0,1,10,10),
(4,26,160,384,160,160,16,0),               #(26,'Tocineta Premiun(x32)','','un',0,1,0,1,1,1),
(4,27,12,125,50,50,17,0),            #(27,'Salchicha Perro(x25)','','un',0,1,0,1,25,25),
(4,4,1.25,6,2,2,18,0),              #(4,'Queso tajado(x5/18)','','un',0,2,0,0,1,1),
(4,49,20,100,10,20,19,0),           #(49,'Papas','','kg',0,0,0,1,50,1),
(4,28,1000,3500,1000,0,20,0),    #(28,'Chorzo.Coctelero(x1250)','','gr',0,2,0,0,1250,1250),
(4,50,5,15,5,5,21,0),               #(50,'Longaniza(x20)','','un',0,0,0,1,20,1),
(4,51,500,3500,1000,0,22,0),         #(51,'Manguera(x500)','','gr',0,0,0,0,500,500),
(4,29,96,288,72,96,23,0),            #(29,'Huevo Codorniz(x24)','','un',0,1,0,1,24,24),
(4,52,50,150,50,50,24,0),            #(52,'Porta Perro(x50)','','un',0,0,0,0,50,50),
(4,53,100,700,100,100,25,0),           #(53,'Porta Hamburguesa(x50)','','un',0,0,0,0,50,50),

(4,30,0,7300,1500,0,26,0),             #(30,'S. Mayonesa(x3650)','','g',1,3,0,0,3650,3650),    
(4,31,2000,21900,3650,3650,27,0),             #(31,'S. Rosada(x3650)','','g',1,3,0,0,3650,3650),
(4,33,1500,14600,3650,3650,28,0),             #(33,'S. Tartara(x3650)','','g',1,3,0,0,3650,3650), 
(4,32,1200,10950,3650,3650,29,0),             #(32,'S. Ajo(x3650)','','g',1,3,0,0,3650,3650),
(4,34,0,8000,4000,4000,30,0),          #(34,'S. Roja(x4000)','','g',0,3,0,0,4000,4000),
(4,35,0,4000,4000,4000,31,0),          #(35,'S. Mostaza(x4000)','','g',0,3,0,0,4000,4000),
(4,36,0,8000,4000,4000,32,0),          #(36,'S. Piña(x4000)','','g',0,3,0,0,4000,4000),
(4,37,0,4000,4000,4000,33,0),          #(37,'S. BBQ(x4000)','','g',0,3,0,0,4000,4000),
(4,54,0,0,0,0,34,0),                #(54,'Azucar','','gr',0,0,0,0,500,500), >> falta parametrizar Stock_xSemana
(4,55,0,0,0,0,35,0),                #(55,'Zanahoria','','gr',0,0,0,0,50,50), >> falta parametrizar Stock_xSemana
(4,56,0,0,0,0,36,0),                #(56,'Repollo','','gr',0,0,0,0,100,100), >> falta parametrizar Stock_xSemana
(4,57,5,0,0,0,37,0),                #(57,'Aceite(x18)','','gr',0,0,0,0,18,1), >> falta parametrizar Stock_xSemana
(4,5,0.25,2,1,0,38,0),           #(5,'Papel Chicle(x300)','','mt',0,2,0,0,1,1),
(4,6,2,0,0,0,39,0),                 #(6,'Rllo. Caja','','un',0,2,0,0,1,1), >> falta parametrizar Stock_xSemana
(4,7,0,3,1,0,40,0),                 #(7,'T15(x100)','','un',0,2,0,0,1,1),
(4,8,0,2,1,0,41,0),                 #(8,'T20(x100)','','un',0,2,0,0,1,1),
(4,9,0,2,1,0,42,0),                 #(9,'T25(x100)','','un',0,2,0,0,1,1),
(4,10,0,1,1,0,43,0),                #(10,'T30(x100)','','un',0,2,0,0,1,1),
(4,11,0,6,1,0,44,0),                #(11,'Opaca(x100)','','un',0,2,0,0,1,1),
(4,12,0,2,1,0,45,0),                #(12,'Aluminio(x100)','','un',0,2,0,0,1,1),
(4,13,2,6,2,0,46,0),                #(13,'Servilleta Nuve(x300)','','un',0,2,0,0,1,1),
(4,14,1,5,1,0,47,0),                #(14,'Servilleta Plus(x100)','','un',0,2,0,0,1,1),
(4,15,0,0,0,0,48,0),                #(15,'Papel Higienico','','un',0,2,0,0,1,1), >> falta parametrizar Stock_xSemana
(4,16,0,0,0,0,49,0),                #(16,'Citronela','','un',0,2,0,0,1,1), >> falta parametrizar Stock_xSemana
(4,17,0,0,0,0,50,0),                #(17,'jabon Liquido','','un',0,2,0,0,1,0.25), >> falta parametrizar Stock_xSemana
(4,18,0,0,0,0,51,0),                #(18,'Limpido','','un',0,2,0,0,1,0.25), >> falta parametrizar Stock_xSemana
(4,19,0,0,0,0,52,0),                #(19,'Axion','','un',0,2,0,0,1,1), >> falta parametrizar Stock_xSemana
(4,20,0,0,0,0,53,0),                #(20,'Jabon Rey','','un',0,2,0,0,1,0.5), >> falta parametrizar Stock_xSemana
(4,58,3,7,3,0,54,0),               #(58,'Bolsa Basura','','un',0,0,0,0,10,1),
(4,21,0,0,0,0,55,0),                #(21,'Jabon Fab','','un',0,2,0,0,1,0.25), >> falta parametrizar Stock_xSemana
(4,22,0.25,200,100,0,56,0),         #(22,'Tenedores(x100)','','un',0,2,0,0,1,1),
(4,1,0.25,1,1,0,57,0),              #(1,'Palillos(x120)','','un',0,2,0,0,1,1),
(4,59,0,80,50,0,58,0),                #(59,'Paprica','','gr',0,0,0,0,1000,10),
(4,60,50,120,50,50,59,0),            #(60,'Plato Hondo','','un',0,0,0,1,20,1),
(4,61,50,120,50,50,60,0),            #(61,'Bandeja 17','','un',0,0,0,1,20,1),
(4,62,10,10,10,10,61,0),             #(62,'Bandeja 4','','un',0,0,0,1,20,1),
(4,63,5,10,5,5,62,0),               #(63,'Bandeja Ovalada','','un',0,0,0,1,20,1),
(4,64,5,0,10,10,63,0),                #(64,'Chuzos Cerdo','','un',0,0,0,1,1,1), >> falta parametrizar Stock_xSemana
(4,65,5,0,5,5,64,0),                #(65,'Chuzos Pollo','','un',0,0,0,1,1,1), >> falta parametrizar Stock_xSemana
(4,66,1,0,5,0,65,0),                #(66,'Cocas Ensalada','','un',0,0,0,1,50,1), >> falta parametrizar Stock_xSemana
(4,67,5,0,5,5,66,0),                #(67,'Chorizo Cerdo','','un',0,0,0,1,1,1), >> falta parametrizar Stock_xSemana
(4,68,20,0,20,20,67,0),                #(68,'Arepas','','un',0,0,0,0,50,1), >> falta parametrizar Stock_xSemana
(4,2,0,0,0,0,68,0),                 #(2,'Pitillos','','un',0,2,0,0,1,0.15), >> falta parametrizar Stock_xSemana
(4,70,0.25,2,1,0,69,0),              #(70,'Papel Chicle Papas.(x300)','','mt',0,2,0,0,1,1),


(2,38,0,0,0,0,1,0),                #(38,'Gaseosas 1/5','','un',0,0,0,1,6,1),
(2,39,0,0,0,0,2,0),              #(39,'Coca-Cola 1/5','','un',0,0,0,1,6,1),
(2,40,0,0,0,0,3,0),              #(40,'Hit','','un',0,0,0,1,12,1),
(2,41,0,0,0,0,4,0),                #(41,'Econolitro','','un',0,0,0,1,12,1),
(2,42,0,0,0,0,5,0),                #(42,'Malta','','un',0,0,0,1,15,1),
(2,43,0,0,0,0,6,0),              #(43,'Coca-Cola 250','','un',0,0,0,1,12,1),
(2,44,0,0,0,0,7,0),              #(44,'Gaseosa 250','','un',0,0,0,1,12,1),
(2,45,0,0,0,0,8,0),                #(45,'Mr tea 300','','un',0,0,0,1,15,1),
(2,46,0,0,0,0,9,0),                 #(46,'Agua Normal','','un',0,0,0,1,20,1),
(2,47,0,0,0,0,10,0),               #(47,'Del valle','','un',0,0,0,1,12,1),

# Villa
(2,48,0,0,0,0,11,0),            #(48,'Vasos Plasticos(x50)','','un',0,0,0,0,50,50),
(2,3,0,0,0,0,12,0),                #(3,'Ripio(x1000)','','gr',0,2,0,0,1,1),
(2,23,0,0,0,0,13,0),          #(23,'Pan Hamburguesa(x12)','','un',0,1,0,1,12,12),
(2,24,0,0,0,0,14,0),            #(24,'Pan Perro(x10)','','un',0,1,0,1,10,10),
(2,25,0,0,0,0,15,0),          #(25,'Carne Hamb 700(x10)','','un',0,1,0,1,10,10),
(2,26,0,0,0,0,16,0),               #(26,'Tocineta Premiun(x32)','','un',0,1,0,1,1,1),
(2,27,0,0,0,0,17,0),            #(27,'Salchicha Perro(x25)','','un',0,1,0,1,25,25),
(2,4,0,0,0,0,18,0),              #(4,'Queso tajado(x5/18)','','un',0,2,0,0,1,1),
(2,49,0,0,0,0,19,0),           #(49,'Papas','','kg',0,0,0,1,50,1),
(2,28,0,0,0,0,20,0),    #(28,'Chorzo.Coctelero(x500)','','gr',0,2,0,0,500,500),
(2,50,0,0,0,0,21,0),               #(50,'Longaniza(x20)','','un',0,0,0,1,20,1),
(2,51,0,0,0,0,22,0),         #(51,'Manguera(x500)','','gr',0,0,0,0,500,500),
(2,29,0,0,0,0,23,0),            #(29,'Huevo Codorniz(x24)','','un',0,1,0,1,24,24),
(2,52,0,0,0,0,24,0),            #(52,'Porta Perro(x50)','','un',0,0,0,0,50,50),
(2,53,0,0,0,0,25,0),           #(53,'Porta Hamburguesa(x50)','','un',0,0,0,0,50,50),

(2,30,0,0,0,0,26,0),             #(30,'S. Mayonesa(x3650)','','g',1,3,0,0,3650,3650),    
(2,31,0,0,0,0,27,0),             #(31,'S. Rosada(x3650)','','g',1,3,0,0,3650,3650),
(2,33,0,0,0,0,28,0),             #(33,'S. Tartara(x3650)','','g',1,3,0,0,3650,3650), 
(2,32,0,0,0,0,29,0),             #(32,'S. Ajo(x3650)','','g',1,3,0,0,3650,3650),
(2,34,0,0,0,0,30,0),          #(34,'S. Roja(x4000)','','g',0,3,0,0,4000,4000),
(2,35,0,0,0,0,31,0),          #(35,'S. Mostaza(x4000)','','g',0,3,0,0,4000,4000),
(2,36,0,0,0,0,32,0),          #(36,'S. Piña(x4000)','','g',0,3,0,0,4000,4000),
(2,37,0,0,0,0,33,0),          #(37,'S. BBQ(x4000)','','g',0,3,0,0,4000,4000),
(2,54,0,0,0,0,34,0),                #(54,'Azucar','','gr',0,0,0,0,500,500), >> falta parametrizar Stock_xSemana
(2,55,0,0,0,0,35,0),                #(55,'Zanahoria','','gr',0,0,0,0,50,50), >> falta parametrizar Stock_xSemana
(2,56,0,0,0,0,36,0),                #(56,'Repollo','','gr',0,0,0,0,100,100), >> falta parametrizar Stock_xSemana
(2,57,0,0,0,0,37,0),                #(57,'Aceite(x18)','','gr',0,0,0,0,18,1), >> falta parametrizar Stock_xSemana
(2,5,0,0,0,0,38,0),           #(5,'Papel Chicle(x300)','','mt',0,2,0,0,1,1),
(2,6,0,0,0,0,39,0),                 #(6,'Rllo. Caja','','un',0,2,0,0,1,1), >> falta parametrizar Stock_xSemana
(2,7,0,0,0,0,40,0),                 #(7,'T15(x100)','','un',0,2,0,0,1,1),
(2,8,0,0,0,0,41,0),                 #(8,'T20(x100)','','un',0,2,0,0,1,1),
(2,9,0,0,0,0,42,0),                 #(9,'T25(x100)','','un',0,2,0,0,1,1),
(2,10,0,0,0,0,43,0),                #(10,'T30(x100)','','un',0,2,0,0,1,1),
(2,11,0,0,0,0,44,0),                #(11,'Opaca(x100)','','un',0,2,0,0,1,1),
(2,12,0,0,0,0,45,0),                #(12,'Aluminio(x100)','','un',0,2,0,0,1,1),
(2,13,0,0,0,0,46,0),                #(13,'Servilleta Nuve(x300)','','un',0,2,0,0,1,1),
(2,14,0,0,0,0,47,0),                #(14,'Servilleta Plus(x100)','','un',0,2,0,0,1,1),
(2,15,0,0,0,0,48,0),                #(15,'Papel Higienico','','un',0,2,0,0,1,1), >> falta parametrizar Stock_xSemana
(2,16,0,0,0,0,49,0),                #(16,'Citronela','','un',0,2,0,0,1,1), >> falta parametrizar Stock_xSemana
(2,17,0,0,0,0,50,0),                #(17,'jabon Liquido','','un',0,2,0,0,1,0.25), >> falta parametrizar Stock_xSemana
(2,18,0,0,0,0,51,0),                #(18,'Limpido','','un',0,2,0,0,1,0.25), >> falta parametrizar Stock_xSemana
(2,19,0,0,0,0,52,0),                #(19,'Axion','','un',0,2,0,0,1,1), >> falta parametrizar Stock_xSemana
(2,20,0,0,0,0,53,0),                #(20,'Jabon Rey','','un',0,2,0,0,1,0.5), >> falta parametrizar Stock_xSemana
(2,58,0,0,0,0,54,0),               #(58,'Bolsa Basura','','un',0,0,0,0,10,1),
(2,21,0,0,0,0,55,0),                #(21,'Jabon Fab','','un',0,2,0,0,1,0.25), >> falta parametrizar Stock_xSemana
(2,22,0,0,0,0,56,0),         #(22,'Tenedores(x100)','','un',0,2,0,0,1,1),
(2,1,0,0,0,0,57,0),              #(1,'Palillos(x120)','','un',0,2,0,0,1,1),
(2,59,0,0,0,0,58,0),                #(59,'Paprica','','gr',0,0,0,0,1000,10),
(2,60,0,0,0,0,59,0),            #(60,'Plato Hondo','','un',0,0,0,1,20,1),
(2,61,0,0,0,0,60,0),            #(61,'Bandeja 17','','un',0,0,0,1,20,1),
(2,62,0,0,0,0,61,0),             #(62,'Bandeja 8','','un',0,0,0,1,20,1),
(2,63,0,0,0,0,62,0),               #(63,'Bandeja Ovalada','','un',0,0,0,1,20,1),
(2,64,0,0,0,0,63,0),                #(64,'Chuzos Cerdo','','un',0,0,0,1,1,1), >> falta parametrizar Stock_xSemana
(2,65,0,0,0,0,64,0),                #(65,'Chuzos Pollo','','un',0,0,0,1,1,1), >> falta parametrizar Stock_xSemana
(2,66,0,0,0,0,65,0),                #(66,'Cocas Ensalada','','un',0,0,0,1,50,1), >> falta parametrizar Stock_xSemana
(2,67,0,0,0,0,66,0),                #(67,'Chorizo Cerdo','','un',0,0,0,1,1,1), >> falta parametrizar Stock_xSemana
(2,68,0,0,0,0,67,0),                #(68,'Arepas','','un',0,0,0,0,50,1), >> falta parametrizar Stock_xSemana
(2,2,0,0,0,0,68,0),                 #(2,'Pitillos','','un',0,2,0,0,1,0.15), >> falta parametrizar Stock_xSemana
(2,70,0,0,0,0,69,0)              #(70,'Papel Chicle Papas.(x300)','','mt',0,2,0,0,1,1)


#tabla materiasprimas poner clasificación: bebidas, aseo, papeleria, materia prima

UPDATE DtlleInventario
SET Uds = 0.75
WHERE IdFoto = 5 and CodMP = 3

##agregar columna StockMin, Stock_xSemana,StockMax_xDiaNmal,StockMax_xDiaFtvo


sql = """


"""
   
try:
    cursor.execute(sql)
    conexion.commit()
    print("Inserción masiva exitosa")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conexion.close()


DELETE FROM InformeInvxDia; 

INSERT INTO InformeInvxDia (CodMP,InventarioFinal_DiaAnt,Consumos_Dia,InventarioInicial_Dia,InventarioFinal_Dia)
SELECT D.CodMP,0,0,0,(D.Uds+ D.Pquetes) FROM EncInventario E INNER JOIN DtlleInventario D ON (E.IdFoto  = D.IdFoto) WHERE E.CodBod = 2 AND E.FechaRegistro = '2025-06-20'


UPDATE InformeInvxDia I
JOIN (
    SELECT D.CodMP, (D.Uds + D.Pquetes) AS InventarioFinal
    FROM EncInventario E
    INNER JOIN DtlleInventario D ON E.IdFoto = D.IdFoto
    WHERE E.CodBod = 2 AND E.FechaRegistro = '2025-06-19'
) AS T ON I.CodMP = T.CodMP
SET 
    I.InventarioFinal_DiaAnt = T.InventarioFinal;


UPDATE InformeInvxDia I
JOIN (
    SELECT C.CodMP, C.Uds AS Consumo
    FROM EncInventario E
    INNER JOIN Kardex C ON (C.IdFotoRef = E.IdFoto)
    WHERE C.CodBod = 2 AND E.FechaRegistro = '2025-06-20'
) AS T ON I.CodMP = T.CodMP
SET 
    I.Consumos_Dia = T.Consumo;

UPDATE InformeInvxDia I
SET I.InventarioInicial_Dia = I.InventarioFinal_DiaAnt + I.Consumos_Dia;

"""

sql = """

INSERT INTO BodegasxFranquicia (CodFca,CodBod,Nombre)
VALUES 
(1,2,'Preparación'),
(1,4,'Bodega')




"""
   
try:
    cursor.execute(sql)
    conexion.commit()
    print("Inserción masiva exitosa")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    conexion.close()