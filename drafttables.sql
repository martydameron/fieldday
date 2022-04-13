use fieldday_db;

drop table if exists game;
drop table if exists feed;
drop table if exists post;
drop table if exists form;
drop table if exists user;
drop table if exists sport;
drop table if exists college;

CREATE TABLE college (
    cid int not null auto_increment,
    name varchar(60),

    primary key (cid),

    index(name)
)
ENGINE = InnoDB; 

CREATE TABLE sport (
    sid int not null auto_increment,
    sport varchar(30),

    primary key (sid)
)
ENGINE = InnoDB;

CREATE TABLE user (
    uid int not null auto_increment,
    username varchar(15),
    password varchar(15),
    firstname varchar(30),
    lastname varchar(30),
    school int,
    collegeemail varchar(60),
    classyear char(4),
    role varchar(30),
    club set('1', '2', '3', '4', '5', '6', '7', '8'),
    `admin` boolean,

    primary key(uid),

    index(school),
    index(username),
    index(lastname),

    foreign key (school) references college(cid)
        on update cascade
        on delete cascade
)
ENGINE = InnoDB;

CREATE TABLE form (
    foid int not null auto_increment,
    club enum('1', '2', '3', '4', '5', '6', '7', '8'),
    type enum('interest', 'attend', 'injury'),
    email varchar(60),
    studentname varchar(60),
    studentID varchar(15),
    description mediumtext,
    submittedby int,
    submittedon date,

    primary key (foid),

    index(submittedby),

    foreign key (submittedby) references user(uid)
        on update cascade
        on delete cascade
)
ENGINE = InnoDB;

CREATE TABLE post (
    pid int not null auto_increment,
    caption mediumtext,
    `date` date,
    team enum('1', '2', '3', '4', '5', '6', '7', '8'),
    likes int,
    dislikes int,
    -- picture varbinary(max),
    primary key (pid),

    index(date),
    index(team)
)
ENGINE = InnoDB;

CREATE TABLE feed (
    viewer int not null,
    poster int,
    currentpost int,

    index(viewer),
    index(poster),
    index(currentpost),

    foreign key (viewer) references user(uid) 
        on update cascade
        on delete cascade,
    foreign key (poster) references user(uid) 
        on update cascade
        on delete cascade,
    foreign key (currentpost) references post(pid)
        on update cascade
        on delete cascade
)
ENGINE = InnoDB;

CREATE TABLE game (
    teamone int,
    teamtwo int,
    onescore int,
    twoscore int,
    location varchar(30),
    `date` date,

    primary key (teamone,teamtwo,`date`),
    index(teamone),
    index(teamtwo),

    foreign key (teamone) references sport(sid)
        on update cascade
        on delete cascade,
    foreign key (teamtwo) references sport(sid)
        on update cascade
        on delete cascade
)
ENGINE = InnoDB;
