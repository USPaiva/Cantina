-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema cantina
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema cantina
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cantina` DEFAULT CHARACTER SET utf8 ;
USE `cantina` ;

-- -----------------------------------------------------
-- Table `cantina`.`typeUser`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cantina`.`typeUser` (
  `IdtypeUser` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdtypeUser`),
  UNIQUE INDEX `idUser_UNIQUE` (`IdtypeUser` ))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cantina`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cantina`.`user` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(16) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `ativo` TINYINT NOT NULL,
  `typeUser_IdtypeUser` INT NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE INDEX `Id_UNIQUE` (`Id` ),
  UNIQUE INDEX `username_UNIQUE` (`username` ),
  INDEX `fk_user_typeUser_idx` (`typeUser_IdtypeUser` ),
  CONSTRAINT `fk_user_typeUser`
    FOREIGN KEY (`typeUser_IdtypeUser`)
    REFERENCES `cantina`.`typeUser` (`IdtypeUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `cantina`.`tipo_pagamento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cantina`.`tipo_pagamento` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `tipo_pagamento` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE INDEX `Id_UNIQUE` (`Id` ),
  UNIQUE INDEX `tipo_pagamento_UNIQUE` (`tipo_pagamento` ))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cantina`.`pedidos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cantina`.`pedidos` (
  `Id` INT NOT NULL,
  `date` DATETIME NOT NULL,
  `retirada` DATETIME NOT NULL,
  `valor` VARCHAR(45) NOT NULL,
  `user_Id` INT NOT NULL,
  `tipo_pagamento_Id` INT NOT NULL,
  PRIMARY KEY (`Id`),
  INDEX `fk_pedidos_user1_idx` (`user_Id` ),
  INDEX `fk_pedidos_tipo_pagamento1_idx` (`tipo_pagamento_Id` ),
  CONSTRAINT `fk_pedidos_user1`
    FOREIGN KEY (`user_Id`)
    REFERENCES `cantina`.`user` (`Id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pedidos_tipo_pagamento1`
    FOREIGN KEY (`tipo_pagamento_Id`)
    REFERENCES `cantina`.`tipo_pagamento` (`Id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cantina`.`produto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cantina`.`produto` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `quantidade` INT NOT NULL,
  `nome` VARCHAR(40) NOT NULL,
  `valorCompra` DOUBLE NOT NULL,
  `valorVenda` DOUBLE NOT NULL,
  `descricao` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE INDEX `Id_UNIQUE` (`Id` ),
  UNIQUE INDEX `nome_UNIQUE` (`nome` ))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cantina`.`produto_has_pedidos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cantina`.`produto_has_pedidos` (
  `produto_Id` INT NOT NULL,
  `pedidos_Id` INT NOT NULL,
  PRIMARY KEY (`produto_Id`, `pedidos_Id`),
  INDEX `fk_produto_has_pedidos_pedidos1_idx` (`pedidos_Id` ),
  INDEX `fk_produto_has_pedidos_produto1_idx` (`produto_Id` ),
  CONSTRAINT `fk_produto_has_pedidos_produto1`
    FOREIGN KEY (`produto_Id`)
    REFERENCES `cantina`.`produto` (`Id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_produto_has_pedidos_pedidos1`
    FOREIGN KEY (`pedidos_Id`)
    REFERENCES `cantina`.`pedidos` (`Id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
