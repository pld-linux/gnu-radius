




CREATE DATABASE RADIUS;
USE RADIUS;

CREATE TABLE passwd (
  user_name           varchar(32) binary default '' not null,
  service             char(16) default 'Framed-PPP' not null,
  password            char(64),
  active              enum ('Y','N') default 'Y' not null ,
  INDEX uname (user_name,active) ,
  UNIQUE usrv (user_name,service,active) 
);
CREATE TABLE groups (
  user_name           char(32) binary default '' not null,
  user_group          char(32) ,
  INDEX grp (user_name)
);
CREATE TABLE attrib (
  user_name           varchar(32) binary default '' not null,
  attr                char(32) default '' not null,
  value               char(128),
  op                  enum ('=','!=','<','>','<=','>=') default NULL ,
  INDEX uattr (user_name,attr,op)
);
CREATE TABLE calls (
  status              int(5) not null,
  user_name           varchar(32) binary default '' not null,
  event_date_time     datetime DEFAULT '1970-01-01 00:00:00' NOT NULL,
  nas_ip_address      char(17) default '0.0.0.0' not null,
  nas_port_id         int(10),
  acct_session_id     char(17) DEFAULT '' NOT NULL,
  acct_session_time   int(10),
  acct_input_octets   int(10),
  acct_output_octets  int(10),
  connect_term_reason int(10),
  framed_ip_address   char(17),
  called_station_id   char(32),
  calling_station_id  char(32) ,
  INDEX name_sid (user_name,acct_session_id) ,
  INDEX name_stat_sid (user_name,status,acct_session_id) ,
  INDEX stat_nas (status,nas_ip_address)
);

CREATE TABLE naspools (
  nas char(17) default '0.0.0.0' not null,
  pool char(8),
  PRIMARY KEY (nas)
);

CREATE TABLE ippool (
  pool char(8) default 'DEFAULT' NOT NULL,
  ipaddr char(17) default '' not null,
  status enum ('FREE','BLCK','FIXD','ASGN','RSRV') default 'FREE' not null,
  time datetime DEFAULT '1970-01-01 00:00:00' NOT NULL,
  user_name varchar(32) binary default '' not null ,
  INDEX ippool_name (user_name) ,
  INDEX ippool_ipaddr (ipaddr)
);



USE mysql;
DELETE FROM user WHERE user='radius';
DELETE FROM db WHERE user='radius';
GRANT INSERT,UPDATE,DELETE,SELECT on RADIUS.calls to radius@'%';
GRANT SELECT on RADIUS.passwd to radius@'%';
GRANT SELECT on RADIUS.groups to radius@'%';
GRANT SELECT on RADIUS.attrib to radius@'%';
GRANT SELECT on RADIUS.naspools to radius@'%';
GRANT SELECT,UPDATE on RADIUS.ippool to radius@'%';
UPDATE user set password=password('guessme') where user='radius';
FLUSH PRIVILEGES;

