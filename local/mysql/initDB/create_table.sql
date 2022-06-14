 -- ユーザ管理テーブル
 CREATE TABLE IF NOT EXISTS `DB`.`Users`(
     `user_id` CHAR(48) NOT NULL,
     `user_name` CHAR(16) NOT NULL,
     `prefecture_id` INT NOT NULL,
     PRIMARY KEY (`user_id`));

 CREATE TABLE IF NOT EXISTS `DB`.`Prefectures`(
     `prefecture_id` INT NOT NULL,
     `prefecture_name` CHAR(16) NOT NULL,
     PRIMARY KEY (`prefecture_id`));

 CREATE TABLE IF NOT EXISTS `DB`.`Connections`(
     `connection_id` CHAR(48) NOT NULL,
     `user_id1` CHAR(48) NOT NULL,
     `user_id2` CHAR(48) NOT NULL,
     `status` CHAR(48) NOT NULL,
     PRIMARY KEY (`connection_id`));