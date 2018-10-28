-- MySQL Script generated by MySQL Workbench
-- Sun Oct 28 09:47:10 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema Alice
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Alice
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Alice` DEFAULT CHARACTER SET utf8 ;
USE `Alice` ;

-- -----------------------------------------------------
-- Table `Alice`.`newspaper`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Alice`.`newspaper` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `content` LONGTEXT NOT NULL,
  `label` INT NULL,
  `sentences` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;