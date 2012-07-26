#!/bin/sh
#
# This script creates the initial PVM database.
#
# Warning: all data will be erased!
#
# 2012, Pietro Pizzo <pietro.pizzo@hp.com>
########################################################################

# Read configuration file
eval $(cat config |grep dbfile)
eval $(cat config |grep sqlite)

# Create database
$sqlite $dbfile <<EOF

drop table daily_details;
create table daily_details (
  timestamp text,
  status integer,
  generator_voltage real,
  generator_current real,
  generator_power real,
  grid_voltage real,
  grid_current real,
  delivered_power real,
  device_temperature integer,
  daily_yeld real
);

drop table daily_totals;
create table daily_totals (
  timestamp text,
  daily_max_delivered_power real,
  daily_delivered_power real,
  total_delivered_power real,
  partial_delivered_power real,
  daily_running_hours text,
  total_running_hours text,
  partial_running_hours text
);

drop table reference_production;
create table reference_production (
  month integer,
  daily_production real,
  monthly_production real
);

insert into reference_production (month, daily_production, monthly_production) values (1, 11.066, 343.032);
insert into reference_production (month, daily_production, monthly_production) values (2, 13.632, 395.323);
insert into reference_production (month, daily_production, monthly_production) values (3, 19.13, 593.028);
insert into reference_production (month, daily_production, monthly_production) values (4, 22.134, 664.007);
insert into reference_production (month, daily_production, monthly_production) values (5, 26.207, 812.403);
insert into reference_production (month, daily_production, monthly_production) values (6, 27.673, 830.184);
insert into reference_production (month, daily_production, monthly_production) values (7, 28.052, 869.609);
insert into reference_production (month, daily_production, monthly_production) values (8, 25.347, 785.771);
insert into reference_production (month, daily_production, monthly_production) values (9, 20.652, 619.555);
insert into reference_production (month, daily_production, monthly_production) values (10, 16.265, 504.218);
insert into reference_production (month, daily_production, monthly_production) values (11, 11.874, 356.208);
insert into reference_production (month, daily_production, monthly_production) values (12, 9.257, 286.971);



