PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE log (mac text not null, dt datetime not null, pm25 int, tmp float, hum int, co2 int);
CREATE TABLE mac (mac text not null, location text default 'Nowhere');
INSERT INTO "mac" VALUES('b8:27:eb:fe:fe:65','A19F Test');
CREATE INDEX log_mac on log (mac);
CREATE INDEX mac_mac on mac (mac);
COMMIT;
