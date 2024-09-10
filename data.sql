drop table if exists redfunny;
drop table if exists clearfunny;
drop table if exists redlove;
drop table if exists clearlove;
drop table if exists redfantasy;
drop table if exists clearfantasy;
drop table if exists redmeta;
create table redfunny (
	标题 varchar(20),
    id int auto_increment primary key,
    汤面 VARCHAR(500),
    汤底 VARCHAR(500)
);
create table clearfunny (
    标题 varchar(20),
    id int auto_increment primary key,
    汤面 VARCHAR(500),
    汤底 VARCHAR(500)
);
create table redlove (
    标题 varchar(20),
    id int auto_increment primary key,
    汤面 VARCHAR(500),
    汤底 VARCHAR(500)
);
create table clearlove (
    标题 varchar(20),
    id int auto_increment primary key,
    汤面 VARCHAR(500),
    汤底 VARCHAR(500)
);
create table redfantasy (
    标题 varchar(20),
    id int auto_increment primary key,
    汤面 VARCHAR(500),
    汤底 VARCHAR(500)
);
create table clearfantasy (
    标题 varchar(20),
    id int auto_increment primary key,
    汤面 VARCHAR(500),
    汤底 VARCHAR(500)
);
create table redmeta(
    标题 varchar(20),
    id int auto_increment primary key,
    汤面 VARCHAR(500),
    汤底 VARCHAR(500)
);
