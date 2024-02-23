from collections import defaultdict
from datetime import datetime, timedelta
import psycopg2
from config import config

con = None

# Calculates the total working time by subtracting start_time and lunchbreak from end_time 
# and returns it for future use
def calculate_total_working_time(start_time, end_time, lunch_break):
	start_datetime = datetime.strptime(str(start_time), "%Y-%m-%d %H:%M:%S")
	end_datetime = datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S")
	lunch_break_timedelta = timedelta(seconds=lunch_break.total_seconds())
	
	total_working_time = end_datetime - start_datetime - lunch_break_timedelta
	return total_working_time

# Creates table of total working time if it doesnt already exsist
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

# Inserts the total working time into new_table, if the consultant already exists it adds the total time
def insert_total_balance(person_id, consultant_name, total_balance):
	try:
		con = psycopg2.connect(**config())
		cursor = con.cursor()

		cursor.execute("SELECT * FROM total_working_time WHERE consultant_name = %s", (consultant_name,))
		existing_row = cursor.fetchone()

		if existing_row:
			# If exists, update total_balance
			new_total_balance = existing_row[2] + total_balance
			print(new_total_balance)
			cursor.execute("UPDATE total_working_time SET total_balance = %s WHERE consultant_name = %s",
						(new_total_balance, consultant_name))
		else:
			# If not exists, insert new row
			cursor.execute("INSERT INTO total_working_time (person_id, consultant_name, total_balance) VALUES (%s, %s, %s)",
						(person_id, consultant_name, total_balance))

		con.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if con is not None:
			con.close()

# Queries all information from working_hours table
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

# Main function that does everything: creates table if necessary, calculates total working time and fills table with data.
def extra_table_main():
	create_total_working_time_table()
	data = all_rows()

	for record in data:
		person_id = record[0]
		start_time = record[1]
		end_time = record[2]
		lunch_break = record[3]
		consultant_name = record[4]

		total_working_time = calculate_total_working_time(start_time, end_time, lunch_break)
		insert_total_balance(person_id, consultant_name, total_working_time)

if __name__ == '__main__':
	extra_table_main()