import psycopg2
from config import config

con=None

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

def main():
    all_rows()

main()