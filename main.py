import flask
import psycopg2
from config import config

#Selects all rows from Working hours (first table)
def all_rows():
	try:
		con = psycopg2.connect(**config())
		cursor = con.cursor()
		SQL = 'SELECT * FROM working_hours;'
		cursor.execute(SQL)
		row = cursor.fetchall()
		print(row)
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if con is not None:
			con.close()
#Inserts new person to Working hours table (first table)
def add_new_person(start_time, end_time, lunch_break, consultant_name, customer_name):
	try:
		con = psycopg2.connect(**config())
		cursor = con.cursor()
		cursor.execute("""
		INSERT INTO working_hours (start_time, end_time, lunch_break, consultant_name, customer_name)
		VALUES (%s, %s, %s, %s, %s);
	""", (start_time, end_time, lunch_break, consultant_name, customer_name))
		con.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if con is not None:
			con.close()

# def main():
# 	start_time = "2024-02-19 09:00:00"
# 	end_time = "2024-02-19 17:00:00"
# 	lunch_break = "1 hour"
# 	consultant_name = "Jaakko Jaakkola"
# 	customer_name = "Apple"

# 	add_new_person(start_time, end_time, lunch_break, consultant_name, customer_name)
# all_rows()
			
# def drop_total_working_time_table():
#     try:
#         con = psycopg2.connect(**config())
#         cursor = con.cursor()

#         # Drop the total_working_time table if it exists
#         cursor.execute("""
#             DROP TABLE IF EXISTS total_working_time;
#         """)

#         con.commit()
#         cursor.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if con is not None:
#             con.close()

# Example usage
# drop_total_working_time_table()

# main()