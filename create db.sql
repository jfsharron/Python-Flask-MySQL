CREATE DATABASE f19_msci3300;

USE f19_msci3300;

DROP TABLE IF EXISTS colbert_friend_app;

CREATE TABLE colbert_friends_app(
    friendId int(11) NOT NULL AUTO_INCREMENT,
    first_name varchar(255),
    last_name varchar(255),
    PRIMARY KEY (`friendId`)
) ENGINE = InnoDB AUTO_INCREMENT = 1;