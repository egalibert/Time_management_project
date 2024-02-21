import psycopg2
from config import config
from datetime import timedelta, datetime
from collections import defaultdict

con = None

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

def timedelta_to_hours(td):
    return td.total_seconds() / 3600.0

def write_to_file(data):
    consultant_hours = defaultdict(timedelta)
    customer_hours = defaultdict(timedelta)

    for record in data:
        record_id = record[0]
        start_time = datetime.strptime(str(record[1]), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(str(record[2]), '%Y-%m-%d %H:%M:%S')
        lunch_break = record[3]
        consultant_name = record[4]
        customer_name = record[5]

        total_working_time = end_time - start_time - lunch_break
        consultant_hours[consultant_name] += total_working_time
        customer_hours[customer_name] += total_working_time

    with open('working_hours_report.txt', 'w') as file:
        file.write("Consultant Report:\n")
        for consultant, total_hours in consultant_hours.items():
            file.write(f"{consultant}: {total_hours}\n")

        file.write("\nCustomer Report:\n")
        for customer, total_hours in customer_hours.items():
            file.write(f"{customer}: {total_hours}\n")


def main():
    data = all_rows()
    write_to_file(data)

main()