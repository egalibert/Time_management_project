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

# Inserts the total working time into new_table
def insert_total_balance(person_id, consultant_name, total_balance):
	try:
		con = psycopg2.connect(**config())
		cursor = con.cursor()

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

# Calculates the average working hours per consultant using both tables
def get_average_hours_per_day_per_consultant():
	try:
		con = psycopg2.connect(**config())
		cursor = con.cursor()

		# SQL query to calculate average hours per day per consultant with rounding
		query = """
		SELECT
			twt.consultant_name,
			DATE(wh.start_time) AS work_date,
			ROUND(AVG(EXTRACT(EPOCH FROM twt.total_balance) / 3600), 2) AS average_hours
		FROM
			total_working_time twt
		JOIN
			working_hours wh ON twt.consultant_name = wh.consultant_name
		GROUP BY
			twt.consultant_name, work_date
		ORDER BY
			twt.consultant_name, work_date;
		"""

		cursor.execute(query)
		result = cursor.fetchall()
		# print(result)
		return result

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if con is not None:
			con.close()

# Main function that does everything: creates table if necessary, calculates total working time and fills table with data.
def main():
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
	main()