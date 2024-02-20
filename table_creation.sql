CREATE TABLE working_hours (
	id SERIAL PRIMARY KEY,
	start_time TIMESTAMP NOT NULL,
	end_time TIMESTAMP NOT NULL,
	lunch_break INTERVAL, 
	consultantName VARCHAR(50),
	customerName VARCHAR (50)
);