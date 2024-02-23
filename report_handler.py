import psycopg2
from config import config
from datetime import timedelta, datetime
from collections import defaultdict, namedtuple
# from extra_table_creation import get_average_hours_per_day_per_consultant

con = None

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

# Changes the seconds (from using datetime) into hours
def timedelta_to_hours(td):
    return td.total_seconds() / 3600.0

# Calculates the average working hours per consultant using both tables
def get_average_hours_per_day_per_consultant():
	try:
		con = psycopg2.connect(**config())
		cursor = con.cursor()

		# SQL query to calculate average hours per day per consultant with rounding
		query = """
        SELECT
            w.consultant_name,
            SUM(EXTRACT(EPOCH FROM AGE(w.end_time, w.start_time) - w.lunch_break) / 3600) / COUNT(DISTINCT DATE(w.start_time)) AS average_working_time_per_day
        FROM
            working_hours w
        JOIN
            total_working_time t ON w.consultant_name = t.consultant_name
        GROUP BY
            w.consultant_name;
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


# Calculates the proper values and writes consultant_hours, customer_hours and cumulative_customer_hours and average hours into a file
def write_to_file(data):
    consultant_hours = defaultdict(timedelta)
    customer_hours = defaultdict(timedelta)
    cumulative_customer_hours = defaultdict(timedelta)
    CustomerRecord = namedtuple('CustomerRecord', ['customer_name', 'total_hours'])

    # takes the passed data (working_hours) and splits it into variables and calculates the needed information
    for record in data:
        record_id = record[0]
        start_time = datetime.strptime(str(record[1]), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(str(record[2]), '%Y-%m-%d %H:%M:%S')
        lunch_break = record[3]
        consultant_name = record[4]
        customer_name = record[5]

        total_working_time = end_time - start_time - lunch_break
        consultant_hours[consultant_name] += total_working_time
        customer_hours[(consultant_name, customer_name)] += total_working_time
        cumulative_customer_hours[customer_name] += total_working_time

    # opens report file and writes information based on calculations
    with open('working_hours_report.txt', 'w') as file:
        file.write("Consultant Report:\n")
        for consultant, total_hours in consultant_hours.items():
            file.write(f"{consultant}: {total_hours}\n")

        file.write("\nCustomer Report:\n")
        for (consultant, customer), total_hours in customer_hours.items():
            file.write(f"{consultant} - {customer}: {total_hours}\n")

        file.write("\nTotal Working Hours Grouped by Customer:\n")
        for customer, total_hours in cumulative_customer_hours.items():
            file.write(f"{customer}: {total_hours}\n")
        
        file.write("\nAverage Working Time per Day per Consultant Report:\n")
        report = get_average_hours_per_day_per_consultant()
        if report is not None:
            for row in report:
                file.write(f"{row[0]}: {row[1]:.2f} hours\n")
        else:
            print("No data retrieved from get_average_hours_per_day_per_consultantt")


# main function runs the program
def main():
    data = all_rows()
    write_to_file(data)
    # new_file_test(data)

if __name__ == '__main__':
    main()

