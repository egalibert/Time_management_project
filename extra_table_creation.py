from collections import defaultdict
from datetime import datetime, timedelta
import psycopg2
from config import config

con = None

def calculate_total_working_time(start_time, end_time, lunch_break):
	start_datetime = datetime.strptime(str(start_time), "%Y-%m-%d %H:%M:%S")
	end_datetime = datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S")
	lunch_break_timedelta = timedelta(seconds=lunch_break.total_seconds())
	
	total_working_time = end_datetime - start_datetime - lunch_break_timedelta
	return total_working_time

def create_total_working_time_table():
	try:
		con = psycopg2.connect(**config())
		cursor = con.cursor()

		# Create a new table for total balance
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS total_working_time (
				person_id SERIAL PRIMARY KEY,
				consultant_name VARCHAR(255) NOT NULL,
				total_balance INTERVAL
			);
		""")

		con.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if con is not None:
			con.close()

def insert_total_balance(person_id, consultant_name, total_balance):
	try:
		con = psycopg2.connect(**config())
		cursor = con.cursor()

		# Insert total balance into the new table
		cursor.execute("""
			INSERT INTO total_working_time (person_id, consultant_name, total_balance)
			VALUES (%s, %s, %s);
		""", (person_id, consultant_name, total_balance))

		con.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if con is not None:
			con.close()

# Assuming you have data in the format you provided earlier
def all_rows():
	try:
		con = psycopg2.connect(**config())
		cursor = con.cursor()
		SQL = 'SELECT * FROM working_hours;'
		cursor.execute(SQL)
		row = cursor.fetchall()
		# print(row)
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if con is not None:
			con.close()
	return(row)

# Create the total balance table

def main():
	create_total_working_time_table()
	data = all_rows()

	# Calculate total working time and insert into the new table
	for record in data:
		person_id = record[0]
		start_time = record[1]
		end_time = record[2]
		lunch_break = record[3]
		consultant_name = record[4]

		total_working_time = calculate_total_working_time(start_time, end_time, lunch_break)
		insert_total_balance(person_id, consultant_name, total_working_time)

	print("Total balance table created and populated.")


main()