-- Creazione della Dimensione Vehicle
CREATE TABLE Dimension_Vehicle (
    CRASH_UNIT_ID INT PRIMARY KEY,
    UNIT_NO INT,
    UNIT_TYPE VARCHAR(100),
    VEHICLE_ID FLOAT,
    MAKE VARCHAR(100),
    MODEL VARCHAR(100),
    LIC_PLATE_STATE VARCHAR(100),
    VEHICLE_YEAR FLOAT,
    VEHICLE_DEFECT VARCHAR(100),
    VEHICLE_TYPE VARCHAR(100),
    VEHICLE_USE VARCHAR(100),
    TRAVEL_DIRECTION VARCHAR(20),
    MANEUVER VARCHAR(100),
    OCCUPANT_CNT FLOAT,
    FIRST_CONTACT_POINT VARCHAR(100)
);

-- Creazione della Dimensione Person
CREATE TABLE Dimension_Person (
    PERSON_ID VARCHAR (100) PRIMARY KEY,
    PERSON_TYPE VARCHAR(100),
    VEHICLE_ID FLOAT,
    INJURY_CLASSIFICATION VARCHAR(50),
    CITY VARCHAR(100),
    STATE VARCHAR(50),
    SEX VARCHAR(3),
    AGE FLOAT,
    SAFETY_EQUIPMENT VARCHAR(100),
    AIRBAG_DEPLOYED VARCHAR(100),
    EJECTION VARCHAR(100),
    DAMAGE_CATEGORY VARCHAR(100),
    DRIVER_ACTION VARCHAR(100),
    DRIVER_VISION VARCHAR(100),
    PHYSICAL_CONDITION VARCHAR(100),
    BAC_RESULT VARCHAR(100)
);


-- Creazione della Dimensione Crash
CREATE TABLE Dimension_Crash (
    RD_NO VARCHAR PRIMARY KEY,
    TRAFFICWAY_TYPE VARCHAR(100),
    POSTED_SPEED_LIMIT INT,
    FIRST_CRASH_TYPE VARCHAR(100),
    TRAFFIC_CONTROL_DEVICE VARCHAR(100),
    REPORT_TYPE VARCHAR(100),
    CRASH_TYPE VARCHAR(100),
    BEAT_OF_OCCURRENCE FLOAT,
    ALIGNMENT VARCHAR(100)
);

-- Creazione della Dimensione Date
CREATE TABLE Dimension_Date (
    DATE_ID INT PRIMARY KEY,
    CRASH_DATE VARCHAR(100), 
    CRASH_DAY_OF_WEEK INT,
    CRASH_HOUR INT,
    CRASH_MONTH INT, 
    DATE_POLICE_NOTIFIED VARCHAR(100),
    CRASH_YEAR INT,
    QUARTER INT
);

-- Creazione della Dimensione Geography
CREATE TABLE Dimension_Geography (
    GEOGRAPHY_ID INT PRIMARY KEY,
    STREET_NO INT,
    STREET_DIRECTION VARCHAR(100),
    STREET_NAME VARCHAR(100),
    LATITUDE VARCHAR(200),
    LONGITUDE VARCHAR(200),
    LOCATION VARCHAR(200)   
);

-- Creazione della Dimensione Cause
CREATE TABLE Dimension_Cause (
    CAUSE_ID INT PRIMARY KEY,
    PRIM_CONTRIBUTORY_CAUSE VARCHAR(255),
    SEC_CONTRIBUTORY_CAUSE VARCHAR(255),
    DEVICE_CONDITION VARCHAR(100),
    ROAD_DEFECT VARCHAR(100),
    ROADWAY_SURFACE_COND VARCHAR(100),
);

-- Creazione della Dimensione Weather
CREATE TABLE Dimension_Weather (
    WEATHER_ID INT PRIMARY KEY,
    WEATHER_CONDITION VARCHAR(100),
    LIGHTING_CONDITION VARCHAR(100)
);



-- Creazione della Dimensione Injuries
CREATE TABLE Dimension_Injuries (
    INJURIES_ID INT NOT NULL PRIMARY KEY,
    INJURIES_FATAL FLOAT,
    INJURIES_INCAPACITATING FLOAT,
    INJURIES_NON_INCAPACITATING FLOAT,
    INJURIES_REPORTED_NOT_EVIDENT FLOAT,
    INJURIES_NO_INDICATION FLOAT,
    INJURIES_UNKNOWN FLOAT,
    MOST_SEVERE_INJURY VARCHAR(100),
    INJURIES_TOTAL FLOAT
);



-- Creazione della Fact_Table
CREATE TABLE Damage_to_users ( 
    Damage_to_users_ID INT NOT NULL PRIMARY KEY,
    DAMAGE FLOAT,
    NUM_UNITS FLOAT, 
    RD_NO VARCHAR (100) NOT NULL,
    PERSON_ID VARCHAR (100) NOT NULL,
    CRASH_UNIT_ID INT NOT NULL,
    DATE_ID INT NOT NULL,
    CAUSE_ID INT NOT NULL,
    GEOGRAPHY_ID INT NOT NULL,
    INJURIES_ID INT NOT NULL,
    WEATHER_ID INT NOT NULL,
    FOREIGN KEY (RD_NO) REFERENCES Dimension_Crash(RD_NO),
    FOREIGN KEY (PERSON_ID) REFERENCES Dimension_Person(PERSON_ID),
    FOREIGN KEY (CRASH_UNIT_ID) REFERENCES Dimension_Vehicle(CRASH_UNIT_ID),
    FOREIGN KEY (INJURIES_ID) REFERENCES Dimension_Injuries(INJURIES_ID),
    FOREIGN KEY (DATE_ID) REFERENCES Dimension_Date(DATE_ID),
    FOREIGN KEY (GEOGRAPHY_ID) REFERENCES Dimension_Geography(GEOGRAPHY_ID),
    FOREIGN KEY (CAUSE_ID) REFERENCES Dimension_Cause(CAUSE_ID),
    FOREIGN KEY (WEATHER_ID) REFERENCES Dimension_Weather(WEATHER_ID)
);



