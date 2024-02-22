CREATE TABLE working_hours (
	id SERIAL PRIMARY KEY,
	start_time TIMESTAMP NOT NULL,
	end_time TIMESTAMP NOT NULL,
	lunch_break INTERVAL, 
	consultant_name VARCHAR(50),
	customer_name VARCHAR (50)
);