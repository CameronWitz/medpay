LOAD DATA LOCAL INFILE 'Medicare_Provider_Util_Payment_PUF_CY2016.txt'
        into table medicareMaster
	IGNORE 1 ROWS;

