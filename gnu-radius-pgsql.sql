








CREATE TABLE passwd (
  user_name           character(32)  default '' not null,
  service             character(16) default 'Framed-PPP' not null,
  password            character(64),
  active              char default 'Y' not null 
   
   
);

CREATE INDEX uname on passwd (user_name,active);

CREATE UNIQUE INDEX usrv on passwd (user_name,service,active);




CREATE TABLE groups (
  user_name           character(32)  default '' not null,
  user_group          character(32) 
  
);

CREATE INDEX grp on groups (user_name);




CREATE TABLE attrib (
  user_name           character(32)  default '' not null,
  attr                character(32) default '' not null,
  value               character(128),
  op                  character(2) default NULL 
  
);

CREATE INDEX uattr on attrib (user_name,attr,op);




CREATE TABLE calls (
  status              int2 not null,
  user_name           character(32)  default '' not null,
  event_date_time     timestamp NOT NULL,
  nas_ip_address      character(17) default '0.0.0.0' not null,
  nas_port_id         int8,
  acct_session_id     character(17) DEFAULT '' NOT NULL,
  acct_session_time   int8,
  acct_input_octets   int8,
  acct_output_octets  int8,
  connect_term_reason int8,
  framed_ip_address   character(17),
  called_station_id   character(32),
  calling_station_id  character(32) 
   
   
  
);

CREATE INDEX name_sid on calls (user_name,acct_session_id);

CREATE INDEX name_stat_sid on calls (user_name,status,acct_session_id);

CREATE INDEX stat_nas on calls (status,nas_ip_address);





CREATE TABLE naspools (
  nas character(17) default '0.0.0.0' not null,
  pool character(8),
  PRIMARY KEY (nas)
);





CREATE TABLE ippool (
  pool character(8) default 'DEFAULT' NOT NULL,
  ipaddr character(17) default '' not null,
  status character(4) default 'FREE' not null,
  time timestamp NOT NULL,
  user_name character(32)  default '' not null 
   
  
);

CREATE INDEX ippool_name on ippool (user_name);

CREATE INDEX ippool_ipaddr on ippool (ipaddr);




CREATE USER "radius" WITH PASSWORD 'guessme';
REVOKE ALL on "calls" from PUBLIC;
GRANT INSERT,UPDATE,DELETE,SELECT on "calls" to "radius";
REVOKE ALL on "passwd" from PUBLIC;
GRANT SELECT on "passwd" to "radius";
REVOKE ALL on "groups" from PUBLIC;
GRANT SELECT on "groups" to "radius";
REVOKE ALL on "attrib" from PUBLIC;
GRANT SELECT on "attrib" to "radius";
REVOKE ALL on "naspools" from PUBLIC;
GRANT SELECT on "naspools" to "radius";
REVOKE ALL on "ippool" from PUBLIC;
GRANT SELECT,UPDATE on "ippool" to "radius";

