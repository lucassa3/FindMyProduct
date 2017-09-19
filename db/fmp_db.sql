-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema fmp_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema fmp_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `fmp_db` DEFAULT CHARACTER SET utf8 ;
USE `fmp_db` ;

-- -----------------------------------------------------
-- Table `fmp_db`.`usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `fmp_db`.`usuario` ;

CREATE TABLE IF NOT EXISTS `fmp_db`.`usuario` (
  `usuario_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `sobrenome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(55) NOT NULL,
  `data_nasc` DATE NOT NULL,
  `sexo` VARCHAR(15) NULL,
  `senha` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`usuario_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `fmp_db`.`loja`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `fmp_db`.`loja` ;

CREATE TABLE IF NOT EXISTS `fmp_db`.`loja` (
  `loja_id` INT NOT NULL AUTO_INCREMENT,
  `endereco` VARCHAR(70) NOT NULL,
  `telefone` VARCHAR(15) NULL,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(65) NOT NULL,
  `senha` VARCHAR(255) NOT NULL,
  `latitude` varchar(45) NOT NULL,
  `longitude` varchar(45) NOT NULL,
  PRIMARY KEY (`loja_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `fmp_db`.`produto`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `fmp_db`.`produto` ;

CREATE TABLE IF NOT EXISTS `fmp_db`.`produto` (
  `produto_id` INT NOT NULL AUTO_INCREMENT,
  `preco` DECIMAL(8,2) UNSIGNED NOT NULL,
  `marca` VARCHAR(45) NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `path_foto` VARCHAR(250),
  `descricao` VARCHAR(250),
  `quantidade` INT NOT NULL,
  `loja_loja_id` INT NOT NULL,
  PRIMARY KEY (`produto_id`),
  INDEX `fk_produto_loja1_idx` (`loja_loja_id` ASC),
  CONSTRAINT `fk_produto_loja1`
    FOREIGN KEY (`loja_loja_id`)
    REFERENCES `fmp_db`.`loja` (`loja_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `fmp_db`.`compra`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `fmp_db`.`compra` ;

CREATE TABLE IF NOT EXISTS `fmp_db`.`compra` (
  `compra_id` INT NOT NULL AUTO_INCREMENT,
  `data_compra` DATE NOT NULL,
  `quantidade` INT NOT NULL,
  `usuario_usuario_id` INT UNSIGNED NOT NULL,
  `produto_produto_id` INT NOT NULL,
  PRIMARY KEY (`compra_id`),
  INDEX `fk_compra_usuario_idx` (`usuario_usuario_id` ASC),
  INDEX `fk_compra_produto1_idx` (`produto_produto_id` ASC),
  CONSTRAINT `fk_compra_usuario`
    FOREIGN KEY (`usuario_usuario_id`)
    REFERENCES `fmp_db`.`usuario` (`usuario_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_compra_produto1`
    FOREIGN KEY (`produto_produto_id`)
    REFERENCES `fmp_db`.`produto` (`produto_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `fmp_db`.`categoria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `fmp_db`.`categoria` ;

CREATE TABLE IF NOT EXISTS `fmp_db`.`categoria` (
  `categoria_id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`categoria_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `fmp_db`.`produto_categoria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `fmp_db`.`produto_categoria` ;

CREATE TABLE IF NOT EXISTS `fmp_db`.`produto_categoria` (
  `categoria_id` INT NOT NULL,
  `produto_id` INT NOT NULL,
  PRIMARY KEY (`categoria_id`, `produto_id`),
  INDEX `fk_produto_categoria_produto1_idx` (`produto_id` ASC),
  CONSTRAINT `fk_produto_categoria_categoria1`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `fmp_db`.`categoria` (`categoria_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_produto_categoria_produto1`
    FOREIGN KEY (`produto_id`)
    REFERENCES `fmp_db`.`produto` (`produto_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
