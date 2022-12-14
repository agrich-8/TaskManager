-- MySQL Script generated by MySQL Workbench
-- Mon Nov 28 13:23:52 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema tmdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema tmdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tmdb` DEFAULT CHARACTER SET utf8 ;
USE `tmdb` ;

-- -----------------------------------------------------
-- Table `tmdb`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmdb`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `hashed_password` VARCHAR(500) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tmdb`.`projects`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmdb`.`projects` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `is_base_project` TINYINT(1) NULL,
  `color` VARCHAR(45) NULL,
  `user_id` INT NOT NULL,
  `is_favorite` TINYINT(1) NULL,
  PRIMARY KEY (`id`, `user_id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_projects_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `user`
    FOREIGN KEY (`user_id`)
    REFERENCES `tmdb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tmdb`.`tasks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmdb`.`tasks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `description` VARCHAR(1000) NULL,
  `is_completed` TINYINT(1) NULL,
  `position` INT NULL,
  `section` VARCHAR(45) NULL,
  `datetime_expiration` DATETIME NULL,
  `datetime_completion` DATETIME NULL,
  `datetime_added` DATETIME NULL,
  `project_id` INT NOT NULL,
  `priority` INT NULL,
  PRIMARY KEY (`id`, `project_id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_tasks_projects1_idx` (`project_id` ASC) VISIBLE,
  CONSTRAINT `project`
    FOREIGN KEY (`project_id`)
    REFERENCES `tmdb`.`projects` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
