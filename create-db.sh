#!/bin/sh
#
# PVM PhotoVoltaic Monitor
#
# This script creates the initial PVM database.
# Warning: all data will be erased!
#
# Copyright (C) 2012, 2013 Pietro Pizzo <pietro.pizzo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

# Read configuration file
eval $(cat config |grep dbfile)
eval $(cat config |grep sqlite)

# Create database
$sqlite $dbfile <<EOF

drop table parameters;
create table parameters (
  key text,
  value text
);

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

insert into reference_production (month, daily_production, monthly_production) values (1, 11066, 343.032);
insert into reference_production (month, daily_production, monthly_production) values (2, 13632, 395.323);
insert into reference_production (month, daily_production, monthly_production) values (3, 19130, 593.028);
insert into reference_production (month, daily_production, monthly_production) values (4, 22134, 664.007);
insert into reference_production (month, daily_production, monthly_production) values (5, 26207, 812.403);
insert into reference_production (month, daily_production, monthly_production) values (6, 27673, 830.184);
insert into reference_production (month, daily_production, monthly_production) values (7, 28052, 869.609);
insert into reference_production (month, daily_production, monthly_production) values (8, 25347, 785.771);
insert into reference_production (month, daily_production, monthly_production) values (9, 20652, 619.555);
insert into reference_production (month, daily_production, monthly_production) values (10, 16265, 504.218);
insert into reference_production (month, daily_production, monthly_production) values (11, 11874, 356.208);
insert into reference_production (month, daily_production, monthly_production) values (12, 9257, 286.971);



