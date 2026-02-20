/*
    last update November 9th, 2019
    Author: Roberto Patrizi
    This SQL script drops and creates 
    MBDA database Version 01.00
*/

DROP DATABASE IF EXISTS mbda_01_00;

CREATE DATABASE IF NOT EXISTS mbda_01_00;

USE mbda_01_00;

CREATE TABLE IF NOT EXISTS measure
(
  measure_id        SMALLINT    UNSIGNED    NOT NULL AUTO_INCREMENT PRIMARY KEY,
  unitID            VARCHAR(25)             NOT NULL,
  unit 	            VARCHAR(50)	            NOT NULL,
  measure           VARCHAR(50)   	        NOT NULL,

  CONSTRAINT `unique_measue_measure`
		UNIQUE (measure),

  CONSTRAINT `unique_measure_unit`
		UNIQUE (unitID)

);

CREATE TABLE IF NOT EXISTS area
( 
  area_id         SMALLINT    UNSIGNED    NOT NULL AUTO_INCREMENT PRIMARY KEY,
  areaID         	VARCHAR(25) 	        NOT NULL,
  area       		  VARCHAR(25) 	        NOT NULL,

  CONSTRAINT `unique_area`
		UNIQUE (areaID)

);

CREATE TABLE IF NOT EXISTS machine
( 
  machine_id            SMALLINT    UNSIGNED    NOT NULL AUTO_INCREMENT PRIMARY KEY,
  area_id		        SMALLINT    UNSIGNED    NOT NULL,
  machineClass 		    VARCHAR(25) 	        NOT NULL,
  machineID      	    VARCHAR(25) 	        NOT NULL,
  measure_id            SMALLINT    UNSIGNED    NOT NULL,
  machine_mttf	        DOUBLE,
  machine_mtbf	        DOUBLE,
  machine_mttr	        DOUBLE,
  activationTime 	    DATETIME               NOT NULL,
  deactivationTime	    DATETIME,

  CONSTRAINT `fk_area_id`
		FOREIGN KEY (area_id) REFERENCES area (area_id)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,

  CONSTRAINT `fk_machine_measure_id`
		FOREIGN KEY (measure_id) REFERENCES measure (measure_id)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,

  CONSTRAINT `unique_machineID`
		UNIQUE (machineID)
);

CREATE TABLE IF NOT EXISTS component
( 
  component_id	    SMALLINT    UNSIGNED    NOT NULL AUTO_INCREMENT PRIMARY KEY,
  machine_id        SMALLINT    UNSIGNED    NOT NULL,
  componentClass	VARCHAR(25) 	        NOT NULL,
  componentID   	VARCHAR(25) 	        NOT NULL,
  measure_id		SMALLINT    UNSIGNED    NOT NULL,   -- refers to mttf, mtbf, mttr
  component_mttf    DOUBLE,
  component_mtbf    DOUBLE,
  component_mttr    DOUBLE,
  activationTime 	DATETIME      	        NOT NULL,
  deactivationTime	DATETIME,

  CONSTRAINT `fk_machine_id`
		FOREIGN KEY (machine_id) REFERENCES machine (machine_id)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,

  CONSTRAINT `fk_component_measure_id`
		FOREIGN KEY (measure_id) REFERENCES measure (measure_id)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,

  CONSTRAINT `unique_componentID`
		UNIQUE (componentID)
);

CREATE TABLE IF NOT EXISTS item
( 
  item_id           SMALLINT    UNSIGNED    NOT NULL AUTO_INCREMENT PRIMARY KEY,
  itemID            VARCHAR(25)             NOT NULL,
  measure_id        SMALLINT    UNSIGNED    NOT NULL,
  cycleTime         DOUBLE                  NOT NULL,

  CONSTRAINT `fk_item_measure_id`
		FOREIGN KEY (measure_id) REFERENCES measure (measure_id)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,

  CONSTRAINT `unique_itemID`
		UNIQUE (itemID)
);

CREATE TABLE IF NOT EXISTS measure_component
( 
  measure_component_id     SMALLINT    UNSIGNED    NOT NULL AUTO_INCREMENT PRIMARY KEY,
  component_id             SMALLINT    UNSIGNED    NOT NULL,
  measure_id               SMALLINT    UNSIGNED    NOT NULL,

  CONSTRAINT `fk_measure_component_component_id`
		FOREIGN KEY (component_id) REFERENCES component (component_id)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,

  CONSTRAINT `fk_measure_component_measure_id`
		FOREIGN KEY (measure_id) REFERENCES measure (measure_id)
        	ON DELETE CASCADE
		ON UPDATE RESTRICT,

  CONSTRAINT `unique_measure_component`
		UNIQUE (component_id, measure_id)
);

CREATE TABLE IF NOT EXISTS item_measure_component
( 
  item_measure_component_id     SMALLINT    UNSIGNED    NOT NULL AUTO_INCREMENT PRIMARY KEY,
  measure_component_id          SMALLINT    UNSIGNED    NOT NULL,
  item_id                       SMALLINT    UNSIGNED    NOT NULL,
  min_value                     DOUBLE                  NOT NULL,
  avg_value                     DOUBLE                  NOT NULL,
  max_value                     DOUBLE                  NOT NULL,

  CONSTRAINT `fk_item_measure_component_measure_component_id`
		FOREIGN KEY (measure_component_id) REFERENCES measure_component (measure_component_id)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,

  CONSTRAINT `fk_item_measure_component_item_id`
		FOREIGN KEY (item_id) REFERENCES item (item_id)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,

  CONSTRAINT `unique_item_measure_component`
		UNIQUE (measure_component_id, item_id)
);

# production plan table
CREATE TABLE IF NOT EXISTS prodPlan 
(
    prodPlan_id         SMALLINT    UNSIGNED    NOT NULL AUTO_INCREMENT PRIMARY KEY,
    batchID             VARCHAR(25)             NOT NULL,
    item_id           SMALLINT    UNSIGNED    NOT NULL,
    startTime    	    DATETIME,
    endTime 		    DATETIME,
    itemQuantity        DOUBLE,
    event_time   	    DATETIME(6)             NOT NULL,
    recording_time   	DATETIME(6)             NOT NULL,

    CONSTRAINT `fk_prodPlan_item_id`
		FOREIGN KEY (item_id) REFERENCES item (item_id)
		ON DELETE CASCADE
		ON UPDATE RESTRICT,

  CONSTRAINT `unique_prodPlan`
		UNIQUE (batchID)
);



