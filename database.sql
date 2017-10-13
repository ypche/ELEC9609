DROP TABLE IF EXISTS SHUTTERDB.USER;
CREATE TABLE IF NOT EXISTS SHUTTERDB.USER (
ID	INT	NOT NULL	PRIMARY KEY,
NAME VARCHAR(20),
GENDER CHAR(1),
EMAIL VARCHAR(50),
PASSWORD VARCHAR(20),
AUTHORIZATION VARCHAR(10),
PQUESTION1 VARCHAR(200),
PANSWER1 VARCHAR(200),
PQUESTION2	VARCHAR(200),
PANSWER2 VARCHAR(200),
REMARKS	VARCHAR(500)
);

drop table if exists SHUTTERDB.MESSAGE;
create table if not exists SHUTTERDB.MESSAGE (
ID	INT	not null	primary key,
author	INT,
receiver	INT,
content	varchar(500),
create_time	datetime,
remarks	varchar(500),

foreign key (author) references user(id) on update cascade on delete cascade,
foreign key (receiver) references user(id) on update cascade on delete cascade
);

drop table if exists SHUTTERDB.TOPIC;
create table if not exists SHUTTERDB.TOPIC (
ID	INT not null	primary key,
TITLE	varchar(100),
CONTENT	varchar(500),
CREATE_TIME	datetime,
AUTHOR	INT,
REMARKS	varchar(500),

foreign key (AUTHOR) references user(id) on update cascade on delete cascade
);

drop table if exists SHUTTERDB.TOPICCOMMENT;
create table if not exists SHUTTERDB.TOPICCOMMENT (
ID	INT not null	primary key,
TOPIC	INT,
COMMENT	INT,
CONTENT	varchar(500),
CREATE_TIME	datetime,
AUTHOR	INT,
REMARKS	varchar(500),

foreign key (TOPIC) references topic(id) on update cascade on delete cascade,
foreign key (COMMENT) references topiccomment(id) on update cascade on delete cascade,
foreign key (AUTHOR) references user(id) on update cascade on delete cascade
);

drop table if exists SHUTTERDB.NEWS;
create table if not exists SHUTTERDB.NEWS (
ID	INT not null	primary key,
TITLE	varchar(100),
CONTENT	varchar(500),
CREATE_TIME	datetime,
AUTHOR	INT,
REMARKS	varchar(500),

foreign key (AUTHOR) references user(id) on update cascade on delete cascade
);

drop table if exists SHUTTERDB.NEWSCOMMENT;
create table if not exists SHUTTERDB.NEWSCOMMENT (
ID	INT not null	primary key,
TOPIC	INT,
COMMENT	INT,
CONTENT	varchar(500),
CREATE_TIME	datetime,
AUTHOR	INT,
REMARKS	varchar(500),

foreign key (TOPIC) references news(id) on update cascade on delete cascade,
foreign key (COMMENT) references newscomment(id) on update cascade on delete cascade,
foreign key (AUTHOR) references user(id) on update cascade on delete cascade
);

drop table if exists SHUTTERDB.PHOTO;
create table if not exists SHUTTERDB.PHOTO (
ID	INT	not null primary key,
AUTHOR	INT,
PHOTO_PATH	varchar(200),
THUMBS_UP_NUMBER	int,
CATEGORY	varchar(20),
CREATE_TIME	datetime,
REMARKS	varchar(500),

foreign key (AUTHOR) references user(id) on update cascade on delete cascade
);

drop table if exists SHUTTERDB.PHOTOCOMMENT;
create table if not exists SHUTTERDB.PHOTOCOMMENT (
ID	INT	not null primary key,
AUTHOR	INT,
PHOTO	int,
COMMENT	int,
THUMBS_UP_NUMBER	int,
THUMBS_DOWN_NUMBER	int,
CREATE_TIME	datetime,
CONTENT	varchar(500),
REMARKS	varchar(500),

foreign key (AUTHOR) references user(id) on update cascade on delete cascade,
foreign key (PHOTO) references photo(id) on update cascade on delete cascade,
foreign key (COMMENT) references photocomment(id) on update cascade on delete cascade
);