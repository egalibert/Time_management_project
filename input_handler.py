from flask import Flask, request
import psycopg2
from config import config
from main import add_new_person, all_rows
from datetime import datetime

app = Flask(__name__)

# The connection to /working_hours. Takes posted json data validates it and inserts it into working_hours table. 
@app.route('/working_hours', methods=['POST'])
def post_working_hours():
	data = request.get_json()
	# print(data)

	insert_data(data)

	if validate_input(data):
		return {"message": "Data successfully inserted into the database"}
	else:
		return {"error": "Invalid input data"}, 400

# Used to make sure data is valid for inserting
def validate_input(data):
	return True  # Placeholder, implement your validation logic

# Uses SQL to insert posted data into table.
def insert_data(data):
	con = psycopg2.connect(**config())
	cur = con.cursor()

	# Insert data into the working_hours table
	sql = """
		INSERT INTO working_hours (start_time, end_time, lunch_break, consultant_name, customer_name)
		VALUES (%s, %s, %s, %s, %s);
	"""
	values = (
		data.get('start_time'),
		data.get('end_time'),
		data.get('lunch_break'),
		data.get('consultant_name'),
		data.get('customer_name')
	)

	cur.execute(sql, values)
	con.commit()

	cur.close()
	con.close()
	all_rows()

if __name__ == '__main__':
	app.run(debug=True)