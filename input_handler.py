from flask import Flask, request
import psycopg2
from config import config
from main import add_new_person, all_rows
from datetime import datetime

app = Flask(__name__)

@app.route('/working_hours', methods=['POST'])
def post_working_hours():
	data = request.get_json()
	print(data)

	insert_data(data)

	# Validate and process input data
	if validate_input(data):
		return {"message": "Data successfully inserted into the database"}
	else:
		return {"error": "Invalid input data"}, 400

def validate_input(data):
	return True  # Placeholder, implement your validation logic

def insert_data(data):
	# Connect to PostgreSQL database
	con = psycopg2.connect(**config())

	# Create a cursor
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

	# Commit the transaction
	con.commit()

	# Close the cursor and connection
	cur.close()
	con.close()
	all_rows()

if __name__ == '__main__':
	app.run(debug=True)