-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`usuario` ;

CREATE TABLE IF NOT EXISTS `mydb`.`usuario` (
  `usuario_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `sobrenome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(55) NOT NULL,
  `data_nasc` DATE NULL,
  `sexo` VARCHAR(15) NULL,
  PRIMARY KEY (`usuario_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`loja`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`loja` ;

CREATE TABLE IF NOT EXISTS `mydb`.`loja` (
  `loja_id` INT NOT NULL AUTO_INCREMENT,
  `endereco` VARCHAR(70) NOT NULL,
  `telefone` VARCHAR(15) NULL,
  `nome` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`loja_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`produto`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`produto` ;

CREATE TABLE IF NOT EXISTS `mydb`.`produto` (
  `produto_id` INT NOT NULL AUTO_INCREMENT,
  `preco` DECIMAL(5,2) UNSIGNED NOT NULL,
  `marca` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`produto_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`compra`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`compra` ;

CREATE TABLE IF NOT EXISTS `mydb`.`compra` (
  `compra_id` INT NOT NULL AUTO_INCREMENT,
  `data_compra` DATE NOT NULL,
  `usuario_usuario_id` INT UNSIGNED NOT NULL,
  `produto_produto_id` INT NOT NULL,
  PRIMARY KEY (`compra_id`),
  INDEX `fk_compra_usuario_idx` (`usuario_usuario_id` ASC),
  INDEX `fk_compra_produto1_idx` (`produto_produto_id` ASC),
  CONSTRAINT `fk_compra_usuario`
    FOREIGN KEY (`usuario_usuario_id`)
    REFERENCES `mydb`.`usuario` (`usuario_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_compra_produto1`
    FOREIGN KEY (`produto_produto_id`)
    REFERENCES `mydb`.`produto` (`produto_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`categoria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`categoria` ;

CREATE TABLE IF NOT EXISTS `mydb`.`categoria` (
  `categoria_id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`categoria_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`produto_categoria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`produto_categoria` ;

CREATE TABLE IF NOT EXISTS `mydb`.`produto_categoria` (
  `categoria_id` INT NOT NULL,
  `produto_id` INT NOT NULL,
  PRIMARY KEY (`categoria_id`, `produto_id`),
  INDEX `fk_produto_categoria_produto1_idx` (`produto_id` ASC),
  CONSTRAINT `fk_produto_categoria_categoria1`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `mydb`.`categoria` (`categoria_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_produto_categoria_produto1`
    FOREIGN KEY (`produto_id`)
    REFERENCES `mydb`.`produto` (`produto_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`produto_loja`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`produto_loja` ;

CREATE TABLE IF NOT EXISTS `mydb`.`produto_loja` (
  `loja_id` INT NOT NULL,
  `produto_id` INT NOT NULL,
  PRIMARY KEY (`loja_id`, `produto_id`),
  INDEX `fk_produto_loja_produto1_idx` (`produto_id` ASC),
  CONSTRAINT `fk_produto_loja_loja1`
    FOREIGN KEY (`loja_id`)
    REFERENCES `mydb`.`loja` (`loja_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_produto_loja_produto1`
    FOREIGN KEY (`produto_id`)
    REFERENCES `mydb`.`produto` (`produto_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
