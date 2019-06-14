create table provider(
npi varchar(10) not null primary key,
name varchar(75),
credentials varchar(20),
gender varchar(1),
street1 varchar(50),
street2 varchar(50),
city varchar(30),
zip varchar(10),
state varchar(20),
country varchar(20) 
);

create table med_proc(
code varchar(5) not null primary key,
descr varchar(256) not null,
drug_indicator varchar(1) not null	
);

create table proc_stats(
npi varchar(10),
code varchar(5), 
avg_medicare_allowed_amt FLOAT,
avg_submitted_charge_amt FLOAT,
avg_medicare_payment_amt FLOAT,
avg_medicare_std_amount FLOAT,
PRIMARY KEY(npi, code),
FOREIGN KEY(npi) REFERENCES provider(npi),
FOREIGN KEY(code) REFERENCES med_proc(code)
);

create table hospital(
hospital_name varchar(40) not null primary key,
address varchar(40) not null,
city varchar(20),
state varchar(20),
zip varchar(10),
county varchar(30),
phone_number varchar(15),
hospital_type varchar(30),
hospital_ownership varchar(50),
emergency_services varchar(5)
);

--LOAD DATA LOCAL INFILE 'provider_data.txt'
--  INTO TABLE  provider
--  (npi, @dummy, @dummy, @dummy, gender, credentials, street1, street2, city, zip, state, country, name);

--LOAD DATA LOCAL INFILE 'Medicare_Provider_Util_Payment_PUF_CY2016.txt' 
--  INTO TABLE med_proc
--  (@dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, code, descr, drug_indicator);

--LOAD DATA LOCAL INFILE 'hospital_data.txt'
 -- INTO TABLE hospital
  --(@dummy, hospital_name, address, city, state, zip, county, phone_number, hospital_type, hospital_ownership, emergency_services, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy); 

--LOAD DATA LOCAL INFILE 'Medicare_Provider_Util_Payment_PUF_CY2016.txt' 
--  INTO table proc_stats
--  (npi, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, code, @dummy, @dummy, @dummy, @dummy, @dummy, avg_medicare_allowed_amt, avg_submitted_charge_amt, avg_medicare_payment_amt, avg_medicare_std_amount);

