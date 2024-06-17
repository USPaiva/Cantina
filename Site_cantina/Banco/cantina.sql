-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           10.4.32-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.5.0.6677
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para cantina
CREATE DATABASE IF NOT EXISTS `cantina` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `cantina`;

-- Copiando estrutura para tabela cantina.pedidos
CREATE TABLE IF NOT EXISTS `pedidos` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `retirada` datetime NOT NULL,
  `valor` varchar(45) NOT NULL,
  `user_Id` int(11) NOT NULL,
  `tipo_pagamento_Id` int(11) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `user_Id` (`user_Id`),
  KEY `tipo_pagamento_Id` (`tipo_pagamento_Id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`user_Id`) REFERENCES `user` (`Id`),
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`tipo_pagamento_Id`) REFERENCES `tipo_pagamento` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela cantina.pedidos: ~0 rows (aproximadamente)

-- Copiando estrutura para tabela cantina.produto
CREATE TABLE IF NOT EXISTS `produto` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `quantidade` int(11) NOT NULL,
  `nome` varchar(40) NOT NULL,
  `valorCompra` float NOT NULL,
  `valorVenda` float NOT NULL,
  `descricao` varchar(45) NOT NULL,
  `foto` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela cantina.produto: ~0 rows (aproximadamente)

-- Copiando estrutura para tabela cantina.produto_has_pedidos
CREATE TABLE IF NOT EXISTS `produto_has_pedidos` (
  `produto_Id` int(11) NOT NULL,
  `pedidos_Id` int(11) NOT NULL,
  `quantidade` int(11) DEFAULT NULL,
  PRIMARY KEY (`produto_Id`,`pedidos_Id`),
  KEY `pedidos_Id` (`pedidos_Id`),
  CONSTRAINT `produto_has_pedidos_ibfk_1` FOREIGN KEY (`produto_Id`) REFERENCES `produto` (`Id`),
  CONSTRAINT `produto_has_pedidos_ibfk_2` FOREIGN KEY (`pedidos_Id`) REFERENCES `pedidos` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela cantina.produto_has_pedidos: ~0 rows (aproximadamente)

-- Copiando estrutura para tabela cantina.tipo_pagamento
CREATE TABLE IF NOT EXISTS `tipo_pagamento` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_pagamento` varchar(45) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `tipo_pagamento` (`tipo_pagamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela cantina.tipo_pagamento: ~0 rows (aproximadamente)

-- Copiando estrutura para tabela cantina.user
CREATE TABLE IF NOT EXISTS `user` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(16) NOT NULL,
  `password` varchar(32) NOT NULL,
  `email` varchar(255) NOT NULL,
  `ativo` tinyint(1) NOT NULL,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela cantina.user: ~1 rows (aproximadamente)
INSERT IGNORE INTO `user` (`Id`, `username`, `password`, `email`, `ativo`, `type`) VALUES
	(1, 'admin', 'admin', 'admin@admin.com', 1, 'Admin');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
